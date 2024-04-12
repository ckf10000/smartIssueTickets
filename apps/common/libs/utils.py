# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     utils.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/06 01:54:01
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import re
import hashlib
import typing as t
from collections import OrderedDict
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


def get_ui_object_proxy_attr(ui_object_proxy: AndroidUiautomationPoco) -> OrderedDict:
    ordered_dict = OrderedDict()
    ordered_dict["type"] = (
        ui_object_proxy.attr("type").strip()
        if isinstance(ui_object_proxy.attr("type"), str)
        else ui_object_proxy.attr("type")
    )
    ordered_dict["name"] = (
        ui_object_proxy.attr("name").strip()
        if isinstance(ui_object_proxy.attr("name"), str)
        else ui_object_proxy.attr("name")
    )
    ordered_dict["text"] = (
        ui_object_proxy.attr("text").strip()
        if isinstance(ui_object_proxy.attr("text"), str)
        else ui_object_proxy.attr("text")
    )
    ordered_dict["desc"] = (
        ui_object_proxy.attr("desc").strip()
        if isinstance(ui_object_proxy.attr("desc"), str)
        else ui_object_proxy.attr("desc")
    )
    ordered_dict["enabled"] = (
        ui_object_proxy.attr("enabled").strip()
        if isinstance(ui_object_proxy.attr("enabled"), str)
        else ui_object_proxy.attr("enabled")
    )
    ordered_dict["visible"] = (
        ui_object_proxy.attr("visible").strip()
        if isinstance(ui_object_proxy.attr("visible"), str)
        else ui_object_proxy.attr("visible")
    )
    ordered_dict["resourceId"] = (
        ui_object_proxy.attr("resourceId").strip()
        if isinstance(ui_object_proxy.attr("resourceId"), str)
        else ui_object_proxy.attr("resourceId")
    )
    ordered_dict["zOrders"] = (
        ui_object_proxy.attr("zOrders").strip()
        if isinstance(ui_object_proxy.attr("zOrders"), str)
        else ui_object_proxy.attr("zOrders")
    )
    ordered_dict["package"] = (
        ui_object_proxy.attr("package").strip()
        if isinstance(ui_object_proxy.attr("package"), str)
        else ui_object_proxy.attr("package")
    )
    ordered_dict["anchorPoint"] = (
        ui_object_proxy.attr("anchorPoint").strip()
        if isinstance(ui_object_proxy.attr("anchorPoint"), str)
        else ui_object_proxy.attr("anchorPoint")
    )
    ordered_dict["dismissable"] = (
        ui_object_proxy.attr("dismissable").strip()
        if isinstance(ui_object_proxy.attr("dismissable"), str)
        else ui_object_proxy.attr("dismissable")
    )
    ordered_dict["checkable"] = (
        ui_object_proxy.attr("checkable").strip()
        if isinstance(ui_object_proxy.attr("checkable"), str)
        else ui_object_proxy.attr("checkable")
    )
    ordered_dict["scale"] = (
        ui_object_proxy.attr("scale").strip()
        if isinstance(ui_object_proxy.attr("scale"), str)
        else ui_object_proxy.attr("scale")
    )
    ordered_dict["boundsInParent"] = (
        ui_object_proxy.attr("boundsInParent").strip()
        if isinstance(ui_object_proxy.attr("boundsInParent"), str)
        else ui_object_proxy.attr("boundsInParent")
    )
    ordered_dict["focusable"] = (
        ui_object_proxy.attr("focusable").strip()
        if isinstance(ui_object_proxy.attr("focusable"), str)
        else ui_object_proxy.attr("focusable")
    )
    ordered_dict["touchable"] = (
        ui_object_proxy.attr("touchable").strip()
        if isinstance(ui_object_proxy.attr("touchable"), str)
        else ui_object_proxy.attr("touchable")
    )
    ordered_dict["longClickable"] = (
        ui_object_proxy.attr("longClickable").strip()
        if isinstance(ui_object_proxy.attr("longClickable"), str)
        else ui_object_proxy.attr("longClickable")
    )
    ordered_dict["size"] = (
        ui_object_proxy.attr("size").strip()
        if isinstance(ui_object_proxy.attr("size"), str)
        else ui_object_proxy.attr("size")
    )
    ordered_dict["pos"] = (
        ui_object_proxy.attr("pos").strip()
        if isinstance(ui_object_proxy.attr("pos"), str)
        else ui_object_proxy.attr("pos")
    )
    ordered_dict["focused"] = (
        ui_object_proxy.attr("focused").strip()
        if isinstance(ui_object_proxy.attr("focused"), str)
        else ui_object_proxy.attr("focused")
    )
    ordered_dict["checked"] = (
        ui_object_proxy.attr("checked").strip()
        if isinstance(ui_object_proxy.attr("checked"), str)
        else ui_object_proxy.attr("checked")
    )
    ordered_dict["editalbe"] = (
        ui_object_proxy.attr("editalbe").strip()
        if isinstance(ui_object_proxy.attr("editalbe"), str)
        else ui_object_proxy.attr("editalbe")
    )
    ordered_dict["selected"] = (
        ui_object_proxy.attr("selected").strip()
        if isinstance(ui_object_proxy.attr("selected"), str)
        else ui_object_proxy.attr("selected")
    )
    ordered_dict["scrollable"] = (
        ui_object_proxy.attr("scrollable").strip()
        if isinstance(ui_object_proxy.attr("scrollable"), str)
        else ui_object_proxy.attr("scrollable")
    )
    return ordered_dict


def poco_to_dict(poco: AndroidUiautomationPoco) -> t.List:
    # 初始化空字典，用于存储 Poco 对象的属性数据
    poco_dict = {}
    # 将 Poco 对象的属性数据添加到字典中
    poco_dict.update(get_ui_object_proxy_attr(ui_object_proxy=poco))

    # 如果 Poco 对象有子对象，则递归处理子对象，并将子对象的字典数据添加到当前字典中
    if poco.children():
        poco_dict["children"] = [poco_to_dict(child) for child in poco.children()]

    return poco_dict


def update_nested_dict(original_dict: t.Dict, update_dict: t.Dict) -> t.Dict:
    """更新多层嵌套字典，如果key存在，则跳过，否则就更新"""
    for key, value in update_dict.items():
        if key in original_dict and isinstance(original_dict[key], dict) and isinstance(value, dict):
            # 如果当前键已存在于原始字典中，并且对应的值都是字典类型，则递归更新
            update_nested_dict(original_dict[key], value)
        elif key not in original_dict:
            # 如果当前键不存在于原始字典中，则将键值对添加到原始字典中
            original_dict[key] = value


def encryp_md5(data: str) -> str:
    # 创建一个 hashlib.md5 对象
    md5_hash = hashlib.md5()
    # 将输入的字符串转换为 bytes，并更新 MD5 哈希对象
    md5_hash.update(data.encode())
    # 获取 MD5 值的十六进制表示形式（32 位小写）
    md5_hex_digest = md5_hash.hexdigest()
    return md5_hex_digest


def covert_dict_key_to_lower(d: t.Dict) -> t.Dict:
    result = dict()
    for key, value in d.items():
        if isinstance(key, str):
            key_new = key.lower()
            result[key_new] = value
    return result


def get_html_title(html: str) -> str:
    # 使用正则表达式提取目标字符串
    pattern = '<title>(.*?)</title>'
    match = re.search(pattern, html)
    if match:
        title = match.group(1)
    else:
        title = "Abnormal HTML document structure"
    return title
