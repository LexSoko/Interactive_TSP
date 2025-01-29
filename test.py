import dearpygui.dearpygui as dpg
import time

ANIMATION_DURATION = 2 #sec

dpg.create_context()

with dpg.window(label="Node link  animation", width=400, height=400):

    link_theme = dpg.add_theme()
    with dpg.theme_component(dpg.mvNodeLink,parent=link_theme):
        link_theme_color = dpg.add_theme_color(dpg.mvNodeCol_Link, (20, 255, 20), category=dpg.mvThemeCat_Nodes)
        
    attr_out = None
    attr_in = None
    with dpg.node_editor():
        with dpg.node(label="Node 1"):
            with dpg.node_attribute(label="Out", attribute_type=dpg.mvNode_Attr_Output) as _attr:
                dpg.add_input_float(label="Out", width=100)
                attr_out = _attr
        with dpg.node(label="Node 2") as _node_2:
            with dpg.node_attribute(label="In") as _attr:
                dpg.add_input_float(label="In", width=100)
                attr_in = _attr

        link = dpg.add_node_link( attr_out, attr_in)
        dpg.bind_item_theme(link, link_theme)

dpg.create_viewport(title='Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()

t0 = time.time()
c = 0
while dpg.is_dearpygui_running():
    delta = (time.time() - t0)*1000
    c = (c + (delta / ANIMATION_DURATION) * 230) % 230
    dpg.set_value(link_theme_color, (int(c+20), 255, int(c+20)))
    dpg.render_dearpygui_frame()

    t0 = time.time()

dpg.destroy_context()