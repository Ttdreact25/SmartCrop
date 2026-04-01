# 🌱 Smart Crop Recommendation System

A machine learning-powered web application that provides intelligent crop recommendations based on soil properties, weather conditions, and geographical location. Built with Streamlit and Python, this system helps farmers make data-driven decisions for optimal crop selection.

## Project Live Link

https://smart-crop-recommendation-system-dqh0.onrender.com/

## 🎯 Features

- **🔐 User Authentication**: Secure login and registration system with password hashing.
- **🌍 Location-Based Recommendations**: Select your state and city for localized predictions.
- **🌤️ Real-Time Weather Integration**: Fetches current weather conditions including temperature, humidity, pressure, and wind speed.
- **🧪 Soil Analysis**: Input soil properties including NPK values, pH levels, and rainfall data.
- **📊 Interactive Visualizations**:
  - Overview of soil and weather conditions
  - Top-5 crop probability rankings
  - Data visualization charts
- **🔮 AI-Powered Predictions**: Machine learning model trained on agricultural data.
- **📱 Responsive Design**: Clean, modern UI with enhanced user experience.
- **💧 Fertilizer Recommendation**: Enter soil, crop and environment details to get a suggested fertilizer.
- **🍃 Plant Leaf Detection**: Upload a photo of a leaf to automatically identify the plant species or diagnose common diseases (requires a trained model).

## 🏗️ Project Structure

```
CROP_PREDICTION_PROJECT/
├── .vscode/                    # VS Code configuration
├── .users/                     # User database (created at first registration)
│   └── users.json              # Stores registered user credentials (hashed)
├── data/                       # Dataset files
│   ├── Crop_Recommendation.csv
│   ├── Indian_cities_coordinates.csv
│   └── leaf_dataset/          # place leaf images organised by class
├── notebooks/                  # Jupyter notebooks
│   ├── train_model.ipynb
│   └── train_leaf_model.ipynb  # skeleton for leaf detection training
├── saved_models/              # Trained ML models
│   ├── crop_model.pkl
│   └── leaf_model.pkl         # optional classifier used by leaf detector
├── smart_crop/               # Source code modules (renamed from src to avoid import conflicts)
│   ├── __pycache__/
│   ├── __init__.py
│   ├── auth.py               # User authentication & registration logic
│   ├── data_loader.py         # Data loading utilities
│   ├── location_mapper.py     # Location mapping functions
│   ├── predictor.py           # ML prediction logic
│   ├── weather_api.py         # Weather API integration
│   └── translator.py          # Multi-language translation support
├── streamlit_app/             # Streamlit application
│   ├── __init__.py
│   └── app.py                 # Main Streamlit app with authentication
├── .env                       # Environment variables
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── setup_demo_user.py         # Script to create demo user account
├── train_leaf_model.py        # Leaf detection model training script
├── train_leaf_model_advanced.py # Advanced leaf detection training
└── train_fertilizer_model.py  # Fertilizer model training script
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for weather API)

> **Optional (leaf detection training)**: To train a leaf detection model you'll also need libraries such as `tensorflow` (version 2.x), `opencv-python`, and `pillow` (or `scikit-learn` if using a classical classifier). These are not required to run the main app but are mentioned in the training notebook.
>
> Install the optional training dependencies with:
> ```bash
> pip install tensorflow opencv-python pillow
> ```
> If you run `python train_leaf_model_advanced.py` without TensorFlow installed, the script will print an error message and exit, as seen earlier.
### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MunishUpadhyay/Smart-Crop-Recommendation-System.git
   cd Smart-Crop-Recommendation-System
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file and add your weather API key
   echo "WEATHER_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run streamlit_app/app.py
   ```

## 🔐 User Authentication

The application includes a secure user authentication system with registration and login.

### Creating a Demo Account

To quickly test the app with a demo account:

```bash
python setup_demo_user.py
```

This creates a demo account with:
- **Username**: `demo`
- **Password**: `Demo@123`
- **Email**: `demo@example.com`

### Creating Your Own Account

1. On the login page, click **"Sign Up"**
2. Fill in the registration form with:
   - **Username** (at least 3 characters)
   - **Email** (valid email format)
   - **Password** (must include uppercase, lowercase, digit, and special character; minimum 8 characters)
   - **Confirm Password**
3. Click **"Register"** to create your account
4. You'll be redirected to the login page to sign in

### Security Features

- ✅ Passwords are hashed using bcrypt
- ✅ Strong password validation (minimum 8 characters, mixed case, numbers, special characters)
- ✅ Duplicate username and email prevention
- ✅ Session-based login with secure logout
- ✅ User data stored securely in `.users/users.json`

## 🎮 Usage

### 1. Location Selection
- Choose your **State** from the dropdown menu
- Select your **City** to get localized recommendations
- Available locations include major Indian states and cities

### 2. Weather Conditions
The system automatically fetches current weather data including:
- 🌡️ **Temperature** (°C)
- 💧 **Humidity** (%)
- 📊 **Pressure** (hPa)
- 💨 **Wind Speed** (m/s)
- 🌫️ **Weather Description**

