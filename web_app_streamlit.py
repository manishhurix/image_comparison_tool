#!/usr/bin/env python3
"""
Image Comparison Tool - Web Interface (Streamlit Cloud Compatible)

Run with: streamlit run web_app_streamlit.py
"""

import streamlit as st
import numpy as np
import os
import tempfile
from PIL import Image, ImageChops, ImageEnhance
import io
import base64
from skimage.metrics import structural_similarity as ssim
from skimage import img_as_float
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def load_image_pil(image_path: str) -> np.ndarray:
    """
    Load an image using PIL and convert to numpy array.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        np.ndarray: Loaded image as RGB numpy array
    """
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return np.array(img)


def resize_images_to_common_size_pil(image1: np.ndarray, image2: np.ndarray) -> tuple:
    """
    Resize two images to the smallest common dimensions using PIL.
    
    Args:
        image1 (np.ndarray): First image
        image2 (np.ndarray): Second image
        
    Returns:
        tuple: Resized images
    """
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]
    
    # Find smallest common dimensions
    min_height = min(h1, h2)
    min_width = min(w1, w2)
    
    # Convert numpy arrays to PIL Images
    pil_img1 = Image.fromarray(image1)
    pil_img2 = Image.fromarray(image2)
    
    # Resize images
    resized_img1 = pil_img1.resize((min_width, min_height), Image.Resampling.LANCZOS)
    resized_img2 = pil_img2.resize((min_width, min_height), Image.Resampling.LANCZOS)
    
    # Convert back to numpy arrays
    return np.array(resized_img1), np.array(resized_img2)


