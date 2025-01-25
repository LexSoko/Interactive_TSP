import time
import sys
import os 
import json
import dearpygui.dearpygui as dpg
import argparse
from node_editor.node_editor import Node_editor

def get_settings():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--setting",
        type=str,
        default=os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         'settings/setting.json')),
    )
    #parser.add_argument(
    #    "--verbose",
    #    type = bool,
    #)
    arg = parser.parse_args()
    return arg.setting

def update_nodes(
        node_editor,
        node_image_dict = {},
        node_results = {}
):
    node_list = node_editor.get_node_list()
    connection_dict = node_editor.get_node_connection_dict()

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    #updating the window size
    dpg.set_item_width(node_editor._childwindow_nodeeditor_tag, viewport_width- node_editor._side_menu_width)
    dpg.set_item_height(node_editor._childwindow_nodeeditor_tag, viewport_height)
    dpg.set_item_width(node_editor._node_editor_tag, viewport_width- node_editor._side_menu_width)
    dpg.set_item_height(node_editor._node_editor_tag, viewport_height)
    dpg.set_item_height(node_editor._childwindow_sidemenu_tag, viewport_height)
    dpg.set_item_width(node_editor._node_tag, viewport_width)
    dpg.set_item_height(node_editor._node_tag, viewport_height)
    for node_name in node_list:
        node_id , node_name = node_name.split(":")
        
        node = node_editor.get_node_instance(node_name)
        frame, result = node.update(
            node_id,
            connection_dict,
            node_image_dict,
            node_results
            )
        pass

    

    
    
def main():
    args_setting = get_settings()
    setting_dict = None
    with open(args_setting) as fp:
        setting_dict = json.load(fp)
    dpg.create_context()
    dpg.setup_dearpygui()
    dpg.create_viewport(
        title ="Interactive TSP",
        width = setting_dict['editor_width'],
        height = setting_dict['editor_height']
    )
    node_editor = Node_editor(
        width = setting_dict['editor_width']-40,
        height = setting_dict['editor_height']-60,
        setting_dict= setting_dict
    )
    dpg.show_viewport()
    dpg.set_primary_window(f"{node_editor._node_tag}",True)
    node_image_dict = {}
    node_results = {}
    while dpg.is_dearpygui_running():
        
        update_nodes(node_editor,
               node_image_dict,
               node_results)
        dpg.render_dearpygui_frame()
        
        
    dpg.destroy_context()
if __name__ == '__main__':
    main()
