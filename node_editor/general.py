

def build_coordinate_list( node_source_paths, side_menu_width):
    number_of_nodes = len(node_source_paths)
    coordinates_buttons = []
    for i in range(0,number_of_nodes):
        coordinates_buttons.append([(i%2)*side_menu_width*0.55, (i//2) * 90])
    return coordinates_buttons

