import dearpygui.dearpygui as dpg
import numpy as np
from node_editor.general import dpg_set_value
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
        """
        creates a table object where the data from a selected file is displayed
        also creates an invisible scatter plotcontainer where the data is loaded into, 
        because as it seems it is the only way to store arrays in the dpg library

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

        tag_node_input01_name = tag_node_name + ":Cities:Input01"
        tag_node_input01_value_name = tag_node_name + ":Cities:Input01Value"
        
        tag_node_output01_name = tag_node_name + ":Cities:Output01"
        tag_node_output01_value_name = tag_node_name + ":Cities:Output01Value"
        
        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['input_window_width']
        small_window_h = self._opencv_setting_dict['input_window_height'] + 100

        self.updated_table = False
        self._default_xdata = np.array([4,2,0])
        self._default_ydata = np.array([4,2,0])

        

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
                                   tag=tag_node_input01_value_name,
                                   width= small_window_w,
                                   height=small_window_h,
                                   policy=dpg.mvTable_SizingStretchProp,
                                   resizable=False,
                                   ):

                        dpg.add_table_column(label="x coordinate", parent=tag_node_input01_value_name)
                        dpg.add_table_column(label="y coordinate", parent=tag_node_input01_value_name)
                        for xi, yi in zip(self._default_xdata,self._default_ydata):
                            row_tag = dpg.add_table_row(parent=tag_node_input01_value_name)
                            dpg.add_input_float(default_value=xi,parent=row_tag)
                            dpg.add_input_float(default_value=yi,parent=row_tag)

                with dpg.plot(show=False):
                    dpg.add_plot_axis(
                        dpg.mvXAxis,
                        tag=tag_node_output01_value_name + "xaxis",
                    )
                    dpg.add_plot_axis(
                        dpg.mvYAxis,
                        tag=tag_node_output01_value_name + "yaxis",
                    )
                    dpg.add_scatter_series(
                        self._default_xdata,
                        self._default_ydata,
                        label="Cities Positions",
                        show=False,
                        parent=tag_node_output01_value_name + "yaxis",
                        tag= tag_node_output01_value_name + "cities_pos"
                    )
                
                with dpg.file_dialog(
                    directory_selector=False,
                    show=False,
                    callback=self.callback_file_dialog,
                    id=str(node_id) +":file_dialog_data_id",
                    user_data=[tag_node_input01_value_name,tag_node_output01_value_name+ "cities_pos"],
                    width=700 ,
                    height=400
                ):
                    dpg.add_file_extension(".csv")
                
                dpg.add_button(label="Select Data", callback= lambda: dpg.show_item(str(node_id) +":file_dialog_data_id"))
                

            
        return tag_node_name      
      
    def update(
        self,
        node_id,
        connection_list,
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
        """
        Extracts a path to a file 
        updates the table contents based on data
        stores the arrays into a scatter container
        
        Args:
            sender (str): tag of container the callback originates from
            app_data (any): data associated with the dpg container, file dialog information
            user_data (any): custom data transmitted, in this case tag of table and the tag of the plot container
        """
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
        print(user_data)
        
        self.update_table_contents(user_data[0])
        dpg_set_value(
                user_data[1],
                [np.array(self._default_xdata),np.array(self._default_ydata)])
        

    
    def update_table_contents(
            self,
            table_tag,
    ):
        """
        based on the table tag finds children of container.
        the children are the rows, and the rows are parents of inputfloats

        Args:
            table_tag (str): table tag
        """
        rows = dpg.get_item_children(table_tag,1)
        for row in rows:
            dpg.delete_item(row)
        
        for xi, yi in zip(self._default_xdata,self._default_ydata):
            row_tag = dpg.add_table_row(parent=table_tag)
            dpg.add_input_float(default_value=xi,parent=row_tag)
            dpg.add_input_float(default_value=yi,parent=row_tag)
                

   