import os
import json
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import ipywidgets as widgets
from IPython.display import display

def load_point_cloud(file_path):
    # Load the .ply file
    mesh = trimesh.load_mesh(file_path)
    return mesh.vertices

def rotation_matrix(roll, pitch, yaw):
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])

    # Combined rotation matrix
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R

def update(val):
    ax.clear()

    # Plot the object point cloud
    ax.scatter(object_vertices[:, 0], object_vertices[:, 1], object_vertices[:, 2], label='Object', s=1)

    # Plot the superquadric point clouds with updated position, scale, and shape
    for i, sliders in enumerate(superquadric_sliders):
        vertices = superquadric_vertices_list[i]
        tx = sliders['tx'].val
        ty = sliders['ty'].val
        tz = sliders['tz'].val
        scale = sliders['scale'].val
        a1 = sliders['a1'].val
        a2 = sliders['a2'].val
        a3 = sliders['a3'].val
        roll = sliders['roll'].val
        pitch = sliders['pitch'].val
        yaw = sliders['yaw'].val

        R = rotation_matrix(roll, pitch, yaw)
        transformed_vertices = np.dot(vertices * [a1, a2, a3] * scale, R.T) + [tx, ty, tz]

        ax.scatter(transformed_vertices[:, 0], transformed_vertices[:, 1], transformed_vertices[:, 2],
                   label=f'Superquadric {i + 1}', s=1)

    # Set labels and show plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-0.2, 0.2])
    ax.set_ylim([-0.2, 0.2])
    ax.set_zlim([-0.2, 0.2])
    ax.legend()
    plt.draw()

