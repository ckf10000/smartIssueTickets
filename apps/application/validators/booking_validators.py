# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     booking_validators.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/05 01:00:49
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from decimal import Decimal
from apps.annotation.log_service import logger
from apps.common.config.flight_ticket import ticket_fee

__all__ = ["FlightTicketValidator"]

class FlightTicketValidator(object):
    """机票校验器"""

    @classmethod
    def validator_payment_with_deduction(cls, pre_sale_amount: Decimal, actual_amount: Decimal, deduction_amount: Decimal) -> bool:
        """支付校验, 抵扣场景，默认积分抵扣场景，可以抵扣10.00元"""
        if deduction_amount >= 10.00:
            expected_amount = pre_sale_amount + ticket_fee.get("fuel_fee") + ticket_fee.get("airport_fee") - deduction_amount
            if expected_amount >= actual_amount:
                logger.info("订单的实际支付金额<{}>小于或等于预期的支付金额<{}>，可以正常交易.".format(actual_amount, expected_amount))
                return True
            else:
                logger.error("订单的实际支付金额<{}>大于预期的支付金额<{}>，交易需要取消.".format(actual_amount, expected_amount))
                return False
        else:
            if deduction_amount > 0:
                logger.warning("抵扣金额<{}>不足10.00元.".format(deduction_amount))
            else:
                logger.error("获取到的抵扣金额<{}>有异常.".format(deduction_amount))
            return False


