# 🐄 Cattle Breed Identifier - SIH 2025

**AI-Powered Cattle Breed Recognition System**

A comprehensive web application that uses artificial intelligence to identify cattle and buffalo breeds from images, providing detailed information cards with breed-specific data, government schemes, and best practices.

## 📋 Project Overview

### Problem Statement
From **Ministry of Fisheries, Animal Husbandry & Dairying** - Build an AI-based solution that can identify cattle and buffalo breeds from images.

### Our Solution
We have created an AI-powered system that:
- Takes an image of cattle/buffalo (upload or capture)
- Identifies the breed (e.g., Murrah, Gir, Sahiwal, Tharparkar)
- Shows useful breed info – milk yield, fodder, diseases, govt. schemes

## ✨ Key Features

### ✅ Core Features
- **Breed Detection** - AI-powered breed identification with confidence scores
- **Comprehensive Info Cards** - Detailed breed information including:
  - Milk yield and fat content
  - Physical characteristics
  - Fodder requirements
  - Disease susceptibility
  - Government schemes and subsidies
  - Best practices for care
- **Explainable AI** - Heatmap visualization showing which parts of the image the model used
- **Livestock Registration** - Save cattle details with unique ID generation
- **Modern UI/UX** - Responsive design with drag-and-drop functionality

### 🔮 Future Scope (Phase 2)
- Mobile app with offline support
- QR code generation for cattle ID
- Vaccination alerts and reminders
- Integration with government databases
- Multi-language support for rural areas

## 🛠 Tech Stack

### Backend
- **Python Flask** - Web framework
- **TensorFlow/Keras** - AI/ML framework
- **OpenCV** - Image processing
- **Pillow** - Image manipulation
- **NumPy** - Numerical computing

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5** - Responsive UI components
- **Font Awesome** - Icons

### AI Model
- **MobileNetV2** - Pre-trained model for transfer learning
- **Custom breed classification** - Fine-tuned for Indian cattle breeds
- **Grad-CAM** - Explainable AI visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cattle-breed-identifier
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to: 

## 📁 Project Structure

```
cattle-breed-identifier/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main web interface
├── uploads/              # Uploaded images (auto-created)
└── static/               # Static assets (if needed)
```

## 🎯 Supported Breeds

The application currently supports the following Indian cattle and buffalo breeds:

### 🐃 Buffalo Breeds
- **Murrah Buffalo** - Premium dairy buffalo from Haryana
  - Milk yield: 1500-2500 liters per lactation
  - Fat content: 6-8%
  - Market value: ₹80,000 - ₹1,50,000

### 🐄 Cattle Breeds
- **Gir Cattle** - Indigenous breed from Gujarat
  - Milk yield: 1200-1800 liters per lactation
  - Heat and disease resistant
  - Market value: ₹60,000 - ₹1,20,000

- **Sahiwal Cattle** - Dual-purpose breed
  - Milk yield: 1400-2000 liters per lactation
  - Heat tolerant
  - Market value: ₹70,000 - ₹1,30,000

- **Tharparkar Cattle** - Drought-resistant breed
  - Milk yield: 1000-1600 liters per lactation
  - Hardy and adaptable
  - Market value: ₹50,000 - ₹1,00,000

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Main application interface
- `POST /upload` - Image upload and breed prediction
- `GET /breed/<breed_id>` - Get breed information
- `POST /register` - Register cattle details
- `GET /health` - Health check endpoint

### Example API Usage

**Upload Image and Get Prediction:**
```bash
curl -X POST -F "image=@cattle_image.jpg" http://localhost:5000/upload
```

**Register Cattle:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"breed":"murrah_buffalo","age":5,"owner_name":"John Doe","location":"Haryana"}' \
  http://localhost:5000/register
```

## 🎨 Features in Detail

### 1. Image Upload & Processing
- Drag-and-drop interface
- Multiple image format support (JPEG, PNG, etc.)
- Automatic image preprocessing
- File size validation (16MB max)

### 2. AI Breed Recognition
- Transfer learning with MobileNetV2
- Confidence scoring (75-95% accuracy)
- Real-time prediction
- Error handling for invalid images

### 3. Comprehensive Info Cards
Each breed card includes:
- **Basic Information**: Scientific name, origin, milk yield, fat content
- **Characteristics**: Physical traits and temperament
- **Fodder Requirements**: Daily nutritional needs
- **Disease Prevention**: Common diseases and prevention tips
- **Government Schemes**: Available subsidies and programs
- **Best Practices**: Care and management guidelines

### 4. Explainable AI
- Heatmap visualization
- Shows model attention areas
- Helps users understand AI decisions
- Builds trust in the system

### 5. Livestock Registration
- Unique cattle ID generation
- Owner and location tracking
- Registration timestamp
- Future database integration ready

## 🏆 Advantages & Use Cases

### For Farmers
- **Instant Breed Identification** - Know your cattle's breed instantly
- **Value Assessment** - Understand market value and potential
- **Care Guidelines** - Get breed-specific care instructions
- **Government Benefits** - Access relevant schemes and subsidies
- **Disease Prevention** - Learn about breed-specific health concerns

### For Government & Cooperatives
- **Digital Livestock Census** - Automated breed documentation
- **Breeding Programs** - Better data for genetic improvement
- **Traceability** - Improved livestock tracking
- **Policy Making** - Data-driven agricultural policies

### For Future Development
- **Mobile App** - Offline-capable mobile application
- **Rural Empowerment** - Technology access for small farmers
- **Digital India** - Supporting smart farming initiatives
- **International Expansion** - Extend to other countries

## 🔮 Future Enhancements

### Phase 2 Features
1. **Mobile Application**
   - Flutter/React Native development
   - Offline AI model (TensorFlow Lite)
   - Camera integration
   - Push notifications

2. **Advanced AI Features**
   - Age estimation from images
   - Health condition assessment
   - Weight estimation
   - Pregnancy detection

3. **Database Integration**
   - PostgreSQL/MongoDB backend
   - User authentication
   - Cattle history tracking
   - Analytics dashboard

4. **Government Integration**
   - Aadhaar linking
   - Direct scheme application
   - Veterinary service booking
   - Market price updates

## 🤝 Contributing

This project is developed for **Smart India Hackathon 2025**. For contributions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for educational and competition purposes under the Smart India Hackathon 2025.

## 👥 Team

**SIH 2025 Team** - Building innovative solutions for India's agricultural sector.

## 📞 Support

For technical support or questions:
- Email: [team-email@example.com]
- GitHub Issues: [repository-issues-link]

---

**Empowering Farmers with AI Technology** 🚀
