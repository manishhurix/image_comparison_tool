import cv2
import numpy as np
from PIL import Image
import os
from typing import Tuple, Optional


def load_image(image_path: str) -> np.ndarray:
    """
    Load an image from file path and convert to RGB format.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        np.ndarray: Loaded image in RGB format
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image cannot be loaded
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Load image using OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot load image: {image_path}")
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb


def resize_images_to_common_size(image1: np.ndarray, image2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Resize two images to the smallest common dimensions.
    
    Args:
        image1 (np.ndarray): First image
        image2 (np.ndarray): Second image
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Resized images
    """
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]
    
    # Find smallest common dimensions
    min_height = min(h1, h2)
    min_width = min(w1, w2)
    
    # Resize images to common size
    resized_image1 = cv2.resize(image1, (min_width, min_height))
    resized_image2 = cv2.resize(image2, (min_width, min_height))
    
    return resized_image1, resized_image2


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert RGB image to grayscale.
    
    Args:
        image (np.ndarray): RGB image
        
    Returns:
        np.ndarray: Grayscale image
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image


def save_diff_image(diff_image: np.ndarray, output_path: str = "diff_output/diff.png") -> str:
    """
    Save the difference image to file.
    
    Args:
        diff_image (np.ndarray): Difference image to save
        output_path (str): Path where to save the image
        
    Returns:
        str: Path where image was saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert to BGR for OpenCV saving
    if len(diff_image.shape) == 3:
        diff_bgr = cv2.cvtColor(diff_image, cv2.COLOR_RGB2BGR)
    else:
        diff_bgr = cv2.cvtColor(diff_image, cv2.COLOR_GRAY2BGR)
    
    # Save the image
    cv2.imwrite(output_path, diff_bgr)
    return output_path


def create_side_by_side_comparison(image1: np.ndarray, image2: np.ndarray) -> np.ndarray:
    """
    Create a side-by-side comparison of two images.
    
    Args:
        image1 (np.ndarray): First image
        image2 (np.ndarray): Second image
        
    Returns:
        np.ndarray: Combined image showing both images side by side
    """
    # Ensure both images have the same dimensions
    img1_resized, img2_resized = resize_images_to_common_size(image1, image2)
    
    # Create side-by-side comparison
    combined = np.hstack([img1_resized, img2_resized])
    return combined


def validate_image_format(image_path: str) -> bool:
    """
    Validate if the file is a supported image format.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if valid image format, False otherwise
    """
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    file_ext = os.path.splitext(image_path.lower())[1]
    return file_ext in supported_formats 