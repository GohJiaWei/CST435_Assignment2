import os
import time
import concurrent.futures
import filters

import shutil

# Input and output directories
INPUT_DIR = "input_images"
OUTPUT_DIR = "output_concurrent"

def process_single_image(filename):
    """
    Task function for concurrent.futures. 
    It determines paths internally or takes full paths.
    Using closure or partials usually works, but top-level function is best for pickling.
    We will pass the filename and define paths inside or pass full paths.
    """
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)
    return filters.process_pipeline(input_path, output_path)

import argparse

def main():
    # Parse command-line arguments for worker configuration
    parser = argparse.ArgumentParser(description="Image processing using concurrent threads.")
    parser.add_argument("--workers", type=int, default=None, help="Number of worker threads.")
    args = parser.parse_args()

    if not os.path.exists(INPUT_DIR):
        print(f"Input directory {INPUT_DIR} not found.")
        return

    # Clean up output directory
    if os.path.exists(OUTPUT_DIR):
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

    # Display worker configuration
    worker_msg = args.workers if args.workers else "default"
    print(f"Starting concurrent.futures processing (Threading) with {worker_msg} workers on {len(image_files)} images...")
    
    # Start timing (includes thread creation and task scheduling)
    start_time = time.time()
    
    # Use ThreadPoolExecutor for Multi-threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        # submit tasks
        futures = {executor.submit(process_single_image, filename): filename for filename in image_files}
        
        results = []
        # Collect results as tasks complete
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Generated an exception: {e}")
                
    # Stop timing
    end_time = time.time()
    duration = end_time - start_time
    
    successful = [r for r in results if r is not None]
    
    # Benchmark summary
    print(f"Processing complete.")
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Images processed successfully: {len(successful)}/{len(image_files)}")

if __name__ == "__main__":
    main()
