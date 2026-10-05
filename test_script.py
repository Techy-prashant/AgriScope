import pandas as pd
from data_processing import load_and_validate_data, get_summary_metrics, get_crop_stats, get_data_quality_report, get_comparison_stats
import os

def run_tests():
    print("--- STARTING TESTS ---")
    data_path = "DataSet/Crop_recommendation.csv"
    
    # 1. Test successful load and calculate
    print("1. Testing normal load")
    df = load_and_validate_data(data_path)
    
    # Verify manual pandas vs function
    total, unique, avg_t, avg_h = get_summary_metrics(df)
    assert total == len(df)
    assert unique == df['label'].nunique()
    assert abs(avg_t - df['temperature'].mean()) < 1e-6
    assert abs(avg_h - df['humidity'].mean()) < 1e-6
    print("Normal load and summary metrics passed.")
    
    # 2. Test crop stats
    print("2. Testing crop stats for 'rice'")
    stats, crop_df = get_crop_stats(df, 'rice')
    manual_rice_N = df[df['label'] == 'rice']['N'].mean()
    assert abs(stats['avg_N'] - manual_rice_N) < 1e-6
    print("Crop stats passed.")
    
    # 3. Test comparison stats
    print("3. Testing comparison stats")
    comp_stats, comp_df = get_comparison_stats(df, ['rice', 'maize'])
    assert len(comp_stats) == 2
    assert comp_stats[comp_stats['label'] == 'rice']['avg_N'].iloc[0] == manual_rice_N
    print("Comparison stats passed.")
    
    # 4. Test missing file
    print("4. Testing missing file")
    try:
        load_and_validate_data("missing.csv")
        print("FAILED: Missing file did not raise error")
    except FileNotFoundError:
        print("Missing file handled correctly.")
        
    # 5. Test empty data
    print("5. Testing empty data")
    empty_df = pd.DataFrame(columns=df.columns)
    empty_df.to_csv("empty.csv", index=False)
    try:
        load_and_validate_data("empty.csv")
        print("FAILED: Empty data did not raise error")
    except ValueError as e:
        if "empty" in str(e).lower():
            print("Empty data handled correctly.")
    os.remove("empty.csv")
        
    # 6. Test invalid schema
    print("6. Testing invalid schema")
    invalid_df = df.drop(columns=['N'])
    invalid_df.to_csv("invalid.csv", index=False)
    try:
        load_and_validate_data("invalid.csv")
        print("FAILED: Invalid schema did not raise error")
    except ValueError as e:
        if "missing required columns" in str(e).lower():
            print("Invalid schema handled correctly.")
    os.remove("invalid.csv")
    
    print("--- ALL TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
