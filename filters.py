import cv2
import numpy as np

def load_image(path):
    # cv2.imread returns BGR or None if failed
    return cv2.imread(path)

def save_image(image, path):
    cv2.imwrite(path, image)

def to_grayscale(image):
    """
    Convert BGR image to grayscale using luminance formula:
    Y = 0.299*R + 0.587*G + 0.114*B
    OpenCV uses BGR order.
    """
    if len(image.shape) == 2:
        return image # Already grayscale
        
    # Manual implementation using numpy
    # BGR weights: B=0.114, G=0.587, R=0.299
    # We use dot product to apply weights to the last axis (channels)
    grayscale = np.dot(image[..., :3], [0.114, 0.587, 0.299])
    return grayscale.astype(np.uint8)

def gaussian_blur(image):
    """
    Apply 3x3 Gaussian kernel for smoothing manually.
    Kernel approximation:
    1 2 1
    2 4 2
    1 2 1
    (Divided by 16)
    """
    kernel = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ], dtype=np.float32) / 16.0
    
    return cv2.filter2D(image, -1, kernel)

def edge_detection(image):
    """
    Apply Sobel filter to detect edges manually.
    Input image is expected to be grayscale (from pipeline).
    """
    # Manual Sobel Kernels
    # Sobel X
    kx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)
    
    # Sobel Y
    ky = np.array([
        [-1, -2, -1],
         [0,  0,  0],
         [1,  2, 1]
    ], dtype=np.float32)
    
    # Apply filters
    # Use float32 to avoid overflow during calculation
    grad_x = cv2.filter2D(image, cv2.CV_32F, kx)
    grad_y = cv2.filter2D(image, cv2.CV_32F, ky)
    
    # Calculate magnitude
    # Standard: sqrt(x^2 + y^2)
    # Approx for speed: |x| + |y|
    
    # Let's use the magnitude function for better accuracy or simple abs add
    # Using absolute sum to stay consistent with previous look/feel if desired, 
    # but strictly "Sobel" often implies magnitude. 
    # Previous implementation was: addWeighted(abs(x), 0.5, abs(y), 0.5)
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    
    return cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

def sharpen(image):
    """
    Enhance edges and details.
    """
    # Kernel:
    # [ 0, -1,  0]
    # [-1,  5, -1]
    # [ 0, -1,  0]
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    return cv2.filter2D(image, -1, kernel)

def adjust_brightness(image, factor=1.2):
    """
    Increase or decrease image brightness.
    Wrapper for convertScaleAbs which performs strictly linear transformation.
    dst = alpha * src + beta
    We use alpha=factor for scaling pixel values (simulating brightness/contrast adjustment).
    """
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def process_pipeline(image_path, output_path):
    """
    Apply the full pipeline of filters to a single image.
    Pipeline: Brightness -> Gaussian Blur -> Sharpen -> Grayscale -> Edge Detection
    """
    try:
        img = load_image(image_path)
        if img is None:
            print(f"Failed to load image: {image_path}")
            return None
        
        # 1. Grayscale Conversion
        img = to_grayscale(img)

        # 2. Gaussian Blur
        img = gaussian_blur(img)
        
        # 3. Edge Detection
        img = edge_detection(img)

        # 4. Image Sharpening
        img = sharpen(img)

        # 5. Brightness Adjustment
        img = adjust_brightness(img, factor=1.2)
        
        save_image(img, output_path)
        
        return output_path
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None
