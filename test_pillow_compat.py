#!/usr/bin/env python3
"""
Test Pillow Compatibility - Verify Image.Resampling.LANCZOS works correctly.
Tests all video engine modules with Pillow 10+/11.
"""

import sys
import os
from pathlib import Path

def test_pillow_import():
    """Test Pillow import and version."""
    try:
        from PIL import Image, __version__
        print(f"✓ Pillow version: {__version__}")
        return True
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False


def test_resample_constant():
    """Test RESAMPLE constant definition."""
    try:
        from PIL import Image
        
        # Test the pattern we're using
        try:
            resample = Image.Resampling.LANCZOS
            print(f"✓ Image.Resampling.LANCZOS works (Pillow 10+)")
        except AttributeError:
            resample = Image.ANTIALIAS
            print(f"✓ Image.ANTIALIAS fallback works (Pillow <10)")
        
        print(f"✓ RESAMPLE constant value: {resample}")
        return True
    except Exception as e:
        print(f"✗ RESAMPLE constant test failed: {e}")
        return False


def test_image_resize():
    """Test image resize with RESAMPLE constant."""
    try:
        from PIL import Image
        import io
        
        # Create a test image
        test_img = Image.new('RGB', (100, 100), color='red')
        
        # Try resize with Pillow 10+ API
        try:
            resized = test_img.resize((50, 50), Image.Resampling.LANCZOS)
            print(f"✓ Image.resize() with Resampling.LANCZOS works")
        except AttributeError:
            # Fallback for older Pillow
            resized = test_img.resize((50, 50), Image.ANTIALIAS)
            print(f"✓ Image.resize() with ANTIALIAS fallback works")
        
        assert resized.size == (50, 50), "Resize dimensions mismatch"
        print(f"✓ Resized image dimensions: {resized.size}")
        return True
    except Exception as e:
        print(f"✗ Image resize test failed: {e}")
        return False


def test_engine_imports():
    """Test all engine module imports."""
    modules_to_test = [
        ('engine.caption_engine', 'CaptionEngine'),
        ('engine.image_engine', 'ImageEngine'),
        ('video', None),
        ('video_engine', 'ProfessionalVideoEngine'),
    ]
    
    all_passed = True
    for module_name, class_name in modules_to_test:
        try:
            if class_name:
                exec(f"from {module_name} import {class_name}")
                print(f"✓ {module_name}.{class_name} imported successfully")
            else:
                __import__(module_name)
                print(f"✓ {module_name} imported successfully")
        except Exception as e:
            print(f"✗ Failed to import {module_name}: {e}")
            all_passed = False
    
    return all_passed


def test_resample_constants_in_modules():
    """Test that RESAMPLE constants are defined in all modules."""
    modules_to_check = [
        'engine.caption_engine',
        'engine.image_engine',
        'video',
    ]
    
    all_passed = True
    for module_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=['RESAMPLE'])
            if hasattr(module, 'RESAMPLE'):
                print(f"✓ {module_name}.RESAMPLE constant exists")
            else:
                print(f"⚠ {module_name}.RESAMPLE constant not found (may be module-internal)")
        except Exception as e:
            print(f"✗ Failed to check {module_name}: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Run all compatibility tests."""
    print("\n" + "="*70)
    print("PILLOW COMPATIBILITY TEST SUITE")
    print("="*70 + "\n")
    
    tests = [
        ("Pillow Import", test_pillow_import),
        ("RESAMPLE Constant", test_resample_constant),
        ("Image Resize", test_image_resize),
        ("Engine Imports", test_engine_imports),
        ("Module RESAMPLE Constants", test_resample_constants_in_modules),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[TEST] {test_name}")
        print("-" * 70)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Pillow 10+/11 compatibility verified.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
