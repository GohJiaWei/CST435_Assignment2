import os
import time
import multiprocessing
import filters

# Input and output directories
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
    # Parse number of worker processes (default = CPU core count)
    parser = argparse.ArgumentParser(description="Image processing using multiprocessing.")
    parser.add_argument("--workers", type=int, default=multiprocessing.cpu_count(), help="Number of worker processes.")
    args = parser.parse_args()

    # Validate input directory
    if not os.path.exists(LOCAL_INPUT_DIR := INPUT_DIR): # Use global
        print(f"Input directory {INPUT_DIR} not found.")
        return

    # Clean up output directory
    if os.path.exists(OUTPUT_DIR):
        # Delete everything inside EXCEPT .gitkeep
        for item in os.listdir(OUTPUT_DIR):
            # Preserve version control placeholder
            if item == ".gitkeep":
                continue
            item_path = os.path.join(OUTPUT_DIR, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        # Create output directory if missing
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
    
    # Start timing (includes process creation and task scheduling)
    start_time = time.time()
    
    # Use Pool to parallelize
    with multiprocessing.Pool(processes=args.workers) as pool:
        # Pool.map distributes tasks evenly across worker processes
        # Results are returned in the same order as input tasks
        results = pool.map(process_image_task, tasks)
        
    # Stop timing
    end_time = time.time()
    duration = end_time - start_time
    
    successful = [r for r in results if r is not None]
    
    # Benchmark summary
    print(f"Processing complete.")
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Images processed successfully: {len(successful)}/{len(tasks)}")
    
if __name__ == "__main__":
    main()
