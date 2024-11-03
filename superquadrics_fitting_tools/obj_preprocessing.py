import os
import trimesh
import numpy as np
import matplotlib.pyplot as plt


def farthest_point_sampling(vertices, num_samples):
    """
    Perform farthest point sampling to downsample the point cloud.

    :param vertices: (N, 3) array of vertices from the point cloud.
    :param num_samples: Number of points to sample.
    :return: (num_samples, 3) array of sampled vertices.
    """
    sampled_indices = np.zeros(num_samples, dtype=int)
    sampled_indices[0] = np.random.randint(len(vertices))
    distances = np.linalg.norm(vertices - vertices[sampled_indices[0]], axis=1)

    for i in range(1, num_samples):
        sampled_indices[i] = np.argmax(distances)
        new_distances = np.linalg.norm(vertices - vertices[sampled_indices[i]], axis=1)
        distances = np.minimum(distances, new_distances)

    return vertices[sampled_indices]


def visualize_point_cloud(ply_file):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    mesh = trimesh.load_mesh(ply_file)
    vertices = mesh.vertices

    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=1)
    ax.set_title(os.path.basename(ply_file))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.tight_layout()
    plt.show()


def convert_obj_to_ply(obj_file_path, ply_file_path, num_samples=None):
    mesh = trimesh.load_mesh(obj_file_path)
    vertices = mesh.vertices

    if num_samples and num_samples < len(vertices):
        vertices = farthest_point_sampling(vertices, num_samples)

    point_cloud = trimesh.points.PointCloud(vertices)

    with open(ply_file_path, 'w') as f:
        point_cloud.export(f, file_type='ply', encoding='ascii')

    print(f"Converted {obj_file_path} to {ply_file_path}")


# Paths
obj_file_path = '/home/yifeng/PycharmProjects/Diffusion/general_case/model_auto/097_obj.obj'
output_dir = '/home/yifeng/PycharmProjects/Diffusion/general_case/point_cloud_lib'
custom_ply_file_name = '097_obj.ply'
ply_file_path = os.path.join(output_dir, custom_ply_file_name)

num_samples = 8000  # Downsample to 5000 points

os.makedirs(output_dir, exist_ok=True)
convert_obj_to_ply(obj_file_path, ply_file_path, num_samples=num_samples)
visualize_point_cloud(ply_file_path)

