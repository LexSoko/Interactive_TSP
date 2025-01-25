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
        tag_node_input01_value_name = tag_node_name + ":Cities:Input01Value"
        
        tag_node_output01_name = tag_node_name + ":Cities:Output01"
        tag_node_output01_value_name = tag_node_name + ":Cities:Output01Value"
        
        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['input_window_width']
        small_window_h = self._opencv_setting_dict['input_window_height'] + 100

        self.updated_table = False
        self._default_xdata = np.array([])
        self._default_ydata = np.array([])

        

        with dpg.node(
            tag = tag_node_name,
            parent=parent,
            label = self.node_label
        ):
            
            with dpg.node_attribute(
                tag = tag_node_output01_name,
                attribute_type=dpg.mvNode_Attr_Output
            ): 
                with dpg.child_window(
                    width= small_window_w,
                    height=small_window_h,
                ):
                    with dpg.table(header_row=True,
                                   tag=tag_node_output01_value_name,
                                   width= small_window_w,
                                   height=small_window_h,
                                   policy=dpg.mvTable_SizingStretchProp,
                                   resizable=False,
                                   ):

                        dpg.add_table_column(label="x coordinate", parent=tag_node_output01_value_name)
                        dpg.add_table_column(label="y coordinate", parent=tag_node_output01_value_name)
                        for xi, yi in zip(self._default_xdata,self._default_ydata):
                            row_tag = dpg.add_table_row(parent=tag_node_output01_value_name)
                            dpg.add_input_float(default_value=xi,parent=row_tag)
                            dpg.add_input_float(default_value=yi,parent=row_tag)
                                #dpg.add_text(xi)
                                #dpg.add_text(yi)
                
                with dpg.file_dialog(
                    directory_selector=False,
                    show=False,
                    callback=self.callback_file_dialog,
                    id=str(node_id) +":file_dialog_data_id",
                    user_data=tag_node_output01_value_name,
                    width=700 ,
                    height=400
                ):
                    dpg.add_file_extension(".csv")
                
                dpg.add_button(label="Select Data", callback= lambda: dpg.show_item(str(node_id) +":file_dialog_data_id"))
                dpg.add_button(label="retrieve matrix", callback=self.retrieve_matrix, user_data=tag_node_output01_value_name)

            
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
        print("###### filedialog ######")
        print("Sender: ", sender)
        print("App Data: ", app_data)
        print("#########################")

        data = np.genfromtxt(app_data["file_path_name"],delimiter=";").T

        if np.isnan(data[0][0]): 
            self._default_xdata = data[0][1:]
            self._default_ydata = data[1][1:]
        else:
            self._default_xdata = data[0]
            self._default_ydata = data[1]
        
        self.update_table_contents(user_data)

    
    def update_table_contents(
            self,
            table_tag,
    ):
        
        rows = dpg.get_item_children(table_tag,1)
        for row in rows:
            dpg.delete_item(row)
        
        for xi, yi in zip(self._default_xdata,self._default_ydata):
            row_tag = dpg.add_table_row(parent=table_tag)
            dpg.add_input_float(default_value=xi,parent=row_tag)
            dpg.add_input_float(default_value=yi,parent=row_tag)
                #dpg.add_text(xi)
                #dpg.add_text(yi)

    def retrieve_matrix(
            self,
            sender,
            app_data,
            user_data
            ):
        table_tag = user_data
        rows = dpg.get_item_children(table_tag,1)
        print(rows)
        matrix = []
    
    
        for row in rows:
            row_values = []
            
            cells = dpg.get_item_children(row,1)
            
            for cell in cells:
                
                value = dpg.get_value(cell)
                row_values.append(value)  

            # Append the row of values to the matrix
            matrix.append(np.array(row_values))
        print(matrix)
        return np.array(matrix).T