from typing import Dict
import pandas as pd
import requests
from sqlalchemy import text
from .recode_id import recode_id

OPEN_DATA = ["dcp_projects", "dcp_projectbbls"]


PICKLIST_METADATA_LINK = "https://nycdcppfs.crm9.dynamics.com/api/data/v9.1/EntityDefinitions(LogicalName='dcp_project')/Attributes/Microsoft.Dynamics.CRM.PicklistAttributeMetadata?$select=LogicalName&$expand=OptionSet"
STATUS_METADATA_LINK = "https://nycdcppfs.crm9.dynamics.com/api/data/v9.1/EntityDefinitions(LogicalName='dcp_project')/Attributes/Microsoft.Dynamics.CRM.StatusAttributeMetadata?$select=LogicalName&$expand=OptionSet"
RECODE_FIELDS = {
    "dcp_projects": [
        ("dcp_visibility", "dcp_visibility"),
        ("statuscode", "project_status"),
        ("dcp_publicstatus", "public_status"),
        ("dcp_ulurp_nonulurp", "ulurp_non"),
        ("dcp_ceqrtype", "ceqr_type"),
        ("dcp_easeis", "eas_eis"),
        ("dcp_applicanttype", "applicant_type"),
        ("dcp_borough", "borough"),
        ("dcp_citycouncildistrict", "cc_district"),
        ("dcp_mihmappedbutnotproposed", "mih_mapped_no_res"),
    ],
    "dcp_projectbbls": ["validated_borough", "unverified_borough"],
}

CRM_CODE_PROJECT_IS_VISIBLE = "717170003"


def make_crm_table(sql_engine, dataset_name) -> None:
    # TODO add missing MapZAP non-public here
    if dataset_name == "dcp_projects":
        statement_crm = """
            BEGIN;
            DROP TABLE IF EXISTS dcp_projects_crm;
            CREATE TABLE dcp_projects_crm as 
            (SELECT dcp_name as project_id,
                    dcp_projectname as project_name,
                    dcp_projectid as crm_project_id,
                    dcp_projectbrief as project_brief,
                    dcp_visibility,
                    statuscode as project_status,
                    dcp_publicstatus as public_status,
                    dcp_ulurp_nonulurp as ulurp_non,
                    dcp_actionnumbers as actions,
                    dcp_ulurpnumbers as ulurp_numbers,
                    dcp_ceqrtype as ceqr_type, 
                    dcp_ceqrnumber as ceqr_number,
                    dcp_eis as eas_eis, 
                    _dcp_leadagencyforenvreview_value as ceqr_leadagency,
                    _dcp_applicant_customer_value as primary_applicant, 
                    dcp_applicanttype as applicant_type, 
                    dcp_borough as borough, 
                    dcp_validatedcommunitydistricts as community_district,
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
                    from dcp_projects);
                COMMIT;
            """
        with sql_engine.begin() as sql_conn:
            sql_conn.execute(statement=text(statement_crm))
    elif dataset_name == "dcp_projectbbls":
        statement = """
            BEGIN;
            DROP TABLE IF EXISTS dcp_projectbbls_crm;
            CREATE TABLE dcp_projectbbls_crm as 
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
             from dcp_projectbbls INNER JOIN dcp_projects_crm 
            on SUBSTRING(dcp_projectbbls.dcp_name, 0,10) = dcp_projects_crm.project_id);
            COMMIT;
        """
        with sql_engine.begin() as sql_conn:
            sql_conn.execute(statement=text(statement))
    else:
        raise NotImplementedError(f"Unimplemented open dataset: {dataset_name}")

