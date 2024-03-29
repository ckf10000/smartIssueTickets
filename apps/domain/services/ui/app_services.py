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

from apps.infrastructure.api.platforms import PlatformService
from apps.infrastructure.api.mobile_terminals import stop_app
from apps.annotation.delay_wait import SleepWait, LoopFindElement
from apps.common.libs.dir import get_images_dir, is_exists, join_path
from apps.common.libs.date_extend import (
    get_trip_year_month_day,
    get_datetime_area,
    is_public_holiday,
)


class CtripAppService(PlatformService):
    """
    携程APP
    """

    APP_NAME = "ctrip.android.view"
    IMAGE_DIR = get_images_dir()

    def __init__(self, device=None, app_name: str = None) -> None:
        self.device = device or PlatformService().device
        self.device.start_app(app_name or self.APP_NAME)

    @SleepWait(wait_time=1)
    def touch_home(self) -> None:
        """进入app后，点击【首页】"""
        file_name = join_path([get_images_dir(), "首页.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (154, 2878)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def touch_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】"""
        file_name = join_path([get_images_dir(), "机票.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (445, 560)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def touch_special_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】，点击【特价机票】"""
        file_name = join_path([get_images_dir(), "特价机票.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (517, 592)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def select_departure_city(self) -> None:
        departure_city = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner="\S+",
            global_num=0,
            local_num=2,
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

    def __get_search_first_city(self):
        po = self.device.get_po(
            type="android.view.ViewGroup", name="城市页第1条搜索结果"
        )
        return po[0].children()[1]

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
            type="android.widget.Button",
            name="ctrip.android.view:id/a",
            text="确认",
            global_num=0,
            local_num=2,
            touchable=True,
        )[0]
        search_result.click()

    @SleepWait(wait_time=1)
    def select_arrive_city(self) -> None:
        arrive_city = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner="\S+",
            global_num=0,
            local_num=4,
        )[0]
        arrive_city.click()

    @SleepWait(wait_time=1)
    def select_trip_date(self) -> None:
        trip_date = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner="^出发.*",
            global_num=0,
            local_num=9,
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
        day_str = "{}_red".format(trip_day) if is_public_holiday(date_str=date_str) else trip_day
        file_name = join_path([get_images_dir(), "{}.png".format(day_str)])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
            find_results = self.device.find_all(v=temp)
            if len(find_results) > 0:
                sorted_list = sorted(find_results, key=lambda x: x['result'][0])
                temp = sorted_list[0].get("result")
            else:
                raise ValueError(
                    "According to the image file <{}>, no corresponding element was found".format(
                        file_name
                    )
                )
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
            touchable=True,
        )[0]
        query_special_flight.click()

    @SleepWait(wait_time=1)
    def is_exist_flight_in_screen(self, flight: str) -> bool:
        """
        检索需要购买的航班是否出现在初始的屏幕中
        """
        in_screen = self.device.get_po(type="android.widget.TextView", name="第{}航班航司信息".format(flight))
        if in_screen.exists():
            return True
        else:
            return False

    def touch_flight_inland_single_list_filter(self) -> None:
        po = self.device.get_po(type="android.widget.TextView", name="筛选")
        if po.exists():
            # 说明筛选入口在底部
            print("查询到的航班数量不多，筛选的按钮在UI的底部。")
            self.__touch_flight_inland_single_list_bottom_filter()
        else:
            self.__touch_flight_inland_single_list_top_filter()

    @SleepWait(wait_time=1)
    def touch_clear_filter(self) -> None:
        """
        点击【清空】，防止缓存数据，干扰配置过滤条件，当然需要判断，【清空】按钮，是否为激活状态，未激活的情况下，按钮是灰色，无法点击
        """
        clear_button = self.device.get_po(
            type="android.view.ViewGroup", name="筛选清空按钮"
        )[0]
        clear_button_attr = self.device.get_ui_object_proxy_attr(
            ui_object_proxy=clear_button
        )
        is_enabled = clear_button_attr.get("enabled")
        if is_enabled is True:
            clear_text = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="清空",
                global_num=0,
                local_num=1,
                touchable=False,
            )[0]
            clear_text.click()

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
            touchable=False,
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
            touchable=False,
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
            touchable=False,
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
            # name="{}筛选控件".format(time_area_str),
            text=time_area_str,
            global_num=0,
            local_num=1,
            touchable=False,
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
            touchable=False,
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
            touchable=False,
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
            touchable=False,
        )[0]
        submit_button.click()

    @SleepWait(wait_time=5)
    def select_special_flight(self, flight: str) -> None:
        """
        从特价机票列表中选择本次订单的航班
        """
        desc = "第{}航班航司信息".format(flight)
        special_flight = self.device.get_po(type="android.widget.TextView", name=desc)
        special_flight.click()

    @SleepWait(wait_time=1)
    def get_special_flight_price(self) -> float:
        """
        检索航班经济舱的第二条数据的票价
        """
        lowerest_price_po = self.device.get_po(
            type="android.widget.TextView", name="第2个政策成人价格金额"
        )[0]
        ui_object_proxy_attr = self.device.get_ui_object_proxy_attr(
            ui_object_proxy=lowerest_price_po
        )
        text = ui_object_proxy_attr.get("text")
        print("获取到的机票最低价为：", text)
        # 9999999999.9999999999 表示金额无限大，仅限于作为后续的比较逻辑默认值
        return (
            float(text)
            if isinstance(text, str) and text.isdigit()
            else 9999999999.9999999999
        )

    def is_direct_booking(self) -> True:
        """
        在经济舱航班列表中，存在某些航班，没有【选购】按钮，点击【订】直接进入下单界面，相当于少了一次点击
        """
        booking = self.device.get_po(type="android.widget.TextView", name="btn_book_2预订按钮", text="订")
        if booking.exists():
            return True
        else:
            return False

    @SleepWait(wait_time=1)
    def touch_direct_booking_button(self) -> None:
        """
        在经济舱航班列表中，存在某些航班，点击【订】直接进入下单界面
        """
        direct_booking_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="btn_book_2预订按钮",
            text="订",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        direct_booking_button.click()

    @SleepWait(wait_time=1)
    def touch_booking_the_second_button(self) -> None:
        """
        点击航班经济舱第二条数据中的【选购】
        """
        the_second_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="drop_book_2预订按钮",
            text="选购",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        the_second_button.click()

    @SleepWait(wait_time=5)
    def touch_ordinary_booking_button(self) -> None:
        """
        点击航班经济舱第二条数据中的【普通预订】
        """
        ordinary_booking_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="第2个政策选购第7个X产品预订按钮",
            text="订",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        ordinary_booking_button.click()

    @LoopFindElement(loop=5)
    # @SleepWait(wait_time=3)
    def touch_more_passengers_button(self) -> None:
        """
        点击【更多乘机人】按钮
        """
        add_passenger_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="新增乘机人按钮icon",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        add_passenger_button.click()

    @SleepWait(wait_time=1)
    def touch_add_passengers_button(self) -> None:
        """
        点击【新增乘机人】按钮
        """
        add_passenger_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="乘机人列表新增乘机人文案",
            text="新增乘机人",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        add_passenger_button.click()

    @SleepWait(wait_time=1)
    def enter_passenger_username(self, passenger: str) -> None:
        """
        录入乘客姓名
        """
        passenger_username = self.device.get_po_extend(
            type="android.widget.EditText",
            name="新增乘机人姓名框文案",
            text="与乘机证件一致",
            global_num=0,
            local_num=1,
            touchable=True,
        )[0]
        passenger_username.click()
        passenger_username.set_text(passenger)

    @SleepWait(wait_time=1)
    def enter_passenger_card_id(self, card_id: str) -> None:
        """
        录入乘客证件号码
        """
        passenger_card_id = self.device.get_po_extend(
            type="android.widget.EditText",
            name="新增乘机人证件号码文案",
            text="请输入证件号",
            global_num=0,
            local_num=1,
            touchable=True,
        )[0]
        passenger_card_id.click()
        passenger_card_id.set_text(card_id)

    @SleepWait(wait_time=1)
    def enter_passenger_phone_number(self, phone: str) -> None:
        """
        录入乘客手机号码
        """
        passenger_phone_number = self.device.get_po_extend(
            type="android.widget.EditText",
            name="新增乘机人手机框文案",
            global_num=0,
            local_num=1,
            touchable=True,
        )[0]
        passenger_phone_number.click()
        passenger_phone_number.set_text(phone)

    @SleepWait(wait_time=1)
    def submit_passenger_info(self) -> None:
        """
        点击【完成】按钮，提交乘客信息
        """
        self.device.hide_keyword()
        passenger_info = self.device.get_po_extend(
            type="android.widget.TextView",
            name="新增乘机人完成按钮",
            text="完成",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        passenger_info.click()

    @SleepWait(wait_time=3)
    def submit_passenger_info_confirm(self) -> None:
        """
        点击【确认无误】按钮，提交乘客信息
        """
        passenger_info_confirm = self.device.get_po_extend(
            type="android.view.ViewGroup",
            name="android.view.ViewGroup",
            global_num=0,
            local_num=5,
            touchable=True,
        )[0]
        passenger_info_confirm.click()

    @SleepWait(wait_time=1)
    def add_passenger(self, passenger: str) -> None:
        """
        点击【确定】按钮，添加乘客
        """
        passenger_po = self.device.get_po_extend(
            type="android.widget.TextView",
            name="乘机人列表确定按钮",
            text="确定",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        passenger_po.click()
        print("预定特价机票，已添加乘客: <{}>".format(passenger))

    @SleepWait(wait_time=1)
    def select_insecure(self) -> None:
        """
        选择【无保障】航意航延组合险
        """
        insecure = self.device.get_po_extend(
            type="android.widget.TextView",
            name="航意航延组合险无保障标题",
            text="无保障",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        insecure.click()

    @SleepWait(wait_time=5)
    def touch_fill_order_next_step(self) -> None:
        """
        填订单界面，点击【下一步】
        """
        next_step = self.device.get_po_extend(
            type="android.widget.TextView",
            name="下一步",
            text="下一步",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        next_step.click()

    @SleepWait(wait_time=1)
    def is_duplicate_order(self) -> str:
        """
        如果用户已经下单，系统会有弹框提示，下单重复了
        """
        duplicate_order_1 = self.device.get_po(type="android.widget.TextView",text="我知道了")
        duplicate_order_2 = self.device.get_po(type="android.widget.TextView",name="android.widget.TextView", text="继续预订当前航班")
        duplicate_order_3 = self.device.get_po(type="android.widget.TextView",name="重复订单标题", text="行程冲突提示")
        if duplicate_order_1.exists():
            conflict_prompt = self.device.get_po_extend(
                type="android.widget.TextView",
                name="重复订单提示文案",
                global_num=0,
                local_num=2,
                touchable=False,
            )[0]
            conflict_prompt_str = self.device.get_ui_object_proxy_attr(ui_object_proxy=conflict_prompt).get("text")
            duplicate_order_1.click()
            return conflict_prompt_str
        elif duplicate_order_2.exists():
            conflict_prompt = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                global_num=0,
                local_num=1,
                touchable=False,
            )[0]
            conflict_prompt_str = self.device.get_ui_object_proxy_attr(ui_object_proxy=conflict_prompt).get("text")
            duplicate_order_2.click()
            return conflict_prompt_str
        elif duplicate_order_3.exists():
            conflict_prompt = self.device.get_po_extend(
                type="android.widget.TextView",
                name="重复订单提示文案",
                global_num=0,
                local_num=3,
                touchable=False,
            )[0]
            conflict_prompt_str = self.device.get_ui_object_proxy_attr(ui_object_proxy=conflict_prompt).get("text")
            self.device.touch((400, 500)) # 点击一个随机坐标，尽量靠近上半屏，相当于点击空白处，隐藏掉提示框
            return conflict_prompt_str
        else:
            return ""

    @SleepWait(wait_time=1)
    def touch_select_service_no_need(self) -> None:
        """
        选服务界面，点击【不用了，谢谢】
        """
        no_need = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="不用了，谢谢",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        no_need.click()

    @SleepWait(wait_time=1)
    def touch_to_payment(self) -> None:
        """
        选服务界面，点击【去支付】
        """
        to_payment = self.device.get_po_extend(
            type="android.widget.TextView",
            name="去支付",
            text="去支付",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        to_payment.click()

    @SleepWait(wait_time=1)
    def touch_insure_no(self) -> None:
        """
        选航空意外险界面，点击【否】
        """
        no = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="否",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        no.click()

    @SleepWait(wait_time=5)
    def touch_read_agree(self) -> None:
        """
        我已阅读并同意，点击【同意并支付】
        """
        agree = self.device.get_po_extend(
            type="android.widget.TextView",
            name="去支付",
            text="同意并支付",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        agree.click()

    @SleepWait(wait_time=1)
    def select_more_payment(self) -> None:
        """
        当【同意并支付】后，特殊情况下，会出现支付小弹框，这个时候需要先判断是否存在小框，如果存在，则切换到通用支付选择界面
        """
        more_payment = self.device.get_po(type="", name="", text="")
        if more_payment.exists():
            more_payment.click()
        else:
            print("没有出现支付小弹框，请在通用支付选择界面操作.")

    @SleepWait(wait_time=1)
    def select_point_deduction(self) -> None:
        """
        支付界面，选择【积分抵扣】
        """
        point_deduction = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="100积分抵扣1元",
            global_num=0,
            local_num=4,
            touchable=False,
        )[0]
        point_deduction.click()

    @SleepWait(wait_time=5)
    def touch_bank_card_payment(self) -> None:
        """
        支付界面，选择【银行卡支付】
        """
        point_deduction = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="银行卡支付 ",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        point_deduction.click()

    """
    def __del__(self) -> None:
        stop_app(app_name=self.APP_NAME)
    """


if __name__ == "__main__":
    # from time import sleep

    app = CtripAppService()
    app.device.hide_keyword()
    # app.device.wake()
    # sleep(8)
    # app.touch_home()
    # app.touch_flight_ticket()
    # app.touch_special_flight_ticket()
    # app.select_departure_city()
    # app.enter_search_value(search_value="HET")
    # app.select_search_result_first_city()
    # app.sumbit_search_result()
    # app.select_arrive_city()
    # app.enter_search_value(search_value="HLH")
    # app.select_search_result_first_city()
    # app.sumbit_search_result()
    # app.select_trip_date()
    # app.select_trip_expect_month(date_str="2024-04-04 13:00")
    # app.select_trip_expect_day(date_str="2024-04-04 13:00")
    # app.touch_only_query_some_day()
    # app.touch_query_special()
    # app.touch_flight_inland_single_list_filter()
    # app.touch_filter_departure_time()
    # app.select_filter_departure_time_area(date_str="2024-04-04 13:00")
    # app.touch_filter_airline()
    # app.select_filter_airline_company("华夏航空")
    # app.touch_filter_submit_button()
