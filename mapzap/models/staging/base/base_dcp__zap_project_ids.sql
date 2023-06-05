with source as (

    select * from {{ source('zap_projects', '20230605_test_recoded') }}

),

zap_project_ids as (

    select
        project_id as dcp_name,
        crm_project_id as project_id
    from source
)

select * from zap_project_ids
