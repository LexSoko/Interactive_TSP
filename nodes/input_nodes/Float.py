#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dearpygui.dearpygui as dpg

_Node_Name = "Float-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")

class Node:
    node_label = 'Float Value'
    node_tag = 'FloatValue'

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
        """
        add a float value input which is can be connected to other nodes and dynamicly changed

        Args:
            parent (str): node editor tag
            node_id (int): unique node id
            pos (list, optional): position of added node. Defaults to [0, 0].
            opencv_setting_dict (dict, optional): settings for size of node windows. Defaults to None.
            callback (callable, optional): callback function for adding (reserved for later implementation). Defaults to None.

        Returns:
            str: the uniquelly generated node tag for the added node
        """
        tag_node_name = str(node_id) + ":" + self.node_tag
        tag_node_output01_name = tag_node_name + ':' + "Float" + ":Output01"
        tag_node_output01_value_name = tag_node_name + ':' + "Float" + ":Output01Value"
        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict["input_window_width"]

        with dpg.node(
                tag=tag_node_name,
                parent=parent,
                label=self.node_label,
                pos=pos,
        ):
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
    ):
        return None, None
    
    def close(self, node_id):
        pass

    