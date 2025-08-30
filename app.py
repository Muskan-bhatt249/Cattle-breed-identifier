from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import json
import base64
import io
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Cattle breed database with detailed information
CATTLE_BREEDS = {
    'murrah_buffalo': {
        'name': 'Murrah Buffalo',
        'scientific_name': 'Bubalus bubalis',
        'origin': 'Haryana, India',
        'milk_yield': '1500-2500 liters per lactation',
        'fat_content': '6-8%',
        'characteristics': [
            'Jet black coat with white markings on face and legs',
            'Short, curved horns',
            'Strong and muscular build',
            'Excellent milk producer',
            'Good temperament'
        ],
        'fodder_requirements': [
            'Green fodder: 25-30 kg/day',
            'Dry fodder: 8-10 kg/day',
            'Concentrate: 2-3 kg/day',
            'Mineral mixture: 50-100g/day'
        ],
        'diseases_susceptible': [
            'Mastitis',
            'Foot and Mouth Disease',
            'Brucellosis',
            'Tuberculosis'
        ],
        'govt_schemes': [
            'National Livestock Mission',
            'Rashtriya Gokul Mission',
            'Dairy Entrepreneurship Development Scheme',
            'Kisan Credit Card for Animal Husbandry'
        ],
        'market_value': '₹80,000 - ₹1,50,000',
        'best_practices': [
            'Regular vaccination schedule',
            'Clean and dry housing',
            'Proper milking hygiene',
            'Regular health check-ups'
        ]
    },
    'gir_cattle': {
        'name': 'Gir Cattle',
        'scientific_name': 'Bos indicus',
        'origin': 'Gujarat, India',
        'milk_yield': '1200-1800 liters per lactation',
        'fat_content': '4.5-5.5%',
        'characteristics': [
            'Reddish brown to white coat',
            'Long, drooping ears',
            'Prominent hump',
            'Docile temperament',
            'Heat and disease resistant'
        ],
        'fodder_requirements': [
            'Green fodder: 20-25 kg/day',
            'Dry fodder: 6-8 kg/day',
            'Concentrate: 1.5-2.5 kg/day',
            'Mineral mixture: 50g/day'
        ],
        'diseases_susceptible': [
            'Foot and Mouth Disease',
            'Bovine Tuberculosis',
            'Brucellosis',
            'Tick-borne diseases'
        ],
        'govt_schemes': [
            'Rashtriya Gokul Mission',
            'National Programme for Bovine Breeding',
            'Dairy Entrepreneurship Development Scheme'
        ],
        'market_value': '₹60,000 - ₹1,20,000',
        'best_practices': [
            'Regular deworming',
            'Tick control measures',
            'Proper shelter from heat',
            'Clean drinking water'
        ]
    },
    'sahiwal_cattle': {
        'name': 'Sahiwal Cattle',
        'scientific_name': 'Bos indicus',
        'origin': 'Punjab, Pakistan',
        'milk_yield': '1400-2000 liters per lactation',
        'fat_content': '4.5-5.5%',
        'characteristics': [
            'Reddish brown coat',
            'Short horns',
            'Loose skin with dewlap',
            'Heat tolerant',
            'Good milk producer'
        ],
        'fodder_requirements': [
            'Green fodder: 22-28 kg/day',
            'Dry fodder: 7-9 kg/day',
            'Concentrate: 2-3 kg/day',
            'Mineral mixture: 50-75g/day'
        ],
        'diseases_susceptible': [
            'Foot and Mouth Disease',
            'Bovine Tuberculosis',
            'Brucellosis',
            'Parasitic infections'
        ],
        'govt_schemes': [
            'Rashtriya Gokul Mission',
            'National Livestock Mission',
            'Dairy Entrepreneurship Development Scheme'
        ],
        'market_value': '₹70,000 - ₹1,30,000',
        'best_practices': [
            'Regular vaccination',
            'Clean housing',
            'Proper nutrition',
            'Regular health monitoring'
        ]
    },
    'tharparkar_cattle': {
        'name': 'Tharparkar Cattle',
        'scientific_name': 'Bos indicus',
        'origin': 'Rajasthan, India',
        'milk_yield': '1000-1600 liters per lactation',
        'fat_content': '4.5-5.5%',
        'characteristics': [
            'White or light grey coat',
            'Medium-sized horns',
            'Strong and hardy',
            'Drought resistant',
            'Good draught animal'
        ],
        'fodder_requirements': [
            'Green fodder: 18-25 kg/day',
            'Dry fodder: 6-8 kg/day',
            'Concentrate: 1.5-2.5 kg/day',
            'Mineral mixture: 50g/day'
        ],
        'diseases_susceptible': [
            'Foot and Mouth Disease',
            'Bovine Tuberculosis',
            'Brucellosis',
            'Parasitic diseases'
        ],
        'govt_schemes': [
            'Rashtriya Gokul Mission',
            'National Livestock Mission',
            'Dairy Entrepreneurship Development Scheme'
        ],
        'market_value': '₹50,000 - ₹1,00,000',
        'best_practices': [
            'Regular deworming',
            'Clean water supply',
            'Proper shelter',
            'Regular health check-ups'
        ]
    }
}

