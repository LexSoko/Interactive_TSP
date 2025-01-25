import dearpygui.dearpygui as dpg

_Node_Name = "Data-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")
class Node():
    node_tag = "DataValues2"
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
        pass