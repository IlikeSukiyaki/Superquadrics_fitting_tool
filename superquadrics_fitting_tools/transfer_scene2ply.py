import os
import json
from obj_preprocessing import convert_obj_to_ply


def process_scene_to_ply(scene_gt_path, obj_base_path, output_dir, num_samples=8000):
    # Load the scene_gt.json file
    with open(scene_gt_path, 'r') as f:
        scene_gt_data = json.load(f)

    # Iterate over all entries in the scene
    for entry in scene_gt_data["3"]:
        obj_id = entry["obj_id"]

        # Construct the paths for the .obj and .ply files
        obj_file_name = f'{str(obj_id).zfill(3)}_obj.obj'  # Pad the object ID with leading zeros
        obj_file_path = os.path.join(obj_base_path, obj_file_name)

        if not os.path.exists(obj_file_path):
            print(f"Warning: {obj_file_path} not found, skipping...")
            continue

        # Define the custom output .ply file name and path
        # Strip leading zeros from the object ID in the output file name
        custom_ply_file_name = f'{int(obj_id)}_obj.ply'  # Use int() to strip leading zeros
        ply_file_path = os.path.join(output_dir, custom_ply_file_name)

        # Convert the .obj file to .ply
        convert_obj_to_ply(obj_file_path, ply_file_path, num_samples=num_samples)
        print(f"Processed and saved: {ply_file_path}")

    print("Processing complete!")


if __name__ == "__main__":
    # Paths
    scene_gt_path = '/home/yifeng/PycharmProjects/Diffusion/general_case/gt_label/scene296/scene_gt.json'  # Replace with your scene_gt.json path
    obj_base_path = '/home/yifeng/PycharmProjects/Diffusion/general_case/model_auto'  # Replace with your base directory for .obj files
    output_dir = '/home/yifeng/PycharmProjects/Diffusion/general_case/point_cloud_lib'  # Replace with your desired output directory

    # Number of samples for downsampling
    num_samples = 8000

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process the scene and convert to .ply
    process_scene_to_ply(scene_gt_path, obj_base_path, output_dir, num_samples=num_samples)
