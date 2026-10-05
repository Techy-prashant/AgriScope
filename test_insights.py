import pandas as pd
from data_processing import load_and_validate_data, get_comparison_stats, generate_comparison_insights

def run_insight_tests():
    data_path = "DataSet/Crop_recommendation.csv"
    df = load_and_validate_data(data_path)
    
    comp_stats, _ = get_comparison_stats(df, ['rice', 'maize', 'apple'])
    insights = generate_comparison_insights(comp_stats)
    
    for i in insights:
        print(i)
        assert "Dataset Observation" in i

    print("Insights test passed.")

if __name__ == "__main__":
    run_insight_tests()
