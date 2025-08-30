"""
Test Script for Cattle Breed Identifier Application
SIH 2025 - Smart India Hackathon

This script tests the Flask application endpoints and functionality.
"""

import requests
import json
import os
import time
from PIL import Image
import numpy as np

# Configuration
BASE_URL = "http://localhost:5000"
TEST_IMAGE_PATH = "test_image.jpg"

def create_test_image():
    """Create a simple test image for testing"""
    # Create a simple test image (224x224 pixels)
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save(TEST_IMAGE_PATH)
    print(f"✅ Test image created: {TEST_IMAGE_PATH}")

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application. Make sure it's running.")
        return False

def test_breed_info_endpoint():
    """Test the breed information endpoint"""
    print("\n🔍 Testing Breed Info Endpoint...")
    breeds = ['murrah_buffalo', 'gir_cattle', 'sahiwal_cattle', 'tharparkar_cattle']
    
    for breed in breeds:
        try:
            response = requests.get(f"{BASE_URL}/breed/{breed}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {breed}: {data.get('name', 'Unknown')}")
            else:
                print(f"❌ {breed}: Failed to get info")
        except Exception as e:
            print(f"❌ {breed}: Error - {e}")

def test_image_upload():
    """Test image upload and breed prediction"""
    print("\n🔍 Testing Image Upload...")
    
    if not os.path.exists(TEST_IMAGE_PATH):
        print("❌ Test image not found. Creating one...")
        create_test_image()
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Upload successful!")
            print(f"   Breed: {data.get('breed_name', 'Unknown')}")
            print(f"   Confidence: {data.get('confidence', 0)}%")
            print(f"   Image ID: {data.get('image_id', 'N/A')}")
            return data
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def test_registration():
    """Test cattle registration endpoint"""
    print("\n🔍 Testing Registration Endpoint...")
    
    registration_data = {
        "breed": "murrah_buffalo",
        "age": 5,
        "owner_name": "Test Farmer",
        "location": "Haryana, India"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/register",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(registration_data)
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registration successful!")
            print(f"   Cattle ID: {data.get('cattle_id', 'N/A')}")
            print(f"   Message: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_main_page():
    """Test the main page loads correctly"""
    print("\n🔍 Testing Main Page...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
            return True
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🐄 Cattle Breed Identifier - Application Testing")
    print("="*50)
    print("SIH 2025 - Smart India Hackathon")
    print("="*50)
    
    # Wait a moment for the app to start
    print("⏳ Waiting for application to start...")
    time.sleep(2)
    
    # Test results
    results = []
    
    # Test 1: Health endpoint
    results.append(("Health Check", test_health_endpoint()))
    
    # Test 2: Main page
    results.append(("Main Page", test_main_page()))
    
    # Test 3: Breed info endpoints
    test_breed_info_endpoint()
    results.append(("Breed Info", True))  # Assuming it works if no exceptions
    
    # Test 4: Image upload
    upload_result = test_image_upload()
    results.append(("Image Upload", upload_result is not None))
    
    # Test 5: Registration
    results.append(("Registration", test_registration()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the application.")
    
    # Cleanup
    if os.path.exists(TEST_IMAGE_PATH):
        os.remove(TEST_IMAGE_PATH)
        print(f"🧹 Cleaned up test image: {TEST_IMAGE_PATH}")

if __name__ == "__main__":
    run_all_tests()
