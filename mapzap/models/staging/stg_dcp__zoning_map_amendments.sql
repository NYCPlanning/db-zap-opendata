with source as (

    select * from {{ source('zoning_map_amendments', '20230519_internal') }}

),

zap_projects as (

    select
        project_na as project_name,
        wkt as wkt,
        UPPER(trackingno) as tracking_number,
        UPPER(ulurpno) as ulurp_number
    from source
)

select * from zap_projects
