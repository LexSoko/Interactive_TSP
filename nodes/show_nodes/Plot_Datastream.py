import dearpygui.dearpygui as dpg
import numpy as np 
from node_editor.general import retrieve_matrix , dpg_get_value , dpg_set_value
_Node_Name = "Plot-Datastream-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")
class Node:

    node_label = "Plot-Datastream Node"
    node_tag = "Plot_Datastream"

    k_indecces = {}
    current_data_dict = {}
    lenght_datastream_dict = {}
    inf_data_dict = {}
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
        tag_node_name = str(node_id) + ':' + self.node_tag
        
        tag_node_input01_name = tag_node_name + ":" + "Float" + ":Input01"
        tag_node_input01_value_name = tag_node_name +":Float" + ":Input01Value"

        tag_node_input02_name = tag_node_name + ":" + "Int" + ":Input02"
        tag_node_input02_value_name = tag_node_name +":Int" + ":Input02Value"

        tag_node_input03_name = tag_node_name + ":" + "Bool" + ":Input03"
        tag_node_input03_value_name = tag_node_name +":Bool" + ":Input03Value"

        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['result_width']
        small_window_h = self._opencv_setting_dict['result_height']

        self.lenght_datastream_dict[tag_node_name] = 400
        self.inf_data_dict[tag_node_name] = False
        self.k_indecces[tag_node_name] = [0]
        self.current_data_dict[tag_node_name] = [0]
        self._default_xdata = np.arange(0, 30, 1)
        self._default_ydata = 100 * np.linspace(0, 1, 30)*np.cos(3*np.linspace(0, 2*np.pi, 30))

        with dpg.node(
            tag = tag_node_name,
            parent=parent,
            label = self.node_label
        ):
            with dpg.node_attribute(
                tag= tag_node_input01_name,
                attribute_type=dpg.mvNode_Attr_Input
            ):
                with dpg.plot(
                    width=small_window_w,
                    height=small_window_h,
                    tag = tag_node_input01_value_name,
                    no_menus=True
                ):
                    dpg.add_plot_axis(
                        dpg.mvXAxis,
                        tag=tag_node_input01_value_name + "xaxis",
                    )
                    dpg.add_plot_axis(
                        dpg.mvYAxis,
                        tag=tag_node_input01_value_name + "yaxis",
                    )
                    dpg.add_line_series(
                        self._default_xdata,
                        self._default_ydata,
                        label= "shortest path",
                        parent = tag_node_input01_value_name + "yaxis",
                        tag = tag_node_input01_value_name + "paths"
                    )
                with dpg.group(horizontal=True):
                    dpg.add_drag_int(
                        label = "N Values",
                        width=50,
                        tag= tag_node_input02_value_name,
                        default_value= self.lenght_datastream_dict[tag_node_name],
                        callback=self.call_back_datastream_size,
                        user_data=tag_node_name
                    )
                    dpg.add_checkbox(
                        label="Full Data",
                        user_data=tag_node_name,
                        callback=self.call_back_checkbox
                    )

                    
        
        return tag_node_name
    
    def update(
        self,
        node_id,
        connection_list,
        node_image_dict,
        node_result_dict,
    ):
        tag_node_name = str(node_id) + ':' + self.node_tag
        tag_node_input01_name = tag_node_name + ":" + "Float" + ":Input01"
        tag_node_input01_value_name = tag_node_name +":Float" + ":Input01Value"
        
        link = connection_list.get(tag_node_input01_name, None)
       
        if link is not None:
            
            
            Data = dpg_get_value(link[0] + "Value")

            

            if type(Data) == float:
                self.current_data_dict[tag_node_name].append(Data)
                k = self.k_indecces[tag_node_name][-1]
                self.k_indecces[tag_node_name].append(k+1)
                max_lenght = self.lenght_datastream_dict[tag_node_name]

                if (len(self.current_data_dict[tag_node_name]) > max_lenght) and (self.inf_data_dict[tag_node_name] != True):
                    self.k_indecces[tag_node_name] = self.k_indecces[tag_node_name][-max_lenght:]
                    self.current_data_dict[tag_node_name] = self.current_data_dict[tag_node_name][-max_lenght:]
                #print(self.current_data_dict)
                dpg_set_value(
                    tag_node_input01_value_name + "paths",
                    [np.array(self.k_indecces[tag_node_name]), np.array(self.current_data_dict[tag_node_name])])
                   
                if dpg.does_item_exist(tag_node_input01_value_name +"yaxis") and dpg.does_item_exist(tag_node_input01_value_name +"xaxis"):
                    current_data = self.current_data_dict[tag_node_name]
                    current_k = self.k_indecces[tag_node_name]

                    y_min = int(np.min(current_data))
                    y_max = int(np.max(current_data))
                    x_min = int(np.min(current_k))
                    x_max = int(np.max(current_k))


                    dpg.set_axis_limits(
                        tag_node_input01_value_name +"yaxis", 
                        y_min,
                        y_max)
                    dpg.set_axis_limits(
                        tag_node_input01_value_name +"xaxis", 
                        x_min, 
                        x_max)
                
            else:
                dpg_set_value(
                    tag_node_input01_value_name + "paths",
                    [np.array(Data[0]), np.array(Data[1])])   
                if dpg.does_item_exist(tag_node_input01_value_name +"yaxis") and dpg.does_item_exist(tag_node_input01_value_name +"xaxis"):

                    y_min = int(np.min(Data[1]) - 0.1*np.max(Data[1]))
                    y_max = int(np.max(Data[1]) + 0.1*np.max(Data[1]))
                    x_min = int(np.min(Data[0]) - 0.1*np.max(Data[0]))
                    x_max = int(np.max(Data[0]) + 0.1*np.max(Data[0]))


                    dpg.set_axis_limits(
                        tag_node_input01_value_name +"yaxis", 
                        y_min,
                        y_max)
                    dpg.set_axis_limits(
                        tag_node_input01_value_name +"xaxis", 
                        x_min, 
                        x_max)
        else:
            self.k_indecces[tag_node_name] = [0]
            self.current_data_dict[tag_node_name] = [0]
        

        return None, None
    
    def call_back_datastream_size(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.lenght_datastream_dict[tag_node_name]

    def call_back_checkbox(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.inf_data_dict[tag_node_name] = app_data