import os
import trimesh

def rescale_ply_vertices(input_file, output_file, scale_factor):
    """
    Rescales the vertices of a .ply file by the given scale factor and saves it as an ASCII .ply file.

    :param input_file: Path to the input .ply file.
    :param output_file: Path to save the rescaled .ply file.
    :param scale_factor: The factor by which to divide each vertex coordinate.
    """
    # Load the .ply file
    mesh = trimesh.load_mesh(input_file)

    # Rescale the vertices
    mesh.vertices /= scale_factor

    # Save the rescaled mesh to a new .ply file in ASCII format
    mesh.export(output_file, file_type='ply', encoding='ascii')
    print(f"Rescaled and saved {output_file} in ASCII format")


def process_directory(input_directory, output_directory, scale_factor=10):
    """
    Processes all .ply files in the specified input directory, rescaling their vertices,
    and saving them to the specified output directory.

    :param input_directory: Path to the directory containing .ply files.
    :param output_directory: Path to the directory where rescaled .ply files will be saved.
    :param scale_factor: The factor by which to divide each vertex coordinate.
    """
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith('.ply'):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename)

            # Rescale the .ply file vertices
            rescale_ply_vertices(input_file, output_file, scale_factor)


# Specify the directory containing the original .ply files
input_directory = '/home/yifeng/PycharmProjects/Diffusion/superquadric_library'

# Specify the output directory where rescaled .ply files will be saved
output_directory = '/home/yifeng/PycharmProjects/Diffusion/superquadric_lib_rescale'

# Process all .ply files in the input directory and save them to the output directory
process_directory(input_directory, output_directory)
