with project_geometries as (
    select * from {{ ref('product_zap_project_geometries') }}
),

project_geometries_counts as (
    select
        project_certified_referred_year,
        project_pluto_version,
        COUNT(*) as project_count,
        SUM(case when project_bbls is null then 1 else 0 end)
            as projects_without_a_bbl,
        SUM(case when project_geometry_wkt is null then 1 else 0 end)
            as projects_without_a_geography
    from
        project_geometries
    group by
        project_certified_referred_year,
        project_pluto_version
),

project_geometries_stats as (
    select
        project_certified_referred_year,
        project_pluto_version,
        project_count,
        projects_without_a_bbl,
        projects_without_a_geography,
        CAST(ROUND(
            projects_without_a_bbl
            / project_count, 2
        ) * 100 as INT64) as percent_projects_without_a_bbl,
        CAST(ROUND(
            projects_without_a_geography
            / project_count, 2
        ) * 100 as INT64) as percent_projects_without_a_geography
    from
        project_geometries_counts

),

project_geometries_stats_ordered as (
    select
        project_certified_referred_year,
        project_pluto_version,
        project_count,
        projects_without_a_bbl,
        percent_projects_without_a_bbl,
        projects_without_a_geography,
        percent_projects_without_a_geography
    from project_geometries_stats
    order by
        project_certified_referred_year
)

select * from project_geometries_stats_ordered
