import json
import os
import sys

import pandas as pd
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
        self.output_file = f"{self.output_dir}/output.csv"
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

    def combine(self):
        files = os.listdir(self.output_dir)
        for _file in files:
            with open(f"{self.output_dir}/{_file}") as f:
                data = json.load(f)
            df = pd.DataFrame(data["value"])
            if os.path.isfile(self.output_file):
                df.to_csv(self.output_file, mode="a", header=False, index=False)
            else:
                df.to_csv(self.output_file, mode="w", header=True, index=False)

            os.remove(f"{self.output_dir}/{_file}")

    def clean(self):
        if os.path.isdir(self.output_dir):
            files = os.listdir(self.output_dir)
            for _file in files:
                os.remove(f"{self.output_dir}/{_file}")

    def export(self):
        print(f"exporting {self.name} to postgres ...")
        df = pd.read_csv(self.output_file, index_col=False, low_memory=False)
        df.to_sql(
            name=self.name,
            con=self.engine,
            index=False,
            if_exists="replace",
            method=psql_insert_copy,
        )

    def __call__(self):
        self.clean()
        self.download()
        self.combine()
        self.export()


if __name__ == "__main__":
    name = sys.argv[1]
    Runner(name)()
