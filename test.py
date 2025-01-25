import dearpygui.dearpygui as dpg

# Initialize Dear PyGui context
dpg.create_context()

# Load the custom icon (ensure the image exists and is in the correct path)
icon_path = "icon.png"  # Replace with the path to your icon file
#icon_image = dpg.add_static_texture(width=32, height=32, default_value=[255, 0, 0, 255])  # Placeholder (create icon texture)
icon_image = dpg.load_image(icon_path)[0]  # Load the actual image from the file

# Create the window and set the viewport icon for the taskbar thumbnail
dpg.create_viewport(title="Custom Thumbnail", width=600, height=400)
dpg.set_viewport_icon(icon_image)

# Create the window and the content
with dpg.window(label="Main Window"):
    dpg.add_text("Custom Taskbar Thumbnail Example")

# Setup and show the window
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

# Clean up the context after use
dpg.destroy_context()
