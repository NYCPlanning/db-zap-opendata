with project_bbl_geometries as (
    select *
    from
        {{ ref('int_zap_project_bbl_geometries') }}
),

project_bbl_geometries_aggregated as (
    select
        project_id,
        project_name,
        project_code,
        project_certified_referred_year,
        project_pluto_version,
        SUM(ST_AREA(bbl_geometry_wkt)) as bbl_areas_sum,
        ARRAY_AGG(project_bbl) as project_bbls_array,
        ST_UNION_AGG(bbl_geometry_wkt) as project_geometry_wkt
    from project_bbl_geometries
    group by
        project_id,
        project_name,
        project_code,
        project_certified_referred_year,
        project_pluto_version
),

project_geometries as (
    select
        project_id,
        project_name,
        project_code,
        project_certified_referred_year,
        project_pluto_version,
        bbl_areas_sum,
        NULLIF(ARRAY_TO_STRING(project_bbls_array, '|'), '') as project_bbls,
        ST_AREA(project_geometry_wkt) as project_area,
        ST_ASTEXT(project_geometry_wkt) as project_geometry_wkt
    from project_bbl_geometries_aggregated
)

select * from project_geometries
