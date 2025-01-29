import dearpygui.dearpygui as dpg
import numpy as np 
from node_editor.general import retrieve_matrix , dpg_get_value , dpg_set_value
import numsolvers.TSP as tsp

_Node_Name = "Mixed-Node"

def check_if_works():
    print(f"{_Node_Name} successfully imported")
class Node:

    node_label = "Mixed Node"
    node_tag = "Mixed"

    received_data = {}  #a dict which tracks for every node if a connection has been made
    run_dict = {} #a dict which tracks for every node if the run button has been pressed
    k_indecces = {}
    all_cities_specimen_dict = {}
    all_cities_lenghts_dict = {}
    n_mutations_dict = {}
    tstart_dict = {}
    q_dict = {}
    temperatures_dict = {}
    lenght_dict = {}

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
        
        tag_node_input01_name = tag_node_name + ":Cities" + ":Input01"
        tag_node_input01_value_name = tag_node_name +":Cities" + ":Input01Value"

        tag_node_input02_name = tag_node_name + ":Func" + ":Input02"
        tag_node_input02_value_name = tag_node_name +":Func" + ":Input02Value"

        tag_node_input03_name = tag_node_name + ":Int" + ":Input03"
        tag_node_input03_value_name = tag_node_name +":Int" + ":Input03Value"
        
        tag_node_input04_name = tag_node_name + ":Int" + ":Input04"
        tag_node_input04_value_name = tag_node_name +":Int" + ":Input04Value"

        tag_node_input05_name = tag_node_name + ":Float" + ":Input05"
        tag_node_input05_value_name = tag_node_name +":Float" + ":Input05Value"

        tag_node_input06_name = tag_node_name + ":Float" + ":Input06"
        tag_node_input06_value_name = tag_node_name +":Float" + ":Input06Value"

        tag_node_output01_name = tag_node_name + ":Cities" + ":Output01"
        tag_node_output01_value_name = tag_node_name + ":Cities" + ':Output01Value'

        tag_node_output02_name = tag_node_name + ":Float" +":Output02" 
        tag_node_output02_value_name = tag_node_name + ":Float" +":Output02Value"
        
        tag_node_output03_name = tag_node_name + ":Float" +":Output03" 
        tag_node_output03_value_name = tag_node_name + ":Float" +":Output03Value"

        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['process_width']
        small_window_h = self._opencv_setting_dict['process_height']

        self.k_indecces[tag_node_name] = 1
        self.received_data[tag_node_name] = False
        self.run_dict[tag_node_name] = False
        self._default_xdata = 100*np.linspace(0, 1, 30)* np.cos(3*np.linspace(0, 2*np.pi, 30))
        self._default_ydata = 100 * np.linspace(0, 1, 30)*np.sin(3*np.linspace(0, 2*np.pi, 30))
        self._default_limits = (-110,110,-110,110)
        self.all_cities_specimen_dict[tag_node_name] = tsp.create_diversity(np.array([self._default_xdata,self._default_ydata]).T,8)
        self.all_cities_lenghts_dict[tag_node_name] = tsp.calculate_lenght(self.all_cities_specimen_dict[tag_node_name])
        self.n_mutations_dict[tag_node_name] = 500
        self.tstart_dict[tag_node_name] = 10
        self.q_dict[tag_node_name] = 0.1
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
                with dpg.child_window(
                    width= small_window_w,
                    height=50,
                ):      
                    with dpg.group(horizontal=True):
                        with dpg.group(horizontal=False):
                                    dpg.add_input_int(
                                    tag=tag_node_input03_value_name,
                                    label="Population Size",
                                    width=80,
                                    default_value=4, 
                                    callback=self._call_back_Pop_size, 
                                    user_data= [tag_node_output01_value_name + "cities_pos",tag_node_name])
                                    dpg.add_input_int(
                                    tag=tag_node_input04_value_name,
                                    label="Number Mutations",
                                    width=80,
                                    default_value=self.n_mutations_dict[tag_node_name], 
                                    callback=self._call_back_mutations, 
                                    user_data= tag_node_name)
                        with dpg.group(horizontal=False):            
                            with dpg.group(horizontal=True):
                                    dpg.add_spacer(width=40)  # Adjust width to push buttons to the right
                                    dpg.add_button(label="RUN", callback=self._call_back_run, user_data=tag_node_name)
                                    dpg.add_button(label="STOP", callback=self._call_back_stop, user_data=tag_node_name)
                                    dpg.add_button(label="RESET K", callback=self._call_back_reset, user_data=tag_node_name)
                                    
                            with dpg.group(horizontal=True):
                                dpg.add_spacer(width=20)
                                dpg.add_drag_float(
                                    tag=tag_node_input05_value_name,
                                    label = "Tstart",
                                    width = 50,
                                    default_value=self.tstart_dict[tag_node_name],
                                    callback = self._call_back_tstart,
                                    user_data= tag_node_name
                                )
                                dpg.add_drag_float(
                                    tag=tag_node_input06_value_name,
                                    label = "q",
                                    width = 50,
                                    default_value=self.q_dict[tag_node_name],
                                    callback = self._call_back_q,
                                    user_data= tag_node_name
                                )

                
            with dpg.node_attribute(
            tag= tag_node_input01_name,
            attribute_type=dpg.mvNode_Attr_Input
            ):
                dpg.add_text("Cities Input")

            with dpg.node_attribute(
                tag= tag_node_input02_name,
                label="Temperature Function",
                attribute_type=dpg.mvNode_Attr_Input
            ):
                dpg.add_text("Temp Func")

            
            with dpg.node_attribute(
                tag= tag_node_output02_name,
                label= "Current Lenght1",
                attribute_type=dpg.mvNode_Attr_Output
            ):
                dpg.add_drag_float(
                                    tag=tag_node_output02_value_name,
                                    label = "Current Lenght",
                                    width = 50,
                                    default_value=0.0,
                                    show=False
                                )
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=small_window_w-130)
                    dpg.add_text("Current Lenght")    

            with dpg.node_attribute(
                tag= tag_node_output03_name,
                label= "Current Temp",
                attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_drag_float(
                                    tag=tag_node_output03_value_name,
                                    label = "Current Lenght",
                                    width = 50,
                                    default_value=0.0,
                                    show=False
                                )
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=small_window_w-130)
                    dpg.add_text("Current Temp")    
                
            
               
        
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

        tag_node_output02_name = tag_node_name + ":Float" +":Output02" 
        tag_node_output02_value_name = tag_node_name + ":Float" +":Output02Value"
        
        tag_node_output03_name = tag_node_name + ":Float" +":Output03" 
        tag_node_output03_value_name = tag_node_name + ":Float" +":Output03Value"

        link = connection_list.get(tag_node_input01_name, None)
       
        if link is not None and self.received_data[tag_node_name] == False:
            
            Cities = dpg_get_value(link[0] + "Value" + "cities_pos")[0:2]
            
            self.all_cities_specimen_dict[tag_node_name] = tsp.create_diversity(np.array(Cities).T,8)
            self.all_cities_lenghts_dict[tag_node_name] = tsp.calculate_lenght(self.all_cities_specimen_dict[tag_node_name])
            
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
            
            self.k_indecces[tag_node_name] += 1
            #print(f"k index = {self.k_indecces[tag_node_name]} tag_node_name = {tag_node_name}")
            temp = self.tstart_dict[tag_node_name]*self.k_indecces[tag_node_name]**(-self.q_dict[tag_node_name])
            #print(f"temp = {temp}")
            all_cities_specimen, all_cities_lenghts = tsp.run_mixed(
                self.all_cities_specimen_dict[tag_node_name],
                self.all_cities_lenghts_dict[tag_node_name],
                self.n_mutations_dict[tag_node_name],
                temp)
            
            self.all_cities_specimen_dict[tag_node_name] = all_cities_specimen
            self.all_cities_lenghts_dict[tag_node_name] = all_cities_lenghts
            best_route = np.array(all_cities_specimen[np.argmin(all_cities_lenghts)])
            #print(f"number pop {len(all_cities_lenghts)}")
            #print(f"best route = {best_route}")
            
            dpg_set_value(
                tag_node_output01_value_name + "cities_pos",
                [np.array(best_route.T[0]),np.array(best_route.T[1])])
            dpg_set_value(
                tag_node_output01_value_name + "paths",
                [np.array(best_route.T[0]),np.array(best_route.T[1])])
            dpg_set_value(
                tag_node_output02_value_name,
                all_cities_lenghts[np.argmin(all_cities_lenghts)]
            )
            dpg_set_value(
                tag_node_output03_value_name,
                temp
            )
        #else:

            #print("OH NOOOOOOO")
        

        return None, None
    


    def _call_back_run(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.run_dict[tag_node_name] = True
        pass

    def _call_back_stop(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.run_dict[tag_node_name] = False
       

    def _call_back_reset(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.k_indecces[tag_node_name] = 1

    def _call_back_Pop_size(
            self,
            sender,
            app_data,
            user_data,
    ):
        
        Cities = np.array(dpg_get_value(user_data[0]))
        self.all_cities_specimen_dict[user_data[1]] = tsp.create_diversity(np.array(Cities).T,app_data)
        self.all_cities_lenghts_dict[user_data[1]] = tsp.calculate_lenght(self.all_cities_specimen_dict[user_data[1]])
        
        

    def _call_back_mutations(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.n_mutations_dict[tag_node_name] = app_data
        

    def _call_back_tstart(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.tstart_dict[tag_node_name] = app_data

    def _call_back_q(
            self,
            sender,
            app_data,
            user_data
    ):
        tag_node_name = user_data
        self.q_dict[tag_node_name] = app_data