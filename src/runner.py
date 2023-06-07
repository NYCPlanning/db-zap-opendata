import json
import os
import sys
from typing import List

import pandas as pd
from pathlib import Path
import requests
from sqlalchemy import text

from . import CLIENT_ID, SECRET, TENANT_ID, ZAP_DOMAIN, ZAP_ENGINE
from .client import Client
from .copy import psql_insert_copy
from .pg import PG
from .visible_projects import (
    OPEN_DATA,
    make_crm_table,
    make_open_data_table,
    open_data_recode,
    recode_id,
)
from .util import timestamp_to_date


class Runner:
    def __init__(self, name, schema: str):
        self.c = Client(
            zap_domain=ZAP_DOMAIN,
            tenant_id=TENANT_ID,
            client_id=CLIENT_ID,
            secret=SECRET,
        )
        self.name = name
        self.output_dir = f".output/{name}"
        self.cache_dir = f".cache/{name}"
        self.output_file = f"{self.output_dir}/{self.name}"
        self.headers = self.c.request_header
        self.schema = schema
        self.pg = PG(ZAP_ENGINE, self.schema)
        self.engine = self.pg.engine
        # self.open_dataset = False # DEV for testing
        self.open_dataset = self.name in OPEN_DATA

    def clean(self):
        if os.path.isdir(self.output_dir):
            files = os.listdir(self.output_dir)
            for _file in files:
                os.remove(f"{self.output_dir}/{_file}")

    def create_output_cache_dir(self):
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

    def download(self):
        print(f"downloading {self.name} from ZAP CRM ...")
        self.create_output_cache_dir()
        nextlink = f"{ZAP_DOMAIN}/api/data/v9.1/{self.name}"
        counter = 0
        while nextlink != "":
            response = requests.get(nextlink, headers=self.headers)
            result = response.text
            result_json = response.json()
            if list(result_json.keys()) == ["error"]:
                raise FileNotFoundError(result_json["error"])
            filename = f"{self.name}_{counter}.json"
            self.write_to_json(response.text, filename)
            counter += 1
            nextlink = response.json().get("@odata.nextLink", "")

    def write_to_json(self, content: str, filename: str) -> bool:
        print(f"writing {filename} ...")
        with open(f"{self.cache_dir}/{filename}", "w") as f:
            f.write(content)
        return os.path.isfile(f"{self.cache_dir}/{filename}")

    def check_table_existence(self, name):
        with self.engine.begin() as sql_conn:
            statement = """
                select * from information_schema.tables 
                where
                    table_schema='%(schema)s'
                    and table_name='%(name)s'
            """ % {
                "schema": self.pg.schema,
                "name": name,
            }
            r = sql_conn.execute(statement=text(statement))
        return bool(r.rowcount)

    def combine(self):
        print("running combine ...")
        files = os.listdir(self.cache_dir)
        if self.check_table_existence(self.name):
            print("check_table_existence ...")
            with self.engine.begin() as sql_conn:
                statement = """
                    BEGIN; DROP TABLE IF EXISTS %(newname)s; 
                    ALTER TABLE %(name)s RENAME TO %(newname)s; COMMIT;
                """ % {
                    "name": self.name,
                    "newname": self.name + "_",
                }
                sql_conn.execute(statement=text(statement))
        else:
            print("table does not exist")
        for _file in files:
            print(f"json.load {self.cache_dir}/{_file} ...")
            with open(f"{self.cache_dir}/{_file}") as f:
                data = json.load(f)
            df = pd.DataFrame(data["value"], dtype=str)
            if self.open_dataset:
                print("open_data_cleaning ...")
                df = self.open_data_cleaning(df)
            print("df.to_sql ...")
            df.to_sql(
                name=self.name,
                con=self.engine,
                index=False,
                if_exists="append",
                method=psql_insert_copy,
            )
            # os.remove(f"{self.output_dir}/{_file}")

        # fmt:off
        with self.engine.begin() as sql_conn:
            statement =  "BEGIN; DROP TABLE IF EXISTS %(name)s; COMMIT;" % {"name": self.name + "_"}
            sql_conn.execute(statement=text(statement))
        # fmt:on
        if self.open_dataset:
            # TODO rename so that combine() output can be _crm
            make_crm_table(self.engine, self.name)

    def open_data_cleaning(self, df):
        if self.name == "dcp_projects":  # To-do: figure out better design for this
            df["dcp_visibility"] = df["dcp_visibility"].str.split(".", expand=True)[0]
        return df

    @property
    def columns(self):
        with open(f"{Path(__file__).parent.parent}/schemas/{self.name}.json") as f:
            schema = json.load(f)
        return [s["name"] for s in schema]

    def recode(self):
        recode_table_name = f"{self.name}_recoded"
        print("pd.read_sql ...")
        df = pd.read_sql(
            "select * from %(name)s"
            % {
                "name": f"{self.name}_crm",
            },
            con=self.engine,
        )
        if not self.open_dataset:
            print("Nothing to recode in non-open dataset")
        else:
            print("open_data_recode ...")
            df = open_data_recode(self.name, df, self.headers)
            print("df.to_csv ...")
            df.to_csv(
                f"{self.output_dir}/{recode_table_name}_before_recode_id.csv",
                index=False,
            )
            if self.name == "dcp_projects":
                print("timestamp_to_date ...")
                df = timestamp_to_date(
                    df,
                    date_columns=[
                        "completed_date",
                        "certified_referred",
                        "current_milestone_date",
                        "current_envmilestone_date",
                        "app_filed_date",
                        "noticed_date",
                        "approval_date",
                    ],
                )
                print("current_milestone_date ...")
                df.loc[
                    (~df.current_milestone.isnull())
                    & (df.current_milestone.str.contains("MM - Project Readiness")),
                    "current_milestone_date",
                ] = None
                print("current_milestone ...")
                df.loc[
                    (~df.current_milestone.isnull())
                    & (df.current_milestone.str.contains("MM - Project Readiness")),
                    "current_milestone",
                ] = None

                # TODO re-enable this
                # print("recode_id ...")
                # df = recode_id(df)

            print("df.to_csv ...")
            df.to_csv(f"{self.output_dir}/{recode_table_name}.csv", index=False)

            df.to_sql(
                name=recode_table_name,
                con=self.engine,
                index=False,
                if_exists="replace",
                method=psql_insert_copy,
            )

    def export(self):
        print(f"self.sql_to_csv for {self.name} ...")
        # TODO ensure this outputs the last built table, not the combine() result
        self.sql_to_csv(self.name, self.output_file, all_columns=False, open_data=False)
        if self.open_dataset:
            print(f"self.sql_to_csv for {self.name}_visible ...")
            make_open_data_table(self.engine, self.name)

            self.sql_to_csv(
                f"{self.name}_visible",
                f"{self.output_file}_visible",
                all_columns=True,
                open_data=True,
            )

    def sql_to_csv(self, table_name, output_file, all_columns, open_data):
        print("pd.read_sql ...")
        df = pd.read_sql(
            "select * from %(name)s" % {"name": table_name}, con=self.engine
        )
        print("self.export_cleaning ...")
        df = self.export_cleaning(df, open_data)

        if not all_columns:
            df = df[self.columns]

        print("df.to_csv ...")
        df.to_csv(f"{output_file}.csv", index=False)

    def export_cleaning(self, df, open_data):
        """Written because sql int to csv writes with decimal and big query wants int"""
        if self.name == "dcp_projectbbls" and "timezoneruleversionnumber" in df.columns:
            df["timezoneruleversionnumber"] = (
                df["timezoneruleversionnumber"]
                .str.split(".", expand=True)[0]
                .astype(int, errors="ignore")
            )
        return df

    def __call__(self):
        print("~~~ RUNNING clean ~~~")
        self.clean()
        print("~~~ RUNNING download ~~~")
        self.download()
        print("~~~ RUNNING combine ~~~")
        self.combine()
        print("~~~ RUNNING recode ~~~")
        self.recode()
        print("~~~ RUNNING export ~~~")
        self.export()


if __name__ == "__main__":
    name = sys.argv[1]
    runner = Runner(name)
