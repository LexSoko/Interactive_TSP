import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.node_editor():
    with dpg.node(label="Example Node") as node:
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag="input_attr"):
            dpg.add_text("Input")
        
        # Offset the input node attribute to a specific position
        dpg.set_item_pos("input_attr", [0, 50])  # Adjust height as needed

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag="output_attr"):
            dpg.add_text("Output")
        
        # Offset the output node attribute to the same height
        dpg.set_item_pos("output_attr", [200, 50])  # Adjust x (horizontal distance) as needed

dpg.create_viewport(title='Custom Node Editor', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
