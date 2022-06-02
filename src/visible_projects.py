from typing import Dict, List
import pandas as pd
import requests
import json

OPEN_DATA = ["dcp_projects", "dcp_projectbbls"]


PICKLIST_METADATA_LINK = "https://nycdcppfs.crm9.dynamics.com/api/data/v9.1/EntityDefinitions(LogicalName='dcp_project')/Attributes/Microsoft.Dynamics.CRM.PicklistAttributeMetadata?$select=LogicalName&$expand=OptionSet"
STATUS_METADATA_LINK = "https://nycdcppfs.crm9.dynamics.com/api/data/v9.1/EntityDefinitions(LogicalName='dcp_project')/Attributes/Microsoft.Dynamics.CRM.StatusAttributeMetadata?$select=LogicalName&$expand=OptionSet"
RECODE_FIELDS = {
    "dcp_projects": [
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


def make_open_data_table(sql_engine, dataset_name) -> None:
    if dataset_name == "dcp_projects":
        sql_engine.execute(
            """BEGIN;
            DROP TABLE IF EXISTS dcp_projects_visible;
        CREATE TABLE dcp_projects_visible as 
        (SELECT dcp_name as project_id,
                dcp_projectname as project_name,
                dcp_projectid as crm_project_id,
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


def open_data_recode(name: str, data: pd.DataFrame, headers: Dict) -> pd.DataFrame:

    recoder = {}

    fields_to_lookup, fields_to_rename = get_fields(name)

    # Standardize integer representation
    data[fields_to_rename] = data[fields_to_rename].apply(
        func=lambda x: x.str.split(".").str[0], axis=1
    )

    # Get metadata

    metadata_values = get_metadata(headers)

    # Construct list of just fields we want to recode
    fields_to_recode = {}
    for field in metadata_values:
        if field["LogicalName"] in fields_to_lookup:
            fields_to_recode[field["LogicalName"]] = field

    for crm_name, local_name in zip(fields_to_lookup, fields_to_rename):
        field_metadata = fields_to_recode[crm_name]
        field_recodes = {}
        for category in field_metadata["OptionSet"]["Options"]:
            field_recodes[str(category["Value"])] = category["Label"][
                "LocalizedLabels"
            ][0]["Label"]
        if name == "dcp_projectbbls":
            recoder["validated_borough"] = field_recodes
            recoder["unverified_borough"] = field_recodes
        elif name == "dcp_projects":
            recoder[local_name] = field_recodes
    data.replace(to_replace=recoder, inplace=True)

    if name == "dcp_projects":
        print(f"nrows in data passed to recode id {data.shape[0]}")
        data = recode_id(data, headers, debug_rows=1000)
        print(f"nrows in data return by recode id {data.shape[0]}")

    return data


def get_fields(name):
    if name == "dcp_projectbbls":
        fields_to_lookup = ["dcp_borough"]
        fields_to_rename = RECODE_FIELDS[name]

    elif name == "dcp_projects":
        fields_to_lookup = [t[0] for t in RECODE_FIELDS[name]]
        fields_to_rename = [t[1] for t in RECODE_FIELDS[name]]
    else:
        raise f"no recode written for {name}"
    return fields_to_lookup, fields_to_rename


def recode_id(data, headers, debug_rows=False):
    """Recode unique ID's from the CRM to human-readable"""
    if debug_rows:
        data = data.iloc[:debug_rows, :]
    cleaned = data.apply(axis=1, func=recode_single_project, args=(headers,))
    cleaned.drop(columns=["crm_project_id"], inplace=True)
    return cleaned


def recode_single_project(row, headers):
    url = expand_url(row.crm_project_id)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"broken url {url} produced {res.status_code=}")
    expanded_project_data = res.json()
    row = convert_to_human_readable(
        expanded=expanded_project_data,
        row=row,
        local_fieldname="primary_applicant",
        metadata_field_names=[
            "dcp_applicant_customer_account",
            "dcp_applicant_customer_contact",
        ],
        metadata_keys={
            "dcp_applicant_customer_account": ("name", "accountid"),
            "dcp_applicant_customer_contact": ("fullname", "contactid"),
        },
    )
    row = convert_to_human_readable(
        expanded=expanded_project_data,
        row=row,
        local_fieldname="current_milestone",
        metadata_field_names=["dcp_CurrentMilestone"],
        metadata_keys={"dcp_CurrentMilestone": ("dcp_name", "dcp_projectmilestoneid")},
    )
    row = convert_to_human_readable(
        expanded=expanded_project_data,
        row=row,
        local_fieldname="current_envmilestone",
        metadata_field_names=["dcp_currentenvironmentmilestone"],
        metadata_keys={
            "dcp_currentenvironmentmilestone": ("dcp_name", "dcp_projectmilestoneid")
        },
    )
    row = convert_to_human_readable(
        expanded=expanded_project_data,
        row=row,
        local_fieldname="ceqr_leadagency",
        metadata_field_names=["dcp_leadagencyforenvreview"],
        metadata_keys={"dcp_leadagencyforenvreview": ("name", "accountid")},
    )
    return row


def convert_to_human_readable(
    expanded: dict,
    row: pd.Series,
    local_fieldname: str,
    metadata_field_names: List[str],
    metadata_keys: dict,
):
    field_dict = None
    while metadata_field_names and field_dict is None:
        metadata_field = metadata_field_names.pop()
        field_dict = expanded[metadata_field]
    metadata_hr_key, metadata_id_key = (
        metadata_keys[metadata_field][0],
        metadata_keys[metadata_field][1],
    )
    if field_dict is None:
        if row[local_fieldname] is not None:
            raise Exception(
                f"data has {local_fieldname} of {row[local_fieldname]} but expanded of {json.dumps(expanded, indent=2)}"
            )
    else:
        if field_dict[metadata_id_key] != row[local_fieldname]:
            raise Exception(
                f"Mismatch between {field_dict[metadata_id_key]} and {row[local_fieldname]}"
            )

        row[local_fieldname] = field_dict[metadata_hr_key]
    return row


def get_metadata(headers):
    metadata_values = []
    for link in [PICKLIST_METADATA_LINK, STATUS_METADATA_LINK]:
        res = requests.get(link, headers=headers)
        metadata_values.extend(res.json()["value"])
    return metadata_values


def expand_url(project_id):
    return f"https://nycdcppfs.crm9.dynamics.com/api/data/v9.1/dcp_projects({project_id})?$select=_dcp_applicant_customer_value,_dcp_currentmilestone_value,dcp_name&$expand=dcp_CurrentMilestone($select=dcp_name),dcp_leadagencyforenvreview($select=name),dcp_applicant_customer_contact($select=fullname),dcp_currentenvironmentmilestone($select=dcp_name),dcp_applicant_customer_account($select=name)"
