with source as (

    select * from {{ source('zap_projects', '20230515') }}

),

zap_projects as (

    select
        dcp_projectid as project_id,
        dcp_projectname as project_name,
        dcp_name as project_code,
        dcp_certifiedreferred as project_certified_referred_date,
        EXTRACT(
            isoyear
            from
            dcp_certifiedreferred
        ) as project_certified_referred_year,
        -- new columns
        dcp_applicanttype as applicant_type,
        dcp_ulurpnumbers as ulurp_numbers,
        dcp_ceqrnumber as ceqr_number,
        dcp_ceqrtype as ceqr_type,
        dcp_leaddivision as lead_division,
        statuscode as project_status,
        dcp_publicstatus as public_status,
        dcp_actionnumbers as action_numbers,
        dcp_currentzoningdistrict as current_zoning_district,
        dcp_proposedzoningdistrict as proposed_zoning_district,
        dcp_wrpreviewrequired as wrp_review_required,
        dcp_femafloodzonecoastala as fema_flood_zone_coastal,
        dcp_femafloodzonev as fema_flood_zone_v
        -- more to add
    from source
)

select * from zap_projects
