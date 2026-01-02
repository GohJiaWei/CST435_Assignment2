import subprocess
import re
import os
import multiprocessing
import sys

def parse_time(output):
    # Look for "Time taken: X seconds"
    match = re.search(r"Time taken:\s+([\d\.]+)\s+seconds", output)
    if match:
        return float(match.group(1))
    return None

def run_benchmark(script_name, workers):
    cmd = [sys.executable, script_name, "--workers", str(workers)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return parse_time(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name} with {workers} workers: {e}")
        print(e.stdout)
        print(e.stderr)
        return None

def count_images(directory):
    if not os.path.exists(directory):
        return 0
    return len([f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

def main():
    # Define worker counts to test
    worker_counts = [1, 2, 4, 8, 12]
    
    input_dir = "input_images"
    num_images = count_images(input_dir)
    
    if num_images == 0:
        print(f"Error: No images found in '{input_dir}'. Please run setup_dataset.py first.")
        return
        
    # Get CPU count for reference
    cpu_count = multiprocessing.cpu_count()
        
    scripts = [
        ("Multiprocessing", "main_multiprocessing.py"),
        ("Threading", "main_concurrent.py")
    ]
    
    print(f"Benchmarking on {cpu_count} CPU cores.")
    print(f"Dataset Size: {num_images} images")
    print(f"Testing worker counts: {worker_counts}\n")
    
    for name, script in scripts:
        print(f"--- Benchmarking {name} ({script}) ---")
        print(f"{'Workers':<10} | {'Time (s)':<10} | {'Speedup':<10} | {'Efficiency':<10}")
        print("-" * 50)
        
        base_time = None
        
        for w in worker_counts:
            time_taken = run_benchmark(script, w)
            
            if time_taken is None:
                print(f"{w:<10} | {'Failed':<10} | {'-':<10} | {'-':<10}")
                continue
                
            if w == 1:
                base_time = time_taken
                speedup = 1.0
                efficiency = 1.0
            else:
                if base_time:
                    speedup = base_time / time_taken
                    efficiency = speedup / w
                else:
                    speedup = 0.0
                    efficiency = 0.0
            
            print(f"{w:<10} | {time_taken:<10.4f} | {speedup:<10.2f} | {efficiency:<10.2f}")
        print("\n")

if __name__ == "__main__":
    main()
