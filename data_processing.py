import pandas as pd
import os

def load_and_validate_data(filepath):
    """
    Loads the dataset and validates the presence of required columns.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
        
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Error reading the dataset: {e}")
        
    if df.empty:
        raise ValueError("The dataset is empty.")
        
    required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
    return df

def get_summary_metrics(df):
    """
    Calculates overall summary metrics for the dataset.
    """
    total_records = len(df)
    unique_crops = df['label'].nunique()
    avg_temp = df['temperature'].mean()
    avg_humidity = df['humidity'].mean()
    
    return total_records, unique_crops, avg_temp, avg_humidity

def get_crop_stats(df, crop_name):
    """
    Calculates summary statistics for a specific crop.
    """
    crop_df = df[df['label'] == crop_name]
    
    stats = {
        'count': len(crop_df),
        'avg_N': crop_df['N'].mean() if 'N' in crop_df.columns else None,
        'avg_P': crop_df['P'].mean() if 'P' in crop_df.columns else None,
        'avg_K': crop_df['K'].mean() if 'K' in crop_df.columns else None,
        'avg_temperature': crop_df['temperature'].mean() if 'temperature' in crop_df.columns else None,
        'avg_humidity': crop_df['humidity'].mean() if 'humidity' in crop_df.columns else None,
        'avg_ph': crop_df['ph'].mean() if 'ph' in crop_df.columns else None,
        'avg_rainfall': crop_df['rainfall'].mean() if 'rainfall' in crop_df.columns else None,
    }
    return stats, crop_df

def get_data_quality_report(df):
    """
    Generates a data quality report including missing values, duplicates, datatypes,
    and basic descriptive statistics.
    """
    report = {}
    report['total_rows'] = len(df)
    report['duplicates'] = df.duplicated().sum()
    
    # Missing values (distinguish from 0)
    report['missing_values'] = df.isna().sum().to_dict()
    
    # Zero values
    # Filter for numeric columns before checking for 0
    numeric_df = df.select_dtypes(include=['number'])
    report['zero_values'] = (numeric_df == 0).sum().to_dict()
    
    report['data_types'] = df.dtypes.astype(str).to_dict()
    report['descriptive_stats'] = df.describe().round(2)
    
    return report

def get_comparison_stats(df, crops):
    """
    Calculates summary statistics for a list of crops.
    """
    filtered_df = df[df['label'].isin(crops)]
    
    # Group by crop
    comparison_stats = filtered_df.groupby('label').agg(
        count=('label', 'size'),
        avg_N=('N', 'mean'),
        avg_P=('P', 'mean'),
        avg_K=('K', 'mean'),
        avg_temperature=('temperature', 'mean'),
        avg_humidity=('humidity', 'mean'),
        avg_ph=('ph', 'mean'),
        avg_rainfall=('rainfall', 'mean')
    ).reset_index()
    
    return comparison_stats, filtered_df

def generate_crop_insights(stats, crop_df, avg_temp_all, avg_hum_all):
    """
    Generates dynamic textual observations for a single crop.
    """
    insights = []
    insights.append(f"- **Observation Count:** Based on {stats['count']} records.")
    
    if stats['avg_N'] is not None:
        insights.append(f"- **Nutrients:** On average, requires N: {stats['avg_N']:.1f}, P: {stats['avg_P']:.1f}, K: {stats['avg_K']:.1f}.")
    
    if 'temperature' in crop_df.columns:
        t_min, t_max = crop_df['temperature'].min(), crop_df['temperature'].max()
        h_min, h_max = crop_df['humidity'].min(), crop_df['humidity'].max()
        insights.append(f"- **Environment:** Observed temperature range is {t_min:.1f}°C to {t_max:.1f}°C, and humidity range is {h_min:.1f}% to {h_max:.1f}%.")
    
    if stats['avg_rainfall'] is not None:
        insights.append(f"- **Rainfall:** Average recorded rainfall is {stats['avg_rainfall']:.1f} mm.")
    
    if stats['avg_temperature'] is not None and avg_temp_all is not None:
        t_diff = stats['avg_temperature'] - avg_temp_all
        t_comp = "higher" if t_diff > 0 else "lower"
        insights.append(f"- **Overall Comparison:** Average temperature is {abs(t_diff):.1f}°C {t_comp} than the dataset average.")
    
    return insights

def generate_comparison_insights(comp_stats):
    """
    Generates dynamic textual observations based on calculated comparison metrics.
    """
    insights = []
    crops = comp_stats['label'].tolist()
    crop_names = ", ".join([c.capitalize() for c in crops])
    
    insights.append(f"**Comparing {len(crops)} crops:** {crop_names}")
    
    metrics = {
        'avg_N': 'Nitrogen (N)',
        'avg_P': 'Phosphorus (P)',
        'avg_K': 'Potassium (K)',
        'avg_temperature': 'Temperature (°C)',
        'avg_rainfall': 'Rainfall (mm)'
    }
    
    for col, name in metrics.items():
        if col in comp_stats.columns and not comp_stats[col].isna().all():
            max_val = comp_stats[col].max()
            min_val = comp_stats[col].min()
            
            # Only add insight if there is a meaningful difference
            if max_val - min_val > 0.1:
                top_crops = comp_stats[comp_stats[col] == max_val]['label'].tolist()
                top_crops_str = ", ".join([c.capitalize() for c in top_crops])
                insights.append(f"- **{name}:** {top_crops_str} has the highest average ({max_val:.1f}).")
                
    return insights
