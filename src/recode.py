import json
import logging
from typing import List
import pandas as pd
import requests
from .client import Client

from .util import create_logger
from . import CLIENT_ID, SECRET, TENANT_ID, ZAP_DOMAIN, ZAP_ENGINE


def get_headers():
    client = Client(
        zap_domain=ZAP_DOMAIN,
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        secret=SECRET,
    )
    return client.request_header


class RecodeTracker:
    def __init__(self) -> None:
        self.recode_fields = [
            "primary_applicant",
            "ceqr_leadagency",
            "current_milestone",
            "current_envmilestone",
        ]
        self.primary_applicant = {}
        self.ceqr_leadagency = {}
        self.current_milestone = {}
        self.current_envmilestone = {}
        self.logger = create_logger("Recode Logger", "reused_summary.log")
        self.reused_recodings = {f: 0 for f in self.recode_fields}
        self.total_records_recoded = 0
        self.count_unseen_ID = 0

    def new_recode(self, field: str, mapping: dict):
        self.__getattribute__(field).update(mapping)

    def find_recode(self, row):
        new_ID = False
        self.total_records_recoded += 1
        for field in self.recode_fields:
            value = row[field]
            if value is not None:
                if value in self.__getattribute__(field).keys():
                    row[field] = self.__getattribute__(field)[value]
                    self.reused_recodings[field] += 1
                else:
                    self.count_unseen_ID += 1
                    new_ID = True
        return new_ID, row


class AuthRefresher:
    """Serve fresh headers after 401"""

    def __init__(self):
        self.headers = get_headers()
        self.logger = create_logger(
            "Authorization Refresher Logger", "auth_refresher.log"
        )

    def refresh_headers(self):
        self.headers = get_headers()
        self.logger.info("Got new headers")


def recode_id(data, debug_rows=False):
    """Recode unique ID's from the CRM to human-readable"""
    recode_logger = create_logger("Recode Logger", "recode_logger.log")
    auth_refresher = AuthRefresher()
    if debug_rows:
        data = data.sample(debug_rows)
    recode_tracker = RecodeTracker()
    cleaned = data.apply(
        axis=1,
        func=recode_single_project,
        args=(auth_refresher, recode_tracker, recode_logger),
    )
    recode_tracker.logger.info(
        f"Records that had any ID value recoded: {recode_tracker.total_records_recoded} out of {cleaned.shape[0]}"
    )
    recode_tracker.logger.info(
        f"Where existing recode could be used: {recode_tracker.reused_recodings}"
    )
    recode_tracker.logger.info(
        f"Number of records with new ID for which URL had to be hit {recode_tracker.count_unseen_ID}"
    )
    cleaned.drop(columns=["crm_project_id"], inplace=True)
    return cleaned


def recode_single_project(
    row: pd.Series,
    auth: AuthRefresher,
    recode_tracker: RecodeTracker,
    logger: logging.Logger,
):

    additional_recode, row = recode_tracker.find_recode(row)
    if additional_recode:
        logger.info(f"Hitting URL for row {row.name}")
    else:
        logger.info(f"No additional recode needed for row {row.name}")
    if additional_recode:
        url = expand_url(row.crm_project_id)
        res = requests.get(url, headers=auth.headers)
        if res.status_code != 200:
            auth.refresh_headers()
            res = requests.get(url, headers=auth.headers)
            if res.status_code != 200:
                print(f"broken url {url} produced {res.status_code=}")
                return row
        expanded_project_data = res.json()
        # Potential upgrade: return field instead of entire row
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
            recode_tracker=recode_tracker,
            logger=logger,
        )
        row = convert_to_human_readable(
            expanded=expanded_project_data,
            row=row,
            local_fieldname="current_milestone",
            metadata_field_names=["dcp_CurrentMilestone"],
            metadata_keys={
                "dcp_CurrentMilestone": ("dcp_name", "dcp_projectmilestoneid")
            },
            recode_tracker=recode_tracker,
            logger=logger,
        )
        row = convert_to_human_readable(
            expanded=expanded_project_data,
            row=row,
            local_fieldname="current_envmilestone",
            metadata_field_names=["dcp_currentenvironmentmilestone"],
            metadata_keys={
                "dcp_currentenvironmentmilestone": (
                    "dcp_name",
                    "dcp_projectmilestoneid",
                )
            },
            recode_tracker=recode_tracker,
            logger=logger,
        )
        row = convert_to_human_readable(
            expanded=expanded_project_data,
            row=row,
            local_fieldname="ceqr_leadagency",
            metadata_field_names=["dcp_leadagencyforenvreview"],
            metadata_keys={"dcp_leadagencyforenvreview": ("name", "accountid")},
            recode_tracker=recode_tracker,
            logger=logger,
        )
    return row


def convert_to_human_readable(
    expanded: dict,
    row: pd.Series,
    local_fieldname: str,
    metadata_field_names: List[str],
    metadata_keys: dict,
    recode_tracker: RecodeTracker,
    logger=logging.Logger,
):
    id_val = row[local_fieldname]
    logger.info(
        f"Recoding record {row.name}: field {local_fieldname} has id of {id_val}"
    )
    field_dict = None
    while metadata_field_names and field_dict is None:
        metadata_field = metadata_field_names.pop()
        field_dict = expanded[metadata_field]
    metadata_hr_key, metadata_id_key = (
        metadata_keys[metadata_field][0],
        metadata_keys[metadata_field][1],
    )
    if field_dict is None:
        if id_val is not None:
            raise Exception(
                f"data has {local_fieldname} of {id_val} but expanded of {json.dumps(expanded, indent=2)}"
            )
    else:
        human_readable = field_dict[metadata_hr_key]
        if (field_dict[metadata_id_key] != id_val) and (
            field_dict[metadata_hr_key] != id_val
        ):
            message = f"Mismatch between {field_dict[metadata_id_key]}/{field_dict[metadata_hr_key]} and {id_val} for field {local_fieldname}"
            # raise Exception( message)
            logger.info(message)

        logger.info(f"assinging {human_readable} to field {local_fieldname}")
        row[local_fieldname] = human_readable
        recode_tracker.new_recode(local_fieldname, {id_val: human_readable})
    return row


def expand_url(project_id):
    return f"https://nycdcppfs.crm9.dynamics.com/api/data/v9.1/dcp_projects({project_id})?$select=_dcp_applicant_customer_value,_dcp_currentmilestone_value,dcp_name&$expand=dcp_CurrentMilestone($select=dcp_name),dcp_leadagencyforenvreview($select=name),dcp_applicant_customer_contact($select=fullname),dcp_currentenvironmentmilestone($select=dcp_name),dcp_applicant_customer_account($select=name)"
