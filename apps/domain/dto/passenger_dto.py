# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     passenger_dto.py
# Description:  乘客DTO
# Author:       ckf10000
# CreateDate:   2024/04/05 21:25:19
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.common.libs.domain_base_model import DomainBaseModel

class PassengerDTO(DomainBaseModel):
    __age: int
    __phone: str
    __username: str
    __card_id: str # 证件号
    __card_type: str # 证件类型
    __age_stage: str # 乘客年龄阶段，儿童/成人
    __card_expiration_date: str # 证件有效日期

    # 定义__slots__变量，指定允许的属性列表
    # __slots__ = ('age', 'phone', 'card_id', 'username', 'card_type', 'age_stage', 'card_expiration_date')

    def __init__(self, **kwargs) -> None:
        self.__age = kwargs.get("age")
        self.__phone = kwargs.get("phone")
        self.__card_id = kwargs.get("card_id")
        self.__username = kwargs.get("username")
        self.__card_type = kwargs.get("card_type")
        self.__age_stage = kwargs.get("age_stage")
        self.__card_expiration_date = kwargs.get("card_expiration_date")

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, age: int) -> None:
        self.__age = age

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, phone: str) -> None:
        self.__phone = phone

    @property
    def card_id(self) -> int:
        return self.__card_id

    @card_id.setter
    def card_id(self, card_id: str) -> None:
        self.__card_id = card_id

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @property
    def card_type(self) -> str:
        return self.__card_type

    @card_type.setter
    def card_type(self, card_type: str) -> None:
        self.__card_type = card_type

    @property
    def age_stage(self) -> str:
        return self.__age_stage

    @age_stage.setter
    def age_stage(self, age_stage: str) -> None:
        self.__age_stage = age_stage

    @property
    def card_expiration_date(self) -> str:
        return self.__card_expiration_date

    @card_expiration_date.setter
    def card_expiration_date(self, card_expiration_date: str) -> None:
        self.__card_expiration_date = card_expiration_date

    def is_empty(self) -> bool:
        if self.__card_id:
            return False
        else:
            return True


if __name__ == "__main__":
    p = PassengerDTO(card_id="123456789")
    print(p)
    print(p.is_empty())
    print(p.attributes())
