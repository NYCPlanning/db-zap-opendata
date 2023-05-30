with project_bbl_geometries as (
    select *
    from
        {{ ref('int_zap_project_bbl_geometries') }}
),

project_geometries_from_map as (
    select *
    from
        {{ ref('int_zap_project_map_geometries') }}
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

project_geometries_from_bbls as (
    select
        project_id,
        pluto_version,
        bbl_areas_sum,
        NULLIF(ARRAY_TO_STRING(project_bbls_array, '|'), '') as project_bbls,
        ST_AREA(project_geometry_wkt) as project_area,
        ST_ASTEXT(project_geometry_wkt) as bbls_wkt
    from project_bbl_geometries_aggregated
),

project_geometries as (
    select
        project_geometries_from_bbls.*,
        project_geometries_from_map.ulurp_number as map_ammendment_ulurp_numner,
        project_geometries_from_map.project_name as map_ammendment_project_name,
        ST_ASTEXT(project_geometries_from_map.wkt) as map_ammendment_wkt
    from
        project_geometries_from_bbls
    left join
        project_geometries_from_map
        on
            project_geometries_from_bbls.project_id
            = project_geometries_from_map.project_id

),

mapzap as (
    select
        project_details.*,
        project_geometries.map_ammendment_ulurp_numner,
        project_geometries.map_ammendment_project_name,
        project_geometries.pluto_version,
        project_geometries.bbl_areas_sum,
        project_geometries.project_bbls,
        project_geometries.project_area,
        COALESCE(
            project_geometries.map_ammendment_wkt is not null,
            false
        ) as has_map_ammendment_geometry,
        COALESCE(
            project_geometries.bbls_wkt is not null,
            false
        ) as has_bbls_geometry,
        case
            when
                project_geometries.map_ammendment_wkt is not null
                then 'zoning map ammendment'
            when project_geometries.bbls_wkt is not null then 'bbls'
        end
            as geometry_source,
        COALESCE(
            project_geometries.map_ammendment_wkt, project_geometries.bbls_wkt
        ) as wkt
    from
        project_details
    left join
        project_geometries on
        project_details.project_id = project_geometries.project_id

)

select * from mapzap
