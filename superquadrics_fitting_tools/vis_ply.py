import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def farthest_point_sampling(vertices, num_samples):
    """
    Perform farthest point sampling to downsample the point cloud.

    :param vertices: (N, 3) array of vertices from the point cloud.
    :param num_samples: Number of points to sample.
    :return: (num_samples, 3) array of sampled vertices.
    """
    # Initialize an array to store the indices of sampled points
    sampled_indices = np.zeros(num_samples, dtype=int)

    # Initialize the first sampled point randomly
    sampled_indices[0] = np.random.randint(len(vertices))

    # Compute the distance from the first point to all other points
    distances = np.linalg.norm(vertices - vertices[sampled_indices[0]], axis=1)

    for i in range(1, num_samples):
        # Select the point that is farthest from the set of sampled points
        sampled_indices[i] = np.argmax(distances)
        # Update distances to the nearest sampled point
        new_distances = np.linalg.norm(vertices - vertices[sampled_indices[i]], axis=1)
        distances = np.minimum(distances, new_distances)

    return vertices[sampled_indices]


def visualize_ply_point_cloud(file_path, num_samples=None):
    # Load the .ply file
    mesh = trimesh.load_mesh(file_path)

    # Extract the vertices (points)
    vertices = mesh.vertices

    # Downsample the point cloud using FPS if num_samples is specified
    if num_samples and num_samples < len(vertices):
        vertices = farthest_point_sampling(vertices, num_samples)

    # Create a figure and a 3D axis
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the point cloud
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='skyblue', s=1)

    # Set labels and show plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('PLY Point Cloud Visualization')
    plt.show()


# Path to your .ply file
file_path = '/home/yifeng/PycharmProjects/Diffusion/test_case/superquadric_fitting/reconstructed_shape.ply'

# Number of points to sample for visualization (adjust this number as needed)
num_samples = 5000

# Visualize the .ply file with downsampling
visualize_ply_point_cloud(file_path, num_samples)
