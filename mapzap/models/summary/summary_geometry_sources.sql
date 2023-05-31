with product_mapzap as (
    select * from {{ ref('product_mapzap') }}
)

select
    geometry_source,
    count(*) as geometry_source_count,
    sum(case when wkt is not null then 1 else 0 end) as geometry_count
from product_mapzap
group by geometry_source