def make_open_data_table(sql_engine, dataset_name) -> None:
    if dataset_name == "dcp_projects":
        statement_visible = """
            BEGIN;
            DROP TABLE IF EXISTS dcp_projects_visible;
            CREATE TABLE dcp_projects_visible as 
            (SELECT project_id,
                    project_name,
                    crm_project_id,
                    project_brief,
                    dcp_visibility,
                    project_status,
                    public_status,
                    ulurp_non,
                    actions,
                    ulurp_numbers,
                    ceqr_type, 
                    ceqr_number,
                    eas_eis, 
                    ceqr_leadagency,
                    primary_applicant, 
                    applicant_type, 
                    borough, 
                    community_district,
                    cc_district, 
                    flood_zone_a,
                    flood_zone_shadedx, 
                    current_milestone, 
                    current_milestone_date,
                    current_envmilestone, 
                    current_envmilestone_date, 
                    app_filed_date, 
                    noticed_date, 
                    certified_referred, 
                    approval_date,
                    completed_date,
                    mih_flag,
                    mih_option1,
                    mih_option2, 
                    mih_workforce,
                    mih_deepaffordability, 
                    mih_mapped_no_res
                    from dcp_projects_crm where dcp_visibility = '717170003');
                COMMIT;
            """
        with sql_engine.begin() as sql_conn:
            sql_conn.execute(statement=text(statement_visible))
    elif dataset_name == "dcp_projectbbls":
        statement = """
            BEGIN;
            DROP TABLE IF EXISTS dcp_projectbbls_visible;
            CREATE TABLE dcp_projectbbls_visible as 
            (SELECT dcp_projectbbls_crm.project_id as project_id,
                    dcp_projectbbls_crm.bbl as bbl,
                    dcp_projectbbls_crm.validated_borough as validated_borough,
                    dcp_projectbbls_crm.validated_block as validated_block,
                    dcp_projectbbls_crm.validated_lot as validated_lot,
                    dcp_projectbbls_crm.validated as validated,
                    dcp_projectbbls_crm.validated_date as validated_date,
                    dcp_projectbbls_crm.unverified_borough as unverified_borough,
                    dcp_projectbbls_crm.unverified_block as unverified_block,
                    dcp_projectbbls_crm.unverified_lot as unverified_lot
             from dcp_projectbbls_crm INNER JOIN dcp_projects_visible 
            on SUBSTRING(dcp_projectbbls_crm.project_id, 0,10) = dcp_projects_visible.project_id);
            COMMIT;
        """
        with sql_engine.begin() as sql_conn:
            sql_conn.execute(statement=text(statement))
    else:
        raise NotImplementedError(f"Unimplemented open dataset: {dataset_name}")



def open_data_recode(name: str, data: pd.DataFrame, headers: Dict) -> pd.DataFrame:
    recoder = {}

    fields_to_lookup, fields_to_rename = get_fields(name)

    # Standardize integer representation
    print("standardize integer representation ...")
    data[fields_to_rename] = data[fields_to_rename].apply(
        func=lambda x: x.str.split(".").str[0], axis=1
    )

    # Get metadata
    print("get_metadata ...")
    metadata_values = get_metadata(headers)

    # Construct list of just fields we want to recode
    print("Construct list of fields to recode ...")
    fields_to_recode = {}
    for field in metadata_values:
        if field["LogicalName"] in fields_to_lookup:
            fields_to_recode[field["LogicalName"]] = field

    print("populate recoder ...")
    for crm_name, local_name in zip(fields_to_lookup, fields_to_rename):
        field_metadata = fields_to_recode[crm_name]
        field_recodes = {}
        print(f"for {crm_name}, {local_name} ...")
        for category in field_metadata["OptionSet"]["Options"]:
            field_recodes[str(category["Value"])] = category["Label"][
                "LocalizedLabels"
            ][0]["Label"]
        if name == "dcp_projectbbls":
            recoder["validated_borough"] = field_recodes
            recoder["unverified_borough"] = field_recodes
        elif name == "dcp_projects":
            recoder[local_name] = field_recodes

    print("replace values using recoder ...")
    data.replace(to_replace=recoder, inplace=True)

    return data


def get_fields(name) -> tuple[list, list]:
    if name == "dcp_projectbbls":
        fields_to_lookup = ["dcp_borough"]
        fields_to_rename = RECODE_FIELDS[name]
    elif name == "dcp_projects":
        fields_to_lookup = [t[0] for t in RECODE_FIELDS[name]]
        fields_to_rename = [t[1] for t in RECODE_FIELDS[name]]
    else:
        raise f"no recode written for {name}"
    return fields_to_lookup, fields_to_rename


def get_metadata(headers) -> list:
    metadata_values = []
    for link in [PICKLIST_METADATA_LINK, STATUS_METADATA_LINK]:
        res = requests.get(link, headers=headers)
        metadata_values.extend(res.json()["value"])
    return metadata_values
