import trimesh
import matplotlib.pyplot as plt
import numpy as np


def visualize_multiple_ply_point_clouds(file_paths, xlim=None, ylim=None, zlim=None):
    """
    Visualizes multiple 3D point clouds from a list of .ply files as subplots.

    :param file_paths: List of paths to the .ply files.
    :param xlim: Tuple specifying the limits for the x-axis (min, max).
    :param ylim: Tuple specifying the limits for the y-axis (min, max).
    :param zlim: Tuple specifying the limits for the z-axis (min, max).
    """
    num_files = len(file_paths)

    # Create subplots
    fig = plt.figure(figsize=(15, 5 * num_files))

    for i, file_path in enumerate(file_paths):
        ax = fig.add_subplot(num_files, 1, i + 1, projection='3d')

        # Load the .ply file
        mesh = trimesh.load_mesh(file_path)

        # Extract the vertices (points)
        vertices = mesh.vertices

        # Plot the point cloud
        ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=1)

        # Set axis limits if specified
        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)
        if zlim:
            ax.set_zlim(zlim)

        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Point Cloud {i + 1}: {file_path}')

    plt.tight_layout()
    plt.show()


# Example usage
file_paths = [
    '/home/yifeng/PycharmProjects/Diffusion/test_case/point_cloud_lib/39_obj.ply',
    '/home/yifeng/PycharmProjects/Diffusion/test_case/point_cloud_lib/62_obj.ply'
]

# Example axis limits
xlim = (-0.05, 0.05)
ylim = (-0.05, 0.05)
zlim = (-0.05, 0.05)

visualize_multiple_ply_point_clouds(file_paths, xlim, ylim, zlim)
