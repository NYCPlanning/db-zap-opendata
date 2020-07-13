# db-zap-opendata

Workflow for creating subset of ZAP data that's on open data

# Instructions

1. install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pipenv install --skip-lock
```

2. run pull.py

```bash
python pull.py
```

or

```bash
pipenv run pull.py
```

> Note: set the environmental variables in `.env` according to `example.env`. `pipenv run` will automatically load environmental variables from `.env`
