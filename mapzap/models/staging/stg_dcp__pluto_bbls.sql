with pluto_with_bbls as (
    select * from {{ ref('base_dcp__pluto_with_bbls') }}
),

pluto_without_bbls as (
    select * from {{ ref('base_dcp__pluto_without_bbls') }}
),

pluto_geometries_padded_strings as (
    select
        pluto_version,
        borocode,
        wkt,
        LPAD(block, 5, '0') as block,
        LPAD(lot, 4, '0') as lot
    from
        pluto_without_bbls
),

pluto_constructed_bbls as (
    select
        pluto_version,
        borocode,
        block,
        lot,
        wkt,
        CONCAT(borocode, block, lot) as bbl
    from
        pluto_geometries_padded_strings
),

pluto_bbls as (
    select
        pluto_version,
        bbl,
        wkt
    from
        pluto_with_bbls
    union all
    select
        pluto_version,
        bbl,
        wkt
    from
        pluto_constructed_bbls
)

select * from pluto_bbls
