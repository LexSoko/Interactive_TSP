import dearpygui.dearpygui as dpg
import numpy as np 
from node_editor.general import retrieve_matrix , dpg_get_value , dpg_set_value
import numsolvers.TSP as tsp

_Node_Name = "Genetic-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")
class Node:

    node_label = "Genetic Node"
    node_tag = "Genetic"

    received_data = {}
    run_dict = {}
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
        
        tag_node_input01_name = tag_node_name + ":" + "Cities" + ":Input01"
        tag_node_input01_value_name = tag_node_name +":Cities" + ":Input01Value"

        tag_node_input02_name = tag_node_name + ":" + "Func" + ":Input02"
        tag_node_input02_value_name = tag_node_name +":Func" + ":Input02Value"

        
        tag_node_output01_name = tag_node_name + ":" + "Cities" + ":Output01"
        tag_node_output01_value_name = tag_node_name + ":Cities" + ':Output01Value'

        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['result_width']
        small_window_h = self._opencv_setting_dict['result_height']

        self.received_data[tag_node_name] = False
        self.run_dict[tag_node_name] = False
        self._default_xdata = 100*np.linspace(0, 1, 30)* np.cos(3*np.linspace(0, 2*np.pi, 30))
        self._default_ydata = 100 * np.linspace(0, 1, 30)*np.sin(3*np.linspace(0, 2*np.pi, 30))
        self._default_limits = (-110,110,-110,110)
        print(self._default_xdata)
        with dpg.node(
            tag = tag_node_name,
            parent=parent,
            label = self.node_label
        ):
            with dpg.node_attribute(
                tag= tag_node_output01_name,
                attribute_type=dpg.mvNode_Attr_Output
            ):
                with dpg.plot(
                    width=small_window_w,
                    height=small_window_h,
                    tag = tag_node_output01_value_name,
                    no_menus=True
                ):
                    dpg.add_plot_axis(
                        dpg.mvXAxis,
                        tag=tag_node_output01_value_name + "xaxis",
                    ) 
                    dpg.add_plot_axis(
                        dpg.mvYAxis,
                        tag=tag_node_output01_value_name + "yaxis",
                    )
                    dpg.add_line_series(
                        self._default_xdata,
                        self._default_ydata,
                        label= "shortest path",
                        parent = tag_node_output01_value_name + "yaxis",
                        tag = tag_node_output01_value_name + "paths"
                    )

                    dpg.add_scatter_series(
                        self._default_xdata,
                        self._default_ydata,
                        label="Cities Positions",
                        parent = tag_node_output01_value_name + "yaxis",
                        tag= tag_node_output01_value_name + "cities_pos"
                    )
                with dpg.group(horizontal=True):
                        dpg.add_spacer(width=self._opencv_setting_dict['result_width']-100)  # Adjust width to push buttons to the right
                        dpg.add_button(label="RUN", callback=self._call_back_run, user_data=tag_node_name)
                        dpg.add_button(label="STOP", callback=self._call_back_stop, user_data=tag_node_name)

                
            with dpg.node_attribute(
            tag= tag_node_input01_name,
            attribute_type=dpg.mvNode_Attr_Input
            ):
                dpg.add_text("Cities Input")
                
                
                
            
               
        
        return tag_node_name
    
    def update(
        self,
        node_id,
        connection_list,
        node_image_dict,
        node_result_dict,
    ):
        tag_node_name = str(node_id) + ':' + self.node_tag
        tag_node_input01_name = tag_node_name + ":" + "Cities" + ":Input01"
        tag_node_input01_value_name = tag_node_name +":Cities" + ":Input01Value"
        
        tag_node_output01_name = tag_node_name + ":" + "Cities" + ":Output01"
        tag_node_output01_value_name = tag_node_name + ":Cities" + ':Output01Value'

        link = connection_list.get(tag_node_input01_name, None)
       
        if link is not None and self.received_data[tag_node_name] == False:
            
            Cities = dpg_get_value(link[0] + "Value" + "cities_pos")

            dpg_set_value(
                tag_node_output01_value_name + "cities_pos",
                [np.array(Cities[0]), np.array(Cities[1])])
            dpg_set_value(
                tag_node_output01_value_name + "paths",
                [np.array(Cities[0]), np.array(Cities[1])])   
            if dpg.does_item_exist(tag_node_output01_value_name +"yaxis") and dpg.does_item_exist(tag_node_output01_value_name +"xaxis"):
                
                y_min = int(np.min(Cities[1]) - 0.1*np.max(Cities[1]))
                y_max = int(np.max(Cities[1]) + 0.1*np.max(Cities[1]))
                x_min = int(np.min(Cities[0]) - 0.1*np.max(Cities[0]))
                x_max = int(np.max(Cities[0]) + 0.1*np.max(Cities[0]))
                
                dpg.set_axis_limits(
                    tag_node_output01_value_name +"yaxis", 
                    y_min,
                    y_max)
                dpg.set_axis_limits(
                    tag_node_output01_value_name +"xaxis", 
                    x_min, 
                    x_max)
                
            self.received_data[tag_node_name] = True

        elif link is None:
            self.received_data[tag_node_name] = False
            dpg_set_value(
                tag_node_output01_value_name + "cities_pos",
                [self._default_xdata,self._default_ydata])
            dpg_set_value(
                tag_node_output01_value_name + "paths",
                [self._default_xdata,self._default_ydata])
            
            y_min, y_max, x_min, x_max = self._default_limits
            dpg.set_axis_limits(
                    tag_node_output01_value_name +"yaxis", 
                    y_min,
                    y_max)
            dpg.set_axis_limits(
                    tag_node_output01_value_name +"xaxis", 
                    x_min, 
                    x_max)
        
        if self.run_dict[tag_node_name] == True:
            print("LEEETS GOOO BABY")
        else:
            print("OH NOOOOOOO")
        

        return None, None
    
    def _call_back_run(
            self,
            sender,
            app_data,
            user_data
    ):
        self.run_dict[user_data] = True
        pass

    def _call_back_stop(
            self,
            sender,
            app_data,
            user_data
    ):
        self.run_dict[user_data] = False
        pass