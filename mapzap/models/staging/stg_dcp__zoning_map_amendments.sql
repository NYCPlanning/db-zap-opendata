with source as (

    select * from {{ source('zoning_map_amendments', '20230519_internal') }}

),

zap_projects as (

    select
        trackingno as tracking_number,
        project_na as project_name,
        ulurpno as ulurp_number,
        wkt as wkt
    from source
)

select * from zap_projects
