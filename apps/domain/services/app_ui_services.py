# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     app_ui_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/23 23:19:20
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from decimal import Decimal
from poco.exceptions import PocoNoSuchNodeException

from apps.common.annotation.log_service import logger
from apps.common.libs.utils import get_ui_object_proxy_attr
from apps.infrastructure.api.platforms import PlatformService
from apps.infrastructure.api.mobile_terminals import stop_app
from apps.common.libs.dir import get_images_dir, is_exists, join_path
from apps.common.annotation.delay_wait import SleepWait, LoopFindElement
from apps.common.libs.date_extend import get_trip_year_month_day, get_datetime_area, is_public_holiday


class CtripAppService(PlatformService):
    """
    携程APP
    """
    IMAGE_DIR = get_images_dir()

    def __init__(self, device=None, app_name: str = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app_name = app_name or "ctrip.android.view"
        self.device = device or PlatformService().device

    def start(self) -> None:
        self.device.start_app(self.app_name)

    def stop(self) -> None:
        stop_app(self.app_name)

    def restart(self) -> None:
        stop_app(self.app_name)
        self.device.start_app(self.app_name)

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
            textMatches_inner=r"\S+",
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
    def select_search_result_first_city(self, select_value: str):
        search_result = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner=".* {} .*".format(select_value),
            global_num=0,
            local_num=2,
            touchable=False
        )[0]
        value = search_result.get_text().strip()
        search_result.click()
        logger.info("从搜索结果中，选择<{}>这条数据.".format(value))

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
            textMatches_inner=r"\S+",
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
        day_str = "{}_red".format(trip_day) if is_public_holiday(
            date_str=date_str) else "{}_blue".format(trip_day)
        file_name = join_path([get_images_dir(), "{}.png".format(day_str)])
        logger.info("需要识别日历中的日期文件是：{}".format(file_name))
        if is_exists(file_name):
            # threshold 提高识别灵敏度，灵敏度太低，容易将相似的结果匹配出来
            temp = self.device.get_cv_template(
                file_name=file_name, threshold=0.9)
            find_results = self.device.find_all(v=temp)
            if isinstance(find_results, t.List) and len(find_results) > 0:
                sorted_list = sorted(find_results, key=lambda x: (
                    x['result'][1], x['result'][0]))
                temp = sorted_list[0].get("result")
            else:
                raise ValueError(
                    "According to the image file <{}>, no corresponding element was found".format(file_name))
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

    def is_exist_flight_in_screen(self, flight: str) -> bool:
        """
        检索需要购买的航班是否出现在初始的屏幕中
        """
        logger.info("判断航班<{}>机票信息是否在初始列表当中...".format(flight))
        in_screen = self.device.get_po(
            type="android.widget.TextView", name="第{}航班航司信息".format(flight))
        if in_screen.exists():
            return True
        else:
            return False

    def touch_flight_inland_single_list_filter(self) -> None:
        po = self.device.get_po(type="android.widget.TextView", name="筛选")
        if po.exists():
            # 说明筛选入口在底部
            logger.info("查询到的航班数量不多，筛选的按钮在UI的底部。")
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
        clear_button_attr = get_ui_object_proxy_attr(
            ui_object_proxy=clear_button)
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
        filter1 = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="筛选",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        filter1.click()

    @SleepWait(wait_time=1)
    def __touch_flight_inland_single_list_bottom_filter(self) -> None:
        """
        航线特价机票查询列表，点击底部的【筛选】
        """
        filter1 = self.device.get_po_extend(
            type="android.widget.TextView",
            name="筛选",
            text="筛选",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        filter1.click()

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
        special_flight = self.device.get_po(
            type="android.widget.TextView", name=desc)
        if special_flight.exists():
            abs_position = self.device.get_abs_position(element=special_flight)
            # special_flight.click()
            logger.info("选择：{}".format(desc))
            self.device.touch((abs_position[0], abs_position[1] - 200))
        else:
            raise ValueError("当前页面没有找到", desc)

    @SleepWait(wait_time=1)
    def get_special_flight_amount(self) -> Decimal:
        """
        检索航班经济舱的第二条数据的金额
        """
        lowerest_amount_po = self.device.get_po(
            type="android.widget.TextView", name="第2个政策成人价格金额"
        )[0]
        ui_object_proxy_attr = get_ui_object_proxy_attr(
            ui_object_proxy=lowerest_amount_po)
        text = ui_object_proxy_attr.get("text")
        logger.info("获取到的机票最低价为：{}".format(text))
        # 9999999999.9999999999 表示金额无限大，仅限于作为后续的比较逻辑默认值
        return Decimal(text) if isinstance(text, str) and text.isdigit() else 9999999999.9999999999

    def is_direct_booking(self) -> True:
        """
        在经济舱航班列表中，存在某些航班，没有【选购】按钮，点击【订】直接进入下单界面，相当于少了一次点击
        """
        booking = self.device.get_po(
            type="android.widget.TextView", name="btn_book_2预订按钮", text="订")
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

    @SleepWait(wait_time=2)
    def check_user_login(self, username: str, password: str) -> None:
        try:
            login_page_poco = self.device.get_po(type="android.widget.TextView", name="ctrip.android.view:id/a",
                                                 text="账号密码登录")
            if login_page_poco.exists():
                logger.warning("系统用户<{}>已经退出，需要重新登录".format(username))
                username_poco = self.device.get_po_extend(
                    type="android.widget.EditText", name="android.widget.EditText", textMatches_inner=r"^\d+.*",
                    global_num=0, local_num=2, touchable=True
                )[0]
                # username_poco.click()
                username_poco.set_text(username)
                password_poco = self.device.get_po(
                    type="android.widget.EditText", name="android.widget.EditText", text="登录密码"
                )
                # password_poco.click()
                password_poco.set_text(password)
                # 勾选隐私保护
                privacy_protection = self.device.get_po(
                    type="android.widget.ImageView", name="ctrip.android.view:id/a", desc="勾选服务协议和个人信息保护指引"
                )
                privacy_protection.click()
                login_poco = self.device.get_po(type="android.widget.TextView", name="ctrip.android.view:id/a",
                                                text="登录")
                login_poco.click()
        except (PocoNoSuchNodeException, Exception) as e:
            logger.error(str(e))

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

    @LoopFindElement(loop=5)
    # @SleepWait(wait_time=1)
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
    def touch_passenger_card_type(self) -> None:
        """
        点击【证件类型】
        """
        passenger_card_type = self.device.get_po(
            type="android.widget.TextView", name="新增乘机人证件类型文案")
        passenger_card_type.click()
        logger.info("点击【证件类型】")

    @SleepWait(wait_time=1)
    def select_passenger_card_type(self, card_type: str) -> None:
        """
        选择合适的证件类型
        """
        passenger_card_type = self.device.get_po(
            type="android.widget.TextView", text=card_type)
        passenger_card_type.click()
        logger.info("选择【{}】".format(card_type))

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
        file_name = join_path([get_images_dir(), "键盘隐藏.png"])
        self.device.hide_keyword(file_name=file_name)
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
        """
        passenger_info_confirm = self.device.get_po_extend(
            type="android.view.ViewGroup",
            name="android.view.ViewGroup",
            global_num=0,
            local_num=5,
            touchable=True,
        )[0]
        passenger_info_confirm.click()
        """
        file_name = join_path([get_images_dir(), "乘机人信息_确认无误.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (723, 1413)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @LoopFindElement(loop=5)
    # @SleepWait(wait_time=1)
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
        logger.info("预定特价机票，已添加乘客: <{}>".format(passenger))

    @SleepWait(wait_time=1)
    def select_insecure(self) -> None:
        """
        选择【无保障】航意航延组合险
        """
        # 先滑屏
        self.device.quick_slide_screen(duration=0.5)
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
        duplicate_order_1 = self.device.get_po(
            type="android.widget.TextView", text="我知道了")
        duplicate_order_2 = self.device.get_po(type="android.widget.TextView", name="android.widget.TextView",
                                               text="继续预订当前航班")
        duplicate_order_3 = self.device.get_po(
            type="android.widget.TextView", name="重复订单标题", text="行程冲突提示")
        if duplicate_order_1.exists():
            conflict_prompt = self.device.get_po_extend(
                type="android.widget.TextView",
                name="重复订单提示文案",
                global_num=0,
                local_num=2,
                touchable=False,
            )[0]
            conflict_prompt_str = get_ui_object_proxy_attr(
                ui_object_proxy=conflict_prompt).get("text")
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
            conflict_prompt_str = get_ui_object_proxy_attr(
                ui_object_proxy=conflict_prompt).get("text")
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
            conflict_prompt_str = get_ui_object_proxy_attr(
                ui_object_proxy=conflict_prompt).get("text")
            self.device.touch((400, 500))  # 点击一个随机坐标，尽量靠近上半屏，相当于点击空白处，隐藏掉提示框
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
    def touch_payment_method(self) -> None:
        """点击【付款方式】"""
        try:
            payment_method = self.device.get_po(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="付款方式"
            )
            payment_method.click()
            logger.info("在支付弹窗界面，点击选择【付款方式】")
        except (PocoNoSuchNodeException, Exception):
            payment_method = self.device.get_po(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="换卡支付，支持境外卡"
            )
            payment_method.click()
            logger.info("在安全收银台界面，点击选择【换卡支付，支持境外卡】")

    @SleepWait(wait_time=1)
    def select_payment_method(self, payment_method: str = "浦发银行储蓄卡(7397)") -> None:
        """选择【xxxy银行储蓄卡(xxxx)】"""
        method = self.device.get_po(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text=payment_method
        )
        method.click()
        logger.info("点击选择【{}】".format(payment_method))

    @SleepWait(wait_time=1)
    def select_more_payment(self) -> None:
        """
        当【同意并支付】后，特殊情况下，会出现支付小弹框，这个时候需要先判断是否存在小框，如果存在，则切换到通用支付选择界面
        """
        try:
            more_payment = self.device.get_po(type="android.widget.TextView", name="android.widget.TextView",
                                              text="更多付款方式")
            more_payment.click()
            logger.info("小弹框选择【更多付款方式】.")
        except (PocoNoSuchNodeException, Exception):
            logger.info("没有出现支付小弹框，请在通用支付选择界面操作.")

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
            text="银行卡支付",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        point_deduction.click()

    def get_tickect_actual_amount(self) -> Decimal:
        """
        确定使用积分抵扣后，票据的实际支付金额
        """
        tickect_actual_amount = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            textMatches_inner=r"^¥\d+.\d*",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        actual_amount = tickect_actual_amount.get_text()
        actual_amount = Decimal(actual_amount[1:]) if isinstance(
            actual_amount, str) else 9999999999.9999999999
        return actual_amount

    def get_tickect_deduction_amount(self) -> Decimal:
        """
        使用积分抵扣的金额
        """
        tickect_deduction_amount = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            textMatches_inner=r"^-¥\d+.\d*",
            global_num=0,
            local_num=4,
            touchable=False,
        )[0]
        deduction_amount = tickect_deduction_amount.get_text()
        deduction_amount = Decimal(deduction_amount[2:]) if isinstance(deduction_amount,
                                                                       str) else -9999999999.9999999999
        return deduction_amount

    @SleepWait(wait_time=10)
    def enter_payment_pass(self, payment_pass: str) -> None:
        """
        请输入支付密码
        """
        device = PlatformService.minicap_device()
        payment_pass = payment_pass if isinstance(payment_pass, str) else str(payment_pass)
        for char in payment_pass:
            file_name = join_path([get_images_dir(), "支付_{}.png".format(char)])
            if is_exists(file_name):
                temp = device.get_cv_template(file_name=file_name)
                device.touch(v=temp)
            else:
                raise ValueError("文件<{}>缺失...", format(file_name))

    @SleepWait(wait_time=1)
    def get_order_with_payment_amount(self) -> Decimal:
        """获取支付成功后的订单金额"""
        payment_amount = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            textMatches_inner=r"^\d+.\d*",
            global_num=0,
            local_num=5,
            touchable=False,
        )[0]
        payment_amount = payment_amount.get_text()
        logger.info("从支付成功界面获取到的实际支付金额是: {}".format(payment_amount))
        payment_amount = Decimal(payment_amount) if isinstance(
            payment_amount, str) else -9999999999.9999999999
        return payment_amount

    @SleepWait(wait_time=1)
    def get_order_with_payment_method(self) -> t.Dict:
        """获取支持成功后的支付方式"""
        payment_method = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            textMatches_inner=".+(?:储蓄卡|信用卡).*",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        payment_method = payment_method.get_text()
        logger.info("从支付成功界面获取到的支付方式是: {}".format(payment_method))
        payment_method_slice = payment_method.split(" ")
        return dict(
            bank_name=payment_method_slice[0],  # 银行名称
            card_type=payment_method_slice[1],  # 银行卡类型，这里支持储蓄卡，信用卡
            last_four_digits=payment_method_slice[1:-1]  # 银行卡末四位数字
        )

    @SleepWait(wait_time=8)
    def touch_payment_complete(self) -> None:
        """在支付成功界面，点击【完成】"""
        payment_complete_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="完成",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        payment_complete_button.click()
        logger.info("点击支付成功界面的【完成】按钮.")

    @SleepWait(wait_time=1)
    def close_coupon_dialog(self) -> None:
        """支付完成后，会有一个优惠卷弹框，需要关闭"""
        try:
            coupon_dialog = self.device.get_po(
                type="android.view.ViewGroup", name="领券弹窗关闭按钮")
            if coupon_dialog.exists():
                coupon_dialog.click()
        except (PocoNoSuchNodeException, Exception):
            logger.warning("没有出现领券弹窗关闭按钮.")

    @SleepWait(wait_time=1)
    def expand_order_detail(self) -> None:
        """展开【详情/首页】"""
        file_name = join_path([get_images_dir(), "完成后的订单详情.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (902, 202)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)
        logger.info("展开【详情/首页】，接下来可以点击【查订单/开发票】")

    @SleepWait(wait_time=5)
    def touch_order_detail(self) -> None:
        """点击【查订单/开发票】，进入订单详情界面"""
        order_detail = self.device.get_po(type="android.widget.TextView", name="android.widget.TextView",
                                          text="查订单/开发票")
        order_detail.click()
        logger.info("点击【查订单/开发票】，进入订单详情界面")

    @SleepWait(wait_time=1)
    def close_important_trip_guidelines(self) -> None:
        """关闭出行前必读"""
        try:
            poco = (
                self.device.poco("android.widget.FrameLayout")
                .child("android.view.ViewGroup")
                .offspring("@FlyInModal")
                .child("android.view.ViewGroup")
                .child("android.view.ViewGroup")[1]
                .child("android.widget.TextView")
            )
            if poco.exists() is True:
                poco.click()
                logger.info("【出行前必读】出行前必读小窗口，已关闭.")
        except (PocoNoSuchNodeException, Exception):
            logger.warning("没有检测到【出现前必读】小窗口弹出，可以直接进行下面的操作.")

    @SleepWait(wait_time=1)
    def touch_order_with_finish_button(self) -> None:
        """点击支付成功界面的【完成】按钮"""
        finish_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="完成",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        logger.info("点击【完成】按钮, 关闭流程.")
        finish_button.click()

    @SleepWait(wait_time=1)
    def get_flight_ticket_with_order_id(self) -> str:
        """获取机票订单的id"""
        poco = self.device.get_po_extend(
            type="android.widget.TextView",
            name="pricePolicy_Text_订单号",
            global_num=0,
            local_num=3,
            touchable=False
        )[0]
        return poco.get_text().split("：")[-1].strip()

    @SleepWait(wait_time=1)
    def get_flight_ticket_with_itinerary_id(self):
        """获取机票中乘客的行程单号"""
        # 滑动屏幕三次
        for i in range(3):
            self.device.quick_slide_screen()
        poco = (
            self.device.poco("android.widget.FrameLayout")
            .offspring("android:id/content")
            .child("ctrip.android.view:id/a")
            .child("ctrip.android.view:id/a")
            .offspring("android.widget.LinearLayout")
            .offspring("android.widget.FrameLayout")
            .child("android.view.ViewGroup")
            .child("android.view.ViewGroup")
            .child("android.view.ViewGroup")
            .child("android.view.ViewGroup")
            .child("android.view.ViewGroup")[1]
            .offspring("PullRefreshScrollView_ScrollView")
            .child("android.view.ViewGroup")
            .child("android.view.ViewGroup")
            .offspring("@contactInfo")
            .offspring("contactInfo_Text_票号")[0]
        )
        if poco.exists() is True:
            itinerary_id = poco.get_text().split("：")[-1].strip()
        else:
            itinerary_id = None
        return itinerary_id

    # 为了调式方便，暂时注释
    """
    def __del__(self) -> None:
        self.stop()
    """


if __name__ == "__main__":
    # from time import sleep

    app = CtripAppService()
    app.start()
    # app.select_trip_expect_month(date_str="2024-04-28 11:45")
    # app.select_trip_expect_day(date_str="2024-04-28 11:45")
    # app.select_trip_expect_month(date_str="2024-05-19 22:05")
    # app.select_trip_expect_day(date_str="2024-05-19 22:05")
    # app.is_exist_flight_in_screen(flight="EU1933")
    # app.device.hide_keyword()
    # app.touch_bank_card_payment()
    # app.enter_payment_pass(payment_pass="123456")
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
    # app.submit_passenger_info()
    app.submit_passenger_info_confirm()
