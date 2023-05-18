with projects_source as (
    select *
    from
        {{ ref('int_zap_projects') }}
),

bbls_source as (
    select *
    from
        {{ ref('stg_dcp__zap_bbls') }}
),

zap_project_bbls as (
    select
        projects_source.project_name,
        projects_source.project_certified_referred_date,
        projects_source.project_certified_referred_year,
        projects_source.project_pluto_version,
        bbls_source.project_bbl as project_bbl
    from
        projects_source
    left join
        bbls_source
        on
            projects_source.project_name
            = bbls_source.project_name
)

select *
from
    zap_project_bbls
order by
    project_name desc,
    project_bbl asc
