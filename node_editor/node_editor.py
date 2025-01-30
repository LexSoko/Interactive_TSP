import dearpygui.dearpygui as dpg
from collections import OrderedDict
from glob import glob
import os
import numpy as np
import importlib
from node_editor.general import dpg_get_value, dpg_set_value
class Node_editor(object):
    
    _node_id = 0
    _node_tag = "Playground"
    _node_editor_tag = 'NodeEditor'
    _node_editor_label = 'Node editor'
    _node_instance_list = {}
    _node_list = []
    _node_link_list = []
    
    _childwindow_nodeeditor_tag = "node_editor_child"
    _childwindow_sidemenu_tag = "sidemenu_child"
    _last_pos = None
    def __init__(
            self,
            width=1280,
            height=720,
            width_sidemenu = 300,
            pos= [0,0],
            menu_dict = None,
            setting_dict=None,
            node_dir = "nodes",
            debug = True
    ):
        self._debug = debug
        self._node_id = 0
        self._node_instance_list = {}
        self._node_list = []
        self._node_link_list = []
        self._node_connection_dict = OrderedDict([])
        self._window_width = width
        self._window_height = height
        self._node_editor_width = self._window_width - width_sidemenu
        self._node_editor_position = width_sidemenu
        self._node_editor_height = self._window_height
        self._terminate_flag = False
        self._side_menu_width = width_sidemenu
        self.setting_dict = setting_dict

    

        with dpg.window(
            tag=self._node_tag,
            label=self._node_tag ,
            width=self._window_width,
            height=self._window_height
        ):
            #later implementation
            with dpg.menu_bar(label = 'Menu'):
                with dpg.menu(label='File'):
                    dpg.add_menu_item(
                        tag='Menu_File_Export',
                        label='Export',
                        callback=self._callback_file_export,
                        user_data='Menu_File_Export'
                    )
                    dpg.add_menu_item(
                        tag='Menu_File_Import',
                        label='Import',
                        callback=self._callback_file_import,
                        user_data='Menu_File_Import'
                    )
                    dpg.add_menu_item(
                        tag='Menu_New_Project',
                        label='New',
                        callback=self._callback_new_project,
                        user_data='Menu_New_Project'
                    )
                with dpg.menu(label='Settings'):
                    dpg.add_menu_item(
                        tag='Resolution_Setting',
                        label='Resolution',
                        callback=self._callback_resolution_setting,
                        user_data='Resolution_Setting'
                    )      
            
            #child windows seperate the gui into menu and node editor
            with dpg.child_window(tag=self._childwindow_nodeeditor_tag,
                                  width=self._node_editor_width,
                                  height=self._window_height,
                                  pos=[self._side_menu_width,0]
                                  ): 
                #node editor item is initialiezed
                # tag is for identification as parent 
                with dpg.node_editor(
                    width=self._node_editor_width,
                    height= self._node_editor_height,
                    tag= self._node_editor_tag,
                    callback=self._callback_link,
                    delink_callback=self._callback_delink,
                    minimap=True,
                    minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
                    
                ):

                    pass

            with dpg.child_window(tag= self._childwindow_sidemenu_tag,
                                  width=self._side_menu_width, 
                                  height=self._window_height
                                  ):
                node_source_path = os.path.join(
                    node_dir,
                    "*"
                )
                #get paths for all nodes
                nodes_paths = glob(node_source_path)
                #print(nodes_paths)
                #builds a coordinates for buttons based on the witdth
               
                for i ,node_path in enumerate(nodes_paths):
                    #load all modules and generate buttons 
                    node_sub_paths = os.path.join(
                    node_path,
                    "*.py"
                    )
                    node_sub_paths = glob(node_sub_paths)
                
                    with dpg.collapsing_header(label= node_path.split("\\")[-1]):
                        row_counter = 0  # Track when to create a new row
                        row_container = None
                        for j,node_sub_path in enumerate(node_sub_paths):
                            import_node_path = np.char.replace(node_sub_path,"\\",".")
                            #print(import_node_path)
                            import_node_path = str(import_node_path)[:-3]

                            module = importlib.import_module(import_node_path)
                            try:
                                module.check_if_works()
                            except:
                                print("Module could not be loaded")

                            node = module.Node()
                            self._node_instance_list[node.node_tag] = node
                            #print(node.node_tag)
                            if row_counter == 0:  # Start a new row for every 2 buttons
                                with dpg.group(horizontal=True):  # Horizontal group for row

                                    row_container = dpg.last_item()
                            dpg.add_spacer(width=1)
                            dpg.add_button(
                                label = node_sub_path.split("\\")[-1][:-3],
                                tag= "sub_menu_" + node_sub_path.split("\\")[-1][:-3],
                                width=int(self._side_menu_width*0.45),
                                height=60,
                                parent=row_container,
                                user_data=node.node_tag,
                                callback=self._callback_create_node)
                            
                            row_counter = (row_counter + 1) % 2 
                    
                
            
            

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(
                callback=self._callback_save_last_pos
            )
            dpg.add_key_press_handler(
                    dpg.mvKey_Delete,
                    callback=self._callback_del_key,
                )
            

    # callback runs when user attempts to connect attributes
    def _callback_link(self,sender, link_data):
        # app_data -> (link_id1, link_id2)
        if self._debug:
            print("### link ###")
            print(f"sender: {sender}")
            print(f"link data: {link_data}")

        output_type = link_data[0].split(":")[2]
        input_type = link_data[1].split(":")[2]
        if input_type == output_type:
            dpg.add_node_link(link_data[0], link_data[1], parent=sender)
            self._node_connection_dict[link_data[1]] = link_data
        else:
            print("Datatypes dont match")

    # callback runs when user attempts to disconnect attributes
    def _callback_delink(self,sender, link_data):
    # app_data -> link_id
        if self._debug:
            print("### delink link ###")
            print(f"sender: {sender}")
            print(f"link data: {link_data}")
        config = dpg.get_item_configuration(link_data)
        destination = config["attr_2"]
        self._node_connection_dict.pop(destination) 
        
        dpg.delete_item(link_data)


    
    
    def _callback_create_node(self,sender, data, user_data):
        self._node_id += 1
        if self._debug == True:
            print("##### add node ######")
            print(f"sender = {sender}")
            print(f"data = {data}")
            print(f"user_data = {data}")
        
        node = self._node_instance_list[user_data]
        last_pos = [500, 100]
        if self._last_pos is not None:
            last_pos = [self._last_pos[0] + 30, self._last_pos[1] + 30]
        tag_name = node.add_node(
            self._node_editor_tag,
            self._node_id,
            pos = last_pos,
            opencv_setting_dict=self.setting_dict, 
        )
        self._node_list.append(tag_name)
        

        pass
    def get_node_connection_dict(self):
        return self._node_connection_dict

    def get_node_list(self):
        return self._node_list
    
    def get_node_instance(self,node_name):
        return self._node_instance_list.get(node_name,None)
    
    def _callback_del_key(self):
    
        if len(dpg.get_selected_nodes(self._node_editor_tag)) > 0:
            item_id = dpg.get_selected_nodes(self._node_editor_tag)[0]
        
            node_id_name = dpg.get_item_alias(item_id)
            if self._debug:
                print("###### delete node ######")
                print(f"Node ID name: {node_id_name}")

            node_id, node_name = node_id_name.split(':')
            
            for key in self._node_connection_dict.keys():
                if (node_id_name in key) and ("Input" in key):
                    
                    try:
                        self._node_connection_dict.pop(key)
                    except:
                        pass

            self._node_list.remove(node_id_name)
            if self._debug:
                print(f" connection {self._node_connection_dict}")
                print(f"nodelist {self._node_list}")  
                      
            dpg.delete_item(item_id)
        

        pass

    def _callback_save_last_pos(self):
        if len(dpg.get_selected_nodes(self._node_editor_tag)) > 0:
            self._last_pos = dpg.get_item_pos(
                dpg.get_selected_nodes(self._node_editor_tag)[0])





    #maybe for further versions
    def _callback_new_project(self):
        pass
        return
    
    def _callback_file_export(self):
        pass
        return 
    
    def _callback_file_import(self):
        pass
        return      
    
    def _callback_resolution_setting(self):
        pass
        return
    

    
        
