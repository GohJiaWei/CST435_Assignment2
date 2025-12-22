import cv2
import numpy as np

def load_image(path):
    # cv2.imread returns BGR or None if failed
    return cv2.imread(path)

def save_image(image, path):
    cv2.imwrite(path, image)

def to_grayscale(image):
    """
    Convert BGR image to grayscale.
    """
    if len(image.shape) == 2:
        return image # Already grayscale
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gaussian_blur(image):
    """
    Apply 3x3 Gaussian kernel for smoothing.
    """
    return cv2.GaussianBlur(image, (3, 3), 0)

def edge_detection(image):
    """
    Apply Sobel filter to detect edges.
    """
    # Convert to grayscale if not already
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    # Scale=1, Delta=0, DDepth=CV_64F usually to avoid overflow, then converting back
    # But for simple visualization, CV_8U is okay or we handle absolute.
    # Assignment says "Sobel filter", implies directionality or magnitude.
    # Standard approach: Sobel X + Sobel Y magnitude.
    
    grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3)
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    
    # Combine
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
            
        # 1. Brightness Adjustment
        img = adjust_brightness(img, factor=1.2)
        
        # 2. Gaussian Blur
        img = gaussian_blur(img)
        
        # 3. Image Sharpening
        img = sharpen(img)
        
        # 4. Grayscale Conversion
        img = to_grayscale(img)
        
        # 5. Edge Detection
        img = edge_detection(img)
        
        save_image(img, output_path)
        
        return output_path
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None
