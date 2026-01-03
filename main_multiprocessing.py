import os
import time
import multiprocessing
import filters

INPUT_DIR = "input_images"
OUTPUT_DIR = "output_multiprocessing"

import shutil

def process_image_task(args):
    """
    Wrapper function to unpack arguments for the pipeline.
    """
    input_path, output_path = args
    return filters.process_pipeline(input_path, output_path)

import argparse

def main():
    parser = argparse.ArgumentParser(description="Image processing using multiprocessing.")
    parser.add_argument("--workers", type=int, default=multiprocessing.cpu_count(), help="Number of worker processes.")
    args = parser.parse_args()

    if not os.path.exists(LOCAL_INPUT_DIR := INPUT_DIR): # Use global
        print(f"Input directory {INPUT_DIR} not found.")
        return

    # Clean up output directory
    if os.path.exists(OUTPUT_DIR):
        # Delete everything inside EXCEPT .gitkeep
        for item in os.listdir(OUTPUT_DIR):
            if item == ".gitkeep":
                continue
            item_path = os.path.join(OUTPUT_DIR, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        os.makedirs(OUTPUT_DIR)
        
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("No images found to process.")
        return

    # Prepare arguments for multiprocessing
    # List of tuples: (input_path, output_path)
    tasks = []
    for filename in image_files:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)
        tasks.append((input_path, output_path))
        
    print(f"Starting multiprocessing with {args.workers} cores on {len(tasks)} images...")
    
    start_time = time.time()
    
    # Use Pool to parallelize
    with multiprocessing.Pool(processes=args.workers) as pool:
        # starmap is useful for multiple arguments, 
        # but we packed them into a tuple for 'process_image_task' to keep it simple compatible with map
        # Or we can use pool.imap_unordered for potentially better responsiveness
        results = pool.map(process_image_task, tasks)
        
    end_time = time.time()
    duration = end_time - start_time
    
    successful = [r for r in results if r is not None]
    
    print(f"Processing complete.")
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Images processed successfully: {len(successful)}/{len(tasks)}")
    
if __name__ == "__main__":
    main()
