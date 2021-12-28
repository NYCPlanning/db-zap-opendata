OPEN_DATA = ["dcp_projects", "dcp_projectbbls"]


def make_open_data_table(sql_engine, dataset_name) -> None:
    if dataset_name == "dcp_projects":
        sql_engine.execute(
            """BEGIN;
            DROP TABLE IF EXISTS dcp_projects_visible;
        CREATE TABLE dcp_projects_visible as 
        (SELECT dcp_name as project_id,
                dcp_projectname as project_name,
                dcp_projectbrief as project_brief,
                statuscode as project_status,
                dcp_publicstatus as public_status,
                dcp_ulurp_nonulurp as ulurp_non,
                dcp_actionnumbers as actions,
                dcp_ulurpnumbers as ulurp_numbers,
                dcp_ceqrtype as ceqr_type, 
                dcp_ceqrnumber as ceqr_number,
                dcp_easeis as eas_eis, 
                _dcp_leadagencyforenvreview_value as ceqr_leadagency,
                _dcp_applicant_customer_value as primary_applicant, 
                dcp_applicanttype as dcp_applicanttype, 
                dcp_borough as borough, 
                dcp_validatedcitycouncildistricts as community_district,
                dcp_citycouncildistrict as cc_district, 
                dcp_femafloodzonea as flood_zone_a,
                dcp_femafloodzoneshadedx as flood_zone_shadedx, 
                _dcp_currentmilestone_value as current_milestone, 
                dcp_currentmilestoneactualstartdate as current_milestone_date,
                _dcp_currentenvironmentmilestone_value as current_envmilestone, 
                dcp_currentenvmilestoneactualstartdate as current_envmilestone_date, 
                dcp_applicationfileddate as app_filed_date, 
                dcp_noticeddate as noticed_date, 
                dcp_certifiedreferred as certified_referred, 
                dcp_approvaldate as approval_date,
                dcp_projectcompleted as completed_date,
                dcp_createmodifymandatoryinclusionaryhousinga as mih_flag,
                dcp_createmodifymihareaoption1 as mih_option1,
                dcp_createmodifymihareaoption2 as mih_option2, 
                dcp_createmodifymihareaworkforceoption as mih_workforce,
                dcp_createmodifymihareadeepaffordabilityoptio as mih_deepaffordability, 
                dcp_mihmappedbutnotproposed as mih_mapped_no_res
                from dcp_projects where dcp_visibility = '717170003');
            COMMIT;"""
        )
    if dataset_name == "dcp_projectbbls":
        sql_engine.execute(
            """BEGIN;
            DROP TABLE IF EXISTS dcp_projectbbls_visible;
            CREATE TABLE dcp_projectbbls_visible as 
            (SELECT dcp_projectbbls.dcp_name as project_id,
                    dcp_projectbbls.dcp_bblnumber as bbl,
                    dcp_projectbbls.dcp_validatedborough as validated_borough,
                    dcp_projectbbls.dcp_validatedblock as validated_block,
                    dcp_projectbbls.dcp_validatedlot as validated_lot,
                    dcp_projectbbls.dcp_bblvalidated as validated,
                    dcp_projectbbls.dcp_bblvalidateddate as validated_date,
                    dcp_projectbbls.dcp_userinputborough as unverified_borough,
                    dcp_projectbbls.dcp_userinputblock as unverified_block,
                    dcp_projectbbls.dcp_userinputlot as unverified_lot
             from dcp_projectbbls INNER JOIN dcp_projects_visible 
            on SUBSTRING(dcp_projectbbls.dcp_name, 0,10) = dcp_projects_visible.project_id);
            COMMIT;"""
        )
