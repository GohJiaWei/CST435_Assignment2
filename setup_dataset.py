import os
import shutil
import kagglehub
import glob
import random
import argparse

# Directory where benchmark input images will be stored
INPUT_DIR = "input_images"

def setup_dataset(target_count):
    """
    Prepare a fixed-size subset of the Food-101 dataset.

    This function ensures that INPUT_DIR contains exactly `target_count` images:
    - Removes excess images if there are too many
    - Downloads and copies images if there are too few
    """

    # Create input directory if it does not exist
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
    
    # Check existing images
    existing_images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    current_count = len(existing_images)
    
    print(f"Current image count in '{INPUT_DIR}': {current_count}")
    
    # Case 1: Too many images → randomly remove excess
    if current_count > target_count:
        excess = current_count - target_count
        print(f"Current count ({current_count}) exceeds target ({target_count}). Removing {excess} images...")
        # Random removal prevents bias toward any specific image class
        to_remove = random.sample(existing_images, excess)
        for f in to_remove:
            try:
                os.remove(os.path.join(INPUT_DIR, f))
            except OSError as e:
                print(f"Error deleting {f}: {e}")
        print(f"Removed {excess} images. Total in '{INPUT_DIR}': {target_count}")
        return
    
    # Case 2: Exact match → no action required
    elif current_count == target_count:
        print(f"Target count of {target_count} already satisfied. No changes needed.")
        return
    
    # Case 3: Too few images → download from Food-101 dataset
    needed = target_count - current_count
    print(f"Downloading/Locating Food-101 dataset to add {needed} more images...")
    
    # Download latest version (cached by kagglehub)
    path = kagglehub.dataset_download("dansbecker/food-101")
    print("Path to dataset files:", path)
    
    print("Searching for images in dataset...")
    search_path = os.path.join(path, "**", "*.jpg")
    all_images = glob.glob(search_path, recursive=True)
    
    if not all_images:
        print("No images found in the downloaded dataset path.")
        return

    print(f"Found {len(all_images)} images in source dataset.")
    
    # Randomly sample required number of images
    subset = random.sample(all_images, min(needed, len(all_images)))
    
    print(f"Copying {len(subset)} images to {INPUT_DIR}...")
    
    copied = 0
    for src in subset:
        basename = os.path.basename(src)
        dst = os.path.join(INPUT_DIR, basename)
        
        # If file exists (name collision), rename it
        while os.path.exists(dst):
            base, ext = os.path.splitext(basename)
            dst = os.path.join(INPUT_DIR, f"{base}_{random.randint(1000,9999)}{ext}")
            
        shutil.copy2(src, dst)
        copied += 1
        
    print(f"Added {copied} images. Total in '{INPUT_DIR}': {current_count + copied}")

if __name__ == "__main__":
    # Command-line interface for dataset setup
    parser = argparse.ArgumentParser(description="Setup Food-101 dataset subset.")
    parser.add_argument("--count", type=int, default=50, help="Total number of images desired in input_images.")
    args = parser.parse_args()
    
    setup_dataset(args.count)
