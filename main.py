#!/usr/bin/env python3
"""
CivitAI Model Downloader
A modular tool for downloading AI models from CivitAI with organized file structure.

Usage:
    python main.py [URLs...]
    
Example:
    python main.py "https://civitai.com/models/12345" "https://civitai.com/models/67890?modelVersionId=12345"
"""

import sys
import logging
from pathlib import Path
from model_processor import ModelProcessor
from metadata_manager import MetadataManager
from utils import setup_logging, parse_model_url
from config import Config

def main():
    """Main entry point for the CivitAI downloader"""
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting CivitAI Model Downloader")
    
    # Check if API key is configured
    if not Config.API_KEY:
        logger.warning("No API key found. Some models may require authentication.")
        logger.info("Set CIVITAI_API_KEY environment variable for authenticated downloads.")
    
    # Get URLs from command line arguments or use default empty list
    urls = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not urls:
        logger.info("No URLs provided. Here are some usage examples:")
        print_usage_examples()
        return
    
    # Validate URLs
    valid_items = []
    for url in urls:
        model_id, version_id = parse_model_url(url)
        if model_id:
            valid_items.append(url)
            logger.info(f"Added to queue: Model {model_id}" + (f" (Version {version_id})" if version_id else ""))
        else:
            logger.warning(f"Invalid URL format: {url}")
    
    if not valid_items:
        logger.error("No valid URLs found. Exiting.")
        return
    
    # Create processor and process models
    processor = ModelProcessor()
    
    try:
        logger.info(f"Processing {len(valid_items)} models...")
        results = processor.process_multiple_models(valid_items)
        
        # Generate and display summary
        summary = processor.get_processing_summary(results)
        print_summary(summary)
        
        # Show detailed results
        print_detailed_results(results)
        
    except KeyboardInterrupt:
        logger.info("Download interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        processor.cleanup()
        logger.info("Download session completed")

def print_usage_examples():
    """Print usage examples and help information"""
    print("\n" + "="*60)
    print("CivitAI Model Downloader - Usage Examples")
    print("="*60)
    print("\n1. Download a specific model (latest version):")
    print("   python main.py 'https://civitai.com/models/123456'")
    print("\n2. Download a specific model version:")
    print("   python main.py 'https://civitai.com/models/123456?modelVersionId=789012'")
    print("\n3. Download multiple models:")
    print("   python main.py 'https://civitai.com/models/123456' 'https://civitai.com/models/789012'")
    print("\n4. Configuration:")
    print("   - Set CIVITAI_API_KEY environment variable for authenticated downloads")
    print("   - Modify config.py to change download directories and settings")
    print("\n5. File organization:")
    print("   Models are automatically organized by type and base model:")
    print("   - FLUX models: FLUX/FLUX.1-Dev/Checkpoint/")
    print("   - SDXL models: SDXL/Base/Checkpoint/")
    print("   - LoRA models: [BaseModel]/Lora/")
    print("   - And more...")
    print("\n" + "="*60)

def print_summary(summary):
    """Print processing summary"""
    print("\n" + "="*50)
    print("DOWNLOAD SUMMARY")
    print("="*50)
    print(f"Total processed: {summary['total_processed']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    
    if summary['successful_models']:
        print(f"\nSuccessfully downloaded:")
        for model_name in summary['successful_models']:
            print(f"  ✓ {model_name}")
    
    if summary['failed_items']:
        print(f"\nFailed downloads:")
        for item in summary['failed_items']:
            print(f"  ✗ Model {item['item']}: {item['error']}")

def print_detailed_results(results):
    """Print detailed results for each model"""
    print("\n" + "="*50)
    print("DETAILED RESULTS")
    print("="*50)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. ", end="")
        
        if result['success']:
            print(f"✓ {result['model_name']}")
            print(f"   Location: {result['target_directory']}")
            print(f"   Files: {', '.join(result['downloaded_files'].keys())}")
        else:
            print(f"✗ Model {result.get('model_id', 'Unknown')}")
            print(f"   Error: {result.get('error', 'Unknown error')}")

def interactive_mode():
    """Interactive mode for selecting and downloading models"""
    logger = setup_logging()
    processor = ModelProcessor()
    metadata_manager = MetadataManager()
    
    try:
        print("\n" + "="*50)
        print("CivitAI Model Downloader - Interactive Mode")
        print("="*50)
        
        while True:
            print("\nOptions:")
            print("1. Download model(s)")
            print("2. View existing downloads")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                urls = []
                print("\nEnter CivitAI URLs (one per line, empty line to finish):")
                while True:
                    url = input("URL: ").strip()
                    if not url:
                        break
                    urls.append(url)
                
                if urls:
                    results = processor.process_multiple_models(urls)
                    summary = processor.get_processing_summary(results)
                    print_summary(summary)
                else:
                    print("No URLs entered.")
            
            elif choice == '2':
                metadata_files = metadata_manager.find_existing_downloads(Config.BASE_MODEL_DIR)
                if metadata_files:
                    print(f"\nFound {len(metadata_files)} existing downloads:")
                    for metadata_file in metadata_files[:10]:  # Show first 10
                        summary = metadata_manager.get_download_summary(metadata_file)
                        if summary:
                            print(f"  • {summary['model_name']} ({summary['model_type']}) - {summary['downloaded_at']}")
                    if len(metadata_files) > 10:
                        print(f"  ... and {len(metadata_files) - 10} more")
                else:
                    print("\nNo existing downloads found.")
            
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        processor.cleanup()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, show interactive mode
        interactive_mode()
    else:
        # URLs provided as arguments
        main()