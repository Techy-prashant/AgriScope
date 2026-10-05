import streamlit as st
import plotly.express as px
import os
from data_processing import load_and_validate_data, get_summary_metrics, get_crop_stats, get_data_quality_report, get_comparison_stats, generate_comparison_insights, generate_crop_insights

# Configure the Streamlit page
st.set_page_config(
    page_title="AgriScope: Agricultural Data Intelligence",
    page_icon=":material/agriculture:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium redesign: Deep forest green, muted sage, warm off-white, and charcoal.
st.markdown(
    """
    <style>
    /* Hero section vertical spacing fixes */
    .block-container {
        max-width: 1350px !important;
        padding-left: 32px !important;
        padding-right: 32px !important;
        padding-top: 2rem !important;
        margin: 0 auto;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-left: 16px !important;
            padding-right: 16px !important;
        }
    }
    
    /* Headings */
    h1 {
        font-size: 45px !important;
        color: #18352B !important;
        font-weight: 1000 !important;
    }
    h2, h3 {
        font-size: 22px !important;
        color: #18352B !important;
        font-weight: 500 !important;
        font-style: italic !important;
    }
    
    /* Metrics card styling override */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E1E7DF !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #63746A !important;
        font-size: 14px !important;
    }
    [data-testid="stMetricValue"] {
        color: #18352B !important;
        font-weight: 600 !important;
        font-size: 30px !important;
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #28734B !important;
        border-bottom-color: #28734B !important;
        background-color: #E8F0E7 !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="false"] {
        color: #63746A !important;
    }
    
    /* Inputs */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #CDD8CD !important;
        color: #18352B !important;
    }
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #CDD8CD !important;
    }
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #E8F0E7 !important;
        color: #18352B !important;
    }
    
    /* Buttons */
    .stButton button, .stDownloadButton button {
        background-color: #FFFFFF !important;
        color: #18352B !important;
        border: 1px solid #CDD8CD !important;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        border-color: #28734B !important;
        color: #28734B !important;
    }
    
    /* Info panels and alerts */
    .stAlert {
        background-color: #E8F0E7 !important;
        border: 1px solid #E1E7DF !important;
        color: #18352B !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.dialog("About the Project", width="large")
def show_about_dialog():
    st.markdown("""
        <style>
        /* Increase maximum width of Streamlit dialogs */
        div[data-testid="stDialog"] > div {
            width: min(1100px, calc(100% - 64px)) !important;
            max-width: 1200px !important;
        }
        @media (max-width: 768px) {
            div[data-testid="stDialog"] > div {
                width: calc(100% - 32px) !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.subheader("Project Overview", anchor=False)
    st.write("AgriScope is an interactive web application designed to help users explore and compare agricultural datasets. It includes features for single crop exploration, multi-crop environmental and nutrient comparison, and data-quality reporting.")
    
    about_col1, about_col2 = st.columns(2, gap="large")
    with about_col1:
        st.subheader("Created By", anchor=False)
        st.write("**Name:** Prashant Tiwari")
        st.write("**GitHub:** [Techy-prashant](https://github.com/Techy-prashant)")
        st.write("**Project repository:** [AgriScope](https://github.com/Techy-prashant/AgriScope)")
    with about_col2:
        st.subheader("Technology Stack", anchor=False)
        st.markdown("- **Python**: Core programming language.\n- **Streamlit**: Web framework for building the dashboard interface.\n- **Pandas**: Data manipulation, validation, and aggregation.\n- **Plotly Express**: Interactive and responsive data visualizations.")
        
    st.subheader("Dataset and Resources", anchor=False)
    st.markdown("Every project starts somewhere, and AgriScope started with data. The dataset brings together crop labels, nutrient requirements (Nitrogen, Phosphorus, and Potassium), temperature, humidity, soil pH, and rainfall. I used these records to explore how different crops relate to their growing conditions and to make the numbers easier to understand through visualizations. Along the way, I also worked with data analysis tools and charting libraries to turn rows and columns into something people can actually explore. The original dataset source and supporting resources are credited here so anyone interested can trace the work back to its roots.")
    st.markdown("**Libraries:** Python, Streamlit, Pandas, Plotly Express")

    st.subheader("Dataset: Crop Recommendation Dataset", anchor=False)
    st.markdown("AgriScope uses the **Crop Recommendation Dataset** published by **Siddharth Sharma** on Kaggle. The dataset contains soil nutrient measurements, environmental conditions, and crop labels, providing the foundation for exploring crop requirements and comparing agricultural data.")
    st.markdown("Source: [Crop Recommendation Dataset](https://www.kaggle.com/datasets/siddharthss/crop-recommendation-dataset)")
    st.subheader("Project Inspiration", anchor=False)
    st.markdown("I've always liked the part of technology where something complicated starts making sense. A spreadsheet full of numbers might be useful to someone who knows what they're looking for, but it can be difficult to make sense of at a glance. That got me thinking: what if crop data could be explored visually, compared side by side, and understood without having to dig through endless rows? AgriScope grew from that simple idea. It's an attempt to make agricultural data feel a little less like a spreadsheet and a little more like a conversation with the data itself.")
    
    st.subheader("Development Journey", anchor=False)
    st.write("AgriScope was a journey of figuring things out, trying things, and improving what didn't quite work. It began with understanding the dataset and figuring out which patterns and comparisons were worth exploring. From there came the crop explorer, comparison charts, environmental distributions, and data quality reports. Getting the numbers onto a screen was one thing; presenting them in a way that actually made sense was another challenge entirely. I spent time refining the layout, rethinking visualizations, and making the interface easier to navigate. The project is a reminder that building something useful isn't just about making the code work. It's also about making the result understandable to the person using it.")

# 1. Application Identity
col_head1, col_head2 = st.columns([48, 52], vertical_alignment="center", gap="large")
with col_head1:
    st.markdown("<h1 style='margin-bottom:0; padding-bottom:0;'>AgriScope</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#63746A;'>Agricultural Data Intelligence</h3>", unsafe_allow_html=True)
    st.write("Explore and analyze historical crop requirements, environmental factors, and data quality.")
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("About the Project", icon=":material/info:", use_container_width=True):
            show_about_dialog()
    with btn_col2:
        st.link_button("View on GitHub", "https://github.com/Techy-prashant/AgriScope", icon=":material/code:", use_container_width=True)
with col_head2:
    if os.path.exists("assets/banner.jpg"):
        st.markdown(
            """
            <style>
            [data-testid="stImage"] img {
                max-height: 320px !important;
                object-fit: cover !important;
                border-radius: 8px !important;
            }
            </style>
            """, unsafe_allow_html=True
        )
        st.image("assets/banner.jpg", use_container_width=True)

# Define the relative path to the dataset
DATA_PATH = os.path.join("DataSet", "Crop_recommendation.csv")

@st.cache_data
def fetch_data(path):
    """
    Fetches and caches the dataset to improve performance.
    """
    return load_and_validate_data(path)

try:
    df = fetch_data(DATA_PATH)
    
    # 4. Create Tabs for navigation
    # Using Material Icons in Streamlit tabs
    tab1, tab2, tab3 = st.tabs([
        ":material/dashboard: Overview & Crop Explorer", 
        ":material/bar_chart: Compare Crops", 
        ":material/fact_check: Data Quality"
    ])
    
    with tab1:
        st.header("Overview & Crop Explorer", anchor=False, divider="grey")
        st.markdown("Understand the overall dataset shape and dive into specific crop requirements.")
        
        # 3. Key Metrics
        total_records, unique_crops, avg_temp, avg_humidity = get_summary_metrics(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{total_records:,}")
        with col2:
            st.metric("Crop Categories", f"{unique_crops}")
        with col3:
            st.metric("Avg Temperature", f"{avg_temp:.1f} °C")
        with col4:
            st.metric("Avg Humidity", f"{avg_humidity:.1f} %")
            
        st.write("")
        
        # Crop Selection
        st.subheader("Crop Analysis", anchor=False)
        crop_list = sorted(df['label'].unique().tolist())
        
        selected_crop = st.selectbox("Select a crop to view detailed statistics", options=crop_list)
        
        if selected_crop:
            stats, crop_df = get_crop_stats(df, selected_crop)
            
            st.markdown(f"### {selected_crop.capitalize()} Statistics")
            st.markdown(f"**Total Observations:** {stats['count']}")
            
            scol1, scol2, scol3 = st.columns(3)
            scol1.metric("Nitrogen (N)", f"{stats['avg_N']:.1f}")
            scol2.metric("Phosphorus (P)", f"{stats['avg_P']:.1f}")
            scol3.metric("Potassium (K)", f"{stats['avg_K']:.1f}")
            
            scol4, scol5, scol6, scol7 = st.columns(4)
            scol4.metric("Temperature", f"{stats['avg_temperature']:.1f} °C")
            scol5.metric("Humidity", f"{stats['avg_humidity']:.1f} %")
            scol6.metric("pH Level", f"{stats['avg_ph']:.1f}")
            scol7.metric("Rainfall", f"{stats['avg_rainfall']:.1f} mm")
            
            st.download_button(
                label="Download Crop Data (CSV)",
                data=crop_df.to_csv(index=False),
                file_name=f"{selected_crop}_data.csv",
                mime="text/csv",
                icon=":material/download:"
            )
            
            c_insights = generate_crop_insights(stats, crop_df, avg_temp, avg_humidity)
            st.info("\n".join(c_insights), icon=":material/lightbulb:")
            
            st.subheader("Average NPK Requirements", anchor=False)
            npk_data = {
                'Nutrient': ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
                'Value': [stats['avg_N'], stats['avg_P'], stats['avg_K']]
            }
            fig_npk = px.bar(
                npk_data, 
                x='Nutrient', 
                y='Value', 
                text='Value',
                color='Nutrient',
                color_discrete_sequence=['#28734B', '#18352B', '#63746A']
            )
            fig_npk.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig_npk.update_layout(
                height=300,
                bargap=0.4,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#63746A'),
                yaxis=dict(title='Amount'),
                showlegend=False
            )
            st.plotly_chart(fig_npk, use_container_width=True)
            
            st.subheader("Environmental Distributions", anchor=False)
            col_t, col_h = st.columns(2)
            
            # Using deep forest green and muted sage for charts
            with col_t:
                fig_temp = px.histogram(
                    crop_df, x="temperature", nbins=15, 
                    title="Temperature Distribution (°C)",
                    color_discrete_sequence=['#28734B']
                )
                fig_temp.update_layout(height=240, bargap=0.1, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'))
                st.plotly_chart(fig_temp, use_container_width=True)
                
            with col_h:
                fig_hum = px.histogram(
                    crop_df, x="humidity", nbins=15, 
                    title="Humidity Distribution (%)",
                    color_discrete_sequence=['#18352B']
                )
                fig_hum.update_layout(height=240, bargap=0.1, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'))
                st.plotly_chart(fig_hum, use_container_width=True)
                
    with tab2:
        st.header("Crop Comparison", anchor=False, divider="grey")
        st.markdown("Compare average metrics across multiple crops. *Note: Averages represent historically recorded data, not necessarily scientifically validated ideal growing conditions.*")
        
        if 'crop_list' not in locals():
            crop_list = sorted(df['label'].unique().tolist())
            
        selected_crops = st.multiselect("Select at least two crops to compare:", options=crop_list, default=crop_list[:2] if len(crop_list) >= 2 else None)
        
        if selected_crops and len(selected_crops) >= 2:
            comp_stats, comp_df = get_comparison_stats(df, selected_crops)
            
            display_comp = comp_stats.rename(columns={
                'label': 'Crop',
                'count': 'Observations',
                'avg_N': 'Average Nitrogen (N)',
                'avg_P': 'Average Phosphorus (P)',
                'avg_K': 'Average Potassium (K)',
                'avg_temperature': 'Average Temperature (°C)',
                'avg_humidity': 'Average Humidity (%)',
                'avg_ph': 'Average Soil pH',
                'avg_rainfall': 'Average Rainfall'
            })
            display_comp['Crop'] = display_comp['Crop'].str.capitalize()
            
            st.caption("Measurements: N (Nitrogen), P (Phosphorus), K (Potassium) in dataset units. Soil pH measures acidity/alkalinity.")
            st.dataframe(
                display_comp.style.format(precision=1),
                use_container_width=True,
                hide_index=True
            )
            
            st.download_button(
                label="Download Comparison Stats (CSV)",
                data=comp_stats.to_csv(index=False),
                file_name="crop_comparison.csv",
                mime="text/csv",
                icon=":material/download:"
            )
            
            st.subheader("NPK Comparison", anchor=False)
            npk_cols = st.columns(3)
            with npk_cols[0]:
                fig_n = px.bar(comp_stats, x='label', y='avg_N', title="Nitrogen (N)", color_discrete_sequence=['#28734B'])
                fig_n.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'), yaxis_title="", xaxis_title="Crop")
                st.plotly_chart(fig_n, use_container_width=True)
            with npk_cols[1]:
                fig_p = px.bar(comp_stats, x='label', y='avg_P', title="Phosphorus (P)", color_discrete_sequence=['#18352B'])
                fig_p.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'), yaxis_title="", xaxis_title="Crop")
                st.plotly_chart(fig_p, use_container_width=True)
            with npk_cols[2]:
                fig_k = px.bar(comp_stats, x='label', y='avg_K', title="Potassium (K)", color_discrete_sequence=['#63746A'])
                fig_k.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'), yaxis_title="", xaxis_title="Crop")
                st.plotly_chart(fig_k, use_container_width=True)
            
            st.subheader("Environmental Comparison", anchor=False)
            env_cols = st.columns(3)
            with env_cols[0]:
                fig_t = px.bar(comp_stats, x='label', y='avg_temperature', title="Temperature (°C)", color_discrete_sequence=['#28734B'])
                fig_t.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'), yaxis_title="", xaxis_title="Crop")
                st.plotly_chart(fig_t, use_container_width=True)
            with env_cols[1]:
                fig_h = px.bar(comp_stats, x='label', y='avg_humidity', title="Humidity (%)", color_discrete_sequence=['#18352B'])
                fig_h.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'), yaxis_title="", xaxis_title="Crop")
                st.plotly_chart(fig_h, use_container_width=True)
            with env_cols[2]:
                fig_r = px.bar(comp_stats, x='label', y='avg_rainfall', title="Rainfall (mm)", color_discrete_sequence=['#63746A'])
                fig_r.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#63746A'), yaxis_title="", xaxis_title="Crop")
                st.plotly_chart(fig_r, use_container_width=True)
                
            st.subheader("Data Insights", anchor=False)
            insights = generate_comparison_insights(comp_stats)
            if insights:
                st.info("\n".join(insights), icon=":material/lightbulb:")
                
        elif selected_crops:
            st.info("Please select at least two crops to view the comparison.", icon=":material/info:")
            
    with tab3:
        st.header("Data Quality Report", anchor=False, divider="grey")
        st.markdown("This report summarizes the health of your dataset. Missing values represent gaps, while zero values represent valid measurements.")
        
        report = get_data_quality_report(df)
        
        dq_col1, dq_col2, dq_col3, dq_col4 = st.columns(4)
        with dq_col1:
            st.metric("Total Rows", report['total_rows'])
        with dq_col2:
            st.metric("Duplicate Rows", report['duplicates'])
        with dq_col3:
            st.metric("Columns", len(df.columns))
        with dq_col4:
            st.metric("Missing Values", sum(report['missing_values'].values()))
            
        st.subheader("Column Information", anchor=False)
        col_info = []
        for col in df.columns:
            col_info.append({
                "Column Name": col,
                "Data Type": report['data_types'].get(col, "Unknown"),
                "Missing Values (NaN)": str(report['missing_values'].get(col, 0)),
                "Zero Values (0)": str(report['zero_values'].get(col, "N/A"))
            })
        st.table(col_info)
        
        st.subheader("Descriptive Statistics", anchor=False)
        display_stats = report['descriptive_stats'].rename(index={
            'count': 'Count',
            'mean': 'Mean',
            'std': 'Standard deviation',
            'min': 'Minimum',
            '25%': '25th percentile',
            '50%': 'Median',
            '75%': '75th percentile',
            'max': 'Maximum'
        })
        st.caption("Descriptive statistics for all numeric columns across the entire dataset.")
        st.dataframe(display_stats, use_container_width=True)

except FileNotFoundError:
    st.error("Dataset not found. Please ensure 'Crop_recommendation.csv' is placed inside the 'DataSet' folder.", icon=":material/warning:")
except ValueError as e:
    st.error(f"Validation Error: {e}", icon=":material/error:")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}", icon=":material/error:")
