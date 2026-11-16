"""
Master Pipeline Runner
Executes the end-to-end Marketing Attribution and ROI Intelligence analytics pipeline.
"""

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_step(step_name, func):
    print("\n" + "=" * 70)
    print(f"STEP: {step_name}")
    print("=" * 70)
    start_time = time.time()
    try:
        func()
        elapsed = time.time() - start_time
        print(f"--> [SUCCESS] {step_name} completed in {elapsed:.2f} seconds.")
    except Exception as e:
        print(f"--> [ERROR] {step_name} failed: {e}")
        raise e

def main():
    print("*" * 70)
    print("STARTING COMPLETE MARKETING ATTRIBUTION & ROI PIPELINE")
    print("*" * 70)
    pipeline_start = time.time()

    # 1. Data Cleaning
    from src.data_cleaning import clean_marketing_data
    run_step("1. Data Cleaning & Feature Engineering", clean_marketing_data)

    # 2. Attribution Modeling
    from src.attribution import compute_attribution_weights, summarize_attribution
    import pandas as pd
    def run_attr():
        df_touch = pd.read_csv("data/processed/customer_attribution_touchpoints.csv")
        df_modeled = compute_attribution_weights(df_touch)
        df_modeled.to_csv("data/processed/customer_attribution_modeled.csv", index=False)
        summarize_attribution(df_modeled)
    run_step("2. Multi-Touch Attribution Modeling", run_attr)

    # 3. Exploratory Data Analysis & Visualizations
    from src.eda import run_eda
    run_step("3. Exploratory Data Analysis & Figures Generation", run_eda)

    # 4. Excel Analysis Workbook Generation
    from src.excel_generator import create_excel_report
    run_step("4. Executive Excel Workbook Report Generation", create_excel_report)

    # 5. SQL Business Query Analysis
    from scripts.run_sql_analysis import run_all_sql_queries
    run_step("5. SQL Analysis Queries Execution", run_all_sql_queries)

    # 6. Dashboard JS Data Export
    from scripts.export_dashboard_data import export_data
    run_step("6. Export Interactive Dashboard JS Data", export_data)

    # 7. Jupyter Notebook Build & Execution
    from scripts.build_notebook import build_and_render_notebook
    run_step("7. Jupyter Notebook Generation & Pre-rendering", build_and_render_notebook)

    total_time = time.time() - pipeline_start
    print("\n" + "*" * 70)
    print(f"PIPELINE COMPLETED SUCCESSFULLY IN {total_time:.2f} SECONDS!")
    print("All datasets, figures, SQL outputs, Excel sheets, dashboards, and notebooks are up to date.")
    print("*" * 70)

if __name__ == "__main__":
    main()