# Load pre-trained model (using MobileNetV2 as base)
def load_model():
    """Load the pre-trained model for breed classification"""
    try:
        # For prototype, we'll use MobileNetV2 as base model
        # In production, this would be a custom-trained model on cattle breeds
        model = MobileNetV2(weights='imagenet', include_top=True)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Initialize model
model = load_model()

def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        return x
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_breed(image_path):
    """Predict cattle breed from image"""
    try:
        if model is None:
            return None, 0.0
        
        # Preprocess image
        processed_img = preprocess_image(image_path)
        if processed_img is None:
            return None, 0.0
        
        # Get prediction
        predictions = model.predict(processed_img)
        
        # For prototype, we'll simulate breed prediction
        # In production, this would use a custom-trained model
        import random
        breeds = list(CATTLE_BREEDS.keys())
        predicted_breed = random.choice(breeds)
        confidence = random.uniform(0.75, 0.95)
        
        return predicted_breed, confidence
        
    except Exception as e:
        print(f"Error in breed prediction: {e}")
        return None, 0.0

def generate_heatmap(image_path, predicted_breed):
    """Generate heatmap for explainable AI (simplified version)"""
    try:
        # Load image
        img = cv2.imread(image_path)
        img = cv2.resize(img, (224, 224))
        
        # For prototype, create a simple heatmap
        # In production, this would use Grad-CAM or similar technique
        heatmap = np.random.rand(224, 224)
        heatmap = cv2.resize(heatmap, (224, 224))
        
        # Normalize heatmap
        heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
        
        # Apply heatmap to image
        heatmap_colored = cv2.applyColorMap((heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        
        # Blend with original image
        alpha = 0.6
        blended = cv2.addWeighted(img, 1-alpha, heatmap_colored, alpha, 0)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', blended)
        heatmap_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return heatmap_b64
        
    except Exception as e:
        print(f"Error generating heatmap: {e}")
        return None

@app.route('/')
def index():
    """Main page with image upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and breed prediction"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save uploaded file
        file.save(filepath)
        
        # Predict breed
        predicted_breed, confidence = predict_breed(filepath)
        
        if predicted_breed is None:
            return jsonify({'error': 'Could not predict breed'}), 500
        
        # Get breed information
        breed_info = CATTLE_BREEDS.get(predicted_breed, {})
        
        # Generate heatmap
        heatmap_b64 = generate_heatmap(filepath, predicted_breed)
        
        # Prepare response
        result = {
            'breed': predicted_breed,
            'breed_name': breed_info.get('name', 'Unknown'),
            'confidence': round(confidence * 100, 2),
            'breed_info': breed_info,
            'heatmap': heatmap_b64,
            'timestamp': datetime.now().isoformat(),
            'image_id': str(uuid.uuid4())
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in upload: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/breed/<breed_id>')
def breed_info(breed_id):
    """Get detailed information about a specific breed"""
    breed_info = CATTLE_BREEDS.get(breed_id, {})
    if not breed_info:
        return jsonify({'error': 'Breed not found'}), 404
    
    return jsonify(breed_info)

@app.route('/register', methods=['POST'])
def register_cattle():
    """Register cattle details (prototype feature)"""
    try:
        data = request.json
        required_fields = ['breed', 'age', 'owner_name', 'location']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Generate cattle ID
        cattle_id = f"CATTLE_{uuid.uuid4().hex[:8].upper()}"
        
        # In production, this would save to database
        registration = {
            'cattle_id': cattle_id,
            'breed': data['breed'],
            'age': data['age'],
            'owner_name': data['owner_name'],
            'location': data['location'],
            'registration_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        return jsonify({
            'message': 'Cattle registered successfully',
            'cattle_id': cattle_id,
            'registration': registration
        })
        
    except Exception as e:
        print(f"Error in registration: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
