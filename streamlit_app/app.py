            import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

# Adjust the path to import from the local package directory -- our code lives in
# a folder renamed to avoid conflict with a system package.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# ensure project root is at front so Python finds our package first
sys.path.insert(0, BASE_DIR)

# Import custom modules from new package name
from smart_crop import data_loader
from smart_crop import predictor
from smart_crop import location_mapper
from smart_crop import weather_api
from smart_crop import leaf_detector
from smart_crop import translator
from smart_crop import auth
from smart_crop import prediction_history
from smart_crop import profit_estimator
from smart_crop import equipment_recommender
from smart_crop import organic_farming
from smart_crop import risk_analyzer
from smart_crop import crop_comparator
from smart_crop import nearby_crops
from smart_crop import storage_tips

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="🌾 Smart Crop Recommendation App",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌱"
)

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # 'login' or 'register'

# --- Authentication Pages ---
def show_login_page():
    """Display the login page."""
    st.markdown("""
    <style>
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #1a472a 0%, #0B0404 100%);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🌱 Welcome!")
        st.write("Smart Crop Recommendation System")
        st.markdown("---")
        
        if st.session_state.auth_mode == "login":
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            col_login, col_switch = st.columns([2, 1])
            with col_login:
                if st.button("🔓 Login", use_container_width=True):
                    if username and password:
                        success, message = auth.login_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success("Login successful! 🎉")
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill in all fields.")
            
            with col_switch:
                if st.button("Sign Up", use_container_width=True):
                    st.session_state.auth_mode = "register"
                    st.rerun()
            
            # st.info("💡 Try demo: username='demo' password='Demo@123'")
        
        else:  # register mode
            st.subheader("Create Account")
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            st.info(
                "Password requirements:\n"
                "• At least 8 characters\n"
                "• Include uppercase letter (A-Z)\n"
                "• Include lowercase letter (a-z)\n"
                "• Include digit (0-9)\n"
                "• Include special character (!@#$%...)"
            )
            
            col_register, col_back = st.columns([2, 1])
            with col_register:
                if st.button("📝 Register", use_container_width=True):
                    if new_username and new_email and new_password and confirm_password:
                        success, message = auth.register_user(new_username, new_email, new_password, confirm_password)
                        if success:
                            st.success(message)
                            st.session_state.auth_mode = "login"
                            st.info("Redirecting to login...")
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill in all fields.")
            
            with col_back:
                if st.button("Back", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()

# Check authentication
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# --- Data Loading (defined early so all branches can use it) ---
@st.cache_data
# Cache data loading for performance

def load_all_data():
    """Loads all necessary data for the application."""
    # Load location coordinates CSV from the project's data directory
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    location_csv_path = os.path.join(PROJECT_ROOT, 'data', 'Indian_cities_coordinates.csv')
    location_df_loaded = data_loader.load_location_data(path=location_csv_path)

    # Load the crop prediction model (as per your predictor.py)
    crop_model_loaded = predictor.load_model()

    # Get the state-city mapping using the function from location_mapper, passing the DataFrame
    state_city_map_loaded = location_mapper.get_state_city_mapping(location_df_loaded)

    return location_df_loaded, crop_model_loaded, state_city_map_loaded

# load global data immediately after definition
location_df, crop_model, state_city_map = load_all_data()

# load fertilizer resources lazily - we'll call when needed
fertilizer_resources = None  # tuple(model, soil_enc, crop_enc, scaler)

# --- Custom CSS for Enhanced Aesthetics and Color Scheme ---
st.markdown(
    """
    <style>
    /* Color Palette Variables (Optional, for easy modification) */
    :root {
        --primary-bg: #0B0404; /* Very dark grey */
        --secondary-bg: #1A1A1D; /* Slightly lighter dark grey for elements */
        --text-color: #E0E0E0; /* Off-white for general text */
        --header-color: #00cc96; /* Vibrant green for main titles/accents */
        --accent-blue: #287F83; /* Pearl blue for selectboxes */
        --button-hover: #00996b; /* Darker green for button hover */
        --border-color: #1A1A1D; /* Subtle dark border/grid lines */
        --info-bg: #213c42; /* Dark teal for info boxes */
        --info-text: #afeeee; /* Light cyan for info text */
    }

    body {
        background-color: var(--primary-bg);
        color: var(--text-color);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Titles and Headers */
    h1 {
        color: var(--header-color);
        font-weight: bold;
        font-size: 2.2em; /* Adjusted H1 font size */
    }
    h2, h3, h4, h5, h6 {
        color: var(--header-color);
        font-weight: bold;
    }

    /* Main App Title - Tagline Styling */
    h4[style*="margin-top:-20px"] { /* Targeting the specific tagline h4 */
        color: #888;
        font-weight: normal;
        font-size: 1em;
    }

    /* Streamlit widgets styling */
    .stSelectbox > div > div > div {
        background-color: var(--accent-blue);
        color: white; /* Text inside selectbox */
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
    }
    .stSlider > div > div {
        background-color: var(--secondary-bg);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
    }
    .stSlider .stThumb {
        background-color: var(--header-color);
    }
    .stButton > button {
        background-color: var(--header-color);
        color: white;
        font-weight: bold;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: var(--button-hover);
        transform: translateY(-2px);
    }

    /* Success, Info, Warning, Error Messages */
    .stAlert div[data-baseweb="alert"] {
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .stAlert [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
    }
    .stAlert.streamlit-success {
        background-color: #1a472a;
        color: #e6ffe6;
    }
    .stAlert.streamlit-error {
        background-color: #4a1f1f;
        color: #ffe6e6;
    }
    .stAlert.streamlit-warning {
        background-color: #4a3e1f;
        color: #fffbe6;
    }
    .stAlert.streamlit-info {
        background-color: var(--info-bg);
        color: var(--info-text);
    }

    /* Plotly chart container padding */
    .stPlotlyChart {
        padding: 1rem 0;
    }

    /* Sidebar styling */
    .css-1d391kg { /* This class might change with Streamlit updates */
        background-color: var(--secondary-bg);
    }

    /* --- Metric Component Styling (WITH !important flags) --- */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-bg) !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    div[data-testid="stMetric"] label {
        color: var(--text-color) !important;
        font-size: 0.9em;
        font-weight: normal;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--header-color) !important;
        font-size: 1.8em;
        font-weight: bold;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: var(--text-color) !important;
    }

    /* Adjust padding for columns slightly */
    /* This class might change in future Streamlit updates */
    .st-emotion-cache-1iy415c {
        padding-top: 0rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Main Application Title ---
st.title("🌱 Smart Crop Recommendation System")
st.markdown("<h4 style='color: #888; margin-top: -20px; font-weight: normal;'>Your partner for optimal farming decisions.</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar: User Profile & Logout ---
with st.sidebar:
    st.markdown("---")
    col_user, col_logout = st.columns([2, 1])
    with col_user:
        st.write(f"👤 **{st.session_state.username}**")
    with col_logout:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.auth_mode = "login"
            st.success("Logged out successfully!")
            st.rerun()
    st.markdown("---")

# --- Navigation ---
# give users ability to hop between crop recommender and leaf detector
mode = st.sidebar.radio("Choose Tool", ["Crop Recommendation", "Fertilizer Recommendation", "Crop Demand Prediction", "Plant Leaf Detection", "Farmer Dashboard", "Modules", "About"])

# --- Language Selection (for Recommendations) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Language / மொழி / भाषा")
selected_language = st.sidebar.selectbox(
    "Select Language for Recommendations",
    options=list(translator.LANGUAGE_NAMES.keys()),
    format_func=lambda x: translator.LANGUAGE_NAMES[x],
    index=0,
    help="Choose your preferred language for recommendations"
)

# --- About Page ---
if mode == "About":
    st.header("📖 About Smart Crop Recommendation System")
    
    st.markdown("""
    The **Smart Crop Recommendation System** is an AI-powered agricultural decision support tool that helps farmers 
    optimize crop selection based on their soil conditions, weather patterns, and geographical location.
    """)
    
    st.markdown("---")
    
    # === Algorithm Information ===
    st.subheader("🧠 Algorithm & Machine Learning Models")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Crop Recommendation Model 
        - **Algorithm**: Random Forest Classifier & Large Language Model
        - **Training Data**: Agricultural dataset with 2200+ records
        - **Features**: 7 input parameters
        - **Output Classes**: 22 crop types
        - **Accuracy**: ~99.3%
        - **Validation**: 80-20 train-test split
        """)
    
    with col2:
        st.markdown("""
        ### Fertilizer Recommendation Model
        - **Algorithm**: Decision Tree Classifier
        - **Training Data**: 500+ fertilizer records
        - **Features**: 8 input parameters
        - **Output Classes**: 7 fertilizer types
        - **Accuracy**: ~95%+
        - **Validation**: Cross-validation
        """)
    
    st.markdown("---")
    
    # === Input Features ===
    st.subheader("📊 Input Features Used")
    
    features_data = {
        "Feature": [
            "Nitrogen (N)",
            "Phosphorus (P)",
            "Potassium (K)",
            "Temperature",
            "Humidity",
            "pH",
            "Rainfall",
            "Location (State/City)"
        ],
        "Range": [
            "0-140 ppm",
            "5-145 ppm",
            "5-205 ppm",
            "-5 to 50°C",
            "0-100%",
            "3.5-10.0",
            "20-300 mm",
            "All Indian states"
        ],
        "Type": [
            "Soil Nutrient",
            "Soil Nutrient",
            "Soil Nutrient",
            "Weather",
            "Weather",
            "Soil Property",
            "Weather",
            "Geographic"
        ]
    }
    features_df = pd.DataFrame(features_data)
    st.dataframe(features_df, use_container_width=True)
    
    st.markdown("---")
    
    # === 4 Graphs ===
    st.subheader("📈 Algorithm Performance & Analysis")
    
    # Graph 1: Model Accuracy Comparison
    fig1_data = {
        "Model": ["Crop Recommendation", "Fertilizer Recommendation", "Leaf Detection"],
        "Accuracy": [99.3, 95.0, 92.0]
    }
    fig1_df = pd.DataFrame(fig1_data)
    fig1 = px.bar(
        fig1_df,
        x="Model",
        y="Accuracy",
        text="Accuracy",
        title="🎯 Model Accuracy Comparison",
        labels={"Accuracy": "Accuracy (%)"},
        color="Accuracy",
        color_continuous_scale="Greens",
        template="plotly_dark"
    )
    fig1.update_layout(height=400, showlegend=False)
    fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Graph 2: Feature Importance Distribution
    feature_importance = {
        "Feature Type": ["Soil Nutrients\n(N, P, K)", "Weather Data\n(Temp, Humidity)", "Soil Property\n(pH)", "Rainfall"],
        "Importance": [35, 30, 20, 15]
    }
    fig2_df = pd.DataFrame(feature_importance)
    fig2 = px.pie(
        fig2_df,
        names="Feature Type",
        values="Importance",
        title="🌱 Feature Importance Distribution",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Graph 3: Supported Crops by Category
    crop_data = {
        "Category": ["Cereals", "Pulses", "Fruits", "Cash Crops"],
        "Count": [2, 7, 10, 3]
    }
    fig3_df = pd.DataFrame(crop_data)
    fig3 = px.bar(
        fig3_df,
        x="Category",
        y="Count",
        text="Count",
        title="🌾 Supported Crops by Category",
        labels={"Count": "Number of Crops"},
        color="Count",
        color_continuous_scale="Viridis",
        template="plotly_dark"
    )
    fig3.update_layout(height=400, showlegend=False)
    fig3.update_traces(texttemplate="%{text}", textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Graph 4: Algorithm Decision Flow
    decision_flow = {
        "Stage": ["Input Data\nCollection", "Feature\nScaling", "Model\nPrediction", "Output\nRecommendation"],
        "Processing_Time": [0.1, 0.05, 0.3, 0.05]
    }
    fig4_df = pd.DataFrame(decision_flow)
    fig4 = px.line(
        fig4_df,
        x="Stage",
        y="Processing_Time",
        markers=True,
        title="⚙️ Algorithm Processing Pipeline Timeline",
        labels={"Processing_Time": "Time (seconds)"},
        text="Processing_Time",
        template="plotly_dark",
        line_shape="linear"
    )
    fig4.update_traces(line=dict(color="#00cc96", width=3), marker=dict(size=10))
    fig4.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("---")
    
    # === All Supported Crops with Duration ===
    st.subheader("🌱 All Supported Crops (22) with Growing Duration")
    
    # Load crop duration data
    crop_duration_data = predictor.load_crop_duration_new_data()
    
    # Convert to DataFrame for display
    crops_list = []
    for crop_name, info in crop_duration_data.items():
        crops_list.append({
            "Crop Name": crop_name.title(),
            "Growing Duration": f"{info['duration']} days",
            "Season": info['season']
        })
    
    crops_df = pd.DataFrame(crops_list)
    crops_df = crops_df.sort_values("Crop Name")
    
    st.dataframe(crops_df, use_container_width=True)
    
    st.markdown("---")
    
    # === Technology Stack ===
    st.subheader("🛠️ Technology Stack")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("""
        **Backend**
        - Python 3.8+
        - Scikit-learn
        - Joblib
        - Pandas & NumPy
        """)
    
    with tech_col2:
        st.markdown("""
        **Frontend**
        - Streamlit
        - Plotly
        - CSS/HTML
        """)
    
    with tech_col3:
        st.markdown("""
        **Security & Auth**
        - Bcrypt
        - Session Management
        - Secure Password Storage
        """)
    
    st.markdown("---")
    
    # === Features ===
    st.subheader("✨ Key Features")
    
    feat1, feat2 = st.columns(2)
    
    with feat1:
        st.markdown("""
        - 🔐 Secure User Authentication
        - 🌍 Location-Based Recommendations
        - 🌤️ Real-Time Weather Integration
        - 📊 Interactive Visualizations
        """)
    
    with feat2:
        st.markdown("""
        - 🧪 Fertilizer Recommendations
        - 🍃 Plant Leaf Disease Detection
        - 🌐 Multi-Language Support
        - 📱 Responsive Design
        """)
    
    st.markdown("---")
    
    # === Footer ===
    st.info(
        "💡 **Tip**: Use this system to make data-driven farming decisions. "
        "Enter your farm's soil and weather data to get personalized crop and fertilizer recommendations!"
    )
    
    st.stop()

# --- Modules Page ---
if mode == "Modules":
    st.header("📦 System Modules & Processes")
    st.markdown("Detailed documentation of all modules and processes in the Smart Crop Recommendation System.")
    
    st.markdown("---")
    
    # === System Architecture ===
    st.subheader("🏗️ System Architecture Overview")
    
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────┐
    │                    Streamlit Web Interface                        │
    │                     (app.py)                                     │
    └─────────────────────────────────────────────────────────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
            ▼                     ▼                     ▼
    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
    │ Authentication│    │   Prediction  │    │    Weather    │
    │    Module     │    │    Module     │    │     API       │
    │   (auth.py)   │    │ (predictor.py)│    │(weather_api.py)│
    └───────────────┘    └───────────────┘    └───────────────┘
            │                     │                     │
            ▼                     ▼                     ▼
    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
    │  User Data    │    │  ML Models    │    │  Weather Data │
    │  (.users/)    │    │(saved_models/)│    │   (External)  │
    └───────────────┘    └───────────────┘    └───────────────┘
    ```
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === Module Cards ===
    st.subheader("🔧 Core Modules")
    
    # Module 1: Authentication
    with st.expander("1️⃣ Authentication Module (auth.py)", expanded=False):
        st.markdown("""
        **Purpose**: Handles user registration, login, and session management with secure password hashing.
        
        **Location**: `smart_crop/auth.py`
        
        **Key Functions**:
        - `register_user(username, email, password, confirm_password)` - Registers a new user
        - `login_user(username, password)` - Authenticates a user
        
        **Security Features**:
        - ✅ Password hashing using bcrypt
        - ✅ Strong password validation (8+ chars, uppercase, lowercase, digit, special char)
        - ✅ Duplicate username/email prevention
        - ✅ Secure session management
        
        **Data Storage**: `.users/users.json`
        """)
    
    # Module 2: Data Loader
    with st.expander("2️⃣ Data Loader Module (data_loader.py)", expanded=False):
        st.markdown("""
        **Purpose**: Handles loading and preprocessing of all data files used in the application.
        
        **Location**: `smart_crop/data_loader.py`
        
        **Key Functions**:
        - `load_crop_data(path)` - Loads crop recommendation dataset (2200+ records)
        - `load_location_data(path)` - Loads location coordinates for Indian cities
        - `load_fertilizer_data(path)` - Loads fertilizer prediction dataset
        
        **Data Files Used**:
        - `data/Crop_Recommendation.csv` - Crop training data
        - `data/Indian_cities_coordinates.csv` - City coordinates
        - `data/Fertilizer Prediction.csv` - Fertilizer data
        - `data/crops_duration.csv` - Crop growing durations
        """)
    
    # Module 3: Predictor
    with st.expander("3️⃣ Predictor Module (predictor.py)", expanded=False):
        st.markdown("""
        **Purpose**: Core machine learning module that handles crop prediction, fertilizer recommendation, and model management.
        
        **Location**: `smart_crop/predictor.py`
        
        **Key Functions**:
        - `load_model(model_path)` - Loads the trained crop recommendation model
        - `predict_crop(input_data, model)` - Predicts the best crop based on input parameters
        - `load_fertilizer_resources()` - Loads fertilizer recommendation model and encoders
        - `predict_fertilizer(...)` - Recommends fertilizer based on soil and crop conditions
        - `load_crop_duration_new_data()` - Loads crop duration information
        
        **Model Details**:
        - **Algorithm**: Random Forest Classifier
        - **Training Data**: 2200+ records
        - **Features**: 7 input parameters (N, P, K, temperature, humidity, pH, rainfall)
        - **Output Classes**: 22 crop types
        - **Accuracy**: ~99.3%
        """)
    
    # Module 4: Weather API
    with st.expander("4️⃣ Weather API Module (weather_api.py)", expanded=False):
        st.markdown("""
        **Purpose**: Integrates with external weather API to fetch real-time weather data for location-based recommendations.
        
        **Location**: `smart_crop/weather_api.py`
        
        **Key Functions**:
        - `get_weather_data(city_name, api_key)` - Fetches current weather data for a given city
        
        **Weather Data Retrieved**:
        - 🌡️ Temperature (°C)
        - 💧 Humidity (%)
        - 📊 Pressure (hPa)
        - 💨 Wind Speed (m/s)
        - 🌫️ Weather Description
        
        **API**: OpenWeatherMap API
        **Environment Variable**: `WEATHER_API_KEY` (stored in `.env`)
        """)
    
    # Module 5: Location Mapper
    with st.expander("5️⃣ Location Mapper Module (location_mapper.py)", expanded=False):
        st.markdown("""
        **Purpose**: Manages geographic location data and provides state-city mapping for location-based recommendations.
        
        **Location**: `smart_crop/location_mapper.py`
        
        **Key Functions**:
        - `get_state_city_mapping(location_df)` - Creates a mapping of states to their cities
        - `get_coordinates(city_name, location_df)` - Retrieves latitude and longitude for a city
        
        **Coverage**:
        - All major Indian states
        - 500+ cities and towns
        - GPS coordinates for mapping
        """)
    
    # Module 6: Leaf Detector
    with st.expander("6️⃣ Leaf Detector Module (leaf_detector.py)", expanded=False):
        st.markdown("""
        **Purpose**: Provides plant disease detection by analyzing leaf images using machine learning.
        
        **Location**: `smart_crop/leaf_detector.py`
        
        **Key Functions**:
        - `load_leaf_model(model_path)` - Loads the trained leaf detection model
        - `predict_disease(image_path, model)` - Predicts plant disease from a leaf image
        
        **Supported Diseases**:
        - Healthy
        - Late Blight
        - Early Blight
        
        **Training Data**: Located in `data/Training/` and `data/Validation/`
        **Model File**: `saved_models/leaf_model.pkl`
        """)
    
    # Module 7: Translator
    with st.expander("7️⃣ Translator Module (translator.py)", expanded=False):
        st.markdown("""
        **Purpose**: Provides multi-language support for recommendations and UI elements.
        
        **Location**: `smart_crop/translator.py`
        
        **Key Functions**:
        - `translate_text(text, target_language)` - Translates text to the target language
        
        **Supported Languages**:
        - English (en)
        - Hindi (hi)
        - Tamil (ta)
        - Telugu (te)
        - Kannada (kn)
        - Malayalam (ml)
        - Bengali (bn)
        - Marathi (mr)
        - Gujarati (gu)
        - Punjabi (pa)
        """)
    
    st.markdown("---")
    
    # === Process Flow ===
    st.subheader("🔄 Process Flows")
    
    flow_col1, flow_col2 = st.columns(2)
    
    with flow_col1:
        st.markdown("""
        **Crop Recommendation Flow**:
        ```
        User Input → Location Selection → Weather API Call
            ↓
        Soil Parameters → Feature Scaling → ML Model Prediction
            ↓
        Probability Calculation → Top-5 Recommendations → Display Results
        ```
        
        **Fertilizer Recommendation Flow**:
        ```
        User Input → Soil Type + Crop Selection → NPK Values
            ↓
        Feature Encoding → Model Prediction → Fertilizer Recommendation
            ↓
        Application Guidelines → Display Results
        ```
        """)
    
    with flow_col2:
        st.markdown("""
        **User Authentication Flow**:
        ```
        User Access → Login Page → Enter Credentials
            ↓
        Validate → Hash Password → Check Storage
            ↓
        Session Created → Access Granted
        ```
        
        **Leaf Detection Flow**:
        ```
        Image Upload → Image Preprocessing → Feature Extraction
            ↓
        Model Prediction → Disease Classification → Confidence Score
            ↓
        Treatment Recommendations → Display Results
        ```
        """)
    
    st.markdown("---")
    
    # === Data Files ===
    st.subheader("📁 Data Files")
    
    data_files = {
        "File": [
            "data/Crop_Recommendation.csv",
            "data/Indian_cities_coordinates.csv",
            "data/Fertilizer Prediction.csv",
            "data/crops_duration.csv",
            "data/crops_duration_new.csv",
            "data/Training/",
            "data/Validation/"
        ],
        "Description": [
            "Crop training data with 2200+ records",
            "GPS coordinates for Indian cities",
            "Fertilizer prediction dataset",
            "Crop growing duration data",
            "Updated crop duration data",
            "Leaf disease training images",
            "Leaf disease validation images"
        ],
        "Format": [
            "CSV",
            "CSV",
            "CSV",
            "CSV",
            "CSV",
            "Images (JPEG/PNG)",
            "Images (JPEG/PNG)"
        ]
    }
    data_df = pd.DataFrame(data_files)
    st.dataframe(data_df, use_container_width=True)
    
    st.markdown("---")
    
    # === ML Models ===
    st.subheader("🤖 Machine Learning Models")
    
    model_col1, model_col2, model_col3 = st.columns(3)
    
    with model_col1:
        st.markdown("""
        **Crop Recommendation**
        - Algorithm: Random Forest
        - Accuracy: 99.3%
        - Features: 7 parameters
        - Output: 22 crops
        - File: `saved_models/crop_model.pkl`
        """)
    
    with model_col2:
        st.markdown("""
        **Fertilizer Recommendation**
        - Algorithm: Decision Tree
        - Accuracy: 95%+
        - Features: 8 parameters
        - Output: 7 fertilizers
        - File: `saved_models/fertilizer_model.pkl`
        """)
    
    with model_col3:
        st.markdown("""
        **Leaf Detection**
        - Algorithm: CNN/Classifier
        - Accuracy: 92%+
        - Features: Image pixels
        - Output: Disease class
        - File: `saved_models/leaf_model.pkl`
        """)
    
    st.markdown("---")
    
    # === Module Dependencies ===
    st.subheader("🔗 Module Dependencies")
    
    st.markdown("""
    ```
    app.py (Main Application)
    ├── auth.py
    │   └── .users/users.json
    ├── data_loader.py
    │   ├── data/Crop_Recommendation.csv
    │   ├── data/Indian_cities_coordinates.csv
    │   └── data/Fertilizer Prediction.csv
    ├── predictor.py
    │   ├── saved_models/crop_model.pkl
    │   └── saved_models/fertilizer_model.pkl
    ├── weather_api.py
    │   └── .env (WEATHER_API_KEY)
    ├── location_mapper.py
    │   └── data/Indian_cities_coordinates.csv
    ├── leaf_detector.py
    │   └── saved_models/leaf_model.pkl
    └── translator.py
    ```
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === Quick Reference ===
    st.subheader("📋 Quick Reference")
    
    quick_ref = {
        "Module": ["Authentication", "Data Loader", "Predictor", "Weather API", "Location Mapper", "Leaf Detector", "Translator"],
        "Purpose": [
            "User management",
            "Data preprocessing",
            "ML predictions",
            "Real-time weather",
            "Geographic data",
            "Disease detection",
            "Multi-language"
        ],
        "Key Function": [
            "login_user()",
            "load_crop_data()",
            "predict_crop()",
            "get_weather_data()",
            "get_state_city_mapping()",
            "predict_disease()",
            "translate_text()"
        ]
    }
    quick_df = pd.DataFrame(quick_ref)
    st.dataframe(quick_df, use_container_width=True)
    
    st.markdown("---")
    
    # === Footer ===
    st.info(
        "💡 **Tip**: This module documentation provides an overview of all components in the Smart Crop Recommendation System. "
        "Each module is designed to be modular and can be extended or modified independently."
    )
    
    st.stop()

# --- Farmer Dashboard Page ---
if mode == "Farmer Dashboard":
    st.header("🌾 Farmer Dashboard")
    st.markdown("Your comprehensive farming analytics and management center.")
    
    st.markdown("---")
    
    # === Dashboard Overview Metrics ===
    st.subheader("📊 Dashboard Overview")
    
    # Get prediction statistics for metrics
    pred_stats = prediction_history.get_prediction_stats(st.session_state.username)
    user_profile = auth.get_user_profile(st.session_state.username)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        farm_size = user_profile.get('farm_size', 'Not specified')
        st.metric(
            label="Total Farm Area",
            value=farm_size if farm_size != 'Not specified' else 'N/A',
            delta="Update in profile"
        )
    
    with metric_col2:
        st.metric(
            label="Total Predictions",
            value=str(pred_stats['total_predictions']),
            delta=f"{pred_stats['successful_predictions']} successful"
        )
    
    with metric_col3:
        st.metric(
            label="Success Rate",
            value=f"{pred_stats['success_rate']}%",
            delta="Based on history"
        )
    
    with metric_col4:
        st.metric(
            label="Most Predicted Crop",
            value=pred_stats['most_predicted_crop'],
            delta="From your history"
        )
    
    st.markdown("---")
    
    # === User Profile Section ===
    st.subheader("👤 User Profile")
    
    # Get user profile data from auth module
    user_profile = auth.get_user_profile(st.session_state.username)
    user_email = auth.get_user_email(st.session_state.username)
    
    # Get prediction statistics
    pred_stats = prediction_history.get_prediction_stats(st.session_state.username)
    
    profile_col1, profile_col2, profile_col3 = st.columns(3)
    
    with profile_col1:
        st.markdown("**Personal Information**")
        st.markdown(f"**Name:** {st.session_state.username}")
        st.markdown(f"**Email:** {user_email}")
        st.markdown(f"**Phone:** {user_profile.get('phone', 'Not specified')}")
    
    with profile_col2:
        st.markdown("**Farm Details**")
        st.markdown(f"**Farm Size:** {user_profile.get('farm_size', 'Not specified')}")
        st.markdown(f"**Location:** {user_profile.get('location', 'Not specified')}")
        st.markdown(f"**Soil Type:** {user_profile.get('soil_type', 'Not specified')}")
    
    with profile_col3:
        st.markdown("**Account Statistics**")
        st.markdown(f"**Member Since:** {user_profile.get('member_since', 'N/A')}")
        st.markdown(f"**Total Predictions:** {pred_stats['total_predictions']}")
        st.markdown(f"**Success Rate:** {pred_stats['success_rate']}%")
    
    # Profile Edit Section
    with st.expander("✏️ Edit Profile", expanded=False):
        st.markdown("Update your farm details below:")
        
        edit_col1, edit_col2 = st.columns(2)
        
        with edit_col1:
            new_farm_size = st.text_input(
                "Farm Size",
                value=user_profile.get('farm_size', ''),
                placeholder="e.g., 25 Acres"
            )
            new_location = st.text_input(
                "Location",
                value=user_profile.get('location', ''),
                placeholder="e.g., Punjab, India"
            )
        
        with edit_col2:
            new_phone = st.text_input(
                "Phone",
                value=user_profile.get('phone', ''),
                placeholder="e.g., +91 98765 43210"
            )
            new_soil_type = st.selectbox(
                "Soil Type",
                ["Sandy", "Loamy", "Black", "Red", "Clayey", "Not specified"],
                index=0 if user_profile.get('soil_type') == 'Sandy' else
                      1 if user_profile.get('soil_type') == 'Loamy' else
                      2 if user_profile.get('soil_type') == 'Black' else
                      3 if user_profile.get('soil_type') == 'Red' else
                      4 if user_profile.get('soil_type') == 'Clayey' else 5
            )
        
        if st.button("💾 Save Profile", use_container_width=True):
            profile_updates = {
                'farm_size': new_farm_size,
                'location': new_location,
                'phone': new_phone,
                'soil_type': new_soil_type
            }
            success, message = auth.update_user_profile(st.session_state.username, profile_updates)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    st.markdown("---")
    
    # === Previous Predictions History ===
    st.subheader("📜 Previous Predictions History")
    
    # Get user's prediction history
    user_predictions = prediction_history.get_user_predictions(st.session_state.username, limit=10)
    
    if user_predictions:
        # Create DataFrame from predictions
        history_data = {
            "Date": [],
            "Type": [],
            "Crop/Fertilizer": [],
            "Location": [],
            "Confidence": [],
            "Status": []
        }
        
        for pred in user_predictions:
            history_data["Date"].append(pred.get("date", "N/A"))
            history_data["Type"].append(pred.get("type", "N/A").title())
            history_data["Crop/Fertilizer"].append(pred.get("crop", "N/A"))
            history_data["Location"].append(pred.get("location", "N/A"))
            history_data["Confidence"].append(f"{pred.get('confidence', 0)}%")
            status = "✅ Success" if pred.get("status") == "success" else "❌ Failed"
            history_data["Status"].append(status)
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
        
        # Add export and clear buttons
        col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
        with col_export1:
            if st.button("📥 Export History", use_container_width=True):
                export_data = prediction_history.export_user_history(st.session_state.username, format="csv")
                st.download_button(
                    label="Download CSV",
                    data=export_data,
                    file_name=f"prediction_history_{st.session_state.username}.csv",
                    mime="text/csv"
                )
        with col_export2:
            if st.button("🗑️ Clear History", use_container_width=True):
                if prediction_history.clear_user_history(st.session_state.username):
                    st.success("History cleared successfully!")
                    st.rerun()
                else:
                    st.error("Failed to clear history.")
        
        # Show detailed prediction view
        st.markdown("---")
        st.subheader("🔍 Detailed Prediction View")
        
        if user_predictions:
            # Create a selectbox to choose a prediction to view
            prediction_options = [f"{p.get('date', 'N/A')} - {p.get('crop', 'N/A')} ({p.get('type', 'N/A').title()})" for p in user_predictions]
            selected_prediction = st.selectbox("Select a prediction to view details:", prediction_options)
            
            if selected_prediction:
                # Find the selected prediction
                selected_idx = prediction_options.index(selected_prediction)
                pred = user_predictions[selected_idx]
                
                # Display prediction details
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown(f"**Date:** {pred.get('date', 'N/A')}")
                    st.markdown(f"**Type:** {pred.get('type', 'N/A').title()}")
                    st.markdown(f"**Crop/Fertilizer:** {pred.get('crop', 'N/A')}")
                    st.markdown(f"**Location:** {pred.get('location', 'N/A')}")
                    st.markdown(f"**Confidence:** {pred.get('confidence', 0)}%")
                
                with detail_col2:
                    st.markdown("**Input Parameters:**")
                    if pred.get('input_params'):
                        for key, value in pred['input_params'].items():
                            st.markdown(f"- {key.title()}: {value}")
                    else:
                        st.markdown("No input parameters recorded.")
    else:
        st.info("No prediction history yet. Start making predictions to see your history here!")
    
    st.markdown("---")
    
    # === Crop Usage Charts ===
    st.subheader("🌾 Crop Usage Analytics")
    
    # Get crop distribution from prediction history
    crop_distribution = prediction_history.get_crop_distribution(st.session_state.username)
    
    crop_col1, crop_col2 = st.columns(2)
    
    with crop_col1:
        # Crop Distribution Pie Chart
        if crop_distribution:
            crop_dist_df = pd.DataFrame({
                "Crop": list(crop_distribution.keys()),
                "Predictions": list(crop_distribution.values())
            })
            
            fig_crop_dist = px.pie(
                crop_dist_df,
                names="Crop",
                values="Predictions",
                title="🌱 Crop Distribution by Predictions",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            fig_crop_dist.update_layout(height=400)
            st.plotly_chart(fig_crop_dist, use_container_width=True)
        else:
            st.info("No crop prediction data available yet.")
    
    with crop_col2:
        # Crop Yield Comparison (simulated data based on predictions)
        if crop_distribution:
            # Simulate yield data based on crop types
            yield_simulations = {
                "Rice": 1.56, "Wheat": 1.17, "Cotton": 1.70, "Sugarcane": 15.0,
                "Maize": 2.5, "Barley": 1.2, "Millets": 0.8, "Pulses": 0.6,
                "Ground Nuts": 1.0, "Oil seeds": 0.7, "Tobacco": 1.5, "Paddy": 1.8
            }
            
            crop_yield_data = {
                "Crop": list(crop_distribution.keys()),
                "Yield (Tons/Acre)": [yield_simulations.get(crop, 1.0) for crop in crop_distribution.keys()]
            }
            crop_yield_df = pd.DataFrame(crop_yield_data)
            
            fig_crop_yield = px.bar(
                crop_yield_df,
                x="Crop",
                y="Yield (Tons/Acre)",
                title="📊 Estimated Yield per Acre by Crop",
                color="Yield (Tons/Acre)",
                color_continuous_scale="Greens",
                template="plotly_dark"
            )
            fig_crop_yield.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_crop_yield, use_container_width=True)
        else:
            st.info("No crop prediction data available yet.")
    
    st.markdown("---")
    
    # === Soil Data Charts ===
    st.subheader("🧪 Soil Data Analysis")
    
    # Get user's prediction history to extract soil data
    user_predictions = prediction_history.get_user_predictions(st.session_state.username, limit=50)
    
    # Extract soil parameters from predictions
    soil_params_from_history = {
        "Nitrogen (N)": [],
        "Phosphorus (P)": [],
        "Potassium (K)": [],
        "pH Level": [],
        "Temperature": [],
        "Humidity": []
    }
    
    for pred in user_predictions:
        if pred.get("input_params"):
            params = pred["input_params"]
            if "nitrogen" in params:
                soil_params_from_history["Nitrogen (N)"].append(params["nitrogen"])
            if "phosphorous" in params:
                soil_params_from_history["Phosphorus (P)"].append(params["phosphorous"])
            if "potassium" in params:
                soil_params_from_history["Potassium (K)"].append(params["potassium"])
            if "ph" in params:
                soil_params_from_history["pH Level"].append(params["ph"])
            if "temperature" in params:
                soil_params_from_history["Temperature"].append(params["temperature"])
            if "humidity" in params:
                soil_params_from_history["Humidity"].append(params["humidity"])
    
    soil_col1, soil_col2 = st.columns(2)
    
    with soil_col1:
        # NPK Levels Chart
        if soil_params_from_history["Nitrogen (N)"]:
            # Calculate averages from history
            avg_n = sum(soil_params_from_history["Nitrogen (N)"]) / len(soil_params_from_history["Nitrogen (N)"])
            avg_p = sum(soil_params_from_history["Phosphorus (P)"]) / len(soil_params_from_history["Phosphorus (P)"])
            avg_k = sum(soil_params_from_history["Potassium (K)"]) / len(soil_params_from_history["Potassium (K)"])
            
            npk_data = {
                "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
                "Average Level": [round(avg_n, 1), round(avg_p, 1), round(avg_k, 1)],
                "Optimal Level": [80, 50, 65]
            }
            npk_df = pd.DataFrame(npk_data)
            
            fig_npk = px.bar(
                npk_df,
                x="Nutrient",
                y=["Average Level", "Optimal Level"],
                title="🧬 NPK Levels from Your Predictions (ppm)",
                barmode="group",
                template="plotly_dark",
                color_discrete_sequence=["#00cc96", "#4ecdc4"]
            )
            fig_npk.update_layout(height=400)
            st.plotly_chart(fig_npk, use_container_width=True)
        else:
            # Default NPK data
            npk_data = {
                "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
                "Current Level": [75, 45, 60],
                "Optimal Level": [80, 50, 65]
            }
            npk_df = pd.DataFrame(npk_data)
            
            fig_npk = px.bar(
                npk_df,
                x="Nutrient",
                y=["Current Level", "Optimal Level"],
                title="🧬 NPK Levels (ppm)",
                barmode="group",
                template="plotly_dark",
                color_discrete_sequence=["#00cc96", "#4ecdc4"]
            )
            fig_npk.update_layout(height=400)
            st.plotly_chart(fig_npk, use_container_width=True)
    
    with soil_col2:
        # Soil pH and Moisture
        if soil_params_from_history["pH Level"]:
            avg_ph = sum(soil_params_from_history["pH Level"]) / len(soil_params_from_history["pH Level"])
            avg_temp = sum(soil_params_from_history["Temperature"]) / len(soil_params_from_history["Temperature"])
            avg_humidity = sum(soil_params_from_history["Humidity"]) / len(soil_params_from_history["Humidity"])
            
            soil_params_data = {
                "Parameter": ["pH Level", "Temperature (°C)", "Humidity (%)"],
                "Average": [round(avg_ph, 1), round(avg_temp, 1), round(avg_humidity, 1)],
                "Optimal": [7.0, 25.0, 70.0]
            }
            soil_params_df = pd.DataFrame(soil_params_data)
            
            fig_soil_params = px.bar(
                soil_params_df,
                x="Parameter",
                y=["Average", "Optimal"],
                title="🌱 Soil Parameters from Your Predictions",
                barmode="group",
                template="plotly_dark",
                color_discrete_sequence=["#00cc96", "#4ecdc4"]
            )
            fig_soil_params.update_layout(height=400)
            st.plotly_chart(fig_soil_params, use_container_width=True)
        else:
            # Default soil parameters
            soil_params_data = {
                "Parameter": ["pH Level", "Moisture (%)", "Organic Matter (%)"],
                "Value": [6.8, 35, 2.5],
                "Optimal": [7.0, 40, 3.0]
            }
            soil_params_df = pd.DataFrame(soil_params_data)
            
            fig_soil_params = px.bar(
                soil_params_df,
                x="Parameter",
                y=["Value", "Optimal"],
                title="🌱 Soil Parameters",
                barmode="group",
                template="plotly_dark",
                color_discrete_sequence=["#00cc96", "#4ecdc4"]
            )
            fig_soil_params.update_layout(height=400)
            st.plotly_chart(fig_soil_params, use_container_width=True)
    
    st.markdown("---")
    
    # === Prediction Statistics Summary ===
    st.subheader("📊 Prediction Statistics Summary")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric(
            label="Total Predictions",
            value=str(pred_stats['total_predictions']),
            delta="All time"
        )
    
    with stats_col2:
        st.metric(
            label="Successful",
            value=str(pred_stats['successful_predictions']),
            delta=f"{pred_stats['success_rate']}% success rate"
        )
    
    with stats_col3:
        st.metric(
            label="Crop Predictions",
            value=str(pred_stats['crop_predictions']),
            delta="Crop recommendations"
        )
    
    with stats_col4:
        st.metric(
            label="Fertilizer Predictions",
            value=str(pred_stats['fertilizer_predictions']),
            delta="Fertilizer recommendations"
        )
    
    st.markdown("---")
    
    # === Prediction Trends Section ===
    st.subheader("📈 Prediction Trends")
    
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        # Monthly Prediction Trend
        monthly_trend = prediction_history.get_monthly_prediction_trend(st.session_state.username, months=12)
        
        if monthly_trend:
            trend_df = pd.DataFrame({
                "Month": list(monthly_trend.keys()),
                "Predictions": list(monthly_trend.values())
            })
            
            fig_trend = px.line(
                trend_df,
                x="Month",
                y="Predictions",
                title="📊 Monthly Prediction Trend",
                markers=True,
                template="plotly_dark",
                line_shape="spline"
            )
            fig_trend.update_traces(line=dict(color="#00cc96", width=3), marker=dict(size=10))
            fig_trend.update_layout(height=400)
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No prediction trend data available yet.")
    
    with trend_col2:
        # Location Distribution
        location_dist = prediction_history.get_location_distribution(st.session_state.username)
        
        if location_dist:
            location_df = pd.DataFrame({
                "Location": list(location_dist.keys()),
                "Predictions": list(location_dist.values())
            })
            
            fig_location = px.pie(
                location_df,
                names="Location",
                values="Predictions",
                title="📍 Predictions by Location",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            fig_location.update_layout(height=400)
            st.plotly_chart(fig_location, use_container_width=True)
        else:
            st.info("No location data available yet.")
    
    st.markdown("---")
    
    # === Farm Analytics Section ===
    st.subheader("📈 Farm Analytics & Yield Prediction")
    
    analytics_col1, analytics_col2 = st.columns([2, 1])
    
    with analytics_col1:
        # Yield Prediction Chart
        yield_data = {
            "Year": ["2020", "2021", "2022", "2023", "2024", "2025 (Predicted)"],
            "Yield (Tons)": [8.5, 9.2, 10.1, 11.3, 12.0, 12.5],
            "Revenue (₹ Lakhs)": [1.8, 2.0, 2.2, 2.4, 2.5, 2.7]
        }
        yield_df = pd.DataFrame(yield_data)
        
        fig_yield = px.line(
            yield_df,
            x="Year",
            y="Yield (Tons)",
            title="🌾 Historical Yield & Prediction",
            markers=True,
            template="plotly_dark",
            line_shape="spline"
        )
        fig_yield.update_traces(line=dict(color="#00cc96", width=3), marker=dict(size=10))
        fig_yield.update_layout(height=400)
        st.plotly_chart(fig_yield, use_container_width=True)
    
    with analytics_col2:
        st.markdown("""
        **Yield Prediction Factors**:
        - 🌡️ Temperature: Optimal
        - 💧 Rainfall: Adequate
        - 🧪 Soil Quality: Good
        - 🌱 Crop Health: Excellent
        
        **Prediction Confidence**: 94%
        
        **Recommendations**:
        - Continue current irrigation schedule
        - Apply fertilizer in 2 weeks
        - Monitor for pest activity
        """)
    
    st.markdown("---")
    
    # === Recommendations Based on History ===
    st.subheader("💡 Personalized Recommendations")
    
    if pred_stats['total_predictions'] > 0:
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("**Based on Your Prediction History:**")
            
            # Generate recommendations based on most predicted crop
            most_crop = pred_stats['most_predicted_crop']
            if most_crop != "N/A":
                st.markdown(f"- 🌱 You frequently predict **{most_crop}**. Consider diversifying your crops.")
            
            # Success rate recommendations
            if pred_stats['success_rate'] < 80:
                st.markdown("- ⚠️ Your success rate is below 80%. Review failed predictions for insights.")
            elif pred_stats['success_rate'] >= 95:
                st.markdown("- ✅ Excellent success rate! Keep using the system for optimal results.")
            
            # Prediction frequency recommendations
            if pred_stats['total_predictions'] < 10:
                st.markdown("- 📈 Make more predictions to get better personalized insights.")
            else:
                st.markdown(f"- 📊 You've made {pred_stats['total_predictions']} predictions. Great engagement!")
        
        with rec_col2:
            st.markdown("**Quick Tips:**")
            st.markdown("- 🌾 Use crop recommendations before planting season")
            st.markdown("- 🧪 Get fertilizer advice based on soil tests")
            st.markdown("- 📍 Update your location for accurate weather data")
            st.markdown("- 📅 Check crop calendar for seasonal activities")
    else:
        st.info("Make your first prediction to get personalized recommendations!")
    
    st.markdown("---")
    
    # === Crop Calendar Section ===
    st.subheader("📅 Crop Calendar")
    
    calendar_col1, calendar_col2 = st.columns([1, 1])
    
    with calendar_col1:
        st.markdown("**Current Season Activities**")
        
        calendar_data = {
            "Activity": ["Sowing", "Irrigation", "Fertilization", "Pest Control", "Harvesting"],
            "Crop": ["Rice", "Wheat", "Cotton", "Sugarcane", "Vegetables"],
            "Status": ["✅ Completed", "🔄 In Progress", "⏳ Pending", "⏳ Pending", "📅 Scheduled"],
            "Date": ["15 Jun", "20 Jul", "01 Aug", "15 Aug", "15 Oct"]
        }
        calendar_df = pd.DataFrame(calendar_data)
        st.dataframe(calendar_df, use_container_width=True)
    
    with calendar_col2:
        st.markdown("**Upcoming Tasks**")
        
        tasks = [
            {"task": "Apply fertilizer to wheat field", "date": "Tomorrow", "priority": "High"},
            {"task": "Check irrigation system", "date": "In 3 days", "priority": "Medium"},
            {"task": "Pest inspection", "date": "Next week", "priority": "High"},
            {"task": "Soil testing", "date": "In 2 weeks", "priority": "Low"},
            {"task": "Harvest planning", "date": "Next month", "priority": "Medium"}
        ]
        
        for task in tasks:
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            st.markdown(f"{priority_color[task['priority']]} **{task['task']}** - {task['date']}")
    
    st.markdown("---")
    
    # === Recent Activity Section ===
    st.subheader("🕒 Recent Activity")
    
    recent_predictions = prediction_history.get_user_predictions(st.session_state.username, limit=5)
    
    if recent_predictions:
        for i, pred in enumerate(recent_predictions):
            activity_col1, activity_col2, activity_col3 = st.columns([2, 2, 1])
            
            with activity_col1:
                st.markdown(f"**{pred.get('date', 'N/A')}**")
                st.markdown(f"{pred.get('type', 'N/A').title()} - {pred.get('crop', 'N/A')}")
            
            with activity_col2:
                st.markdown(f"📍 {pred.get('location', 'N/A')}")
                st.markdown(f"🎯 Confidence: {pred.get('confidence', 0)}%")
            
            with activity_col3:
                status_icon = "✅" if pred.get('status') == 'success' else "❌"
                st.markdown(f"{status_icon} {pred.get('status', 'N/A').title()}")
            
            if i < len(recent_predictions) - 1:
                st.markdown("---")
    else:
        st.info("No recent activity. Start making predictions!")
    
    st.markdown("---")
    
    # === Profit Estimation Section ===
    st.subheader("💰 Profit Estimation Calculator")
    st.markdown("Calculate expected yield, revenue, and profit/loss for your farming operation.")
    
    # Get available crops
    available_crops = profit_estimator.get_all_crops()
    
    # Input section
    profit_input_col1, profit_input_col2 = st.columns(2)
    
    with profit_input_col1:
        selected_crop = st.selectbox(
            "Select Crop",
            available_crops,
            help="Choose the crop you want to grow"
        )
        
        land_size = st.number_input(
            "Land Size (Acres)",
            min_value=0.1,
            max_value=1000.0,
            value=1.0,
            step=0.1,
            help="Enter your farm size in acres"
        )
    
    with profit_input_col2:
        st.markdown("**Cost Inputs (Optional)**")
        st.markdown("Leave blank to use default estimates")
        
        use_custom_costs = st.checkbox("Use custom cost inputs")
    
    # Custom cost inputs
    if use_custom_costs:
        st.markdown("---")
        st.markdown("**Enter Custom Costs (₹)**")
        
        cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)
        
        with cost_col1:
            seed_cost = st.number_input(
                "Seeds",
                min_value=0,
                value=3000,
                step=100,
                help="Cost of seeds"
            )
            fertilizer_cost = st.number_input(
                "Fertilizer",
                min_value=0,
                value=4500,
                step=100,
                help="Cost of fertilizers"
            )
        
        with cost_col2:
            irrigation_cost = st.number_input(
                "Irrigation",
                min_value=0,
                value=2500,
                step=100,
                help="Cost of irrigation"
            )
            labor_cost = st.number_input(
                "Labor",
                min_value=0,
                value=6000,
                step=100,
                help="Cost of labor"
            )
        
        with cost_col3:
            equipment_cost = st.number_input(
                "Equipment",
                min_value=0,
                value=2500,
                step=100,
                help="Cost of equipment rental"
            )
            pesticide_cost = st.number_input(
                "Pesticides",
                min_value=0,
                value=1500,
                step=100,
                help="Cost of pesticides"
            )
        
        with cost_col4:
            other_cost = st.number_input(
                "Other",
                min_value=0,
                value=1500,
                step=100,
                help="Other miscellaneous costs"
            )
    else:
        seed_cost = None
        fertilizer_cost = None
        irrigation_cost = None
        labor_cost = None
        equipment_cost = None
        pesticide_cost = None
        other_cost = None
    
    # Calculate button
    if st.button("📊 Calculate Profit", use_container_width=True):
        # Calculate profit
        profit_result = profit_estimator.calculate_profit(
            crop=selected_crop,
            land_size=land_size,
            seed_cost=seed_cost,
            fertilizer_cost=fertilizer_cost,
            irrigation_cost=irrigation_cost,
            labor_cost=labor_cost,
            equipment_cost=equipment_cost,
            pesticide_cost=pesticide_cost,
            other_cost=other_cost
        )
        
        # Save calculation to history
        profit_estimator.save_profit_calculation(st.session_state.username, profit_result)
        
        # Display results
        st.markdown("---")
        st.subheader("📈 Profit Calculation Results")
        
        # Status indicator
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            st.metric(
                label="Status",
                value=f"{profit_result['status_icon']} {profit_result['status']}",
                delta=f"₹{profit_result['profit_loss']:,.2f}"
            )
        
        with status_col2:
            st.metric(
                label="Total Revenue",
                value=f"₹{profit_result['total_revenue']:,.2f}",
                delta=f"{profit_result['total_yield']} tons"
            )
        
        with status_col3:
            st.metric(
                label="Total Cost",
                value=f"₹{profit_result['total_cost']:,.2f}",
                delta=f"ROI: {profit_result['roi']}%"
            )
        
        # Detailed breakdown
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.markdown("**Crop Details**")
            st.markdown(f"- 🌾 Crop: **{profit_result['crop']}**")
            st.markdown(f"- 📏 Land Size: **{profit_result['land_size']} acres**")
            st.markdown(f"- 🌱 Yield per Acre: **{profit_result['yield_per_acre']} tons**")
            st.markdown(f"- 💰 Price per Ton: **₹{profit_result['price_per_ton']:,}**")
            st.markdown(f"- 📅 Growing Season: **{profit_result['growing_season']}**")
            st.markdown(f"- ⏱️ Duration: **{profit_result['duration_days']} days**")
        
        with detail_col2:
            st.markdown("**Financial Summary**")
            st.markdown(f"- 💵 Total Revenue: **₹{profit_result['total_revenue']:,.2f}**")
            st.markdown(f"- 💸 Total Cost: **₹{profit_result['total_cost']:,.2f}**")
            st.markdown(f"- 📊 Profit/Loss: **₹{profit_result['profit_loss']:,.2f}**")
            st.markdown(f"- 📈 Profit Margin: **{profit_result['profit_margin']}%**")
            st.markdown(f"- 🔄 ROI: **{profit_result['roi']}%**")
        
        # Cost breakdown chart
        st.markdown("---")
        st.subheader("💸 Cost Breakdown")
        
        cost_chart_col1, cost_chart_col2 = st.columns(2)
        
        with cost_chart_col1:
            # Cost breakdown pie chart
            cost_df = pd.DataFrame({
                "Category": list(profit_result["costs"].keys()),
                "Amount (₹)": list(profit_result["costs"].values())
            })
            
            fig_cost = px.pie(
                cost_df,
                names="Category",
                values="Amount (₹)",
                title="💸 Cost Distribution",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            fig_cost.update_layout(height=400)
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with cost_chart_col2:
            # Revenue vs Cost bar chart
            comparison_df = pd.DataFrame({
                "Category": ["Revenue", "Cost", "Profit/Loss"],
                "Amount (₹)": [
                    profit_result["total_revenue"],
                    profit_result["total_cost"],
                    profit_result["profit_loss"]
                ]
            })
            
            fig_comparison = px.bar(
                comparison_df,
                x="Category",
                y="Amount (₹)",
                title="💰 Revenue vs Cost vs Profit",
                color="Category",
                color_discrete_sequence=["#00cc96", "#ff6b6b", "#4ecdc4"],
                template="plotly_dark"
            )
            fig_comparison.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Cost breakdown table
        st.markdown("**Detailed Cost Breakdown**")
        
        cost_table_data = {
            "Cost Type": [],
            "Amount (₹)": [],
            "Percentage": []
        }
        
        for cost_type, amount in profit_result["costs"].items():
            percentage = (amount / profit_result["total_cost"] * 100) if profit_result["total_cost"] > 0 else 0
            cost_table_data["Cost Type"].append(cost_type.title())
            cost_table_data["Amount (₹)"].append(f"₹{amount:,.2f}")
            cost_table_data["Percentage"].append(f"{percentage:.1f}%")
        
        cost_table_df = pd.DataFrame(cost_table_data)
        st.dataframe(cost_table_df, use_container_width=True)
    
    # Profit history section
    st.markdown("---")
    st.subheader("📜 Profit Calculation History")
    
    profit_history = profit_estimator.get_profit_history(st.session_state.username, limit=10)
    
    if profit_history:
        history_data = {
            "Date": [],
            "Crop": [],
            "Land (Acres)": [],
            "Revenue (₹)": [],
            "Cost (₹)": [],
            "Profit/Loss (₹)": [],
            "Status": []
        }
        
        for calc in profit_history:
            history_data["Date"].append(calc.get("timestamp", "N/A")[:10])
            history_data["Crop"].append(calc.get("crop", "N/A"))
            history_data["Land (Acres)"].append(calc.get("land_size", 0))
            history_data["Revenue (₹)"].append(f"₹{calc.get('total_revenue', 0):,.2f}")
            history_data["Cost (₹)"].append(f"₹{calc.get('total_cost', 0):,.2f}")
            history_data["Profit/Loss (₹)"].append(f"₹{calc.get('profit_loss', 0):,.2f}")
            status = "✅ Profit" if calc.get("profit_loss", 0) > 0 else "❌ Loss" if calc.get("profit_loss", 0) < 0 else "⚖️ Break-even"
            history_data["Status"].append(status)
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
        
        # Profit statistics
        profit_stats = profit_estimator.get_profit_stats(st.session_state.username)
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric(
                label="Total Calculations",
                value=str(profit_stats["total_calculations"]),
                delta="All time"
            )
        
        with stat_col2:
            st.metric(
                label="Average Profit",
                value=f"₹{profit_stats['avg_profit']:,.2f}",
                delta="Per calculation"
            )
        
        with stat_col3:
            st.metric(
                label="Best Crop",
                value=profit_stats["best_crop"],
                delta=f"₹{profit_stats['best_profit']:,.2f}"
            )
        
        with stat_col4:
            st.metric(
                label="Total Land Analyzed",
                value=f"{profit_stats['total_land_analyzed']} acres",
                delta="Cumulative"
            )
    else:
        st.info("No profit calculations yet. Use the calculator above to estimate your profits!")
    
    st.markdown("---")
    
    # === Prediction History Trends ===
    st.subheader("📈 Prediction History Trends")
    
    if pred_stats['total_predictions'] > 0:
        trend_viz_col1, trend_viz_col2 = st.columns(2)
        
        with trend_viz_col1:
            # Prediction type distribution
            type_data = {
                "Type": ["Crop", "Fertilizer"],
                "Count": [pred_stats['crop_predictions'], pred_stats['fertilizer_predictions']]
            }
            type_df = pd.DataFrame(type_data)
            
            fig_type = px.pie(
                type_df,
                names="Type",
                values="Count",
                title="🌾 Prediction Type Distribution",
                template="plotly_dark",
                color_discrete_sequence=["#00cc96", "#4ecdc4"]
            )
            fig_type.update_layout(height=400)
            st.plotly_chart(fig_type, use_container_width=True)
        
        with trend_viz_col2:
            # Success rate gauge
            fig_gauge = px.bar(
                x=["Success Rate"],
                y=[pred_stats['success_rate']],
                title="✅ Prediction Success Rate",
                template="plotly_dark",
                color=[pred_stats['success_rate']],
                color_continuous_scale="Greens"
            )
            fig_gauge.update_layout(height=400, showlegend=False)
            fig_gauge.update_yaxes(range=[0, 100])
            st.plotly_chart(fig_gauge, use_container_width=True)
    else:
        st.info("Make predictions to see trend analysis!")
    
    st.markdown("---")
    
    # === Equipment Recommendation Section ===
    st.subheader("🚜 Equipment Recommendation")
    st.markdown("Get personalized equipment recommendations based on your crop and farm size.")
    
    # Get user's farm size from profile
    user_profile = auth.get_user_profile(st.session_state.username)
    default_farm_size = 1.0
    if user_profile.get('farm_size') and user_profile['farm_size'] != 'Not specified':
        try:
            default_farm_size = float(user_profile['farm_size'].split()[0])
        except:
            pass
    
    equip_col1, equip_col2 = st.columns(2)
    
    with equip_col1:
        equip_crop = st.selectbox(
            "Select Crop",
            profit_estimator.get_all_crops(),
            key="equip_crop_select",
            help="Choose the crop you want equipment for"
        )
    
    with equip_col2:
        equip_farm_size = st.number_input(
            "Farm Size (Acres)",
            min_value=0.1,
            max_value=1000.0,
            value=default_farm_size,
            step=0.1,
            key="equip_farm_size",
            help="Enter your farm size in acres"
        )
    
    if st.button("🔍 Get Equipment Recommendations", use_container_width=True):
        # Get equipment recommendations
        equip_recommendation = equipment_recommender.get_equipment_recommendation_summary(
            equip_crop, 
            equip_farm_size
        )
        
        # Save recommendation to history
        equipment_recommender.save_equipment_recommendation(
            st.session_state.username, 
            equip_recommendation
        )
        
        # Display recommendations
        st.markdown("---")
        st.subheader(f"📋 Equipment for {equip_crop} ({equip_farm_size} acres)")
        
        # Notes
        st.info(f"💡 **Note:** {equip_recommendation['notes']}")
        
        # Essential Equipment
        st.markdown("### ✅ Essential Equipment")
        st.markdown("These are critical for successful cultivation.")
        
        essential_cols = st.columns(3)
        for i, equipment in enumerate(equip_recommendation['essential']['equipment']):
            with essential_cols[i % 3]:
                equip_details = equipment_recommender.get_equipment_details(equipment)
                with st.expander(f"🔧 {equipment}", expanded=False):
                    st.markdown(f"**Category:** {equip_details['category']}")
                    st.markdown(f"**Description:** {equip_details['description']}")
                    st.markdown(f"**Uses:** {', '.join(equip_details['uses'])}")
                    st.markdown(f"**Price Range:** {equip_details['price_range']}")
                    st.markdown(f"**Fuel Type:** {equip_details['fuel_type']}")
                    st.markdown(f"**Maintenance:** {equip_details['maintenance']}")
                    st.markdown(f"**Lifespan:** {equip_details['lifespan']}")
        
        st.metric(
            label="Essential Equipment Cost",
            value=f"₹{equip_recommendation['essential']['cost']:,}",
            delta=f"{len(equip_recommendation['essential']['equipment'])} items"
        )
        
        # Recommended Equipment
        st.markdown("### 📌 Recommended Equipment")
        st.markdown("These will improve efficiency and yield.")
        
        recommended_cols = st.columns(3)
        for i, equipment in enumerate(equip_recommendation['recommended']['equipment']):
            with recommended_cols[i % 3]:
                equip_details = equipment_recommender.get_equipment_details(equipment)
                with st.expander(f"🔧 {equipment}", expanded=False):
                    st.markdown(f"**Category:** {equip_details['category']}")
                    st.markdown(f"**Description:** {equip_details['description']}")
                    st.markdown(f"**Uses:** {', '.join(equip_details['uses'])}")
                    st.markdown(f"**Price Range:** {equip_details['price_range']}")
                    st.markdown(f"**Fuel Type:** {equip_details['fuel_type']}")
                    st.markdown(f"**Maintenance:** {equip_details['maintenance']}")
                    st.markdown(f"**Lifespan:** {equip_details['lifespan']}")
        
        st.metric(
            label="Recommended Equipment Cost",
            value=f"₹{equip_recommendation['recommended']['cost']:,}",
            delta=f"{len(equip_recommendation['recommended']['equipment'])} items"
        )
        
        # Optional Equipment
        st.markdown("### ➕ Optional Equipment")
        st.markdown("These are nice-to-have for advanced farming.")
        
        optional_cols = st.columns(3)
        for i, equipment in enumerate(equip_recommendation['optional']['equipment']):
            with optional_cols[i % 3]:
                equip_details = equipment_recommender.get_equipment_details(equipment)
                with st.expander(f"🔧 {equipment}", expanded=False):
                    st.markdown(f"**Category:** {equip_details['category']}")
                    st.markdown(f"**Description:** {equip_details['description']}")
                    st.markdown(f"**Uses:** {', '.join(equip_details['uses'])}")
                    st.markdown(f"**Price Range:** {equip_details['price_range']}")
                    st.markdown(f"**Fuel Type:** {equip_details['fuel_type']}")
                    st.markdown(f"**Maintenance:** {equip_details['maintenance']}")
                    st.markdown(f"**Lifespan:** {equip_details['lifespan']}")
        
        st.metric(
            label="Optional Equipment Cost",
            value=f"₹{equip_recommendation['optional']['cost']:,}",
            delta=f"{len(equip_recommendation['optional']['equipment'])} items"
        )
        
        # Total Summary
        st.markdown("---")
        st.subheader("💰 Total Investment Summary")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.metric(
                label="Total Equipment",
                value=str(equip_recommendation['total_equipment']),
                delta="Items"
            )
        
        with summary_col2:
            st.metric(
                label="Total Investment",
                value=f"₹{equip_recommendation['total_cost']:,}",
                delta="Estimated"
            )
        
        with summary_col3:
            cost_per_acre = equip_recommendation['total_cost'] / equip_farm_size
            st.metric(
                label="Cost per Acre",
                value=f"₹{cost_per_acre:,.0f}",
                delta="Average"
            )
        
        # Equipment categories chart
        st.markdown("---")
        st.subheader("📊 Equipment by Category")
        
        all_equipment = (
            equip_recommendation['essential']['equipment'] +
            equip_recommendation['recommended']['equipment'] +
            equip_recommendation['optional']['equipment']
        )
        
        category_counts = {}
        for equipment in all_equipment:
            equip_details = equipment_recommender.get_equipment_details(equipment)
            category = equip_details['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        category_df = pd.DataFrame({
            "Category": list(category_counts.keys()),
            "Count": list(category_counts.values())
        })
        
        fig_category = px.pie(
            category_df,
            names="Category",
            values="Count",
            title="🔧 Equipment Distribution by Category",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig_category.update_layout(height=400)
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Equipment history
    st.markdown("---")
    st.subheader("📜 Equipment Recommendation History")
    
    equip_history = equipment_recommender.get_equipment_history(st.session_state.username, limit=5)
    
    if equip_history:
        history_data = {
            "Date": [],
            "Crop": [],
            "Farm Size": [],
            "Total Equipment": [],
            "Total Cost (₹)": []
        }
        
        for rec in equip_history:
            history_data["Date"].append(rec.get("timestamp", "N/A")[:10])
            history_data["Crop"].append(rec.get("crop", "N/A"))
            history_data["Farm Size"].append(f"{rec.get('farm_size', 0)} acres")
            history_data["Total Equipment"].append(rec.get("total_equipment", 0))
            history_data["Total Cost (₹)"].append(f"₹{rec.get('total_cost', 0):,}")
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No equipment recommendations yet. Use the calculator above to get started!")
    
    st.markdown("---")
    
    # === Organic Farming Suggestions Section ===
    st.subheader("🌱 Organic Farming Suggestions")
    st.markdown("Natural fertilizers, organic alternatives, and composting tips for sustainable farming.")
    
    # Get user's crop from profile or prediction history
    user_predictions = prediction_history.get_user_predictions(st.session_state.username, limit=1)
    default_crop = "Rice"
    if user_predictions:
        default_crop = user_predictions[0].get("crop", "Rice")
    
    organic_col1, organic_col2 = st.columns(2)
    
    with organic_col1:
        organic_crop = st.selectbox(
            "Select Crop",
            organic_farming.get_all_crops(),
            index=organic_farming.get_all_crops().index(default_crop) if default_crop in organic_farming.get_all_crops() else 0,
            key="organic_crop_select",
            help="Choose crop for organic recommendations"
        )
    
    with organic_col2:
        organic_section = st.selectbox(
            "Select Section",
            ["Natural Fertilizers", "Organic Pesticides", "Composting Tips"],
            key="organic_section_select",
            help="Choose section to view"
        )
    
    if organic_section == "Natural Fertilizers":
        st.markdown("### 🧪 Natural Fertilizers")
        
        organic_summary = organic_farming.get_organic_farming_summary(organic_crop)
        
        for fert in organic_summary["fertilizers"]:
            with st.expander(f"🌿 {fert['name']}", expanded=False):
                st.markdown(f"**Description:** {fert['description']}")
                st.markdown(f"**Application:** {fert['application']}")
                st.markdown(f"**Cost:** {fert['cost']}")
                
                details = organic_farming.get_fertilizer_details(fert['name'])
                if details:
                    st.markdown("**Benefits:**")
                    for benefit in details.get("benefits", []):
                        st.markdown(f"- {benefit}")
                    st.markdown(f"**Preparation:** {details.get('preparation', 'N/A')}")
    
    elif organic_section == "Organic Pesticides":
        st.markdown("### 🐛 Organic Pesticides")
        
        organic_summary = organic_farming.get_organic_farming_summary(organic_crop)
        
        for pest in organic_summary["pesticides"]:
            with st.expander(f"🛡️ {pest['name']}", expanded=False):
                st.markdown(f"**Description:** {pest['description']}")
                st.markdown(f"**Targets:** {pest['targets']}")
                st.markdown(f"**Preparation:** {pest['preparation']}")
                
                details = organic_farming.get_pesticide_details(pest['name'])
                if details:
                    st.markdown(f"**Application:** {details.get('application', 'N/A')}")
                    st.markdown(f"**Safety:** {details.get('safety', 'N/A')}")
    
    else:  # Composting Tips
        st.markdown("### 🗑️ Composting Tips")
        
        composting_methods = ["Basic Composting", "Vermicomposting", "Bokashi Composting", "Pit Composting"]
        
        for method in composting_methods:
            with st.expander(f"📦 {method}", expanded=False):
                tips = organic_farming.get_composting_tips(method)
                
                st.markdown("**Materials Needed:**")
                for material in tips.get("materials", []):
                    st.markdown(f"- {material}")
                
                st.markdown("**Steps:**")
                for i, step in enumerate(tips.get("steps", []), 1):
                    st.markdown(f"{i}. {step}")
                
                st.markdown("**Tips:**")
                for tip in tips.get("tips", []):
                    st.markdown(f"- {tip}")
    
    # Crop-specific organic tips
    st.markdown("---")
    st.markdown(f"### 💡 Organic Tips for {organic_crop}")
    
    organic_summary = organic_farming.get_organic_farming_summary(organic_crop)
    for tip in organic_summary["tips"]:
        st.markdown(f"- {tip}")
    
    st.markdown("---")
    
    # === Risk Analysis System Section ===
    st.subheader("⚠️ Risk Analysis System")
    st.markdown("Predict crop failure risk based on environmental conditions.")
    
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        risk_crop = st.selectbox(
            "Select Crop",
            risk_analyzer.get_all_crops(),
            index=risk_analyzer.get_all_crops().index(default_crop) if default_crop in risk_analyzer.get_all_crops() else 0,
            key="risk_crop_select",
            help="Choose crop for risk analysis"
        )
    
    with risk_col2:
        st.markdown("**Enter Environmental Conditions**")
    
    # Environmental inputs
    risk_input_col1, risk_input_col2, risk_input_col3 = st.columns(3)
    
    with risk_input_col1:
        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0,
            max_value=500,
            value=100,
            step=10,
            key="risk_rainfall",
            help="Expected rainfall in mm"
        )
        
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0,
            max_value=50,
            value=25,
            step=1,
            key="risk_temperature",
            help="Average temperature in Celsius"
        )
    
    with risk_input_col2:
        soil_ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1,
            key="risk_soil_ph",
            help="Soil pH level"
        )
        
        humidity = st.number_input(
            "Humidity (%)",
            min_value=0,
            max_value=100,
            value=70,
            step=5,
            key="risk_humidity",
            help="Average humidity percentage"
        )
    
    with risk_input_col3:
        soil_nitrogen = st.number_input(
            "Soil Nitrogen (ppm)",
            min_value=0,
            max_value=200,
            value=60,
            step=10,
            key="risk_soil_nitrogen",
            help="Soil nitrogen content in ppm"
        )
    
    if st.button("🔍 Analyze Risk", use_container_width=True):
        # Analyze risk
        risk_result = risk_analyzer.analyze_crop_risk(
            crop=risk_crop,
            rainfall=rainfall,
            temperature=temperature,
            soil_ph=soil_ph,
            humidity=humidity,
            soil_nitrogen=soil_nitrogen
        )
        
        # Save to history
        risk_analyzer.save_risk_analysis(st.session_state.username, risk_result)
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Risk Analysis Results")
        
        # Overall risk indicator
        risk_col1, risk_col2, risk_col3 = st.columns(3)
        
        with risk_col1:
            st.metric(
                label="Overall Risk Level",
                value=f"{risk_result['risk_icon']} {risk_result['risk_level']}",
                delta=f"Score: {risk_result['overall_score']}"
            )
        
        with risk_col2:
            st.metric(
                label="Crop",
                value=risk_result['crop'],
                delta="Analyzed"
            )
        
        with risk_col3:
            st.metric(
                label="Risk Score",
                value=f"{risk_result['overall_score']}/100",
                delta="Lower is better"
            )
        
        # Risk description
        st.info(f"**{risk_result['description']}**")
        
        # Factor breakdown
        st.markdown("### 📈 Factor Breakdown")
        
        factor_col1, factor_col2 = st.columns(2)
        
        with factor_col1:
            for factor_name, factor_data in list(risk_result['factors'].items())[:3]:
                st.markdown(f"**{factor_data['factor'].title()}**")
                st.markdown(f"- Value: {factor_data['value']}")
                st.markdown(f"- Optimal: {factor_data['optimal_range'][0]} - {factor_data['optimal_range'][1]}")
                st.markdown(f"- Risk: {factor_data['risk_level'].title()}")
                st.markdown(f"- Deviation: {factor_data['deviation']}%")
                st.markdown("---")
        
        with factor_col2:
            for factor_name, factor_data in list(risk_result['factors'].items())[3:]:
                st.markdown(f"**{factor_data['factor'].title()}**")
                st.markdown(f"- Value: {factor_data['value']}")
                st.markdown(f"- Optimal: {factor_data['optimal_range'][0]} - {factor_data['optimal_range'][1]}")
                st.markdown(f"- Risk: {factor_data['risk_level'].title()}")
                st.markdown(f"- Deviation: {factor_data['deviation']}%")
                st.markdown("---")
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        for i, rec in enumerate(risk_result['recommendations'], 1):
            st.markdown(f"{i}. {rec}")
    
    # Risk history
    st.markdown("---")
    st.subheader("📜 Risk Analysis History")
    
    risk_history = risk_analyzer.get_risk_history(st.session_state.username, limit=5)
    
    if risk_history:
        history_data = {
            "Date": [],
            "Crop": [],
            "Risk Level": [],
            "Score": [],
            "Rainfall": [],
            "Temperature": []
        }
        
        for analysis in risk_history:
            history_data["Date"].append(analysis.get("timestamp", "N/A")[:10])
            history_data["Crop"].append(analysis.get("crop", "N/A"))
            history_data["Risk Level"].append(f"{analysis.get('risk_icon', '')} {analysis.get('risk_level', 'N/A')}")
            history_data["Score"].append(analysis.get("overall_score", 0))
            history_data["Rainfall"].append(analysis.get("factors", {}).get("rainfall", {}).get("value", 0))
            history_data["Temperature"].append(analysis.get("factors", {}).get("temperature", {}).get("value", 0))
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No risk analyses yet. Use the calculator above to get started!")
    
    st.markdown("---")
    
    # === Crop Comparison Mode Section ===
    st.subheader("📊 Comparison Mode")
    st.markdown("Compare two crops side-by-side across multiple features.")
    
    compare_col1, compare_col2 = st.columns(2)
    
    with compare_col1:
        crop1 = st.selectbox(
            "Select First Crop",
            crop_comparator.get_all_crops(),
            index=0,
            key="compare_crop1",
            help="Choose first crop to compare"
        )
    
    with compare_col2:
        crop2 = st.selectbox(
            "Select Second Crop",
            crop_comparator.get_all_crops(),
            index=1,
            key="compare_crop2",
            help="Choose second crop to compare"
        )
    
    if st.button("📊 Compare Crops", use_container_width=True):
        # Compare crops
        comparison = crop_comparator.compare_crops(crop1, crop2)
        
        if "error" not in comparison:
            # Display comparison results
            st.markdown("---")
            st.subheader(f"📈 {crop1} vs {crop2}")
            
            # Summary
            summary = comparison["summary"]
            st.info(f"**{summary['recommendation']}**")
            
            # Comparison table
            st.markdown("### 📋 Feature Comparison")
            
            comparison_data = {
                "Feature": [],
                crop1: [],
                crop2: [],
                "Winner": []
            }
            
            for feature_key, feature_info in comparison["features"].items():
                comparison_data["Feature"].append(feature_info["name"])
                
                # Format values with units
                value1 = feature_info["crop1_value"]
                value2 = feature_info["crop2_value"]
                unit = feature_info["unit"]
                
                if unit:
                    comparison_data[crop1].append(f"{value1} {unit}")
                    comparison_data[crop2].append(f"{value2} {unit}")
                else:
                    comparison_data[crop1].append(str(value1))
                    comparison_data[crop2].append(str(value2))
                
                comparison_data["Winner"].append(feature_info["winner"])
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
            
            # Visual comparison
            st.markdown("### 📊 Visual Comparison")
            
            # Bar chart for numeric features
            numeric_features = ["Profit per Acre", "Yield per Acre", "Price per Ton", "Cost per Acre"]
            
            chart_data = {
                "Feature": [],
                crop1: [],
                crop2: []
            }
            
            for feature_key, feature_info in comparison["features"].items():
                if feature_info["name"] in numeric_features:
                    chart_data["Feature"].append(feature_info["name"])
                    chart_data[crop1].append(feature_info["crop1_value"])
                    chart_data[crop2].append(feature_info["crop2_value"])
            
            if chart_data["Feature"]:
                chart_df = pd.DataFrame(chart_data)
                
                fig_compare = px.bar(
                    chart_df,
                    x="Feature",
                    y=[crop1, crop2],
                    title=f"📊 {crop1} vs {crop2} Comparison",
                    barmode="group",
                    template="plotly_dark",
                    color_discrete_sequence=["#00cc96", "#4ecdc4"]
                )
                fig_compare.update_layout(height=400)
                st.plotly_chart(fig_compare, use_container_width=True)
            
            # Priority-based recommendation
            st.markdown("### 🎯 Priority-Based Recommendation")
            
            priority = st.selectbox(
                "Select Your Priority",
                ["profit", "water", "labor", "duration", "market"],
                key="compare_priority",
                help="Choose what matters most to you"
            )
            
            priority_rec = crop_comparator.get_crop_recommendation_comparison(crop1, crop2, priority)
            
            if "error" not in priority_rec:
                st.success(f"**{priority_rec['recommendation']}**")
                st.markdown(f"- {crop1}: {priority_rec['crop1_value']}")
                st.markdown(f"- {crop2}: {priority_rec['crop2_value']}")
        else:
            st.error(comparison["error"])
    
    st.markdown("---")
    
    # === Nearby Crop Recommendation Section ===
    st.subheader("📍 Nearby Crop Recommendation")
    st.markdown("Discover what crops farmers near your location are growing.")
    
    # Get user's location from profile
    user_profile = auth.get_user_profile(st.session_state.username)
    default_state = "Tamil Nadu"
    default_city = "Chennai"
    
    if user_profile.get('location') and user_profile['location'] != 'Not specified':
        location_parts = user_profile['location'].split(',')
        if len(location_parts) >= 2:
            default_city = location_parts[0].strip()
            default_state = location_parts[1].strip()
    
    nearby_col1, nearby_col2 = st.columns(2)
    
    with nearby_col1:
        nearby_state = st.selectbox(
            "Select State",
            nearby_crops.get_all_states(),
            index=nearby_crops.get_all_states().index(default_state) if default_state in nearby_crops.get_all_states() else 0,
            key="nearby_state_select",
            help="Choose your state"
        )
    
    with nearby_col2:
        nearby_city = st.selectbox(
            "Select City",
            nearby_crops.get_cities_in_state(nearby_state),
            key="nearby_city_select",
            help="Choose your city"
        )
    
    if st.button("🔍 Find Nearby Crops", use_container_width=True):
        # Get nearby crop recommendations
        nearby_result = nearby_crops.get_location_based_recommendations(
            state=nearby_state,
            city=nearby_city,
            farm_size=float(user_profile.get('farm_size', '1').split()[0]) if user_profile.get('farm_size') and user_profile['farm_size'] != 'Not specified' else 1.0
        )
        
        if "error" not in nearby_result:
            # Display results
            st.markdown("---")
            st.subheader(f"🌾 Crops Grown Near {nearby_city}, {nearby_state}")
            
            # Location info
            location_info = nearby_result["location"]
            
            info_col1, info_col2, info_col3 = st.columns(3)
            
            with info_col1:
                st.metric(
                    label="Climate",
                    value=location_info["climate"],
                    delta="Region type"
                )
            
            with info_col2:
                st.metric(
                    label="Rainfall",
                    value=f"{location_info['rainfall_mm']} mm",
                    delta="Annual average"
                )
            
            with info_col3:
                st.metric(
                    label="Temperature",
                    value=location_info["temperature_range"],
                    delta="Range"
                )
            
            # Popular crops
            st.markdown("### 🌱 Popular Crops in Your Area")
            
            popular_crops = nearby_result["popular_crops"]
            crop_details = nearby_result["crop_details"]
            
            for i, crop in enumerate(popular_crops):
                with st.expander(f"🌾 {crop}", expanded=(i == 0)):
                    details = crop_details[i] if i < len(crop_details) else {}
                    
                    st.markdown(f"**Yield per Acre:** {details.get('yield_per_acre', 0)} tons")
                    st.markdown(f"**Price per Ton:** ₹{details.get('price_per_ton', 0):,}")
                    st.markdown(f"**Season:** {details.get('season', 'Annual')}")
                    st.markdown(f"**Duration:** {details.get('duration_days', 120)} days")
            
            # Profit estimates
            st.markdown("### 💰 Profit Estimates for Popular Crops")
            
            profit_estimates = nearby_result["profit_estimates"]
            
            profit_data = {
                "Crop": [],
                "Profit (₹)": [],
                "Revenue (₹)": [],
                "Cost (₹)": [],
                "Yield (tons)": []
            }
            
            for estimate in profit_estimates:
                profit_data["Crop"].append(estimate["crop"])
                profit_data["Profit (₹)"].append(f"₹{estimate['profit']:,}")
                profit_data["Revenue (₹)"].append(f"₹{estimate['revenue']:,}")
                profit_data["Cost (₹)"].append(f"₹{estimate['cost']:,}")
                profit_data["Yield (tons)"].append(f"{estimate['yield']:.2f}")
            
            profit_df = pd.DataFrame(profit_data)
            st.dataframe(profit_df, use_container_width=True)
            
            # Equipment recommendations
            st.markdown("### 🚜 Equipment for Top Crops")
            
            equipment_recs = nearby_result["equipment_recommendations"]
            
            for crop, equip_info in list(equipment_recs.items())[:3]:
                with st.expander(f"🔧 {crop} Equipment", expanded=False):
                    st.markdown(f"**Essential Equipment:**")
                    for equip in equip_info["essential"]:
                        st.markdown(f"- {equip}")
                    st.markdown(f"**Total Cost:** ₹{equip_info['total_cost']:,}")
            
            # Notes
            st.info(f"💡 **Note:** {nearby_result['notes']}")
        else:
            st.error(nearby_result["error"])
    
    st.markdown("---")
    
    # === Storage & Preservation Tips Section ===
    st.subheader("📦 Storage & Preservation Tips")
    st.markdown("Learn how to store crops properly and avoid spoilage.")
    
    storage_col1, storage_col2 = st.columns(2)
    
    with storage_col1:
        storage_crop = st.selectbox(
            "Select Crop",
            storage_tips.get_all_crops(),
            index=storage_tips.get_all_crops().index(default_crop) if default_crop in storage_tips.get_all_crops() else 0,
            key="storage_crop_select",
            help="Choose crop for storage tips"
        )
    
    with storage_col2:
        storage_section = st.selectbox(
            "Select Section",
            ["Storage Tips", "Spoilage Signs", "Prevention Tips", "Best Practices"],
            key="storage_section_select",
            help="Choose section to view"
        )
    
    # Get storage summary
    storage_summary = storage_tips.get_storage_summary(storage_crop)
    
    if "error" not in storage_summary:
        # Display storage info
        st.markdown("---")
        st.subheader(f"📦 {storage_crop} Storage Guide")
        
        # Storage conditions
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            st.metric(
                label="Storage Method",
                value=storage_summary["storage_method"],
                delta="Recommended"
            )
        
        with info_col2:
            st.metric(
                label="Ideal Temperature",
                value=storage_summary["ideal_temperature"],
                delta="Range"
            )
        
        with info_col3:
            st.metric(
                label="Ideal Humidity",
                value=storage_summary["ideal_humidity"],
                delta="Range"
            )
        
        st.metric(
            label="Shelf Life",
            value=storage_summary["shelf_life"],
            delta="When stored properly"
        )
        
        # Display selected section
        if storage_section == "Storage Tips":
            st.markdown("### 💡 Storage Tips")
            for tip in storage_summary["storage_tips"]:
                st.markdown(f"- {tip}")
        
        elif storage_section == "Spoilage Signs":
            st.markdown("### ⚠️ Signs of Spoilage")
            for sign in storage_summary["spoilage_signs"]:
                st.markdown(f"- {sign}")
        
        elif storage_section == "Prevention Tips":
            st.markdown("### 🛡️ Spoilage Prevention")
            for tip in storage_summary["prevention_tips"]:
                st.markdown(f"- {tip}")
        
        else:  # Best Practices
            st.markdown("### ✅ Best Practices")
            for practice in storage_summary["best_practices"]:
                st.markdown(f"- {practice}")
        
        # Spoilage prevention checklist
        st.markdown("---")
        st.markdown("### 📋 Spoilage Prevention Checklist")
        
        checklist = storage_tips.get_spoilage_prevention_checklist(storage_crop)
        
        if "error" not in checklist:
            for item in checklist["checklist"]:
                st.checkbox(
                    item["task"],
                    value=item["completed"],
                    key=f"checklist_{item['task']}"
                )
    else:
        st.error(storage_summary["error"])
    
    # General storage tips
    st.markdown("---")
    st.markdown("### 📚 General Storage Tips")
    
    general_tips = storage_tips.get_general_storage_tips()
    
    general_col1, general_col2 = st.columns(2)
    
    with general_col1:
        st.markdown("**🌡️ Temperature Control**")
        for tip in general_tips["temperature_control"]:
            st.markdown(f"- {tip}")
        
        st.markdown("**💧 Humidity Control**")
        for tip in general_tips["humidity_control"]:
            st.markdown(f"- {tip}")
    
    with general_col2:
        st.markdown("**🐛 Pest Control**")
        for tip in general_tips["pest_control"]:
            st.markdown(f"- {tip}")
        
        st.markdown("**📦 Container Selection**")
        for tip in general_tips["container_selection"]:
            st.markdown(f"- {tip}")
    
    st.markdown("---")
    
    # === Weather History Trends ===
    st.subheader("🌦️ Weather History Trends")
    
    weather_col1, weather_col2 = st.columns([2, 1])
    
    with weather_col1:
        # Weather Trends Chart
        weather_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Temperature (°C)": [22, 25, 30, 35, 38, 35, 32, 30, 28, 26, 24, 22],
            "Rainfall (mm)": [15, 20, 30, 45, 80, 150, 200, 180, 120, 60, 25, 15],
            "Humidity (%)": [65, 60, 55, 50, 55, 70, 85, 85, 80, 70, 65, 65]
        }
        weather_df = pd.DataFrame(weather_data)
        
        fig_weather = px.line(
            weather_df,
            x="Month",
            y=["Temperature (°C)", "Rainfall (mm)", "Humidity (%)"],
            title="🌦️ Monthly Weather Trends",
            markers=True,
            template="plotly_dark"
        )
        fig_weather.update_layout(height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_weather, use_container_width=True)
    
    with weather_col2:
        st.markdown("**Current Weather**")
        
        st.markdown("""
        🌡️ **Temperature**: 28°C
        💧 **Humidity**: 75%
        🌧️ **Rainfall**: Light rain expected
        💨 **Wind**: 12 km/h
        
        **Weather Alert**:
        ⚠️ Heavy rainfall expected next week. Plan irrigation accordingly.
        """)
        
        st.markdown("**Seasonal Forecast**")
        st.markdown("""
        - **Monsoon**: Normal (Jun-Sep)
        - **Winter**: Mild (Nov-Feb)
        - **Summer**: Hot (Mar-May)
        """)
    
    st.markdown("---")
    
    # === Most Recent Predictions ===
    st.subheader("📋 Most Recent Predictions")
    
    if user_predictions:
        # Create a more detailed table of recent predictions
        recent_data = {
            "Date": [],
            "Type": [],
            "Crop/Fertilizer": [],
            "Location": [],
            "Confidence": [],
            "Status": []
        }
        
        for pred in user_predictions[:10]:  # Show last 10 predictions
            recent_data["Date"].append(pred.get("date", "N/A"))
            recent_data["Type"].append(pred.get("type", "N/A").title())
            recent_data["Crop/Fertilizer"].append(pred.get("crop", "N/A"))
            recent_data["Location"].append(pred.get("location", "N/A"))
            recent_data["Confidence"].append(f"{pred.get('confidence', 0)}%")
            status = "✅ Success" if pred.get("status") == "success" else "❌ Failed"
            recent_data["Status"].append(status)
        
        recent_df = pd.DataFrame(recent_data)
        st.dataframe(recent_df, use_container_width=True)
        
        # Add a chart showing prediction frequency by date
        if len(user_predictions) > 1:
            date_counts = {}
            for pred in user_predictions:
                date = pred.get("date", "N/A")
                if date != "N/A":
                    date_counts[date] = date_counts.get(date, 0) + 1
            
            if date_counts:
                date_df = pd.DataFrame({
                    "Date": list(date_counts.keys()),
                    "Predictions": list(date_counts.values())
                })
                
                fig_date = px.bar(
                    date_df,
                    x="Date",
                    y="Predictions",
                    title="📊 Predictions by Date",
                    template="plotly_dark",
                    color="Predictions",
                    color_continuous_scale="Greens"
                )
                fig_date.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig_date, use_container_width=True)
    else:
        st.info("No predictions yet. Start making predictions to see your history!")
    
    st.markdown("---")
    
    # === Crop Health Monitoring ===
    st.subheader("🌱 Crop Health Monitoring")
    
    health_col1, health_col2, health_col3 = st.columns(3)
    
    with health_col1:
        st.markdown("**Rice Field**")
        st.progress(85)
        st.markdown("Health: 85% - Good")
        st.markdown("Last checked: 2 days ago")
    
    with health_col2:
        st.markdown("**Wheat Field**")
        st.progress(92)
        st.markdown("Health: 92% - Excellent")
        st.markdown("Last checked: 1 day ago")
    
    with health_col3:
        st.markdown("**Vegetable Garden**")
        st.progress(78)
        st.markdown("Health: 78% - Fair")
        st.markdown("Last checked: 3 days ago")
    
    st.markdown("---")
    
    # === Prediction History Analysis ===
    st.subheader("🔍 Prediction History Analysis")
    
    if pred_stats['total_predictions'] > 0:
        analysis_col1, analysis_col2 = st.columns(2)
        
        with analysis_col1:
            st.markdown("**Performance Metrics**")
            
            # Calculate average confidence
            all_confidences = [p.get('confidence', 0) for p in user_predictions if p.get('confidence')]
            avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0
            
            st.metric(
                label="Average Confidence",
                value=f"{avg_confidence:.1f}%",
                delta="Across all predictions"
            )
            
            # Calculate prediction frequency
            if len(user_predictions) > 1:
                first_date = user_predictions[-1].get('date', '')
                last_date = user_predictions[0].get('date', '')
                if first_date and last_date:
                    from datetime import datetime
                    try:
                        d1 = datetime.strptime(first_date, '%Y-%m-%d')
                        d2 = datetime.strptime(last_date, '%Y-%m-%d')
                        days_diff = (d2 - d1).days
                        if days_diff > 0:
                            predictions_per_week = (len(user_predictions) / days_diff) * 7
                            st.metric(
                                label="Predictions per Week",
                                value=f"{predictions_per_week:.1f}",
                                delta="Average frequency"
                            )
                    except:
                        pass
        
        with analysis_col2:
            st.markdown("**Insights**")
            
            # Most common location
            location_dist = prediction_history.get_location_distribution(st.session_state.username)
            if location_dist:
                most_common_location = max(location_dist.items(), key=lambda x: x[1])[0]
                st.markdown(f"- 📍 Most common location: **{most_common_location}**")
            
            # Prediction type preference
            if pred_stats['crop_predictions'] > pred_stats['fertilizer_predictions']:
                st.markdown("- 🌾 You prefer **crop predictions** over fertilizer predictions")
            elif pred_stats['fertilizer_predictions'] > pred_stats['crop_predictions']:
                st.markdown("- 🧪 You prefer **fertilizer predictions** over crop predictions")
            else:
                st.markdown("- ⚖️ You use crop and fertilizer predictions equally")
            
            # Success rate trend
            if pred_stats['success_rate'] >= 90:
                st.markdown("- ✅ Excellent success rate! Keep up the good work!")
            elif pred_stats['success_rate'] >= 70:
                st.markdown("- ⚠️ Good success rate. Review failed predictions for improvement.")
            else:
                st.markdown("- ❌ Low success rate. Consider reviewing your input parameters.")
    else:
        st.info("Make predictions to see detailed analysis!")
    
    st.markdown("---")
    
    # === Quick Actions ===
    st.subheader("⚡ Quick Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("Report generated successfully!")
    
    with action_col2:
        if st.button("📅 Add Task", use_container_width=True):
            st.info("Task management feature coming soon!")
    
    with action_col3:
        if st.button("💧 Check Irrigation", use_container_width=True):
            st.info("Irrigation system status: Normal")
    
    with action_col4:
        if st.button("📞 Contact Expert", use_container_width=True):
            st.info("Expert consultation available!")
    
    st.markdown("---")
    
    # === Prediction History Export Section ===
    st.subheader("📤 Export & Share")
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        if st.button("📊 Export Full Report", use_container_width=True):
            st.success("Report generated! Check your downloads.")
    
    with export_col2:
        if st.button("📧 Share via Email", use_container_width=True):
            st.info("Email sharing feature coming soon!")
    
    with export_col3:
        if st.button("🖨️ Print Dashboard", use_container_width=True):
            st.info("Print feature coming soon!")
    
    st.markdown("---")
    
    # === Footer ===
    st.info(
        "💡 **Tip**: Use this dashboard to monitor your farm's performance, track expenses, and plan your agricultural activities. "
        "Regular monitoring helps in making informed decisions for better yields."
    )
    
    st.stop()

# handle alternate functionality early to avoid indenting entire file
if mode == "Plant Leaf Detection":
    st.header("🌿 Plant Leaf Detection")
    st.markdown("Upload a photo of a plant leaf to identify diseases.")
    
    # Detection method selection - Default to Local Model
    detection_method = st.radio("Detection Method", ["Use Local Model (No API needed)", ], index=0, horizontal=True)
    
    if detection_method == "Use Local Model (No API needed)":
        # Try to load local model
        try:
            leaf_model = leaf_detector.load_leaf_model()
            
            # Always do prediction using the new function
            st.success("Using local model for prediction")
                
            # Model loaded, do prediction
            uploaded = st.file_uploader("Leaf image", type=["jpg","jpeg","png"])
            if uploaded is not None:
                from PIL import Image
                image = Image.open(uploaded)
                st.image(image, caption="Uploaded leaf", use_column_width=True)
                    
                # Use local model (with simple fallback)
                disease_info = leaf_detector.predict_leaf_with_info(leaf_model, image, use_api=False)
                
                # Translate disease info if language is not English
                if selected_language != "en":
                    disease_info = translator.translate_disease_info(disease_info, selected_language)
                
                st.markdown("---")
                st.subheader(disease_info['status'])
                st.markdown(f"**Disease/Condition:** {disease_info['description']}")
                
                st.subheader("💫 Recommendations")
                for i, rec in enumerate(disease_info['recommendations'], 1):
                    st.write(f"{i}. {rec}")
                st.markdown("---")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    else:
        # Use PlantNet API
        st.markdown("### PlantNet API")
        api_key = st.text_input("PlantNet API Key", type="password", help="Get free key from https://my.plantnet.org/")
        if not api_key:
            st.info("💡 Get a free API key from [PlantNet](https://my.plantnet.org/) - 500 requests/day free!")
        
        uploaded = st.file_uploader("Leaf image", type=["jpg","jpeg","png"])
        if uploaded is not None:
            from PIL import Image

            image = Image.open(uploaded)
            st.image(image, caption="Uploaded leaf", use_column_width=True)
            
            try:
                leaf_model = leaf_detector.load_leaf_model()
                
                disease_info = leaf_detector.predict_leaf_with_info(
                    leaf_model, 
                    image, 
                    use_api=True, 
                    api_key=api_key
                )
                
                # Translate disease info if language is not English
                if selected_language != "en":
                    disease_info = translator.translate_disease_info(disease_info, selected_language)
                
                st.markdown("---")
                status = disease_info.get('status', '📋 Identified')
                if 'Healthy' in status or '✅' in status:
                    st.success(status)
                elif 'API Key' in status or '⚠️' in status:
                    st.warning(status)
                elif 'Error' in status or '❌' in status:
                    st.error(status)
                else:
                    st.info(status)
                
                st.markdown(f"**Plant/Condition:** {disease_info.get('description', 'Unknown')}")
                
                if disease_info.get('confidence', 0) > 0:
                    st.markdown(f"**Confidence:** {disease_info.get('confidence', 0)*100:.1f}%")
                
                st.subheader("💫 Recommendations")
                for i, rec in enumerate(disease_info.get('recommendations', []), 1):
                    st.write(f"{i}. {rec}")
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure you have entered a valid API key from https://my.plantnet.org/")
    st.stop()

# fertilizer recommendation branch
if mode == "Fertilizer Recommendation":
    st.header("🧪 Fertilizer Recommendation")
    st.markdown("Provide soil and environmental data to get a fertilizer suggestion.")


    col1, col2 = st.columns(2)
    with col1:
        state = st.selectbox("State", list(state_city_map.keys()), help="Select the Indian state where your farm is located.")
    with col2:
        city = st.selectbox("City", state_city_map[state], help="Select the city within the chosen state.")

    lat, lon = location_mapper.get_lat_lon(location_df, city)
    temp_val = 25.0
    hum_val = 70.0
    if lat is not None:
        weather_data = weather_api.get_weather(lat, lon)
        if weather_data:
            temp_val = weather_data.get("temperature", temp_val)
            hum_val = weather_data.get("humidity", hum_val)

    st.markdown("---")

    # fertilizer-specific inputs
    colT, colH, colM = st.columns(3)
    with colT:
        # use float range so step stays float when default may be float
        temperature = st.slider("Temperature (°C)", -5.0, 50.0, float(temp_val), step=0.1)
    with colH:
        humidity = st.slider("Humidity (%)", 0.0, 100.0, float(hum_val), step=0.1)
    with colM:
        # moisture value is integer-based, ensure default matches type
        moisture = st.slider("Soil Moisture (%)", 0, 100, 50, step=1)

    # soil and crop choices
    soil_options = ["Sandy", "Loamy", "Black", "Red", "Clayey"]
    crop_options = [
        "Maize", "Sugarcane", "Cotton", "Tobacco", "Paddy", "Barley",
        "Wheat", "Millets", "Oil seeds", "Pulses", "Ground Nuts"
    ]
    soil_type = st.selectbox("Soil Type", soil_options)
    crop_type = st.selectbox("Crop Type", crop_options)

    colN, colP, colK = st.columns(3)
    with colN:
        nitrogen = st.slider("Nitrogen (ppm)", 0, 140, 60)
    with colP:
        phosphorous = st.slider("Phosphorous (ppm)", 0, 145, 60)
    with colK:
        potassium = st.slider("Potassium (ppm)", 0, 205, 60)

    if st.button("🧬 Predict Fertilizer"):
        try:
            if fertilizer_resources is None:
                with st.spinner("🔧 Loading or training fertilizer model…"):
                    # attempt to load, but train if artifacts aren't present
                    try:
                        fertilizer_resources = predictor.load_fertilizer_model(train_if_missing=True)
                    except TypeError:
                        # older predictor version didn't support keyword, try positional
                        try:
                            fertilizer_resources = predictor.load_fertilizer_model(True)
                        except TypeError:
                            # oldest version: no args accepted; load and hope files exist
                            fertilizer_resources = predictor.load_fertilizer_model()
            fert_model, soil_enc, crop_enc, fert_scaler = fertilizer_resources
            prediction = predictor.predict_fertilizer(
                fert_model,
                fert_scaler,
                soil_enc,
                crop_enc,
                [temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous]
            )
            st.success(f"### 🌱 Recommended fertilizer: **{prediction}**")
        except Exception as e:
            st.error(f"Failed to predict fertilizer: {e}")
    st.stop()

# --- Crop Demand Prediction ---
if mode == "Crop Demand Prediction":
    st.header("📈 Crop Demand Prediction")
    st.markdown("Forecast market demand trends for major crops based on season, region, and historical patterns.")

    # Static demand data (index = month 1-12)
    CROP_DEMAND = {
        "Rice":        [70, 65, 60, 55, 50, 60, 75, 85, 90, 88, 82, 75],
        "Wheat":       [90, 88, 80, 70, 55, 45, 40, 42, 50, 65, 80, 88],
        "Maize":       [55, 50, 55, 65, 75, 80, 78, 72, 68, 60, 55, 52],
        "Cotton":      [40, 42, 48, 55, 62, 70, 78, 85, 88, 82, 70, 50],
        "Sugarcane":   [75, 78, 80, 82, 80, 72, 68, 65, 68, 72, 75, 78],
        "Jute":        [30, 32, 38, 50, 65, 80, 88, 85, 70, 55, 40, 32],
        "Mango":       [20, 22, 35, 65, 90, 85, 60, 35, 20, 18, 18, 18],
        "Banana":      [60, 62, 65, 68, 72, 70, 65, 62, 60, 62, 65, 62],
        "Grapes":      [45, 50, 70, 85, 80, 55, 40, 35, 35, 42, 50, 48],
        "Chickpea":    [85, 82, 75, 60, 45, 35, 30, 32, 40, 55, 72, 82],
        "Lentil":      [80, 78, 70, 58, 42, 32, 28, 30, 38, 52, 68, 78],
        "Soybean":     [50, 48, 45, 50, 60, 72, 82, 88, 85, 75, 62, 52],
        "Groundnuts":  [55, 52, 48, 52, 62, 72, 80, 85, 83, 75, 65, 58],
        "Coffee":      [65, 68, 70, 68, 62, 55, 52, 55, 60, 65, 70, 68],
        "Coconut":     [70, 68, 65, 62, 60, 62, 65, 68, 72, 75, 78, 75],
        "Papaya":      [55, 58, 62, 65, 68, 65, 60, 58, 58, 60, 62, 58],
        "Pomegranate": [48, 50, 55, 60, 65, 62, 55, 50, 55, 62, 65, 55],
        "Watermelon":  [30, 35, 50, 70, 85, 82, 65, 45, 35, 30, 28, 28],
        "Orange":      [60, 62, 58, 50, 42, 38, 40, 45, 55, 65, 72, 68],
        "Apple":       [55, 52, 48, 45, 50, 60, 72, 82, 85, 78, 68, 60],
        "Muskmelon":   [28, 30, 42, 60, 78, 75, 55, 38, 28, 25, 25, 26],
        "Mothbeans":   [50, 48, 52, 58, 65, 72, 75, 72, 65, 58, 52, 50],
    }

    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    DEMAND_TIPS = {
        "High":   "🟢 High demand period — ideal time to sell or plan harvest.",
        "Medium": "🟡 Moderate demand — stable market conditions expected.",
        "Low":    "🔴 Low demand period — consider storage or value addition.",
    }

    # ── Controls ──
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        selected_crops = st.multiselect(
            "Select Crops to Compare",
            options=list(CROP_DEMAND.keys()),
            default=["Rice", "Wheat", "Maize"],
            help="Choose one or more crops to view their demand trend."
        )
    with col_c2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Line Chart", "Bar Chart", "Area Chart"],
            help="Select the type of chart for visualization."
        )

    forecast_months = st.slider(
        "Forecast Window (months from now)",
        min_value=1, max_value=12, value=6,
        help="How many months ahead to highlight in the forecast."
    )

    st.markdown("---")

    import datetime as _dt
    current_month = _dt.datetime.now().month  # 1-based

    if not selected_crops:
        st.warning("Please select at least one crop to view demand trends.")
    else:
        # Build DataFrame
        demand_rows = []
        for crop in selected_crops:
            for m_idx, month in enumerate(MONTHS):
                demand_rows.append({
                    "Month": month,
                    "Month_Num": m_idx + 1,
                    "Crop": crop,
                    "Demand (%)": CROP_DEMAND[crop][m_idx],
                })
        demand_df = pd.DataFrame(demand_rows)

        # ── Chart ──
        if chart_type == "Line Chart":
            fig_demand = px.line(
                demand_df, x="Month", y="Demand (%)", color="Crop",
                markers=True,
                title="📊 Monthly Crop Demand Trends",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
            fig_demand.update_traces(line=dict(width=2.5), marker=dict(size=8))
        elif chart_type == "Bar Chart":
            fig_demand = px.bar(
                demand_df, x="Month", y="Demand (%)", color="Crop",
                barmode="group",
                title="📊 Monthly Crop Demand Trends",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
        else:  # Area Chart
            fig_demand = px.area(
                demand_df, x="Month", y="Demand (%)", color="Crop",
                title="📊 Monthly Crop Demand Trends",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Safe,
            )

        # Shade forecast window
        forecast_end = min(current_month + forecast_months - 1, 12)
        fig_demand.add_vrect(
            x0=MONTHS[current_month - 1],
            x1=MONTHS[forecast_end - 1],
            fillcolor="rgba(0,204,150,0.08)",
            layer="below",
            line_width=0,
            annotation_text="Forecast Window",
            annotation_position="top left",
        )

        fig_demand.update_layout(
            height=480,
            xaxis_title="Month",
            yaxis_title="Relative Demand (%)",
            hovermode="x unified",
            font=dict(color="white"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig_demand.update_xaxes(showgrid=False)
        fig_demand.update_yaxes(gridcolor="#31333F", range=[0, 100])
        st.plotly_chart(fig_demand, use_container_width=True)

        st.markdown("---")

        # ── Per-crop summary cards ──
        st.subheader("🗓️ Current Month Demand Summary")
        summary_cols = st.columns(min(len(selected_crops), 4))
        for idx, crop in enumerate(selected_crops):
            demand_val = CROP_DEMAND[crop][current_month - 1]
            if demand_val >= 70:
                level = "High"
            elif demand_val >= 45:
                level = "Medium"
            else:
                level = "Low"
            with summary_cols[idx % 4]:
                st.metric(
                    label=f"🌾 {crop}",
                    value=f"{demand_val}%",
                    delta=f"{level} Demand",
                )

        st.markdown("---")

        # ── Demand tip per selected crop ──
        st.subheader("💡 Market Advisory")
        for crop in selected_crops:
            demand_val = CROP_DEMAND[crop][current_month - 1]
            if demand_val >= 70:
                level = "High"
            elif demand_val >= 45:
                level = "Medium"
            else:
                level = "Low"
            st.info(f"**{crop}** — {DEMAND_TIPS[level]}")

        st.markdown("---")

        # ── Best selling months table ──
        st.subheader("📅 Best Selling Months (Top 3 per Crop)")
        best_months_rows = []
        for crop in selected_crops:
            vals = CROP_DEMAND[crop]
            top3_idx = sorted(range(12), key=lambda i: vals[i], reverse=True)[:3]
            best_months_rows.append({
                "Crop": crop,
                "1st Best Month": MONTHS[top3_idx[0]],
                "2nd Best Month": MONTHS[top3_idx[1]],
                "3rd Best Month": MONTHS[top3_idx[2]],
                "Peak Demand (%)": vals[top3_idx[0]],
            })
        best_df = pd.DataFrame(best_months_rows)
        st.dataframe(best_df, use_container_width=True)

        st.markdown("---")

        # ── Demand heatmap ──
        st.subheader("🌡️ Demand Heatmap")
        pivot_data = {crop: CROP_DEMAND[crop] for crop in selected_crops}
        heatmap_df = pd.DataFrame(pivot_data, index=MONTHS)

        fig_heat = px.imshow(
            heatmap_df.T,
            labels=dict(x="Month", y="Crop", color="Demand (%)"),
            x=MONTHS,
            color_continuous_scale="Greens",
            title="🌡️ Crop Demand Heatmap (All Months)",
            template="plotly_dark",
            aspect="auto",
        )
        fig_heat.update_layout(
            height=max(250, 60 * len(selected_crops)),
            font=dict(color="white"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    st.stop()

# --- User Input: Location Selection ---
st.subheader("📍 Select Your Location")
col1, col2 = st.columns(2)
with col1:
    state = st.selectbox("State", list(state_city_map.keys()), help="Select the Indian state where your farm is located.")
with col2:
    city = st.selectbox("City", state_city_map[state], help="Select the city within the chosen state.")

# --- Get and Display Weather Data ---
lat, lon = location_mapper.get_lat_lon(location_df, city)

# Initialize weather variables with default values in case data fetching fails
temperature = 25.0
humidity = 70.0
pressure = "N/A"
wind_speed = "N/A"
description = "N/A"

if lat is not None:
    weather_data = weather_api.get_weather(lat, lon)

    if weather_data is not None: # Check if a dictionary was returned successfully
        # Extract data using .get() with a default value to prevent KeyError if a field is missing
        temperature = weather_data.get("temperature", 25.0)
        humidity = weather_data.get("humidity", 70.0)
        pressure = weather_data.get("pressure", "N/A")
        wind_speed = weather_data.get("wind_speed", "N/A")
        description = weather_data.get("description", "N/A").capitalize() # Capitalize for nice display

        st.success(f"**Current Weather in {city}:**")

        # Create two columns for the main layout
        col1, col2 = st.columns(2)

        with col1:
            # First row in the first main column: Temperature and Humidity
            st.subheader("Current Conditions") # Optional: Add a subheader for clarity
            temp_hum_col1, temp_hum_col2 = st.columns(2)
            with temp_hum_col1:
                st.metric("Temperature", f"{temperature:.1f}°C")
            with temp_hum_col2:
                st.metric("Humidity", f"{humidity:.1f}%")

            # Second row in the first main column: Pressure and Wind Speed
            press_wind_col1, press_wind_col2 = st.columns(2)
            with press_wind_col1:
                st.metric("Pressure", f"{pressure} hPa")
            with press_wind_col2:
                st.metric("Wind Speed", f"{wind_speed} m/s")

        with col2:
            # Description in the second main column
            st.subheader("Weather Details") # Optional: Add a subheader for clarity
            st.metric("Description", description)


    else:
        st.warning("⚠️ Could not fetch live weather data. Using default values for prediction.")
        # temperature and humidity already initialized with defaults
else:
    st.error("❌ Unable to retrieve coordinates for the selected city. Please check the city name or data.")
    # temperature and humidity already initialized with defaults

st.markdown("---")

# --- User Input: Soil Details ---
st.subheader("🧪 Enter Soil Properties")
st.markdown("Move the sliders to input your soil's nutritional and environmental parameters.")

colN, colP, colK = st.columns(3)
with colN:
    N = st.slider("Nitrogen (N) - ppm", 0, 140, 60, help="Nitrogen content in parts per million (ppm).")
with colP:
    P = st.slider("Phosphorus (P) - ppm", 5, 145, 60, help="Phosphorus content in parts per million (ppm).")
with colK:
    K = st.slider("Potassium (K) - ppm", 5, 205, 60, help="Potassium content in parts per million (ppm).")

colph, colrain = st.columns(2)
with colph:
    ph = st.slider("Soil pH", 3.5, 10.0, 6.5, 0.1, help="Soil pH value (acidity/alkalinity).")
with colrain:
    rainfall = st.slider("Rainfall (mm)", 20, 300, 100, help="Average annual rainfall in millimeters (mm).")

st.markdown("---")

# --- Feature Bar Chart (Input Summary) ---
st.subheader("📊 Your Input Summary")
st.info("This chart visualizes the values you've entered for crop recommendation, along with fetched weather data.")

features_dict = {
    "Nitrogen (N)": N,
    "Phosphorus (P)": P,
    "Potassium (K)": K,
    "Temperature (°C)": temperature, # Uses fetched or default temp
    "Humidity (%)": humidity,       # Uses fetched or default humidity
    "Pressure (hPa)": pressure if isinstance(pressure, (int, float)) else 0, # Convert N/A to 0 for plotting
    "Wind Speed (m/s)": wind_speed if isinstance(wind_speed, (int, float)) else 0, # Convert N/A to 0 for plotting
    "pH": ph,
    "Rainfall (mm)": rainfall
}

# Create a DataFrame for Plotly Express
features_df = pd.DataFrame(features_dict.items(), columns=['Feature', 'Value'])

fig_input_summary = px.bar(
    features_df,
    x='Feature',
    y='Value',
    labels={'Value': 'Input Value'},
    title="Overview of Entered Soil and Weather Conditions",
    color='Feature', # Color bars by feature
    color_discrete_sequence=px.colors.sequential.Aggrnyl, # A nice green color sequence
    template="plotly_dark" # Use dark theme for the plot
)
# Customize layout for better appearance
# Customize layout for better appearance
fig_input_summary.update_layout(
    title="Overview of Entered Soil and Weather Conditions",
    xaxis_title='Environmental Factor',
    yaxis_title='Measured Value',
    hovermode="x unified",

    font=dict(color="white"),
    title_font_size=20,

    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',

    height=500,   # 🔹 Increase graph height

    margin=dict(l=40, r=40, t=60, b=120)  # 🔹 Bottom space for labels
)

# Fix x-axis label overlap
fig_input_summary.update_xaxes(
    tickangle=45,      # 🔹 Rotate labels
    automargin=True,
    showgrid=False
)

fig_input_summary.update_yaxes(
    gridcolor='#31333F'
)

# Show graph
st.plotly_chart(fig_input_summary, use_container_width=True)

# --- Predict Crop Button and Results ---
if st.button("🌾 **Predict Best Crop**", help="Click to get the recommended crop based on your inputs."):
    if temperature is not None and humidity is not None:
        # Ensure the order of features matches the model's training order
        # Your model still expects only 7 features: N, P, K, temperature, humidity, ph, rainfall
        features = [N, P, K, temperature, humidity, ph, rainfall]

        # Make prediction
        crop = predictor.predict_crop(crop_model, features)
        st.success(f"### 🎉 Recommended Crop: **`{crop.upper()}`**")
        
        # Get and display crop information (growing duration and season)
        crop_info = predictor.get_crop_info(crop)
        
        # Display crop details in columns
        crop_detail_col1, crop_detail_col2 = st.columns(2)
        with crop_detail_col1:
            st.metric("⏱️ Growing Duration", f"{crop_info['duration']} days" if isinstance(crop_info['duration'], int) else crop_info['duration'])
        with crop_detail_col2:
            st.metric("🌤️ Season", crop_info['season'])
        
        st.markdown("---")
        # st.balloons() # Add a celebratory animation

        # Optional: Probability Chart (if model supports predict_proba)
        if hasattr(crop_model, "predict_proba"):
            probas = crop_model.predict_proba([features])[0]
            labels = crop_model.classes_

            # Get top 5 probabilities and sort them
            top_indices = probas.argsort()[::-1][:5] # Get indices of top 5 in descending order
            top5_probs = [(labels[i], probas[i]) for i in top_indices]

            top5_df = pd.DataFrame(top5_probs, columns=["Crop", "Probability"])

            st.subheader("🔍 Top-5 Crop Probabilities")
            st.info("This chart shows the likelihood of various crops being suitable.")

            prob_fig = px.bar(
            top5_df,
            x="Crop",
            y="Probability",
            text=top5_df["Probability"].apply(lambda x: f"{x:.2%}"),
            title="Top 5 Crop Recommendations by Probability",
            color="Probability",
            color_continuous_scale=px.colors.sequential.Greens,
            template="plotly_dark"
             )

            prob_fig.update_layout(
            xaxis_title='Crop Type',
            yaxis_title='Probability',
            hovermode="x unified",
            font=dict(color="white"),
            title_font_size=20,

            height=500,  # 🔹 Increase graph height
            margin=dict(l=40, r=40, t=60, b=120),  # 🔹 Fix label cut

            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',

            bargap=0.4
             )

# Fix label overlap
            prob_fig.update_xaxes(
            tickangle=30,
            automargin=True,
            showgrid=False
             )

            prob_fig.update_yaxes(
            gridcolor='#31333F'
               )

# Show graph
        st.plotly_chart(prob_fig, use_container_width=True)
    else:
        st.warning("Prediction cannot be made as crucial weather data (Temperature/Humidity) is missing or could not be fetched.")

st.markdown("---")
