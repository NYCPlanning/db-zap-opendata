import pandas as pd
from sqlalchemy import create_engine


class PG:
    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(url)
