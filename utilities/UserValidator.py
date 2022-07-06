from typing import Dict, List
from new.models import User
from new.utilities.module import get_current_user


class UserValidator:
    def __init__(self, user_data: Dict, user_model: User = User) -> None:
        self.user_data = user_data
        self.user = user_model

    def _is_column_unique(self, col):
        return self.user.__table__.columns[col].unique and col != 'id'

    def _is_column_required(self, col: str) -> bool:
        return not self.user.__table__.columns[col].nullable

    def _get_columns_name(self) -> List:
        return User.__table__.columns.keys()

    def _get_required_col_list(self) -> List:
        cols_required_list = []
        cols_list = self._get_columns_name()

        for col in cols_list:
            if self._is_column_required(col):
                cols_required_list.append(col)

        cols_required_list.append('password')
        return cols_required_list

    def _get_unique_col_list(self) -> List:
        unique_cols_list = []
        cols_list = self._get_columns_name()

        for col in cols_list:
            if self._is_column_unique(col):
                unique_cols_list.append(col)

        return unique_cols_list

    def _is_column_null(self, col: str) -> bool:
        return not (col in self.user_data and self.user_data.get(col))

    def validate_blank(self) -> List:
        blank_err_msgs = []
        required_list = self._get_required_col_list()

        for attr in required_list:
            if self._is_column_null(attr):
                blank_err_msgs.append({attr: f'\{attr}\ 此欄為不能為空'})
        return blank_err_msgs

    def validate_duplicate(self) -> List:
        duplicate_err = []
        unique_list = self._get_unique_col_list()

        for attr in unique_list:
            user_exist = get_current_user({attr: self.user_data.get(attr)})
            if user_exist:
                duplicate_err.append(
                    {'message': f'this\'{attr}\'is duplicated', 'detail': attr})
        return duplicate_err
