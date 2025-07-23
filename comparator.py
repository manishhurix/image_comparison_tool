import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from typing import Tuple, Dict, Any
import utils


class ImageComparator:
    """
    A class for comparing two images using structural similarity.
    """
    
    def __init__(self):
        self.results = {}
    
    def compare_images(self, image1_path: str, image2_path: str, save_diff: bool = True) -> Dict[str, Any]:
        """
        Compare two images and return detailed results.
        
        Args:
            image1_path (str): Path to the first image
            image2_path (str): Path to the second image
            save_diff (bool): Whether to save the difference image
            
        Returns:
            Dict[str, Any]: Comparison results including similarity score, difference percentage, etc.
        """
        try:
            # Load images
            image1 = utils.load_image(image1_path)
            image2 = utils.load_image(image2_path)
            
            # Validate image formats
            if not utils.validate_image_format(image1_path):
                raise ValueError(f"Unsupported image format for: {image1_path}")
            if not utils.validate_image_format(image2_path):
                raise ValueError(f"Unsupported image format for: {image2_path}")
            
            # Resize images to common size
            resized_image1, resized_image2 = utils.resize_images_to_common_size(image1, image2)
            
            # Convert to grayscale for SSIM comparison
            gray_image1 = utils.convert_to_grayscale(resized_image1)
            gray_image2 = utils.convert_to_grayscale(resized_image2)
            
            # Calculate structural similarity
            similarity_score, diff_image = ssim(gray_image1, gray_image2, full=True)
            
            # Convert similarity score to percentage
            similarity_percentage = similarity_score * 100
            difference_percentage = 100 - similarity_percentage
            
            # Determine if images are exactly the same
            are_identical = np.array_equal(gray_image1, gray_image2)
            
            # Create visual diff image
            diff_image_visual = self._create_visual_diff_image(resized_image1, resized_image2, diff_image)
            
            # Save diff image if requested
            diff_path = None
            if save_diff:
                diff_path = utils.save_diff_image(diff_image_visual)
            
            # Store results
            self.results = {
                'are_identical': are_identical,
                'similarity_score': similarity_score,
                'similarity_percentage': round(similarity_percentage, 2),
                'difference_percentage': round(difference_percentage, 2),
                'diff_image': diff_image_visual,
                'diff_path': diff_path,
                'original_shapes': {
                    'image1': image1.shape,
                    'image2': image2.shape
                },
                'resized_shapes': {
                    'image1': resized_image1.shape,
                    'image2': resized_image2.shape
                }
            }
            
            return self.results
            
        except Exception as e:
            raise Exception(f"Error comparing images: {str(e)}")
    
    def _create_visual_diff_image(self, image1: np.ndarray, image2: np.ndarray, diff_image: np.ndarray) -> np.ndarray:
        """
        Create a visual difference image highlighting changes between two images.
        
        Args:
            image1 (np.ndarray): First image
            image2 (np.ndarray): Second image
            diff_image (np.ndarray): SSIM difference image
            
        Returns:
            np.ndarray: Visual difference image with highlighted changes
        """
        # Convert diff image to proper format for visualization
        diff_image = (diff_image * 255).astype(np.uint8)
        
        # Create a color-coded difference image
        diff_colored = np.zeros((*diff_image.shape, 3), dtype=np.uint8)
        
        # Red channel for differences (higher values = more different)
        diff_colored[:, :, 0] = diff_image  # Red channel
        diff_colored[:, :, 1] = 0  # Green channel
        diff_colored[:, :, 2] = 0  # Blue channel
        
        # Blend with original image for better visualization
        alpha = 0.7
        blended = cv2.addWeighted(image1, 1 - alpha, diff_colored, alpha, 0)
        
        return blended
    
    def get_summary(self) -> str:
        """
        Get a formatted summary of the comparison results.
        
        Returns:
            str: Formatted summary string
        """
        if not self.results:
            return "No comparison results available. Run compare_images() first."
        
        summary = f"""
Image Comparison Results:
========================
Are images identical: {self.results['are_identical']}
Similarity score: {self.results['similarity_percentage']}%
Difference percentage: {self.results['difference_percentage']}%

Original image shapes:
- Image 1: {self.results['original_shapes']['image1']}
- Image 2: {self.results['original_shapes']['image2']}

Resized to common shape: {self.results['resized_shapes']['image1']}
"""
        
        if self.results['diff_path']:
            summary += f"Difference image saved to: {self.results['diff_path']}\n"
        
        return summary
    
    def compare_multiple_pairs(self, image_pairs: list) -> list:
        """
        Compare multiple pairs of images (batch mode).
        
        Args:
            image_pairs (list): List of tuples containing (image1_path, image2_path)
            
        Returns:
            list: List of comparison results for each pair
        """
        results = []
        
        for i, (img1_path, img2_path) in enumerate(image_pairs):
            try:
                print(f"Comparing pair {i+1}/{len(image_pairs)}: {img1_path} vs {img2_path}")
                result = self.compare_images(img1_path, img2_path, save_diff=False)
                result['pair_index'] = i + 1
                result['image1_path'] = img1_path
                result['image2_path'] = img2_path
                results.append(result)
            except Exception as e:
                print(f"Error comparing pair {i+1}: {str(e)}")
                results.append({
                    'error': str(e),
                    'pair_index': i + 1,
                    'image1_path': img1_path,
                    'image2_path': img2_path
                })
        
        return results 