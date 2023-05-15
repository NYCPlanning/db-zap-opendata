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

## MapZAP

MapZAP is a dataset of ZAP project records with spatial data. Based on the BBLs associated with a project when it was referred for review (Project certified referred year), a version of PLUTO from that year is chosen and used to find and aggregate BBL geometries to represent the project.
...

### Data sources

- ZAP Projects
- ZAP Project BBLs
- MapPLUTO (versions from 2002 - 2022)

### Build process

> Planning to do this via dbt

- Currently running saved queries in the BigQuery console and saving query results as tables in the `dcp_mapzap` BigQuery dataset.

```mermaid
%%{ init: { 'flowchart': { 'curve': 'curveMonotoneY' } } }%%
flowchart TB
    %% source data
    src_projects[(ZAP Projects)]
    src_project_bbls[(ZAP Project\nBBLs)]
    src_pluto_years(PLUTO versions\nby year)
    src_MapPLUTO[("MapPLUTO\n(2002 - 2022)")]

    %% intermediate data
    projects_pluto("ZAP Projects")
    pluto_geo("PLUTO\ngeography")
    project_bbl_geo("Project BBLs\ngeography")
    projects_bbl("ZAP Project\nBBLs")

    %% final data
    project_geo("MapZAP")

    %% 
    src_pluto_years --> projects_pluto
    src_projects ---> projects_pluto

    src_project_bbls ---> projects_bbl

    src_MapPLUTO ---> pluto_geo

    %% 
    projects_pluto --> project_bbl_geo
    projects_bbl --> project_bbl_geo
    pluto_geo --> project_bbl_geo

    %% 
    project_bbl_geo --> project_geo
```

### Notes

- All source data is in BigQuery
...
