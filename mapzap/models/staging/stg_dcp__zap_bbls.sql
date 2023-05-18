with source_zap_project_bbls as (

    select * from {{ source('zap_bbls', '20230515') }}

),

zap_bbls as (
    select
        cast(dcp_bblnumber as string) as project_bbl,
        -- replace spaces with nothing,
        -- drop everything to the right of the first hyphen (included),
        -- and strip leading 'P' characters
        ltrim(split(replace(dcp_name, ' ', ''), '-')[
            offset(0)
        ], 'P') as project_name
    from
        source_zap_project_bbls
    where
        dcp_name is not null
        and dcp_bblnumber is not null
    group by
        project_name,
        project_bbl
)

select * from zap_bbls
