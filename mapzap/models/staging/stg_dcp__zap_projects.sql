with source as (

    select * from {{ source('zap_projects', '20230515') }}

),

zap_projects as (

    select
        dcp_name as project_name,
        dcp_certifiedreferred as project_certified_referred_date

    from source
    where
        dcp_name is not null
    group by
        dcp_name,
        dcp_certifiedreferred
)

select * from zap_projects
