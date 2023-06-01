with source as (

    select * from {{ source('zap_projects', '20230526') }}

),

zap_project_ids as (

    select
        dcp_name,
        dcp_projectid as project_id
    from source
)

select * from zap_project_ids