### 3. Soil Properties Input
Use the interactive sliders to input your soil parameters (fertilizer recommendations are calculated using the same inputs plus crop and soil type):

| Parameter | Range | Description |
|-----------|-------|-------------|
| **Nitrogen (N)** | 0-100 ppm | Nitrogen content in soil |
| **Phosphorus (P)** | 0-100 ppm | Phosphorus content in soil |
| **Potassium (K)** | 0-100 ppm | Potassium content in soil |
| **Soil pH** | 0-14 | Soil acidity/alkalinity level |
| **Rainfall** | 0-500 mm | Annual rainfall in millimeters |

### 4. Get Recommendations
- Click **"🔮 Predict Best Crop"** button
- View the recommended crop with probability score
- Analyze the top-5 crop alternatives
- Review the data visualization charts

### 5. Plant Leaf Detection
- Use the sidebar to switch to **Plant Leaf Detection**
- Upload an image of a plant leaf (JPEG/PNG)
- The app will display a prediction after you supply a trained model file located at `saved_models/leaf_model.pkl`
- If no model is present, instructions will be shown explaining how to train one

### 6. Learn About the System
- Use the sidebar to switch to **About**
- View detailed algorithm information for both crop and fertilizer models
- See model accuracy and performance metrics
- Explore 4 interactive graphs:
  - **Model Accuracy Comparison** - Bar chart comparing accuracy of all models
  - **Feature Importance Distribution** - Pie chart showing which features are most important
  - **Supported Crops by Category** - Bar chart displaying crop types available
  - **Algorithm Processing Pipeline** - Timeline showing algorithm workflow
- Review the complete technology stack and key features
## 📊 Sample Results

The system provides comprehensive analysis including:

- **Primary Recommendation**: e.g., "RICE" with detailed explanation
- **Alternative Crops**: Ranked list with probability scores
- **Visual Analytics**:
  - Bar charts showing soil and weather parameter overview
  - Probability distribution of top 5 crops
- **Data Summary**: Complete input parameter visualization

## 🧠 Machine Learning Model

### Model Details
- **Algorithm**: [Random Forest Classifier]
- **Training Data**: Agricultural dataset with soil, weather, and crop yield information
- **Features**: 7 input parameters (N, P, K, pH, Temperature, Humidity, Rainfall)
- **Output**: Multi-class crop classification

### Model Performance
- **Accuracy**: [0.9931818181818182]
- **Validation Method**: [e.g., Cross-validation, Train-Test split]
- **Supported Crops**: Rice, Wheat, Maize, Banana, Papaya, Coconut, Coffee, and many more

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **Scikit-learn**: Machine learning framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Frontend
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualizations
- **CSS3**: Custom styling and responsive design

### APIs & External Services
- **Weather API**: Real-time weather data integration
- **Geolocation Services**: Location-based recommendations

## 📁 Key Files Description

| File | Description |
|------|-------------|
| `streamlit_app/app.py` | Main Streamlit application with UI components |
| `smart_crop/predictor.py` | Machine learning prediction logic |
| `smart_crop/weather_api.py` | Weather API integration and data fetching |
| `smart_crop/data_loader.py` | Data loading and preprocessing utilities |
| `smart_crop/location_mapper.py` | Geographic location mapping functions |
| `data/Crop_Recommendation.csv` | Training dataset for ML model |
| `saved_models/crop_model.pkl` | Trained machine learning model |

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Interactive Elements**: Hover effects, smooth transitions, and animations
- **Responsive Layout**: Mobile-friendly design that works on all devices
- **Data Visualization**: Interactive charts and graphs using Plotly
- **Real-time Updates**: Dynamic content updates based on user input

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Future Enhancements

- [ ] **Mobile App**: Native mobile application
- [ ] **More Crops**: Expand database to include more crop varieties
- [ ] **Market Prices**: Integration with commodity price APIs
- [ ] **Seasonal Analysis**: Time-based crop recommendations
- [ ] **Satellite Data**: Integration with satellite imagery for soil analysis
- [ ] **Multi-language Support**: Support for regional languages
- [ ] **Offline Mode**: Local predictions without internet connectivity

## 🐛 Known Issues

- Weather API rate limits may affect real-time data fetching
- Limited to Indian geographical locations currently
- Requires internet connection for weather data

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

- **Munish Upadhyay** - *Initial work* - [YourGitHub](https://github.com/MunishUpadhyay)

## 🙏 Acknowledgments

- Agricultural research data providers
- Weather API service providers
- Open-source community contributors
- Farmers and agricultural experts for domain knowledge

## 📞 Support

For support, email munishupadhyay183@gmail.com or create an issue in the GitHub repository.

---

**Made with ❤️ for sustainable agriculture and smart farming practices**

🌾 *Helping farmers make data-driven decisions for better crop yields* 🌾
Commit 1
Commit 2
Commit 3
Commit 4
Commit 5
Commit 6
