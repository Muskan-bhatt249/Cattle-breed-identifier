"""
Cattle Breed Classification Model Training Script
SIH 2025 - Smart India Hackathon

This script demonstrates how to train a custom model for cattle breed classification.
For the prototype, we use a simplified approach with transfer learning.

Author: SIH 2025 Team
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import json

# Configuration
CONFIG = {
    'img_height': 224,
    'img_width': 224,
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001,
    'num_classes': 4,  # murrah_buffalo, gir_cattle, sahiwal_cattle, tharparkar_cattle
    'train_data_dir': 'dataset/train',
    'validation_data_dir': 'dataset/validation',
    'model_save_path': 'models/cattle_breed_model.h5',
    'class_names': ['murrah_buffalo', 'gir_cattle', 'sahiwal_cattle', 'tharparkar_cattle']
}

def create_model():
    """
    Create a custom model for cattle breed classification using transfer learning
    """
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(CONFIG['img_height'], CONFIG['img_width'], 3)
    )
    
    # Freeze the base model layers
    base_model.trainable = False
    
    # Create new model on top
    model = tf.keras.Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(CONFIG['num_classes'], activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=CONFIG['learning_rate']),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def prepare_data_generators():
    """
    Prepare data generators for training and validation
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    validation_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        CONFIG['train_data_dir'],
        target_size=(CONFIG['img_height'], CONFIG['img_width']),
        batch_size=CONFIG['batch_size'],
        class_mode='categorical',
        shuffle=True
    )
    
    # Load validation data
    validation_generator = validation_datagen.flow_from_directory(
        CONFIG['validation_data_dir'],
        target_size=(CONFIG['img_height'], CONFIG['img_width']),
        batch_size=CONFIG['batch_size'],
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, validation_generator

def create_callbacks():
    """
    Create training callbacks
    """
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    callbacks = [
        # Save best model
        ModelCheckpoint(
            CONFIG['model_save_path'],
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Early stopping
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    return callbacks

def plot_training_history(history):
    """
    Plot training history
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
    plt.show()

def evaluate_model(model, validation_generator):
    """
    Evaluate the trained model
    """
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    # Evaluate on validation set
    evaluation = model.evaluate(validation_generator)
    print(f"Validation Loss: {evaluation[0]:.4f}")
    print(f"Validation Accuracy: {evaluation[1]:.4f}")
    
    # Predict on validation set
    predictions = model.predict(validation_generator)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = validation_generator.classes
    
    # Calculate per-class accuracy
    class_names = list(validation_generator.class_indices.keys())
    print("\nPer-class Accuracy:")
    for i, class_name in enumerate(class_names):
        class_mask = true_classes == i
        class_accuracy = np.mean(predicted_classes[class_mask] == true_classes[class_mask])
        print(f"{class_name}: {class_accuracy:.4f}")

def save_model_info():
    """
    Save model information and configuration
    """
    model_info = {
        'model_name': 'Cattle Breed Classifier',
        'version': '1.0.0',
        'description': 'AI model for identifying Indian cattle and buffalo breeds',
        'architecture': 'MobileNetV2 + Custom Layers',
        'input_shape': [CONFIG['img_height'], CONFIG['img_width'], 3],
        'num_classes': CONFIG['num_classes'],
        'class_names': CONFIG['class_names'],
        'training_config': CONFIG,
        'supported_breeds': {
            'murrah_buffalo': {
                'name': 'Murrah Buffalo',
                'origin': 'Haryana, India',
                'characteristics': ['Jet black coat', 'Excellent milk producer']
            },
            'gir_cattle': {
                'name': 'Gir Cattle',
                'origin': 'Gujarat, India',
                'characteristics': ['Reddish brown coat', 'Heat resistant']
            },
            'sahiwal_cattle': {
                'name': 'Sahiwal Cattle',
                'origin': 'Punjab, Pakistan',
                'characteristics': ['Reddish brown coat', 'Heat tolerant']
            },
            'tharparkar_cattle': {
                'name': 'Tharparkar Cattle',
                'origin': 'Rajasthan, India',
                'characteristics': ['White coat', 'Drought resistant']
            }
        }
    }
    
    with open('models/model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print("Model information saved to models/model_info.json")

def main():
    """
    Main training function
    """
    print("🐄 Cattle Breed Classification Model Training")
    print("="*50)
    print("SIH 2025 - Smart India Hackathon")
    print("="*50)
    
    # Check if dataset directories exist
    if not os.path.exists(CONFIG['train_data_dir']):
        print(f"❌ Training data directory not found: {CONFIG['train_data_dir']}")
        print("Please create the dataset structure as follows:")
        print("dataset/")
        print("├── train/")
        print("│   ├── murrah_buffalo/")
        print("│   ├── gir_cattle/")
        print("│   ├── sahiwal_cattle/")
        print("│   └── tharparkar_cattle/")
        print("└── validation/")
        print("    ├── murrah_buffalo/")
        print("    ├── gir_cattle/")
        print("    ├── sahiwal_cattle/")
        print("    └── tharparkar_cattle/")
        return
    
    # Create model
    print("📦 Creating model...")
    model = create_model()
    model.summary()
    
    # Prepare data generators
    print("📊 Preparing data generators...")
    train_generator, validation_generator = prepare_data_generators()
    
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    print(f"Classes: {list(train_generator.class_indices.keys())}")
    
    # Create callbacks
    callbacks = create_callbacks()
    
    # Train the model
    print("🚀 Starting training...")
    history = model.fit(
        train_generator,
        epochs=CONFIG['epochs'],
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Plot training history
    print("📈 Plotting training history...")
    plot_training_history(history)
    
    # Evaluate model
    evaluate_model(model, validation_generator)
    
    # Save model information
    save_model_info()
    
    print("\n✅ Training completed successfully!")
    print(f"Model saved to: {CONFIG['model_save_path']}")
    print("Model information saved to: models/model_info.json")
    print("Training history plot saved to: training_history.png")

if __name__ == "__main__":
    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    main()
