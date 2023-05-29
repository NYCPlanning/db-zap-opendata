with zap_projects_recoded as (
    select * from {{ ref('base_dcp__zap_projects_recoded') }}
),

zap_project_ids as (
    select * from {{ ref('base_dcp__zap_project_ids') }}
),


zap_projects as (
    select
        zap_projects_recoded.*,
        zap_project_ids.project_id
    from
        zap_projects_recoded
    left join
        zap_project_ids
        on
            zap_projects_recoded.dcp_name = zap_project_ids.dcp_name
)

select * from zap_projects
