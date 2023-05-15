# db-zap-opendata

Workflow for creating subset of ZAP data that's on open data

## Instructions

> Note: set the environmental variables in `.env` according to `example.env`.

1. open repo in the defined dev container

2. run a ZAP Pull
    ```bash
    python -m src.runner <name of the entity>
    ```

    e.g.

    ```bash
    python -m src.runner dcp_projects
    ```
