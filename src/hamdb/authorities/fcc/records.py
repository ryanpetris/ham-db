#!/usr/bin/env python3

from typing import Callable


def fcc_record(record_type: str, primary_key: str, fields: list[str]):
    def init(class_type):
        record_def = RecordDef(class_type, record_type, primary_key, list(fields))
        Record.record_map[record_def.record_type] = record_def

        return class_type

    return init


def _clean_numeric(value):
    if not value:
        return None

    return int(value)


def _clean_date(value):
    if not value:
        return None

    print(value)
    return value


class RecordDef:
    @property
    def record_class(self):
        return self._record_class

    @property
    def record_type(self):
        return self._record_type

    @property
    def primary_key(self):
        return self._primary_key

    @property
    def fields(self):
        return self._fields

    def __init__(self, record_class: Callable, record_type: str, primary_key: str, fields: list[str]):
        self._record_class: Callable = record_class
        self._record_type: str = record_type.upper()
        self._primary_key: str = primary_key
        self._fields: list[str] = fields

        self._record_class.record_def = self

    def init_record(self, data: list[str] = None):
        record = self._record_class()

        if data:
            self.set_record_data(record, data)

        return record

    def set_record_data(self, record: 'Record', data: list[str]):
        field_length = len(self._fields)
        data_length = len(data)

        if field_length != data_length:
            raise Exception(f"record length mismatch; expected {field_length}, received {data_length}")

        for i in range(0, field_length):
            setattr(record, self._fields[i], data[i])


class Record:
    record_map: dict[str, RecordDef] = {}
    record_def: RecordDef = None

    def __init__(self):
        super().__init__()

        self.record_type: str
        self.unique_system_identifier: int

    @staticmethod
    def init(record_type: str, data: list[str]) -> 'Record':
        record_def = Record.record_map.get(record_type.upper(), None)

        if record_def is None:
            raise Exception(f"invalid or unknown record type: {record_type}")

        return record_def.init_record(data)

    @staticmethod
    def type_exists(record_type: str) -> bool:
        return record_type.upper() in Record.record_map

    @staticmethod
    def get_types() -> list[str]:
        return list(Record.record_map.keys())

    def __repr__(self):
        out = "Record.init("
        out += repr(self.record_def.record_type)
        out += ", "
        out += repr([str(getattr(self, f)) for f in self.record_def.fields])
        out += ")"

        return out

    def __str__(self):
        return str(self.__dict__)

    def __setattr__(self, key, value):
        if not value:
            value = None

        super().__setattr__(key, value)


@fcc_record(
    "AM",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "uls_file_num",
        "ebf_number",
        "callsign",
        "operator_class",
        "group_code",
        "region_code",
        "trustee_callsign",
        "trustee_indicator",
        "physician_certification",
        "ve_signature",
        "systematic_callsign_change",
        "vanity_callsign_change",
        "vanity_relationship",
        "previous_callsign",
        "previous_operator_class",
        "trustee_name"
    ]
)
class AmRecord(Record):
    def __init__(self):
        super().__init__()

        self.uls_file_num: str
        self.ebf_number: str
        self.callsign: str
        self.operator_class: str
        self.group_code: str
        self.region_code: int
        self.trustee_callsign: str
        self.trustee_indicator: str
        self.physician_certification: str
        self.ve_signature: str
        self.systematic_callsign_change: str
        self.vanity_callsign_change: str
        self.vanity_relationship: str
        self.previous_callsign: str
        self.previous_operator_class: str
        self.trustee_name: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier" or key == "region_code":
            value = _clean_numeric(value)

        super().__setattr__(key, value)


@fcc_record(
    "CO",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "uls_file_num",
        "callsign",
        "comment_date",
        "description",
        "status_code",
        "status_date"
    ]
)
class CoRecord(Record):
    def __init__(self):
        super().__init__()

        self.uls_file_num: str
        self.callsign: str
        self.comment_date: str
        self.description: str
        self.status_code: int
        self.status_date: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier":
            value = _clean_numeric(value)

        if key == "status_date":
            value = _clean_date(value)

        super().__setattr__(key, value)


@fcc_record(
    "EN",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "uls_file_num",
        "ebf_number",
        "callsign",
        "entity_type",
        "licensee_id",
        "entity_name",
        "first_name",
        "mi",
        "last_name",
        "suffix",
        "phone",
        "fax",
        "email",
        "street_address",
        "city",
        "state",
        "zip_code",
        "po_box",
        "attention_line",
        "sgin",
        "frn",
        "applicant_type_code",
        "applicant_type_other",
        "status_code",
        "status_date",
        "lic_category_code",
        "linked_license_id",
        "linked_callsign"
    ]
)
class EnRecord(Record):
    def __init__(self):
        super().__init__()

        self.uls_file_num: str
        self.ebf_number: str
        self.callsign: str
        self.entity_type: str
        self.licensee_id: str
        self.entity_name: str
        self.first_name: str
        self.mi: str
        self.last_name: str
        self.suffix: str
        self.phone: str
        self.fax: str
        self.email: str
        self.street_address: str
        self.city: str
        self.state: str
        self.zip_code: str
        self.po_box: str
        self.attention_line: str
        self.sgin: str
        self.frn: str
        self.applicant_type_code: str
        self.applicant_type_other: str
        self.status_code: str
        self.status_date: str
        self.lic_category_code: str
        self.linked_license_id: int
        self.linked_callsign: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier" or key == "linked_license_id":
            value = _clean_numeric(value)

        if key == "status_date":
            value = _clean_date(value)

        super().__setattr__(key, value)

