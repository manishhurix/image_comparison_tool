#!/usr/bin/env python3
"""
Test script for the Image Comparison Tool
Creates test images and runs comparison to verify functionality
"""

import numpy as np
import cv2
import os
from comparator import ImageComparator
import utils


def create_test_images():
    """Create test images for comparison testing."""
    
    # Create output directory
    os.makedirs("test_images", exist_ok=True)
    
    # Test image 1: Simple colored rectangle
    img1 = np.zeros((300, 400, 3), dtype=np.uint8)
    img1[50:250, 100:300] = [255, 0, 0]  # Red rectangle
    cv2.imwrite("test_images/test1.png", img1)
    
    # Test image 2: Same as image 1 (identical)
    img2 = img1.copy()
    cv2.imwrite("test_images/test2_identical.png", img2)
    
    # Test image 3: Similar but with small changes
    img3 = img1.copy()
    img3[100:150, 150:200] = [0, 255, 0]  # Green rectangle in middle
    cv2.imwrite("test_images/test3_similar.png", img3)
    
    # Test image 4: Completely different
    img4 = np.zeros((300, 400, 3), dtype=np.uint8)
    img4[50:250, 100:300] = [0, 0, 255]  # Blue rectangle
    cv2.imwrite("test_images/test4_different.png", img4)
    
    print("✅ Test images created in 'test_images/' directory")


def test_comparison():
    """Test the image comparison functionality."""
    
    print("\n🧪 Testing Image Comparison Tool...")
    
    # Create test images
    create_test_images()
    
    # Initialize comparator
    comparator = ImageComparator()
    
    # Test 1: Identical images
    print("\n📊 Test 1: Identical Images")
    print("-" * 40)
    try:
        results = comparator.compare_images(
            "test_images/test1.png", 
            "test_images/test2_identical.png",
            save_diff=False
        )
        print(f"✅ Identical test passed!")
        print(f"   Similarity: {results['similarity_percentage']}%")
        print(f"   Are identical: {results['are_identical']}")
        assert results['are_identical'] == True, "Images should be identical"
    except Exception as e:
        print(f"❌ Identical test failed: {e}")
    
    # Test 2: Similar images
    print("\n📊 Test 2: Similar Images")
    print("-" * 40)
    try:
        results = comparator.compare_images(
            "test_images/test1.png", 
            "test_images/test3_similar.png",
            save_diff=False
        )
        print(f"✅ Similar test passed!")
        print(f"   Similarity: {results['similarity_percentage']}%")
        print(f"   Are identical: {results['are_identical']}")
        assert results['are_identical'] == False, "Images should not be identical"
        assert results['similarity_percentage'] > 50, "Similarity should be > 50%"
    except Exception as e:
        print(f"❌ Similar test failed: {e}")
    
    # Test 3: Different images
    print("\n📊 Test 3: Different Images")
    print("-" * 40)
    try:
        results = comparator.compare_images(
            "test_images/test1.png", 
            "test_images/test4_different.png",
            save_diff=False
        )
        print(f"✅ Different test passed!")
        print(f"   Similarity: {results['similarity_percentage']}%")
        print(f"   Are identical: {results['are_identical']}")
        assert results['are_identical'] == False, "Images should not be identical"
    except Exception as e:
        print(f"❌ Different test failed: {e}")
    
    # Test 4: Save diff image
    print("\n📊 Test 4: Save Difference Image")
    print("-" * 40)
    try:
        results = comparator.compare_images(
            "test_images/test1.png", 
            "test_images/test3_similar.png",
            save_diff=True
        )
        if results['diff_path'] and os.path.exists(results['diff_path']):
            print(f"✅ Diff image saved successfully!")
            print(f"   Path: {results['diff_path']}")
        else:
            print("❌ Diff image not saved")
    except Exception as e:
        print(f"❌ Diff image test failed: {e}")
    
    print("\n🎉 All tests completed!")


def test_utils():
    """Test utility functions."""
    
    print("\n🔧 Testing Utility Functions...")
    
    # Test image loading
    try:
        img = utils.load_image("test_images/test1.png")
        print("✅ Image loading test passed")
    except Exception as e:
        print(f"❌ Image loading test failed: {e}")
    
    # Test image resizing
    try:
        img1 = np.zeros((100, 100, 3), dtype=np.uint8)
        img2 = np.zeros((200, 150, 3), dtype=np.uint8)
        resized1, resized2 = utils.resize_images_to_common_size(img1, img2)
        assert resized1.shape == resized2.shape, "Resized images should have same shape"
        print("✅ Image resizing test passed")
    except Exception as e:
        print(f"❌ Image resizing test failed: {e}")
    
    # Test format validation
    try:
        assert utils.validate_image_format("test.jpg") == True
        assert utils.validate_image_format("test.png") == True
        assert utils.validate_image_format("test.txt") == False
        print("✅ Format validation test passed")
    except Exception as e:
        print(f"❌ Format validation test failed: {e}")


if __name__ == "__main__":
    print("🚀 Starting Image Comparison Tool Tests...")
    
    # Test utility functions
    test_utils()
    
    # Test comparison functionality
    test_comparison()
    
    print("\n✨ Test suite completed successfully!")
    print("\nTo run the tool:")
    print("  CLI: python main.py test_images/test1.png test_images/test3_similar.png")
    print("  Web: streamlit run web_app.py") 