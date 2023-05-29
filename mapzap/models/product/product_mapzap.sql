with project_bbl_geometries as (
    select *
    from
        {{ ref('int_zap_project_bbl_geometries') }}
),

project_details as (
    select *
    from
        {{ ref('stg_dcp__zap_projects') }}
),

project_bbl_geometries_aggregated as (
    select
        project_id,
        pluto_version,
        SUM(ST_AREA(bbl_geometry_wkt)) as bbl_areas_sum,
        ARRAY_AGG(project_bbl) as project_bbls_array,
        ST_UNION_AGG(bbl_geometry_wkt) as project_geometry_wkt
    from project_bbl_geometries
    group by
        project_id,
        pluto_version
),

project_geometries as (
    select
        project_id,
        pluto_version,
        bbl_areas_sum,
        NULLIF(ARRAY_TO_STRING(project_bbls_array, '|'), '') as project_bbls,
        ST_AREA(project_geometry_wkt) as project_area,
        ST_ASTEXT(project_geometry_wkt) as wkt
    from project_bbl_geometries_aggregated
),

mapzap as (
    select
        project_details.*,
        project_geometries.pluto_version,
        project_geometries.bbl_areas_sum,
        project_geometries.project_bbls,
        project_geometries.project_area,
        project_geometries.wkt
    from
        project_details
    left join
        project_geometries on
        project_details.project_id = project_geometries.project_id

)

select * from mapzap
