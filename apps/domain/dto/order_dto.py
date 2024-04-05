# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     order_dto.py
# Description:  订单DTO
# Author:       ckf10000
# CreateDate:   2024/04/05 20:42:57
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from decimal import Decimal

from apps.domain.dto.passenger_dto import PassengerDTO
from apps.common.libs.domain_base_model import DomainBaseModel

__all__ = ["FlightTicketOrderDTO"]

class FlightItineraryDTO(DomainBaseModel):
    """航班行程单"""
    __itinerary_id: str  # 行程单id
    __passenger: PassengerDTO  # 乘客信息

    # 定义__slots__变量，指定允许的属性列表
    # __slot__ = ('itinerary_id', 'passenger')

    def __init__(self, itinerary_id: str, passenger: t.Dict) -> None:
        self.__passenger = self.__to_passenger_dto(**passenger)
        self.__itinerary_id = itinerary_id

    @property
    def itinerary_id(self) -> str:
        return self.__itinerary_id

    @itinerary_id.setter
    def itinerary_id(self, itinerary_id: str) -> None:
        self.__itinerary_id = itinerary_id

    @property
    def passenger(self) -> PassengerDTO:
        return self.__passenger

    def __to_passenger_dto(self, **kwargs) -> PassengerDTO:
        p = PassengerDTO(**kwargs)
        if p.is_empty() is False:
            return p
        else:
            return None

    @passenger.setter
    def passenger(self, passenger: t.Dict) -> None:
        self.__passenger = self.__to_passenger_dto(**passenger)

    def is_empty(self) -> bool:
        if self.__itinerary_id:
            return False
        else:
            return True

class FlightTicketOrderDTO(DomainBaseModel):
    """机票订单DTO"""
    __order_id: str  # 订单id
    __flight: str  # 航班编号
    __ac: str  # 航司
    __departure_time: str  # 起飞时间
    __arrive_time: str  # 抵达时间
    __order_price: Decimal # 订单价格
    __departure_city: str  # 起飞城市编号
    __arrive_city: str  # 抵达城市编号
    __arrive_city_name: str # 抵达城市名
    __departure_city_name: str  # 起飞城市名
    __itinerary_info: t.Union[FlightItineraryDTO]  # 行程信息

    def __init__(self, itinerary_info: t.List, **kwargs) -> None:
        self.__ac = kwargs.get("ac")
        self.__flight = kwargs.get("flight")
        self.__order_id = kwargs.get("order_id")
        self.__arrive_city = kwargs.get("arrive_city")
        self.__arrive_time = kwargs.get("arrive_time")
        self.__order_price = kwargs.get("order_price")
        self.__departure_time = kwargs.get("departure_time")
        self.__departure_city = kwargs.get("departure_city")
        self.__arrive_city_name = kwargs.get("arrive_city_name")
        self.__departure_city_name = kwargs.get("departure_city_name")
        self.__itinerary_info = self.__to_itinerary_info_dto(*itinerary_info)

    @property
    def ac(self) -> str:
        return self.__ac

    @ac.setter
    def ac(self, ac: str) -> None:
        self.__ac = ac

    @property
    def flight(self) -> str:
        return self.__flight

    @flight.setter
    def flight(self, flight: str) -> None:
        self.__flight = flight

    @property
    def order_id(self) -> str:
        return self.__order_id

    @order_id.setter
    def order_id(self, order_id: str) -> None:
        self.__order_id = order_id

    @property
    def itinerary_info(self) -> t.Union[FlightItineraryDTO]:
        return self.__itinerary_info

    def __to_itinerary_info_dto(self, *args) -> t.Union[FlightItineraryDTO]:
        return self.init_list_model(
            data_list=args, model=FlightItineraryDTO, is_exist_primary_key=True
        )

    @itinerary_info.setter
    def itinerary_info(self, itinerary_info: t.List) -> None:
        self.__itinerary_info = self.__to_itinerary_info_dto(*itinerary_info)

    @property
    def order_price(self) -> Decimal:
        return self.__order_price

    @order_price.setter
    def order_price(self, order_price: Decimal) -> None:
        self.__order_price = order_price

    @property
    def arrive_city(self) -> str:
        return self.__arrive_city

    @arrive_city.setter
    def arrive_city(self, arrive_city: str) -> None:
        self.__arrive_city = arrive_city

    @property
    def arrive_time(self) -> str:
        return self.__arrive_time

    @arrive_time.setter
    def arrive_time(self, arrive_time: str) -> None:
        self.__arrive_time = arrive_time

    @property
    def departure_time(self) -> str:
        return self.__departure_time

    @departure_time.setter
    def departure_time(self, departure_time: str) -> None:
        self.__departure_time = departure_time

    @property
    def departure_city(self) -> str:
        return self.__departure_city

    @departure_city.setter
    def departure_city(self, departure_city: str) -> None:
        self.__departure_city = departure_city

    @property
    def arrive_city_name(self) -> str:
        return self.__arrive_city_name

    @arrive_city_name.setter
    def arrive_city_name(self, arrive_city_name: str) -> None:
        self.__arrive_city_name = arrive_city_name

    @property
    def departure_city_name(self) -> str:
        return self.__departure_city_name

    @departure_city_name.setter
    def departure_city_name(self, departure_city_name: str) -> None:
        self.__departure_city_name = departure_city_name

    def is_empty(self) -> bool:
        if self.__order_id:
            return False
        else:
            return True


if __name__ == "__main__":
    itinerary_info = dict(
        itinerary_id = "187-123456789", 
        passenger=dict(
            card_id="123456789", 
            username="张三", 
            phone="18569520328",
            age_stage="成人",
            age=34,
            card_type="身份证",
            card_expiration_date="2028-10-20"
        )
    )
    f = FlightItineraryDTO(**itinerary_info)
    print(f)
    o = FlightTicketOrderDTO(
        departure_time="2024-04-07 12:10",
        flight="MF8358",
        ac="厦门航空",
        departure_city="WUH",
        departure_city_name="武汉",
        arrive_city="XMN",
        arrive_time="2024-04-07 14:35",
        arrive_city_name="厦门",
        passenger="罗杨",
        age_stage="成人",
        order_price=647.00,
        order_id="202404070001",
        itinerary_info=[itinerary_info],
    )
    print(o)
