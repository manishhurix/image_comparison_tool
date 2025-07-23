#!/usr/bin/env python3
"""
Image Comparison Tool - Web Interface

Run with: streamlit run web_app.py
"""

import streamlit as st
import numpy as np
import cv2
import os
import tempfile
from PIL import Image
import io
import base64
from comparator import ImageComparator
import utils


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
                comparator = ImageComparator()
                results = comparator.compare_images(temp_path1, temp_path2, save_diff=False)
            
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
            side_by_side = utils.create_side_by_side_comparison(
                np.array(image1), np.array(image2)
            )
            st.image(side_by_side, caption="Original Images (Resized to Common Size)", use_column_width=True)
            
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
                    diff_bytes = cv2.imencode('.png', cv2.cvtColor(diff_image, cv2.COLOR_RGB2BGR))[1].tobytes()
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
        <p>Built with ❤️ using Streamlit, OpenCV, and scikit-image</p>
        <p>For CLI usage: <code>python main.py image1.jpg image2.jpg</code></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main() 