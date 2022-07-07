from email import message
from typing import Dict, List
from sqlalchemy.exc import IntegrityError


def qs_filter(queryset, **keyword):
    queryset = queryset.query.filter_by(**keyword)
    if queryset.scalar():
        return queryset
    return queryset.scalar()


def qs_exist(queryset):
    try:
        return queryset.scalar()
    except:
        return False


class NullValidator:

    def __init__(self, request: Dict, message: str = None) -> None:
        self.message = message
        self.request = request

    def _is_column_null(self, col: str) -> bool:
        return not (col in self.request and self.request.get(col))

    def get_error_msg(self, field_name_list: List):
        null_err_list = []

        message = self.message or '此欄位不能為空'

        for attr in field_name_list:
            if self._is_column_null(attr):
                null_err_list.append({attr: message})
        return null_err_list

    def __call__(self, field_name_list):
        null_err_list = self.get_error_msg(field_name_list)

        if len(null_err_list) != 0:
            raise ValueError(null_err_list)


class UniqueValidator:
    def __init__(self, queryset, message: str = None) -> None:
        self.message = message
        self.queryset = queryset

    def filter_query(self, queryset, value: str, filed_name: str):
        filter_kwargs = {filed_name: value}
        return qs_filter(queryset, **filter_kwargs)

    def __call__(self, vlaue, field_name):
        queryset = self.queryset
        queryset = self.filter_query(queryset, vlaue, field_name)

        if qs_exist(queryset):
            message = self.message or '已經有人使用'
            raise ValueError({field_name: message})
