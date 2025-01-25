import dearpygui.dearpygui as dpg
import numpy as np

_Node_Name = "Data-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")
class Node():
    node_label = "Data Node"
    node_tag = "DataValues"
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
        tag_node_name = str(node_id) + ":" + self.node_tag

        tag_node_input01_name = tag_node_name + ":Cities:Input01"
        tag_node_input01_value_name = tag_node_name + ":Cities:Input01"
        
        tag_node_output01_name = tag_node_name + ":Cities:Output01"
        tag_node_output01_value_name = tag_node_name + ":Cities:Output01Value"
        
        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['input_window_width']
        small_window_h = self._opencv_setting_dict['input_window_height'] + 100

        self._default_xdata = np.array([])
        self._default_ydata = np.array([])

        

        with dpg.node(
            tag = tag_node_name,
            parent=parent,
            label = self.node_label
        ):
            
            with dpg.node_attribute(
                tag = tag_node_input01_name,
                attribute_type=dpg.mvNode_Attr_Static
            ):
                with dpg.child_window(
                    width= small_window_w,
                    height=small_window_h,
                ):
                    with dpg.table(header_row=True,
                                   width= small_window_w,
                                   height=small_window_h,
                                   policy=dpg.mvTable_SizingStretchProp,
                                   resizable=False,
                                   ):

                        dpg.add_table_column(label="x coordinate")
                        dpg.add_table_column(label="y coordinate")
                        for xi, yi in zip(self._default_xdata,self._default_ydata):
                            with dpg.table_row():
                                dpg.add_text(xi)
                                dpg.add_text(yi)

                with dpg.file_dialog(
                    directory_selector=False,
                    show=False,
                    callback=self.callback_file_dialog,
                    id="file_dialog_data_id",
                    width=700 ,
                    height=400
                ):
                    dpg.add_file_extension(".csv")

                dpg.add_button(label="Select Data", callback= lambda: dpg.show_item("file_dialog_data_id"))

            
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

    def callback_file_dialog(
            self,
            sender,
            app_data,
            user_data
            ):
        print("Sender: ", sender)
        print("App Data: ", app_data)
        data = np.genfromtxt(app_data["file_path_name"],delimiter=";")
        self._default_xdata = data[0]
        self._default_ydata = data[1]
        