@fcc_record(
    "HD",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "uls_file_num",
        "ebf_number",
        "callsign",
        "license_status",
        "radio_service_code",
        "grant_date",
        "expired_date",
        "cancellation_date",
        "eligibility_rule_num",
        "applicant_type_code_reserved",
        "alien",
        "alien_government",
        "alien_corporation",
        "alien_officer",
        "alien_control",
        "revoked",
        "convicted",
        "adjudged",
        "involved_reserved",
        "common_carrier",
        "non_common_carrier",
        "private_comm",
        "fixed",
        "mobile",
        "radiolocation",
        "satellite",
        "developmental_or_sta",
        "interconnected_service",
        "certifier_first_name",
        "certifier_mi",
        "certifier_last_name",
        "certifier_suffix",
        "certifier_title",
        "gender",
        "african_american",
        "native_american",
        "hawaiian",
        "asian",
        "white",
        "ethnicity",
        "effective_date",
        "last_action_date",
        "auction_id",
        "reg_stat_broad_serv",
        "band_manager",
        "type_serv_broad_serv",
        "alien_ruling",
        "licensee_name_change",
        "whitespace_ind",
        "additional_cert_choice",
        "additional_cert_answer",
        "discontinuation_ind",
        "regulatory_compliance_ind",
        "eligibility_cert_900",
        "transition_plan_cert_900",
        "return_spectrum_cert_900",
        "payment_cert_900"
    ]
)
class HdRecord(Record):
    def __init__(self):
        super().__init__()

        self.uls_file_num: str
        self.ebf_number: str
        self.callsign: str
        self.license_status: str
        self.radio_service_code: str
        self.grant_date: str
        self.expired_date: str
        self.cancellation_date: str
        self.eligibility_rule_num: str
        self.applicant_type_code_reserved: str
        self.alien: str
        self.alien_government: str
        self.alien_corporation: str
        self.alien_officer: str
        self.alien_control: str
        self.revoked: str
        self.convicted: str
        self.adjudged: str
        self.involved_reserved: str
        self.common_carrier: str
        self.non_common_carrier: str
        self.private_comm: str
        self.fixed: str
        self.mobile: str
        self.radiolocation: str
        self.satellite: str
        self.developmental_or_sta: str
        self.interconnected_service: str
        self.certifier_first_name: str
        self.certifier_mi: str
        self.certifier_last_name: str
        self.certifier_suffix: str
        self.certifier_title: str
        self.gender: str
        self.african_american: str
        self.native_american: str
        self.hawaiian: str
        self.asian: str
        self.white: str
        self.ethnicity: str
        self.effective_date: str
        self.last_action_date: str
        self.auction_id: int
        self.reg_stat_broad_serv: str
        self.band_manager: str
        self.type_serv_broad_serv: str
        self.alien_ruling: str
        self.licensee_name_change: str
        self.whitespace_ind: str
        self.additional_cert_choice: str
        self.additional_cert_answer: str
        self.discontinuation_ind: str
        self.regulatory_compliance_ind: str
        self.eligibility_cert_900: str
        self.transition_plan_cert_900: str
        self.return_spectrum_cert_900: str
        self.payment_cert_900: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier" or key == "auction_id":
            value = _clean_numeric(value)

        super().__setattr__(key, value)


@fcc_record(
    "HS",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "uls_file_num",
        "callsign",
        "log_date",
        "code"
    ]
)
class HsRecord(Record):
    def __init__(self):
        super().__init__()

        self.uls_file_num: str
        self.callsign: str
        self.log_date: str
        self.code: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier":
            value = _clean_numeric(value)

        super().__setattr__(key, value)


@fcc_record(
    "LA",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "callsign",
        "attachment_code",
        "attachment_desc",
        "attachment_date",
        "attachment_filename",
        "action_performed"
    ]
)
class LaRecord(Record):
    def __init__(self):
        super().__init__()

        self.callsign: str
        self.attachment_code: str
        self.attachment_desc: str
        self.attachment_date: str
        self.attachment_filename: str
        self.action_performed: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier":
            value = _clean_numeric(value)

        super().__setattr__(key, value)


@fcc_record(
    "SC",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "uls_file_num",
        "ebf_number",
        "callsign",
        "special_condition_type",
        "special_condition_code",
        "status_code",
        "status_date"
    ]
)
class ScRecord(Record):
    def __init__(self):
        super().__init__()

        self.uls_file_num: int
        self.ebf_number: int
        self.callsign: str
        self.special_condition_type: str
        self.special_condition_code: str
        self.status_code: str
        self.status_date: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier" or key == "special_condition_code":
            value = _clean_numeric(value)

        if key == "status_date":
            value = _clean_date(value)

        super().__setattr__(key, value)


@fcc_record(
    "SF",
    "unique_system_identifier",
    [
        "record_type",
        "unique_system_identifier",
        "uls_file_num",
        "ebf_number",
        "callsign",
        "lic_freeform_cond_type",
        "unique_lic_freeform_id",
        "sequence_number",
        "lic_freeform_condition",
        "status_code",
        "status_date"
    ]
)
class SfRecord(Record):
    def __init__(self):
        super().__init__()

        self.uls_file_num: int
        self.ebf_number: int
        self.callsign: str
        self.lic_freeform_cond_type: str
        self.unique_lic_freeform_id: str
        self.sequence_number: str
        self.lic_freeform_condition: str
        self.status_code: str
        self.status_date: str

    def __setattr__(self, key, value):
        if key == "unique_system_identifier" or key == "unique_lic_freeform_id" or key == "sequence_number":
            value = _clean_numeric(value)

        if key == "status_date":
            value = _clean_date(value)

        super().__setattr__(key, value)
