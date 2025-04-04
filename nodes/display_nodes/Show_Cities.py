import dearpygui.dearpygui as dpg
import numpy as np 
from node_editor.general import retrieve_matrix , dpg_get_value , dpg_set_value
_Node_Name = "Show-Cities-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")
class Node:

    node_label = "Show-Cities Node"
    node_tag = "Show_Cities"

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

        tag_node_input02_name = tag_node_name + ":" + "Str" + ":Input02"
        tag_node_input02_value_name = tag_node_name +":Str" + ":Input02Value"

        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['result_width']
        small_window_h = self._opencv_setting_dict['result_height']


        self._default_xdata = 100*np.linspace(0, 1, 30)* np.sin(3*np.linspace(0, 2*np.pi, 30))
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

                    dpg.add_scatter_series(
                        self._default_xdata,
                        self._default_ydata,
                        label="Cities Positions",
                        parent = tag_node_input01_value_name + "yaxis",
                        tag= tag_node_input01_value_name + "cities_pos"
                    )
                    with dpg.file_dialog(
                        directory_selector=True,
                        show=False,
                        callback=self.callback_file_dialog,
                        id=str(node_id) +":file_dialog_data_id",
                        user_data=tag_node_input01_value_name+ "cities_pos",
                        width=700 ,
                        height=400
                        ):
                        dpg.add_file_extension(".csv")
                with dpg.group(horizontal=True):
                    dpg.add_input_text(width = small_window_w*0.2, tag=tag_node_input02_value_name)
                    dpg.add_button(label="Save",user_data=[tag_node_input02_value_name,tag_node_input01_value_name+ "cities_pos"],callback=self.call_back_save)
                    dpg.add_button(label="Save to", callback= lambda: dpg.show_item(str(node_id) +":file_dialog_data_id"), user_data=tag_node_input01_value_name+ "cities_pos")
                    
        
        return tag_node_name
    
    def update(
        self,
        node_id,
        connection_list,
    ):
        tag_node_name = str(node_id) + ':' + self.node_tag
        tag_node_input01_name = tag_node_name + ":" + "Cities" + ":Input01"
        tag_node_input01_value_name = tag_node_name +":Cities" + ":Input01Value"
        
        link = connection_list.get(tag_node_input01_name, None)

        if link is not None:
            
            try:
                Cities = retrieve_matrix(link[0] + "Value")
            except: 
                Cities = dpg_get_value(link[0] + "Value" + "cities_pos")


            dpg_set_value(
                tag_node_input01_value_name + "cities_pos",
                [np.array(Cities[0]), np.array(Cities[1])])
            dpg_set_value(
                tag_node_input01_value_name + "paths",
                [np.array(Cities[0]), np.array(Cities[1])])   
            if dpg.does_item_exist(tag_node_input01_value_name +"yaxis") and dpg.does_item_exist(tag_node_input01_value_name +"xaxis"):
                
                y_min = int(np.min(Cities[1]) - 0.1*np.max(Cities[1]))
                y_max = int(np.max(Cities[1]) + 0.1*np.max(Cities[1]))
                x_min = int(np.min(Cities[0]) - 0.1*np.max(Cities[0]))
                x_max = int(np.max(Cities[0]) + 0.1*np.max(Cities[0]))
                
                
                dpg.set_axis_limits(
                    tag_node_input01_value_name +"yaxis", 
                    y_min,
                    y_max)
                dpg.set_axis_limits(
                    tag_node_input01_value_name +"xaxis", 
                    x_min, 
                    x_max)
        
        

        return None, None
    

    def callback_file_dialog(
            self,
            sender,
            app_data,
            user_data
            ):
        
        print("###### filedialog ######")
        print("Sender: ", sender)
        print("App Data: ", app_data)
        print("User Data: ", user_data)
        print("#########################")
        cities = dpg_get_value(user_data)
        np.savetxt(app_data["file_path_name"],np.array(cities).T,delimiter=";")

       
    def call_back_save(
            self,
            sender,
            app_data,
            user_data
            ):
        filename = dpg_get_value(user_data[0])
        cities = dpg_get_value(user_data[1])
        path_cities = "./results/cities_pos/"
        np.savetxt(path_cities+ filename,np.array(cities).T,delimiter=";")
       
        
