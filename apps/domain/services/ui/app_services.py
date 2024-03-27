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
from apps.common.libs.dir import get_images_dir, is_exists, join_path
from apps.common.libs.date_extend import get_trip_year_month_day, get_datetime_area


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

    @SleepWait(wait_time=5)
    def select_search_result_first_city(self):
        search_result = self.__get_search_first_city()
        search_result.click()

    @SleepWait(wait_time=3)
    def sumbit_search_result(self):
        """选择城市后，需要点击【确认】按钮"""
        """
        file_name = join_path([get_images_dir(), "搜索确认.png"])
        if is_exists(file_name):
            template = self.device.get_cv_template(file_name=file_name)
            result = self.device.find_all(v=template)
            temp = result[0].get("result")
        else:
            temp = (1273, 624) # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.adb_touch(v=temp)
        """
        search_result = self.device.get_po_extend(
            type='android.widget.Button', 
            name='ctrip.android.view:id/a', 
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

    @SleepWait(wait_time=8)
    def touch_query_special(self) -> None:
        """
        特价机票界面，点击【查询特价】
        """
        query_special_flight = self.device.get_po_extend(
            type="android.widget.Button",
            name="ctrip.android.view:id/a",
            text="查询特价",
            global_num=0,
            local_num=5,
            touchable=True
        )[0]
        query_special_flight.click()

    def touch_flight_inland_single_list_filter(self) -> None:
        po = self.device.get_po(type="android.widget.TextView", name="筛选")
        if po.exists():
            # 说明筛选入口在底部
            print("查询到的航班数量不多，筛选的按钮在UI的底部。")
            self.__touch_flight_inland_single_list_bottom_filter()
        else:
            self.__touch_flight_inland_single_list_top_filter()

    @SleepWait(wait_time=1)
    def __touch_flight_inland_single_list_top_filter(self) -> None:
        """
        航线特价机票查询列表，点击顶部的【筛选】
        """
        filter = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="筛选",
            global_num=0,
            local_num=1,
            touchable=False
        )[0]
        filter.click()

    @SleepWait(wait_time=1)
    def __touch_flight_inland_single_list_bottom_filter(self) -> None:
        """
        航线特价机票查询列表，点击底部的【筛选】
        """
        filter = self.device.get_po_extend(
            type="android.widget.TextView",
            name="筛选",
            text="筛选",
            global_num=0,
            local_num=2,
            touchable=False
        )[0]
        filter.click()

    @SleepWait(wait_time=1)
    def touch_filter_departure_time(self) -> None:
        """
        航班列表底部的筛选界面，点击【起飞时间】
        """
        departure_time = self.device.get_po_extend(
            type="android.widget.TextView",
            name="起飞时间",
            text="起飞时间",
            global_num=0,
            local_num=2,
            touchable=False
        )[0]
        departure_time.click()

    @SleepWait(wait_time=1)
    def select_filter_departure_time_area(self, date_str: str) -> None:
        """
        选择筛选条件中的起飞时间区域，00:00~06:00,06:00~12:00,12:00~18:00,18:00~24:00
        """
        time_area_str = get_datetime_area(date_str=date_str)
        time_area = self.device.get_po_extend(
            type="android.widget.TextView",
            name="{}筛选控件".format(time_area_str),
            text=time_area_str,
            global_num=0,
            local_num=1,
            touchable=False
        )[0]
        time_area.click()

    @SleepWait(wait_time=1)
    def touch_filter_airline(self) -> None:
        """
        航班列表底部的筛选界面，点击【航空公司】
        """
        airline = self.device.get_po_extend(
            type="android.widget.TextView",
            name="航空公司",
            text="航空公司",
            global_num=0,
            local_num=2,
            touchable=False
        )[0]
        airline.click()

    @SleepWait(wait_time=1)
    def select_filter_airline_company(self, ac: str) -> None:
        """
        选择筛选条件中的航空公司
        """
        airline_company = self.device.get_po_extend(
            type="android.widget.TextView",
            name="筛选按钮{}".format(ac),
            text=ac,
            global_num=0,
            local_num=2,
            touchable=False
        )[0]
        airline_company.click()

    @SleepWait(wait_time=8)
    def touch_filter_submit_button(self) -> None:
        """
        确认筛选条件
        """
        submit_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="筛选确定按钮文案",
            global_num=0,
            local_num=1,
            touchable=False
        )[0]
        submit_button.click()

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

    """
    def __del__(self) -> None:
        stop_app(app_name=self.APP_NAME)
    """

if __name__ == "__main__":
    from time import sleep
    app = CtripAppService()
    app.device.wake()
    sleep(8)
    app.touch_home()
    app.touch_flight_ticket()
    app.touch_special_flight_ticket()
    app.select_departure_city()
    app.enter_search_value(search_value="HET")
    app.select_search_result_first_city()
    app.sumbit_search_result()
    app.select_arrive_city()
    app.enter_search_value(search_value="HLH")
    app.select_search_result_first_city()
    app.sumbit_search_result()
    app.select_trip_date()
    app.select_trip_expect_month(date_str="2024-04-04 13:00")
    app.select_trip_expect_day(date_str="2024-04-04 13:00")
    app.touch_only_query_some_day()
    app.touch_query_special()
    app.touch_flight_inland_single_list_filter()
    app.touch_filter_departure_time()
    app.select_filter_departure_time_area(date_str="2024-04-04 13:00")
    app.touch_filter_airline()
    app.select_filter_airline_company("华夏航空")
    app.touch_filter_submit_button()
