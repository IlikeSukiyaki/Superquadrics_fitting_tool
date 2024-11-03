#!/usr/bin/env python3

import os
import json
import numpy as np
import trimesh
from plyfile import PlyData, PlyElement


def load_point_cloud(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
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


def reconstruct_shape(fitting_info, superquadric_library_path, output_ply_path):
    print("Starting shape reconstruction...")

    all_points = []
    all_colors = []

    # Define some distinct colors for the primitives
    colors = [
        [255, 0, 0],  # Red
        [0, 255, 0],  # Green
        [0, 0, 255],  # Blue
        [255, 255, 0],  # Yellow
        [255, 0, 255],  # Magenta
        [0, 255, 255]  # Cyan
    ]

    for i, info in enumerate(fitting_info):
        primitive = info['primitive']
        superquadric_path = os.path.join(superquadric_library_path, primitive)
        print(f"Processing primitive: {primitive}")

        try:
            vertices = load_point_cloud(superquadric_path)
        except FileNotFoundError as e:
            print(f"Error: {e}. Skipping this primitive.")
            continue

        transformed_vertices = apply_transformation(vertices, info)

        color = colors[i % len(colors)]  # Assign a color to each primitive
        colors_for_primitive = np.tile(color, (transformed_vertices.shape[0], 1))

        all_points.append(transformed_vertices)
        all_colors.append(colors_for_primitive)

    # Combine all points and colors
    all_points = np.vstack(all_points)
    all_colors = np.vstack(all_colors)

    vertices_with_color = np.empty(all_points.shape[0],
                                   dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('red', 'u1'), ('green', 'u1'),
                                          ('blue', 'u1')])
    vertices_with_color['x'] = all_points[:, 0]
    vertices_with_color['y'] = all_points[:, 1]
    vertices_with_color['z'] = all_points[:, 2]
    vertices_with_color['red'] = all_colors[:, 0]
    vertices_with_color['green'] = all_colors[:, 1]
    vertices_with_color['blue'] = all_colors[:, 2]

    # Save to .ply
    try:
        ply_element = PlyElement.describe(vertices_with_color, 'vertex')
        PlyData([ply_element], text=True).write(output_ply_path)
        print(f"Reconstructed shape successfully saved to: {output_ply_path}")
    except Exception as e:
        print(f"Failed to save .ply file: {e}")


if __name__ == "__main__":
    # Example usage paths
    fitting_info_path = '/home/yifeng/PycharmProjects/Diffusion/general_case/superquadric_fitting/8_obj_fitting_info.json'
    superquadric_library_path = '/home/yifeng/PycharmProjects/Diffusion/superquadric_lib_rescale'
    output_ply_path = '/home/yifeng/PycharmProjects/Diffusion/general_case/reconstruct_lib/8_reconstruct.ply'

    # Load the fitting information
    try:
        with open(fitting_info_path, 'r') as f:
            fitting_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: Fitting info file not found at: {fitting_info_path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from: {fitting_info_path}")
        exit(1)

    # Perform the reconstruction
    reconstruct_shape(fitting_info, superquadric_library_path, output_ply_path)
