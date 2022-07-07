from typing import Dict, List
from flaskapp.models import User
from flaskapp.utilities.module import get_current_user
from flaskapp.utilities.Validator import NullValidator, UniqueValidator


class UserValidator(NullValidator, UniqueValidator):
    def __init__(self, request: Dict, queryset: User = User) -> None:
        UniqueValidator.__init__(self, queryset)
        NullValidator.__init__(self, request)

    def _is_field_unique(self, field):
        return self.queryset.__table__.columns[field].unique and field != 'id'

    def _is_field_required(self, field: str) -> bool:
        return not self.queryset.__table__.columns[field].nullable

    def _get_fields(self) -> List:
        return self.queryset.__table__.columns.keys()

    def _add_password_field(self, list: List) -> List:
        return [*list, 'password']

    def _get_required_fields(self) -> List:
        required_fields = []
        fields_list = self._get_fields()

        for field in fields_list:
            if self._is_field_required(field):
                required_fields.append(field)

        return required_fields

    def _get_unique_fields(self) -> List:
        unique_fields = []
        fields_list = self._get_fields()

        for field in fields_list:
            if self._is_field_unique(field):
                unique_fields.append(field)

        return unique_fields

    def nullValidator(self):
        field_name_list = self._get_required_fields()
        field_name_list = self._add_password_field(field_name_list)
        NullValidator.__call__(self, field_name_list)
        return self

    def uniqueValidator(self):
        unique_list = self._get_unique_fields()
        for field_name in unique_list:
            value = self.request.get(field_name)
            UniqueValidator.__call__(self, value, field_name)