def create_visual_diff_image_pil(image1: np.ndarray, image2: np.ndarray, diff_image: np.ndarray) -> np.ndarray:
    """
    Create a visual difference image highlighting changes between two images using PIL.
    
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
    blended = (image1 * (1 - alpha) + diff_colored * alpha).astype(np.uint8)
    
    return blended


def compare_images_streamlit(image1_path: str, image2_path: str) -> dict:
    """
    Compare two images using structural similarity (Streamlit Cloud compatible).
    
    Args:
        image1_path (str): Path to first image
        image2_path (str): Path to second image
        
    Returns:
        dict: Comparison results
    """
    try:
        # Load images using PIL
        image1 = load_image_pil(image1_path)
        image2 = load_image_pil(image2_path)
        
        # Resize images to common size
        resized_image1, resized_image2 = resize_images_to_common_size_pil(image1, image2)
        
        # Convert to grayscale for SSIM comparison
        gray_image1 = rgb2gray(img_as_float(resized_image1))
        gray_image2 = rgb2gray(img_as_float(resized_image2))
        
        # Calculate structural similarity
        similarity_score, diff_image = ssim(gray_image1, gray_image2, full=True)
        
        # Convert similarity score to percentage
        similarity_percentage = similarity_score * 100
        difference_percentage = 100 - similarity_percentage
        
        # Determine if images are exactly the same
        are_identical = np.array_equal(gray_image1, gray_image2)
        
        # Create visual diff image
        diff_image_visual = create_visual_diff_image_pil(resized_image1, resized_image2, diff_image)
        
        # Create side-by-side comparison
        side_by_side = np.hstack([resized_image1, resized_image2])
        
        return {
            'are_identical': are_identical,
            'similarity_score': similarity_score,
            'similarity_percentage': round(similarity_percentage, 2),
            'difference_percentage': round(difference_percentage, 2),
            'diff_image': diff_image_visual,
            'side_by_side': side_by_side,
            'original_shapes': {
                'image1': image1.shape,
                'image2': image2.shape
            },
            'resized_shapes': {
                'image1': resized_image1.shape,
                'image2': resized_image2.shape
            }
        }
        
    except Exception as e:
        raise Exception(f"Error comparing images: {str(e)}")


def save_image_to_bytes(image_array: np.ndarray) -> bytes:
    """
    Convert numpy array to bytes for download.
    
    Args:
        image_array (np.ndarray): Image as numpy array
        
    Returns:
        bytes: Image as bytes
    """
    pil_image = Image.fromarray(image_array)
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()


def main():
    st.set_page_config(
        page_title="Image Comparison Tool",
        page_icon="🖼️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .similarity-high { color: #28a745; }
    .similarity-medium { color: #ffc107; }
    .similarity-low { color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🖼️ Image Comparison Tool</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. Upload two images to compare
        2. Images will be automatically resized to match dimensions
        3. View similarity score and difference percentage
        4. Download the visual difference image
        """)
        
        st.header("⚙️ Settings")
        save_diff = st.checkbox("Save difference image", value=True)
        
        st.header("ℹ️ About")
        st.markdown("""
        This tool uses **Structural Similarity Index (SSIM)** 
        to compare images and highlight differences.
        
        **Supported formats:** JPG, PNG, BMP, TIFF
        """)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Upload First Image")
        uploaded_file1 = st.file_uploader(
            "Choose first image file",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif'],
            key="image1"
        )
        
        if uploaded_file1 is not None:
            # Display first image
            image1 = Image.open(uploaded_file1)
            st.image(image1, caption="First Image", use_column_width=True)
            
            # Show image info
            st.info(f"**Image 1 Info:** {image1.size[0]}x{image1.size[1]} pixels, {image1.mode} mode")
    
    with col2:
        st.subheader("📸 Upload Second Image")
        uploaded_file2 = st.file_uploader(
            "Choose second image file",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif'],
            key="image2"
        )
        
        if uploaded_file2 is not None:
            # Display second image
            image2 = Image.open(uploaded_file2)
            st.image(image2, caption="Second Image", use_column_width=True)
            
            # Show image info
            st.info(f"**Image 2 Info:** {image2.size[0]}x{image2.size[1]} pixels, {image2.mode} mode")
    
    # Comparison section
    if uploaded_file1 is not None and uploaded_file2 is not None:
        st.markdown("---")
        st.subheader("🔍 Comparison Results")
        
        # Create temporary files for comparison
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file1:
            image1.save(tmp_file1.name)
            temp_path1 = tmp_file1.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file2:
            image2.save(tmp_file2.name)
            temp_path2 = tmp_file2.name
        
        try:
            # Perform comparison
            with st.spinner("Comparing images..."):
                results = compare_images_streamlit(temp_path1, temp_path2)
            
            # Display results in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="Are Images Identical?",
                    value="✅ Yes" if results['are_identical'] else "❌ No"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                similarity = results['similarity_percentage']
                if similarity >= 80:
                    css_class = "similarity-high"
                elif similarity >= 50:
                    css_class = "similarity-medium"
                else:
                    css_class = "similarity-low"
                
                st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="Similarity Score",
                    value=f"{similarity}%",
                    delta=None
                )
                st.markdown(f'<p class="{css_class}">{"High" if similarity >= 80 else "Medium" if similarity >= 50 else "Low"} similarity</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="Difference Percentage",
                    value=f"{results['difference_percentage']}%"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="Resized Dimensions",
                    value=f"{results['resized_shapes']['image1'][1]}x{results['resized_shapes']['image1'][0]}"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Side-by-side comparison
            st.subheader("🔄 Side-by-Side Comparison")
            st.image(results['side_by_side'], caption="Original Images (Resized to Common Size)", use_column_width=True)
            
            # Visual difference image
            st.subheader("🔍 Visual Difference")
            diff_image = results['diff_image']
            st.image(diff_image, caption="Highlighted Differences (Red areas show changes)", use_column_width=True)
            
            # Download section
            st.subheader("💾 Download Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download difference image
                if save_diff:
                    diff_bytes = save_image_to_bytes(results['diff_image'])
                    st.download_button(
                        label="📥 Download Difference Image",
                        data=diff_bytes,
                        file_name="image_difference.png",
                        mime="image/png"
                    )
            
            with col2:
                # Download comparison report
                report = f"""
Image Comparison Report
======================

Are images identical: {results['are_identical']}
Similarity score: {results['similarity_percentage']}%
Difference percentage: {results['difference_percentage']}%

Original image shapes:
- Image 1: {results['original_shapes']['image1']}
- Image 2: {results['original_shapes']['image2']}

Resized to common shape: {results['resized_shapes']['image1']}

Analysis:
- {'Images are exactly the same' if results['are_identical'] else 'Images have differences'}
- {'High similarity' if results['similarity_percentage'] >= 80 else 'Medium similarity' if results['similarity_percentage'] >= 50 else 'Low similarity'}
- {results['difference_percentage']}% of pixels show differences
                """
                
                st.download_button(
                    label="📄 Download Report",
                    data=report,
                    file_name="comparison_report.txt",
                    mime="text/plain"
                )
            
            # Detailed information
            with st.expander("📊 Detailed Information"):
                st.json({
                    "Original Shapes": results['original_shapes'],
                    "Resized Shapes": results['resized_shapes'],
                    "Similarity Score (Raw)": results['similarity_score'],
                    "Are Identical": results['are_identical']
                })
        
        except Exception as e:
            st.error(f"Error during comparison: {str(e)}")
        
        finally:
            # Clean up temporary files
            try:
                os.unlink(temp_path1)
                os.unlink(temp_path2)
            except:
                pass
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit, PIL, and scikit-image</p>
        <p>For CLI usage: <code>python main.py image1.jpg image2.jpg</code></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main() 