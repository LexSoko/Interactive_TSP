#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dearpygui.dearpygui as dpg

_Node_Name = "Float-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")

class Node:
    _ver = '0.0.1'

    node_label = 'Float Value'
    node_tag = 'FloatValue2'

    def __init__(self):
        pass

    def add_node(
        self,
        parent,
        node_id,
        pos=[0, 0],
        opencv_setting_dict=None,
        callback=None,
    ):
        # タグ名
        tag_node_name = str(node_id) + ':' + self.node_tag
        tag_node_output01_name = tag_node_name + ':' + "Float" + ':Output01'
        tag_node_output01_value_name = tag_node_name + ':' + "Float" + ':Output01Value'

        # 設定
        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['input_window_width']

        # ノード
        with dpg.node(
                tag=tag_node_name,
                parent=parent,
                label=self.node_label,
                pos=pos,
        ):
            # 浮動小数点入力
            with dpg.node_attribute(
                    tag=tag_node_output01_name,
                    attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_input_float(
                    tag=tag_node_output01_value_name,
                    label="Float value",
                    width=small_window_w - 94,
                    default_value=0,
                    callback=callback,
                )

        return tag_node_name

    def update(
        self,
        node_id,
        connection_list,
        node_image_dict,
        node_result_dict,
    ):
        return None, None

    def close(self, node_id):
        pass

    