def add_superquadric(event):
    selected_primitive = radio.value_selected
    superquadric_path = os.path.join(superquadric_library_path, selected_primitive)
    vertices = load_point_cloud(superquadric_path)
    superquadric_vertices_list.append(vertices)

    # Create new sliders for this superquadric
    slider_width = 0.65
    slider_height = 0.03

    # Fixed positions for sliders (no shifting up)
    base_position = 0.01
    vertical_spacing = 0.05

    ax_tx = plt.axes([0.25, base_position + 0 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_ty = plt.axes([0.25, base_position + 1 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_tz = plt.axes([0.25, base_position + 2 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_scale = plt.axes([0.25, base_position + 3 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_a1 = plt.axes([0.25, base_position + 4 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_a2 = plt.axes([0.25, base_position + 5 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_a3 = plt.axes([0.25, base_position + 6 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_roll = plt.axes([0.25, base_position + 7 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_pitch = plt.axes([0.25, base_position + 8 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)
    ax_yaw = plt.axes([0.25, base_position + 9 * vertical_spacing, slider_width, slider_height], facecolor=axcolor)

    slider_tx = Slider(ax_tx, f'Tx {len(superquadric_sliders) + 1}', -0.5, 0.5, valinit=0)
    slider_ty = Slider(ax_ty, f'Ty {len(superquadric_sliders) + 1}', -0.5, 0.5, valinit=0)
    slider_tz = Slider(ax_tz, f'Tz {len(superquadric_sliders) + 1}', -0.5, 0.5, valinit=0)
    slider_scale = Slider(ax_scale, f'Scale {len(superquadric_sliders) + 1}', 0.001, 10.0, valinit=1.0)
    slider_a1 = Slider(ax_a1, f'a1 {len(superquadric_sliders) + 1}', 0.1, 5.0, valinit=1.0)
    slider_a2 = Slider(ax_a2, f'a2 {len(superquadric_sliders) + 1}', 0.1, 5.0, valinit=1.0)
    slider_a3 = Slider(ax_a3, f'a3 {len(superquadric_sliders) + 1}', 0.1, 5.0, valinit=1.0)
    slider_roll = Slider(ax_roll, f'Roll {len(superquadric_sliders) + 1}', -np.pi, np.pi, valinit=0)
    slider_pitch = Slider(ax_pitch, f'Pitch {len(superquadric_sliders) + 1}', -np.pi, np.pi, valinit=0)
    slider_yaw = Slider(ax_yaw, f'Yaw {len(superquadric_sliders) + 1}', -np.pi, np.pi, valinit=0)

    slider_tx.on_changed(update)
    slider_ty.on_changed(update)
    slider_tz.on_changed(update)
    slider_scale.on_changed(update)
    slider_a1.on_changed(update)
    slider_a2.on_changed(update)
    slider_a3.on_changed(update)
    slider_roll.on_changed(update)
    slider_pitch.on_changed(update)
    slider_yaw.on_changed(update)

    superquadric_sliders.append({
        'tx': slider_tx,
        'ty': slider_ty,
        'tz': slider_tz,
        'scale': slider_scale,
        'a1': slider_a1,
        'a2': slider_a2,
        'a3': slider_a3,
        'roll': slider_roll,
        'pitch': slider_pitch,
        'yaw': slider_yaw,
        'primitive': selected_primitive  # Store the selected primitive in the sliders dictionary
    })

    # Update the dropdown menu with the new superquadric
    dropdown_menu.options = [f'Superquadric {i + 1}' for i in range(len(superquadric_sliders))]
    dropdown_menu.value = dropdown_menu.options[-1]
    update_active_sliders(None)

def update_active_sliders(change):
    active_index = int(dropdown_menu.value.split()[-1]) - 1
    for i, sliders in enumerate(superquadric_sliders):
        visible = (i == active_index)
        for key, slider in sliders.items():
            slider.ax.set_visible(visible)
    plt.draw()

def save_fitting_info(event):
    fitting_info = []
    for sliders in superquadric_sliders:
        # Extract the object ID from the filename
        object_name = os.path.splitext(os.path.basename(object_ply_path))[0]
        object_id = object_name.split('_')[0]  # Extract the first part before the underscore

        info = {
            'primitive': sliders['primitive'],  # Use the stored primitive value
            'a1': sliders['a1'].val,
            'a2': sliders['a2'].val,
            'a3': sliders['a3'].val,
            'scale': sliders['scale'].val,
            'tx': sliders['tx'].val,
            'ty': sliders['ty'].val,
            'tz': sliders['tz'].val,
            'roll': sliders['roll'].val,
            'pitch': sliders['pitch'].val,
            'yaw': sliders['yaw'].val,
            'object': object_id  # Store the extracted object ID here
        }
        fitting_info.append(info)

    # Create a unique filename based on the object being fitted
    base_output_file = os.path.join(fitting_info_directory, f'{object_name}_fitting_info')

    # Check for existing files and create a new filename with an incremented suffix if necessary
    output_file = f'{base_output_file}.json'
    index = 1
    while os.path.exists(output_file):
        output_file = f'{base_output_file}_{index:02d}.json'
        index += 1

    with open(output_file, 'w') as f:
        json.dump(fitting_info, f, indent=4)
    print(f"Fitting information saved to {output_file}")

# Paths to your object and superquadric .ply files
object_ply_path = '/home/yifeng/PycharmProjects/Diffusion/general_case/point_cloud_lib/8_obj.ply'
superquadric_library_path = '/home/yifeng/PycharmProjects/Diffusion/superquadric_lib_rescale'
fitting_info_directory = '/home/yifeng/PycharmProjects/Diffusion/general_case/superquadric_fitting'

# Ensure the fitting info directory exists
os.makedirs(fitting_info_directory, exist_ok=True)

# Load the point clouds
object_vertices = load_point_cloud(object_ply_path)
superquadric_vertices_list = []

# Create the figure and axis
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d')

# Plot the initial point clouds
ax.scatter(object_vertices[:, 0], object_vertices[:, 1], object_vertices[:, 2], label='Object', s=1)

# Set labels and show initial plot
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim([-0.2, 0.2])
ax.set_ylim([-0.2, 0.2])
ax.set_zlim([-0.2, 0.2])
ax.legend()

# Create sliders for translation, scaling, and rotation adjustments
axcolor = 'lightgoldenrodyellow'
superquadric_sliders = []

# Add button to add another superquadric
ax_add_button = plt.axes([0.8, 0.95, 0.1, 0.04])
button_add = Button(ax_add_button, 'Add Superquadric')
button_add.on_clicked(add_superquadric)

# Create radio buttons to select superquadric primitive
ax_radio = plt.axes([0.01, 0.01, 0.2, 0.9], facecolor=axcolor)
superquadric_files = [f for f in os.listdir(superquadric_library_path) if f.endswith('.ply')]
radio = RadioButtons(ax_radio, superquadric_files)

# Create dropdown menu to select the active superquadric
dropdown_menu = widgets.Dropdown(
    options=[f'Superquadric {i + 1}' for i in range(len(superquadric_sliders))],
    value=None,
    description='Select Superquadric'
)
dropdown_menu.observe(update_active_sliders, names='value')
display(dropdown_menu)

# Add button to save fitting information
ax_save_button = plt.axes([0.8, 0.9, 0.1, 0.04])
button_save = Button(ax_save_button, 'Save Fitting')
button_save.on_clicked(save_fitting_info)

plt.show()
