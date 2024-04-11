# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     ctrip_repository.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/11 15:40:49
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from apps.common.libs.service_environ import get_config

config = get_config()


class CTripConfigRepository(object):
    ctrip_config = getattr(config, "ctrip")
    payment_config = getattr(config, "payment")

    @classmethod
    def get_ctrip_group_config(cls, group_name: str) -> t.Dict:
        group_config = getattr(cls.ctrip_config, group_name)
        return dict(
            ctrip_username=getattr(group_config, "account"),
            user_pass=getattr(group_config, "sec_key"),
            payment_pass=getattr(group_config, "pay_key"),
            internal_phone=getattr(group_config, "internal_phone")
        )

    @classmethod
    def get_payment_group_config(cls, group_name: str) -> t.Tuple:
        group_config = getattr(cls.payment_config, group_name)
        binding_ctrip = getattr(
            getattr(group_config, "pay_account"), "binding_ctrip")
        return binding_ctrip, dict(
            out_pf=getattr(group_config, "out_pf"),
            out_ticket_account=getattr(group_config, "out_ticket_account"),
            pay_account_type=getattr(group_config, "pay_account_type"),
            pay_account=getattr(getattr(group_config, "pay_account"), "qlv")
        )

    @classmethod
    def get_passenger_info(cls, qlv_passengers: t.Dict) -> t.Dict:
        return dict(
            passenger=qlv_passengers.get("PName"),
            card_id=qlv_passengers.get("IDNo"),
            passenger_phone=qlv_passengers.get("Mobile"),
            age_stage=qlv_passengers.get("PType"),
            card_type=qlv_passengers.get("IDType")
        )
