# db-zap-opendata

Workflow for creating subset of ZAP data that's on open data

# Instructions

1. install dependencies

```bash
poetry install
```

or install without dev dependencies (more suitable for just running the scripts)

```bash
poetry install --no-dev
```

2. run a ZAP Pull

```bash
poetry run python -m src.runner <name of the entity>
```

e.g.

```bash
poetry run python -m src.runner dcp_projects
```

> Note: set the environmental variables in `.env` according to `example.env`.
