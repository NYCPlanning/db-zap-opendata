with source as (

    select * from {{ source('zap_projects', '20230526_recoded') }}

),

zap_projects as (

    select
        project_id,
        project_name,
        certified_referred as project_certified_referred_date,
        -- new columns
        applicant_type,
        ulurp_numbers,
        ulurp_non as ulurp_type,
        ceqr_number,
        ceqr_type,
        project_status,
        public_status,
        actions as action_codes,
        EXTRACT(
            isoyear
            from
            certified_referred
        ) as project_certified_referred_year

        -- not in recoded data
        {# dcp_leaddivision as lead_division, #}
        {# dcp_currentzoningdistrict as current_zoning_district, #}
        {# dcp_proposedzoningdistrict as proposed_zoning_district, #}
        {# dcp_wrpreviewrequired as wrp_review_required, #}
        {# dcp_femafloodzonecoastala as fema_flood_zone_coastal, #}
        {# dcp_femafloodzonev as fema_flood_zone_v #}
    from source
)

select * from zap_projects
