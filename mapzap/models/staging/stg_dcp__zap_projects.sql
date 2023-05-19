with source as (

    select * from {{ source('zap_projects', '20230515') }}

),

zap_projects as (

    select
        dcp_projectid as project_id,
        dcp_projectname as project_name,
        dcp_name as project_code,
        dcp_certifiedreferred as project_certified_referred_date
    from source
    where
        dcp_name is not null
    group by
        project_id,
        project_name,
        project_code,
        project_certified_referred_date
)

select * from zap_projects
