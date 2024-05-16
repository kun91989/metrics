import os
import re
import datetime
import matplotlib.pyplot as plt
from skimage import io, color
import numpy as np

# Get the current time and format it as a string
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def numerical_sort(path):
    """Extract numerical value from the filename for sorting."""
    filename = os.path.basename(path)
    parts = re.findall(r'\d+', filename)
    return int(parts[0])

def process_folder(folder_path, target_folder, output_file_path):
    """Process a single folder and its corresponding target folder and output file."""
    # Ensure target folder and output file exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Folder creates: {target_folder}")
    else:
        print(f"Folder already exists: {target_folder}")

    # check if output_file_path exists
    if not os.path.exists(output_file_path):
        # if not, then create output_file_path
        with open(output_file_path, "a") as f:
            f.write(f"Start time: {current_time}\n")
        print(f"File creates: {output_file_path}")
    else:
        with open(output_file_path, "a") as f:
            f.write(f"Start time: {current_time}\n")
        print(f"File already exists: {output_file_path}")

    ##TODO: Decide whether to omit data
    # 设置numpy打印选项以完整打印每行
    # np.set_printoptions(threshold=np.inf)

    with open(output_file_path, "a") as f:
        # Get image paths and sort them
        image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.png')]
        print("Before sort:", image_paths)
        f.write("Before sort:{}\n".format(image_paths))
        image_paths.sort(key=numerical_sort)
        print("After sort:", image_paths)
        f.write("After sort:{}\n".format(image_paths))

        # Process each image
        for i, image_path in enumerate(image_paths, start=1):
            print("Image_index ", i, " path: ", image_path)
            f.write("Index {}, Image path: {}\n".format(i, image_path))
            # Read RGB image
            rgb_image = io.imread(image_path)
            rgb_image = rgb_image.astype(np.float32) / 255.0

            # Convert RGB to LAB
            lab_image = color.rgb2lab(rgb_image)
            l_channel, a_channel, b_channel = lab_image[:, :, 0], lab_image[:, :, 1], lab_image[:, :, 2]

            # Save processed image to target folder
            filename = os.path.basename(image_path)
            target_path = os.path.join(target_folder, filename[:-4] + "_L_A_B.png")

            # Create a 2x2 plot for visualization
            plt.figure()
            plt.subplot(2, 2, 1)
            plt.imshow(rgb_image)
            plt.title('Original RGB Image')
            plt.axis('off')
            plt.subplot(2, 2, 2)
            plt.imshow(l_channel, cmap='gray')
            plt.title('L Channel (Luminance)')
            plt.axis('off')
            plt.subplot(2, 2, 3)
            plt.imshow(a_channel, cmap='coolwarm')
            plt.title('A Channel (Color)')
            plt.axis('off')
            plt.subplot(2, 2, 4)
            plt.imshow(b_channel, cmap='coolwarm')
            plt.title('B Channel (Color)')
            plt.axis('off')

            # Save plot as an image
            plt.savefig(target_path)
            plt.close()

            # Calculate and record mean values of L, A, B channels
            mean_luminance = np.mean(l_channel)
            mean_a = np.mean(a_channel)
            mean_b = np.mean(b_channel)

            # Record data to output file
            f.write(f"Image Index {i}, Image Path: {image_path}\n")
            f.write(f"Mean Luminance: {mean_luminance}\n")
            f.write(f"Mean A-channel: {mean_a}\n")
            f.write(f"Mean B-channel: {mean_b}\n")
            f.write("\n")  # Add a separator

        f.write(f"Processing complete. Data saved to {output_file_path}\n")
        f.write(f"Images processed and saved to {target_folder}\n")
        # 获取当前时间并格式化为字符串
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"End time: {end_time}\n")

    print(f"Processing complete. Data saved to {output_file_path}")
    print(f"Images processed and saved to {target_folder}")

# Define the list of folder_path, target_folder, and output_file_path combinations
folders_to_process = [
    # {
    #     "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_15_200000_202404121941_15_3/data_1/1948_3",
    #     "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_15_200000_202404121941_15_3/data_1/1948_3_15_3_L_A_B_v1",
    #     "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_15_200000_202404121941_15_3/data_1/1948_3_15_3_v1_part.txt"
    # },
    # {
    #     "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_30_200000_202404121905_30_15/data_1/1948_3",
    #     "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_30_200000_202404121905_30_15/data_1/1948_3_30_15_L_A_B_v1",
    #     "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_30_200000_202404121905_30_15/data_1/1948_3_30_15_v1_part.txt"
    # },
    # {
    #     "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202414122046_20_10/data_1/1948_3",
    #     "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202414122046_20_10/data_1/1948_3_20_10_L_A_B_v1",
    #     "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202414122046_20_10/data_1/1948_3_20_10_v1_part.txt"
    # },
    # {
    #     "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202401121855_20_15/data_1/1948_3",
    #     "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202401121855_20_15/data_1/1948_3_20_15_L_A_B_v1",
    #     "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202401121855_20_15/data_1/1948_3_20_15_v1_part.txt"
    # },
    # {
    #     "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202404122156_20_5/data_1/1948_3",
    #     "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202404122156_20_5/data_1/1948_3_20_5_L_A_B_v1",
    #     "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202404122156_20_5/data_1/1948_3_20_5_v1_part.txt"
    # },
    # {
    #     "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_30_200000_202404122247_30_1/data_1/1948_3",
    #     "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_30_200000_202404122247_30_1/data_1/1948_3_30_1_L_A_B_v1",
    #     "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_30_200000_202404122247_30_1/data_1/1948_3_30_1_v1_part.txt"
    # },
    # {
    #     "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202404122245_20_20/data_1/1948_3",
    #     "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202404122245_20_20/data_1/1948_3_20_20_L_A_B_v1",
    #     "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202404122245_20_20/data_1/1948_3_20_20_v1_part.txt"
    # },
    {
        "folder_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202304130024_20_1/data_1/1948_3",
        "target_folder": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202304130024_20_1/data_1/1948_3_20_1_L_A_B_v1",
        "output_file_path": "G:/restoration/Bringing-Old-Films-Back-to-Life-main/dataset/Film1/other results/test_results_20_200000_202304130024_20_1/data_1/1948_3_20_1_v1_part.txt"
    },
    # Add more folder combinations as needed
]

# Process each folder
for folder_combination in folders_to_process:
    process_folder(folder_combination["folder_path"], folder_combination["target_folder"], folder_combination["output_file_path"])
