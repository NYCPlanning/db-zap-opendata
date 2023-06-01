with source as (

    select * from {{ source('zap_projects', '20230526_recoded') }}

),

zap_projects as (

    select
        project_id as dcp_name,
        project_name,
        certified_referred as project_certified_referred_date,
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

    from source
)

select * from zap_projects
