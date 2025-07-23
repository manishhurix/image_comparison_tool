#!/usr/bin/env python3
"""
Image Comparison Tool - CLI Interface

Usage:
    python main.py image1.jpg image2.jpg [--save-diff]
    python main.py --batch folder1 folder2
"""

import argparse
import os
import sys
from comparator import ImageComparator
import utils


def main():
    parser = argparse.ArgumentParser(
        description="Compare two images using structural similarity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py image1.jpg image2.jpg
  python main.py image1.jpg image2.jpg --save-diff
  python main.py --batch folder1 folder2
        """
    )
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Comparison mode')
    
    # Single comparison mode
    single_parser = subparsers.add_parser('single', help='Compare two individual images')
    single_parser.add_argument('image1', help='Path to first image')
    single_parser.add_argument('image2', help='Path to second image')
    single_parser.add_argument('--save-diff', action='store_true', 
                              help='Save visual difference image')
    single_parser.add_argument('--output', '-o', default='diff_output/diff.png',
                              help='Output path for difference image')
    
    # Batch comparison mode
    batch_parser = subparsers.add_parser('batch', help='Compare multiple image pairs')
    batch_parser.add_argument('folder1', help='Folder containing first set of images')
    batch_parser.add_argument('folder2', help='Folder containing second set of images')
    batch_parser.add_argument('--output-dir', default='diff_output',
                             help='Output directory for difference images')
    
    # Legacy mode (for backward compatibility)
    parser.add_argument('--legacy-image1', help='Path to first image (legacy mode)')
    parser.add_argument('--legacy-image2', help='Path to second image (legacy mode)')
    parser.add_argument('--save-diff', action='store_true', 
                       help='Save visual difference image')
    
    args = parser.parse_args()
    
    # Handle legacy mode
    if args.legacy_image1 and args.legacy_image2:
        compare_single_images(args.legacy_image1, args.legacy_image2, args.save_diff)
        return
    
    # Handle different modes
    if args.mode == 'single':
        compare_single_images(args.image1, args.image2, args.save_diff, args.output)
    elif args.mode == 'batch':
        compare_batch_images(args.folder1, args.folder2, args.output_dir)
    else:
        # Default to single mode if no mode specified but two arguments provided
        if len(sys.argv) >= 3 and not any(arg.startswith('--') for arg in sys.argv[1:3]):
            image1 = sys.argv[1]
            image2 = sys.argv[2]
            save_diff = '--save-diff' in sys.argv
            compare_single_images(image1, image2, save_diff)
        else:
            parser.print_help()
            sys.exit(1)


def compare_single_images(image1_path: str, image2_path: str, save_diff: bool = True, output_path: str = None):
    """
    Compare two individual images and display results.
    
    Args:
        image1_path (str): Path to first image
        image2_path (str): Path to second image
        save_diff (bool): Whether to save difference image
        output_path (str): Custom output path for difference image
    """
    try:
        print(f"Comparing images:")
        print(f"  Image 1: {image1_path}")
        print(f"  Image 2: {image2_path}")
        print("-" * 50)
        
        # Validate input files
        if not os.path.exists(image1_path):
            print(f"Error: Image file not found: {image1_path}")
            sys.exit(1)
        
        if not os.path.exists(image2_path):
            print(f"Error: Image file not found: {image2_path}")
            sys.exit(1)
        
        # Perform comparison
        comparator = ImageComparator()
        results = comparator.compare_images(image1_path, image2_path, save_diff)
        
        # Display results
        print(comparator.get_summary())
        
        # Save diff image with custom path if specified
        if save_diff and output_path and output_path != 'diff_output/diff.png':
            utils.save_diff_image(results['diff_image'], output_path)
            print(f"Difference image saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def compare_batch_images(folder1: str, folder2: str, output_dir: str):
    """
    Compare multiple image pairs from two folders.
    
    Args:
        folder1 (str): Path to first folder
        folder2 (str): Path to second folder
        output_dir (str): Output directory for difference images
    """
    try:
        print(f"Batch comparison mode:")
        print(f"  Folder 1: {folder1}")
        print(f"  Folder 2: {folder2}")
        print(f"  Output directory: {output_dir}")
        print("-" * 50)
        
        # Validate folders
        if not os.path.exists(folder1):
            print(f"Error: Folder not found: {folder1}")
            sys.exit(1)
        
        if not os.path.exists(folder2):
            print(f"Error: Folder not found: {folder2}")
            sys.exit(1)
        
        # Get image files from both folders
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        def get_image_files(folder):
            files = []
            for file in os.listdir(folder):
                if os.path.splitext(file.lower())[1] in supported_formats:
                    files.append(os.path.join(folder, file))
            return sorted(files)
        
        images1 = get_image_files(folder1)
        images2 = get_image_files(folder2)
        
        if not images1:
            print(f"Error: No supported image files found in {folder1}")
            sys.exit(1)
        
        if not images2:
            print(f"Error: No supported image files found in {folder2}")
            sys.exit(1)
        
        # Create image pairs
        image_pairs = []
        min_count = min(len(images1), len(images2))
        
        for i in range(min_count):
            image_pairs.append((images1[i], images2[i]))
        
        print(f"Found {len(image_pairs)} image pairs to compare")
        
        # Perform batch comparison
        comparator = ImageComparator()
        results = comparator.compare_multiple_pairs(image_pairs)
        
        # Display summary
        print("\nBatch Comparison Summary:")
        print("=" * 50)
        
        total_pairs = len(results)
        successful_comparisons = sum(1 for r in results if 'error' not in r)
        
        print(f"Total pairs processed: {total_pairs}")
        print(f"Successful comparisons: {successful_comparisons}")
        print(f"Failed comparisons: {total_pairs - successful_comparisons}")
        
        if successful_comparisons > 0:
            avg_similarity = sum(r['similarity_percentage'] for r in results if 'error' not in r) / successful_comparisons
            print(f"Average similarity: {avg_similarity:.2f}%")
        
        # Save individual diff images
        os.makedirs(output_dir, exist_ok=True)
        for i, result in enumerate(results):
            if 'error' not in result and 'diff_image' in result:
                diff_filename = f"diff_pair_{i+1}.png"
                diff_path = os.path.join(output_dir, diff_filename)
                utils.save_diff_image(result['diff_image'], diff_path)
                print(f"Saved diff for pair {i+1}: {diff_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 