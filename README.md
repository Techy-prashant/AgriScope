# Smart Agri-Data Insights Dashboard 🌱

## Project Overview and Objectives
The Smart Agri-Data Insights Dashboard is an interactive web application designed to help users explore and compare agricultural datasets. Our primary objective is to provide an intuitive interface for viewing crop-specific environmental and soil requirements, aiding researchers and students in understanding historical crop performance data without requiring complex coding or database knowledge.

## Features
- **Single Crop Analysis**: View detailed average statistics (Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall) and distributions for any specific crop.
- **Crop Comparison**: Select multiple crops to visually compare their nutrient and environmental profiles using grouped bar charts.
- **Data Quality Report**: Instantly assess dataset health, identifying missing values, duplicate records, and descriptive statistics.
- **CSV Data Export**: Download raw filtered data or summarized comparison metrics directly to your local machine.

## Technology Stack
- **Python**: Core programming language.
- **Streamlit**: Web framework for building the dashboard interface.
- **Pandas**: Data manipulation, validation, and aggregation.
- **Plotly Express**: Interactive and responsive data visualizations.

## Dataset Source and Attribution
The dataset used in this project is an Agricultural Crop Recommendation Dataset, traditionally containing records for 22 unique crops alongside their respective NPK and environmental characteristics. *Note: Averages represent historically recorded data, not necessarily scientifically validated ideal growing conditions.*

## Installation and Execution
1. **Clone or Download** the project repository.
2. Ensure you have **Python 3.8+** installed.
3. Open a terminal in the project directory and create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - **Windows:** `.\.venv\Scripts\activate`
   - **Mac/Linux:** `source .venv/bin/activate`
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the application:
   ```bash
   streamlit run app.py
   ```
7. The application will automatically open in your default browser at `http://localhost:8501`.

## Project Folder Structure
```
📁 Smart Agri-Data Insights Dashboard
│
├── 📁 DataSet
│   └── Crop_recommendation.csv   # The source dataset
│
├── app.py                        # Main Streamlit dashboard application
├── data_processing.py            # Data loading, validation, and analysis functions
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## Known Limitations and Future Improvements
**Limitations:**
- The dashboard currently relies entirely on static, historical CSV data. It does not integrate with real-time IoT sensors, weather APIs, or live databases.
- The platform provides data exploration features; it does not utilize Machine Learning to actively predict or "recommend" crops.
- The displayed averages do not replace certified agronomist advice.

**Future Improvements:**
- Integration with live weather APIs to compare current conditions against historical averages.
- The addition of a machine learning module to actively predict the best crop given user-inputted soil readings.
- User authentication to allow saving favorite crops or comparisons.
