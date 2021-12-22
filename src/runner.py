import json
import os
import sys

import pandas as pd
from pathlib import Path
import requests

from . import CLIENT_ID, SECRET, TENANT_ID, ZAP_DOMAIN, ZAP_ENGINE
from .client import Client
from .copy import psql_insert_copy
from .pg import PG


class Runner:
    def __init__(self, name: str):
        self.c = Client(
            zap_domain=ZAP_DOMAIN,
            tenant_id=TENANT_ID,
            client_id=CLIENT_ID,
            secret=SECRET,
        )
        self.name = name
        self.output_dir = f".output/{name}"
        self.output_file = f"{self.output_dir}/{self.name}"
        self.headers = self.c.request_header
        self.engine = PG(ZAP_ENGINE).engine

    def create_output_dir(self):
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def download(self):
        self.create_output_dir()
        nextlink = f"{ZAP_DOMAIN}/api/data/v9.1/{self.name}"
        counter = 0
        while nextlink != "":
            response = requests.get(nextlink, headers=self.headers)
            result = response.text
            result_json = response.json()
            filename = f"{self.name}_{counter}.json"
            self.write_to_json(response.text, filename)
            counter += 1
            nextlink = response.json().get("@odata.nextLink", "")

    def write_to_json(self, content: str, filename: str) -> bool:
        print(f"writing {filename} ...")
        with open(f"{self.output_dir}/{filename}", "w") as f:
            f.write(content)
        return os.path.isfile(f"{self.output_dir}/{filename}")

    def check_table_existence(self, name):
        r = self.engine.execute(
            """
            select * from information_schema.tables 
            where table_name='%(name)s'
            """
            % {"name": name}
        )
        return bool(r.rowcount)

    def combine(self):
        files = os.listdir(self.output_dir)
        if self.check_table_existence(self.name):
            self.engine.execute(
                """
                BEGIN; DROP TABLE IF EXISTS %(newname)s; 
                ALTER TABLE %(name)s RENAME TO %(newname)s; COMMIT;
                """
                % {"name": self.name, "newname": self.name + "_"}
            )
        for _file in files:
            with open(f"{self.output_dir}/{_file}") as f:
                data = json.load(f)
            df = pd.DataFrame(data["value"], dtype=str)
            self.open_data_cleaning(df)
            df.to_sql(
                name=self.name,
                con=self.engine,
                index=False,
                if_exists="append",
                method=psql_insert_copy,
            )
            os.remove(f"{self.output_dir}/{_file}")

        # fmt:off
        self.engine.execute(
            "BEGIN; DROP TABLE IF EXISTS %(name)s; COMMIT;" 
            % {"name": self.name + "_"}
        )
        # fmt:on
        self.make_open_data_table()

    def make_open_data_table(self):
        if self.name == "dcp_projects":
            self.engine.execute(
                """BEGIN;
                DROP TABLE IF EXISTS dcp_projects_visible;
            CREATE TABLE dcp_projects_visible as 
            (SELECT * from dcp_projects where dcp_visibility = '717170003');
             COMMIT;"""
            )
        if self.name == "dcp_projectbbls":
            self.engine.execute(
                """BEGIN;
                DROP TABLE IF EXISTS dcp_projectbbls_visible;
                CREATE TABLE dcp_projectbbls_visible as 
                (SELECT dcp_projectbbls.* from dcp_projectbbls INNER JOIN dcp_projects 
                on SUBSTRING(dcp_projectbbls.dcp_name, 0,10) = dcp_projects.dcp_name);
                COMMIT;"""
            )

    def open_data_cleaning(self, df):
        if self.name == "dcp_projects":  # To-do: figure out better design for this
            df["dcp_visibility"] = df["dcp_visibility"].str.split(".", expand=True)[0]
        if self.name == "dcp_projectbbls":
            df["timezoneruleversionnumber"] = df["timezoneruleversionnumber"].astype(
                int
            )

    def clean(self):
        if os.path.isdir(self.output_dir):
            files = os.listdir(self.output_dir)
            for _file in files:
                os.remove(f"{self.output_dir}/{_file}")

    @property
    def columns(self):
        with open(f"{Path(__file__).parent.parent}/schemas/{self.name}.json") as f:
            schema = json.load(f)
        return [s["name"] for s in schema]

    def export(self):
        self.sql_to_csv(self.name, self.output_file)
        if self.name in ["dcp_projects", "dcp_projectbbls"]:
            self.sql_to_csv(f"{self.name}_visible", f"{self.output_file}_visible")

    def sql_to_csv(self, table_name, output_file):
        df = pd.read_sql(
            "select * from %(name)s" % {"name": table_name}, con=self.engine
        )
        df[self.columns].to_csv(f"{output_file}.csv", index=False)

    def __call__(self):
        self.clean()
        self.download()
        self.combine()
        self.export()


if __name__ == "__main__":
    name = sys.argv[1]
    Runner(name)()
