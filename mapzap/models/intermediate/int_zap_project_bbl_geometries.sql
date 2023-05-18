with project_bbls as (
    select *
    from
        {{ ref('int_zap_project_bbls') }}
),

pluto_geometries as (
    select *
    from
        {{ ref('stg_dcp__pluto_bbls') }}
),

zap_project_bbls as (
    select
        project_bbls.project_name,
        project_bbls.project_certified_referred_date,
        project_bbls.project_certified_referred_year,
        project_bbls.project_pluto_version,
        project_bbls.project_bbl,
        ST_GEOGFROMTEXT(pluto_geometries.wkt) as bbl_geometry_wkt
    from
        project_bbls
    left join
        pluto_geometries
        on
            project_bbls.project_bbl
            = pluto_geometries.bbl
            and project_bbls.project_pluto_version
            = pluto_geometries.pluto_version
)

select *
from
    zap_project_bbls
order by
    project_name desc,
    project_bbl asc
