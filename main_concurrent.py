import os
import time
import concurrent.futures
import filters

import shutil

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

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory {INPUT_DIR} not found.")
        return

    # Clean up output directory
    if os.path.exists(OUTPUT_DIR):
        print(f"Cleaning up existing output directory: {OUTPUT_DIR}")
        shutil.rmtree(OUTPUT_DIR)
        
    os.makedirs(OUTPUT_DIR)
        
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("No images found to process.")
        return

    print(f"Starting concurrent.futures processing (Threading) on {len(image_files)} images...")
    
    start_time = time.time()
    
    # Use ThreadPoolExecutor for Multi-threading
    # Note: In Python, CPU-bound tasks like image processing are limited by the GIL when using threads.
    # This might be slower than Multiprocessing or even Serial execution, but demonstrates the paradigm.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # submit tasks
        futures = {executor.submit(process_single_image, filename): filename for filename in image_files}
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Generated an exception: {e}")
                
    end_time = time.time()
    duration = end_time - start_time
    
    successful = [r for r in results if r is not None]
    
    print(f"Processing complete.")
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Images processed successfully: {len(successful)}/{len(image_files)}")

if __name__ == "__main__":
    main()
