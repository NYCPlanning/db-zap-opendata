with zap_projects_recoded as (
    select * from {{ ref('base_dcp__zap_projects_recoded') }}
),

zap_project_ids as (
    select * from {{ ref('base_dcp__zap_project_ids') }}
),


zap_projects as (
    select
        zap_projects_recoded.dcp_name,
        zap_projects_recoded.project_name,
        zap_projects_recoded.project_certified_referred_date,
        zap_projects_recoded.project_certified_referred_year,
        zap_projects_recoded.applicant_type,
        zap_projects_recoded.ulurp_numbers,
        zap_projects_recoded.ulurp_type,
        zap_projects_recoded.ceqr_number,
        zap_projects_recoded.ceqr_type,
        zap_projects_recoded.project_status,
        zap_projects_recoded.public_status,
        zap_projects_recoded.action_codes,
        zap_project_ids.project_id
    from
        zap_projects_recoded
    left join
        zap_project_ids
        on
            zap_projects_recoded.dcp_name = zap_project_ids.dcp_name
)

select * from zap_projects_recoded
