import open3d as o3d
import numpy as np
import json
import os
import trimesh

def load_point_cloud(file_path):
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

    R = np.dot(R_z, np.dot(R_y, R_x))
    return R

def apply_transformation(vertices, info):
    R = rotation_matrix(info['roll'], info['pitch'], info['yaw'])
    transformed_vertices = np.dot(vertices * [info['a1'], info['a2'], info['a3']] * info['scale'], R.T)
    transformed_vertices += [info['tx'], info['ty'], info['tz']]
    return transformed_vertices

def reconstruct_shape(fitting_info, superquadric_library_path):
    all_points = []
    all_colors = []

    colors = [
        [1.0, 0.0, 0.0],    # Red
        [0.0, 1.0, 0.0],    # Green
        [0.0, 0.0, 1.0],    # Blue
        [1.0, 1.0, 0.0],    # Yellow
        [1.0, 0.0, 1.0],    # Magenta
        [0.0, 1.0, 1.0]     # Cyan
    ]

    for i, info in enumerate(fitting_info):
        superquadric_path = os.path.join(superquadric_library_path, info['primitive'])
        vertices = load_point_cloud(superquadric_path)
        transformed_vertices = apply_transformation(vertices, info)

        color = colors[i % len(colors)]  # Assign color to each primitive
        colors_for_primitive = np.tile(color, (transformed_vertices.shape[0], 1))

        all_points.append(transformed_vertices)
        all_colors.append(colors_for_primitive)

    all_points = np.vstack(all_points)
    all_colors = np.vstack(all_colors)

    return all_points, all_colors

def visualize_fitted_shape(fitting_info_path, superquadric_library_path):
    with open(fitting_info_path, 'r') as f:
        fitting_info = json.load(f)

    points, colors = reconstruct_shape(fitting_info, superquadric_library_path)

    # Create Open3D PointCloud object
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    # Visualize
    o3d.visualization.draw_geometries([point_cloud], window_name="Fitted Superquadric Point Cloud")

# Example usage
fitting_info_path = '/home/yifeng/PycharmProjects/Diffusion/general_case/superquadric_fitting/31_obj_fitting_info.json'  # Replace with your fitting_info.json path
superquadric_library_path = '/home/yifeng/PycharmProjects/Diffusion/superquadric_lib_rescale'  # Replace with your superquadric library path

visualize_fitted_shape(fitting_info_path, superquadric_library_path)
