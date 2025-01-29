
import dearpygui.dearpygui as dpg
import numpy as np

def build_coordinate_list( node_source_paths, side_menu_width):
    """depriciated 

    Args:
        node_source_paths (str: paths to node scripts to be executed for callback
        side_menu_width (str): _description_

    Returns:
        List: coordinates for buttons
    """
    number_of_nodes = len(node_source_paths)
    coordinates_buttons = []
    for i in range(0,number_of_nodes):
        coordinates_buttons.append([(i%2)*side_menu_width*0.55, (i//2) * 90])
    return coordinates_buttons

def retrieve_matrix(
            table_tag
            ):
        """lets your retrieve a dataset from a table object in dpg

        Args:
            table_tag (str): tag of table

        Returns:
            np.ndarray: matrix with values
        """

        rows = dpg.get_item_children(table_tag,1)
      
        matrix = []
    
    
        for row in rows:
            row_values = []
            
            cells = dpg.get_item_children(row,1)
        
            for cell in cells:
                
                value = dpg.get_value(cell)
                row_values.append(value)  

            
            matrix.append(np.array(row_values))

        return np.array(matrix).T

def dpg_set_value(tag, value):
    if dpg.does_item_exist(tag):
        dpg.set_value(tag, value)


def dpg_get_value(tag):
    value = None
    if dpg.does_item_exist(tag):
        value = dpg.get_value(tag)
    return value