import os
import trimesh
import matplotlib.pyplot as plt
import numpy as np


def visualize_superquadric_primitives(eps1_values, eps2_values, directory):
    """
    Visualizes superquadric primitives based on specified ranges for eps1 and eps2.

    :param eps1_values: List of eps1 values.
    :param eps2_values: List of eps2 values.
    :param directory: Path to the directory containing .ply files.
    """
    num_eps1 = len(eps1_values)
    num_eps2 = len(eps2_values)

    fig, axes = plt.subplots(num_eps1, num_eps2, figsize=(15, 15), subplot_kw={'projection': '3d'})

    for i, eps1 in enumerate(eps1_values):
        for j, eps2 in enumerate(eps2_values):
            # Construct the filename based on the current eps1 and eps2
            filename = f"{eps1}_{eps2}.ply"
            file_path = os.path.join(directory, filename)

            if not os.path.exists(file_path):
                print(f"File {filename} does not exist. Skipping.")
                continue

            # Load the .ply file
            mesh = trimesh.load_mesh(file_path)

            # Extract the vertices (points)
            vertices = mesh.vertices

            # Plot the point cloud
            ax = axes[i, j]
            ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=1)

            # Set plot title and axis labels
            ax.set_title(f'eps1={eps1}, eps2={eps2}')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

    # Adjust layout to avoid overlap
    plt.tight_layout()
    plt.show()


# Example usage
eps1_values = [0, 0.5, 1.0, 1.5]
eps2_values = [0, 0.5, 1.0, 1.5]
directory = '/home/yifeng/PycharmProjects/Diffusion/superquadric_lib_rescale'

visualize_superquadric_primitives(eps1_values, eps2_values, directory)
