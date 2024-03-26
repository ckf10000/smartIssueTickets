# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     app_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/23 23:19:20
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from pandas import DataFrame

from apps.annotation.delay_wait import SleepWait
from apps.infrastructure.api.platforms import PlatformService
from apps.infrastructure.api.mobile_terminals import stop_app
from apps.common.libs.date_extend import get_trip_year_month_day
from apps.common.libs.dir import get_images_dir, is_exists, join_path


class CtripAppService(PlatformService):
    """
    携程APP
    """
    APP_NAME = "ctrip.android.view"
    IMAGE_DIR = get_images_dir()

    def __init__(self, device=None, app_name: str=None) -> None:
        self.device = device or PlatformService().device
        self.device.start_app(app_name or self.APP_NAME)

    @SleepWait(wait_time=1)
    def touch_home(self) -> None:
        """进入app后，点击【首页】"""
        file_name = join_path([get_images_dir(), "首页.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (154, 2878) # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def touch_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】"""
        file_name = join_path([get_images_dir(), "机票.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (445, 560) # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def touch_special_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】，点击【特价机票】"""
        file_name = join_path([get_images_dir(), "特价机票.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (517, 592) # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def select_departure_city(self) -> None:
        departure_city = self.device.get_po_extend(
            type='android.widget.TextView', 
            name='ctrip.android.view:id/a', 
            textMatches_inner="\S+",
            global_num=0,
            local_num=2
        )[0]
        departure_city.click()

    @SleepWait(wait_time=3)
    def enter_search_value(self, search_value: str) -> None:
        search_box = self.device.poco(type="android.widget.EditText")
        search_box.click()
        search_box.set_text(search_value)

    @SleepWait(wait_time=3)
    def select_search_result_first_city(self):
        search_result = self.__get_search_first_city()
        search_result.click()

    @SleepWait(wait_time=3)
    def sumbit_search_result(self):
        """选择城市后，需要点击【确认】按钮"""
        """
        file_name = join_path([get_images_dir(), "搜索确认.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (1273, 624) # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)
        """
        search_result = self.device.get_po_extend(
            type="android.widget.Button",
            name="ctrip.android.view:id/a",
            text="确认",
            global_num=0,
            local_num=2,
            touchable=True
        )[0]
        search_result.click()

    @SleepWait(wait_time=1)
    def select_arrive_city(self) -> None:
        arrive_city = self.device.get_po_extend(
            type='android.widget.TextView', 
            name='ctrip.android.view:id/a', 
            textMatches_inner="\S+",
            global_num=0,
            local_num=4
        )[0]
        arrive_city.click()

    @SleepWait(wait_time=1)
    def select_trip_date(self) -> None:
        trip_date = self.device.get_po_extend(
            type='android.widget.TextView', 
            name='ctrip.android.view:id/a', 
            textMatches_inner="^出发.*",
            global_num=0,
            local_num=9
        )[0]
        trip_date.click()

    @SleepWait(wait_time=1)
    def select_trip_expect_month(self, date_str: str) -> None:
        _, trip_month, _ = get_trip_year_month_day(date_str=date_str)
        top_month_area = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            text=trip_month,
            touchable=False,
            global_num=0,
            local_num=2,
        )[0]
        top_month_area.click()

    @SleepWait(wait_time=2)
    def select_trip_expect_day(self, date_str: str) -> None:
        _, _, trip_day = get_trip_year_month_day(date_str=date_str)
        file_name = join_path([get_images_dir(), "{}.png".format(trip_day)])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
            find_results = self.device.find_all(v=temp)
            if len(find_results) > 0:
                temp = find_results[0].get("result")
            else:
                raise ValueError("According to the image file <{}>, no corresponding element was found".format(file_name))
        else:
            raise ValueError("<{}> file does not exist".format(file_name))
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def touch_only_query_some_day(self) -> None:
        """
        点击 【预计出发日期】 界面的 【仅查询当天】 按钮
        """
        only_query_some_day = self.device.get_po_extend(
            type="android.widget.Button",
            name="ctrip.android.view:id/a",
            text="仅查询当天",
            global_num=0,
            local_num=5,
        )[0]
        only_query_some_day.click()


    def touch_my(self) -> None:
        """进入app后，点击【我的】"""

    def get_flights(self, from_city: str, arrive_city: str, date: str) -> DataFrame:
        """查询航班"""
        pass

    def get_order(self, order_id: str) -> t.Dict:
        """查询订单"""
        pass

    def add_passenger(self, username: str, card_num: str, phone_num: str) -> None:
        """添加乘客/旅客"""
        pass

    def __get_search_first_city(self):
        po = self.device.get_po(type="android.view.ViewGroup", name="城市页第1条搜索结果")
        return po[0].children()[1]

    def __del__(self) -> None:
        stop_app(app_name=self.APP_NAME)

if __name__ == "__main__":
    from time import sleep
    app = CtripAppService()
    sleep(8)
    app.touch_home()
    app.touch_flight_ticket()
    app.touch_special_flight_ticket()
    # app.select_departure_city()
    # app.enter_search_value(search_value="CKG")
    # app.select_search_result_first_city()
    # app.sumbit_search_result()
    app.select_arrive_city()
    app.enter_search_value(search_value="SHA")
    app.select_search_result_first_city()
    app.sumbit_search_result()
    # app.select_trip_date()
    # app.select_trip_expect_month(date_str="2024-04-02 17:30")
    # app.select_trip_expect_day(date_str="2024-04-02 17:30")
    # app.touch_only_query_some_day()


