# Python Parallel Image Processing

This project implements a parallel image processing pipeline using Python with two different approaches: **Multiprocessing** and **Multithreading**. It uses the **Food-101** dataset for testing.

## Sequence to Run the Code

1.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Download and Prepare Dataset**

    ```bash
    python setup_dataset.py --count 700
    ```

    _(This downloads the Food-101 dataset and puts sample images into the `input_images` folder context)_

3.  **Run Parallel Processing (Option 1: Multiprocessing)**

    ```bash
    python main_multiprocessing.py --workers 4
    ```

    _(Results will be in `output_multiprocessing`)_

4.  **Run Parallel Processing (Option 2: Concurrent Futures)**

    ```bash
    python main_concurrent.py --workers 4
    ```

    _(Results will be in `output_concurrent`)_

5.  **Run Performance Analysis**
    ```bash
    python benchmark.py
    ```
    _(Runs both implementations with varying worker counts and outputs Speedup/Efficiency tables)_

## Components

- **`filters.py`**: Contains the logic for 5 filters using **OpenCV**:

  1.  `adjust_brightness`: Increases brightness/contrast by factor of 1.2
  2.  `gaussian_blur`: Applies 3x3 Gaussian kernel
  3.  `sharpen`: Applies sharpening kernel
  4.  `to_grayscale`: Converts BGR to Grayscale
  5.  `edge_detection`: Applies Sobel X and Y combined

- **`setup_dataset.py`**: Helper to manage the dataset.

  - Usage: `python setup_dataset.py --count <number>`
  - If current count < target: Downloads/copies more images.
  - If current count > target: Removes random images from directory to match target.

- **`main_multiprocessing.py`**: Uses `multiprocessing.Pool` (Processes) - True parallelism for CPU tasks.

- **`main_concurrent.py`**: Uses `concurrent.futures.ThreadPoolExecutor` (Threads) - Concurrency with threads (limited by GIL).

- **`benchmark.py`**: Driver script to calculate Speedup and Efficiency metrics across multiple core counts.

## Verification Results

### Dataset

- **Source**: Food-101 (downloaded via `kagglehub`)
- **Input Directory**: `input_images/`

### Execution

Both scripts run successfully with the dataset.

- **Output (Multiprocessing)**: `output_multiprocessing/`
- **Output (Threading)**: `output_concurrent/`

### How to Run Summary

1.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Setup Dataset**:

    ```bash
    # Add or remove images to reach exactly 100 (or desired number)
    python setup_dataset.py --count 100
    ```

3.  **Run Implementations**:
    ```bash
    python main_multiprocessing.py
    python main_concurrent.py
    ```
