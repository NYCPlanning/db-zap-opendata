with stg_zap_projects as (
    select * from {{ ref('stg_dcp__zap_projects') }}
),

seed_pluto_versions as (
    select * from {{ ref('seed_pluto_versions') }}
),

zap_projects_info as (
    select
        project_id,
        project_name,
        project_code,
        project_certified_referred_date,
        EXTRACT(
            isoyear
            from
            project_certified_referred_date
        ) as project_certified_referred_year
        -- -- replace spaces with nothing,
        -- -- drop everything to the right of the first hyphen (included),
        -- -- and trip leading 'P' characters
        -- LTRIM(SPLIT(REPLACE(project_id, ' ', ''), '-')[
        --     OFFSET(0)
        -- ], 'P') as project_id
    from
        stg_zap_projects
),

zap_projects as (
    select
        zap_projects_info.project_id,
        zap_projects_info.project_name,
        zap_projects_info.project_code,
        zap_projects_info.project_certified_referred_date,
        zap_projects_info.project_certified_referred_year,
        seed_pluto_versions.primary_pluto_version as project_pluto_version,
        seed_pluto_versions.has_wkt_geometry as pluto_version_has_geometry
    from
        zap_projects_info left join seed_pluto_versions on
        zap_projects_info.project_certified_referred_year
        = seed_pluto_versions.year
)

select * from zap_projects
