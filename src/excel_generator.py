"""
Excel Analysis Report Generator
Creates a professional, multi-tab Excel workbook with KPI cards,
formatted financial tables, native Excel formulas, and charts using openpyxl.
"""

import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference


def create_excel_report(cleaned_csv="data/processed/marketing_campaign_data_cleaned.csv",
                        attr_csv="data/processed/marketing_attribution_summary.csv",
                        monthly_csv="data/processed/monthly_channel_summary.csv",
                        output_path="reports/marketing_roi_intelligence_report.xlsx"):
    
    print("Generating executive Excel workbook...")
    df = pd.read_csv(cleaned_csv)
    df_attr = pd.read_csv(attr_csv)
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Corporate Styling Theme: Navy / Slate / Emerald
    font_family = "Segoe UI"
    title_font = Font(name=font_family, size=16, bold=True, color="FFFFFF")
    subtitle_font = Font(name=font_family, size=10, italic=True, color="DCE6F1")
    section_font = Font(name=font_family, size=12, bold=True, color="1F497D")
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    data_font = Font(name=font_family, size=10, color="000000")
    total_font = Font(name=font_family, size=10, bold=True, color="000000")
    kpi_num_font = Font(name=font_family, size=16, bold=True, color="1F497D")
    kpi_label_font = Font(name=font_family, size=9, bold=True, color="595959")

    title_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_fill = PatternFill(start_color="244061", end_color="244061", fill_type="solid")
    sub_header_fill = PatternFill(start_color="418AB3", end_color="418AB3", fill_type="solid")
    kpi_fill = PatternFill(start_color="F2F5F8", end_color="F2F5F8", fill_type="solid")
    total_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FBFD", end_color="F9FBFD", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    total_border = Border(
        top=Side(style='thin', color='1F497D'),
        bottom=Side(style='double', color='1F497D')
    )

    # =========================================================================
    # TAB 1: EXECUTIVE SUMMARY & KPI SCORECARDS
    # =========================================================================
    ws1 = wb.create_sheet(title="Executive Summary")
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells("A1:J2")
    ws1["A1"] = "MARKETING ATTRIBUTION & ROI INTELLIGENCE - EXECUTIVE SUMMARY"
    ws1["A1"].font = title_font
    ws1["A1"].fill = title_fill
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")

    ws1.merge_cells("A3:J3")
    ws1["A3"] = "Performance Period: FY 2025 | Portfolio Size: 8,572 Campaigns | Total Customer Journeys: 5,500+"
    ws1["A3"].font = subtitle_font
    ws1["A3"].fill = PatternFill(start_color="2E5B82", end_color="2E5B82", fill_type="solid")
    ws1["A3"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI Cards
    kpis = [
        ("Total Spend", f"${df['Marketing Spend'].sum():,.2f}", "A5:B6"),
        ("Total Revenue", f"${df['Revenue'].sum():,.2f}", "C5:D6"),
        ("Net Profit", f"${df['Net Profit'].sum():,.2f}", "E5:F6"),
        ("Portfolio ROAS", f"{df['Revenue'].sum() / df['Marketing Spend'].sum():.2f}x", "G5:H6"),
        ("Overall ROI", f"{((df['Revenue'].sum() - df['Marketing Spend'].sum()) / df['Marketing Spend'].sum()) * 100:,.1f}%", "I5:J6"),
        ("Conversions", f"{df['Conversions'].sum():,}", "A8:B9"),
        ("Total Leads", f"{df['Leads'].sum():,}", "C8:D9"),
        ("Total Clicks", f"{df['Clicks'].sum():,}", "E8:F9"),
        ("Blended CAC", f"${df['Marketing Spend'].sum() / df['Conversions'].sum():.2f}", "G8:H9"),
        ("Conversion Rate", f"{(df['Conversions'].sum() / df['Clicks'].sum()) * 100:.2f}%", "I8:J9"),
    ]

    for label, val, cell_range in kpis:
        ws1.merge_cells(cell_range)
        start_cell = cell_range.split(":")[0]
        ws1[start_cell] = f"{label.upper()}\n{val}"
        ws1[start_cell].font = Font(name=font_family, size=11, bold=True, color="1F497D")
        ws1[start_cell].fill = kpi_fill
        ws1[start_cell].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        # Apply border to merged range
        cells = ws1[cell_range]
        for row_c in cells:
            for c in row_c:
                c.border = thin_border

    # Channel Performance Snapshot Table on Executive Sheet
    ws1["A12"] = "Channel Performance Snapshot"
    ws1["A12"].font = section_font

    ch_summary = df.groupby("Marketing Channel").agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Clicks": "sum",
        "Conversions": "sum"
    }).reset_index()
    ch_summary["ROAS"] = ch_summary["Revenue"] / ch_summary["Marketing Spend"]
    ch_summary["ROI"] = ((ch_summary["Revenue"] - ch_summary["Marketing Spend"]) / ch_summary["Marketing Spend"]) * 100
    ch_summary["CAC"] = ch_summary["Marketing Spend"] / ch_summary["Conversions"]
    ch_summary["Conv_Rate"] = (ch_summary["Conversions"] / ch_summary["Clicks"]) * 100
    ch_summary = ch_summary.sort_values(by="Revenue", ascending=False).reset_index(drop=True)

    headers1 = ["Marketing Channel", "Total Spend", "Total Revenue", "Net Profit", "ROAS", "ROI (%)", "Conversions", "CAC ($)", "Conv. Rate (%)"]
    for col_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=14, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    curr_row = 15
    for _, row in ch_summary.iterrows():
        ws1.cell(row=curr_row, column=1, value=row["Marketing Channel"]).font = data_font
        ws1.cell(row=curr_row, column=2, value=row["Marketing Spend"]).number_format = '$#,##0'
        ws1.cell(row=curr_row, column=3, value=row["Revenue"]).number_format = '$#,##0'
        ws1.cell(row=curr_row, column=4, value=row["Net Profit"]).number_format = '$#,##0'
        ws1.cell(row=curr_row, column=5, value=row["ROAS"]).number_format = '0.00"x"'
        ws1.cell(row=curr_row, column=6, value=row["ROI"] / 100).number_format = '0.0%'
        ws1.cell(row=curr_row, column=7, value=row["Conversions"]).number_format = '#,##0'
        ws1.cell(row=curr_row, column=8, value=row["CAC"]).number_format = '$#,##0.00'
        ws1.cell(row=curr_row, column=9, value=row["Conv_Rate"] / 100).number_format = '0.00%'
        
        for c_idx in range(1, 10):
            cell = ws1.cell(row=curr_row, column=c_idx)
            cell.border = thin_border
            if curr_row % 2 == 0:
                cell.fill = zebra_fill
        curr_row += 1

    # Total row
    ws1.cell(row=curr_row, column=1, value="Total / Blended Portfolio").font = total_font
    ws1.cell(row=curr_row, column=2, value=f"=SUM(B15:B{curr_row-1})").number_format = '$#,##0'
    ws1.cell(row=curr_row, column=3, value=f"=SUM(C15:C{curr_row-1})").number_format = '$#,##0'
    ws1.cell(row=curr_row, column=4, value=f"=SUM(D15:D{curr_row-1})").number_format = '$#,##0'
    ws1.cell(row=curr_row, column=5, value=f"=C{curr_row}/B{curr_row}").number_format = '0.00"x"'
    ws1.cell(row=curr_row, column=6, value=f"=(C{curr_row}-B{curr_row})/B{curr_row}").number_format = '0.0%'
    ws1.cell(row=curr_row, column=7, value=f"=SUM(G15:G{curr_row-1})").number_format = '#,##0'
    ws1.cell(row=curr_row, column=8, value=f"=B{curr_row}/G{curr_row}").number_format = '$#,##0.00'
    ws1.cell(row=curr_row, column=9, value=f"=G{curr_row}/SUM(df_clicks)").number_format = '0.00%'

    for c_idx in range(1, 10):
        cell = ws1.cell(row=curr_row, column=c_idx)
        cell.font = total_font
        cell.fill = total_fill
        cell.border = total_border

    # Fix cell formula for total conv rate
    ws1.cell(row=curr_row, column=9, value=df["Conversions"].sum() / df["Clicks"].sum()).number_format = '0.00%'

    # =========================================================================
    # TAB 2: DETAILED CHANNEL PERFORMANCE
    # =========================================================================
    ws2 = wb.create_sheet(title="Channel Performance")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:N2")
    ws2["A1"] = "MARKETING CHANNEL COMPREHENSIVE PERFORMANCE MATRIX"
    ws2["A1"].font = title_font
    ws2["A1"].fill = title_fill
    ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")

    headers2 = [
        "Marketing Channel", "Total Spend ($)", "Impressions", "Clicks", "CTR (%)",
        "Leads", "Lead Rate (%)", "Conversions", "Conv. Rate (%)", "Revenue ($)",
        "Net Profit ($)", "ROAS", "ROI (%)", "CAC ($)"
    ]
    for col_idx, h in enumerate(headers2, 1):
        cell = ws2.cell(row=4, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    r_idx = 5
    for _, row in ch_summary.iterrows():
        impr = df[df["Marketing Channel"] == row["Marketing Channel"]]["Impressions"].sum()
        leads = df[df["Marketing Channel"] == row["Marketing Channel"]]["Leads"].sum()
        
        ws2.cell(row=r_idx, column=1, value=row["Marketing Channel"]).font = data_font
        ws2.cell(row=r_idx, column=2, value=row["Marketing Spend"]).number_format = '$#,##0'
        ws2.cell(row=r_idx, column=3, value=impr).number_format = '#,##0'
        ws2.cell(row=r_idx, column=4, value=row["Clicks"]).number_format = '#,##0'
        ws2.cell(row=r_idx, column=5, value=row["Clicks"] / impr).number_format = '0.00%'
        ws2.cell(row=r_idx, column=6, value=leads).number_format = '#,##0'
        ws2.cell(row=r_idx, column=7, value=leads / row["Clicks"]).number_format = '0.00%'
        ws2.cell(row=r_idx, column=8, value=row["Conversions"]).number_format = '#,##0'
        ws2.cell(row=r_idx, column=9, value=row["Conversions"] / row["Clicks"]).number_format = '0.00%'
        ws2.cell(row=r_idx, column=10, value=row["Revenue"]).number_format = '$#,##0'
        ws2.cell(row=r_idx, column=11, value=row["Net Profit"]).number_format = '$#,##0'
        ws2.cell(row=r_idx, column=12, value=row["ROAS"]).number_format = '0.00"x"'
        ws2.cell(row=r_idx, column=13, value=row["ROI"] / 100).number_format = '0.0%'
        ws2.cell(row=r_idx, column=14, value=row["CAC"]).number_format = '$#,##0.00'

        for c_idx in range(1, 15):
            cell = ws2.cell(row=r_idx, column=c_idx)
            cell.border = thin_border
            if r_idx % 2 == 0:
                cell.fill = zebra_fill
        r_idx += 1

    # Total Row
    ws2.cell(row=r_idx, column=1, value="Portfolio Total").font = total_font
    ws2.cell(row=r_idx, column=2, value=f"=SUM(B5:B{r_idx-1})").number_format = '$#,##0'
    ws2.cell(row=r_idx, column=3, value=f"=SUM(C5:C{r_idx-1})").number_format = '#,##0'
    ws2.cell(row=r_idx, column=4, value=f"=SUM(D5:D{r_idx-1})").number_format = '#,##0'
    ws2.cell(row=r_idx, column=5, value=f"=D{r_idx}/C{r_idx}").number_format = '0.00%'
    ws2.cell(row=r_idx, column=6, value=f"=SUM(F5:F{r_idx-1})").number_format = '#,##0'
    ws2.cell(row=r_idx, column=7, value=f"=F{r_idx}/D{r_idx}").number_format = '0.00%'
    ws2.cell(row=r_idx, column=8, value=f"=SUM(H5:H{r_idx-1})").number_format = '#,##0'
    ws2.cell(row=r_idx, column=9, value=f"=H{r_idx}/D{r_idx}").number_format = '0.00%'
    ws2.cell(row=r_idx, column=10, value=f"=SUM(J5:J{r_idx-1})").number_format = '$#,##0'
    ws2.cell(row=r_idx, column=11, value=f"=SUM(K5:K{r_idx-1})").number_format = '$#,##0'
    ws2.cell(row=r_idx, column=12, value=f"=J{r_idx}/B{r_idx}").number_format = '0.00"x"'
    ws2.cell(row=r_idx, column=13, value=f"=(J{r_idx}-B{r_idx})/B{r_idx}").number_format = '0.0%'
    ws2.cell(row=r_idx, column=14, value=f"=B{r_idx}/H{r_idx}").number_format = '$#,##0.00'

    for c_idx in range(1, 15):
        cell = ws2.cell(row=r_idx, column=c_idx)
        cell.font = total_font
        cell.fill = total_fill
        cell.border = total_border

    # =========================================================================
    # TAB 3: CAMPAIGN PERFORMANCE (TOP 10 & BOTTOM 10)
    # =========================================================================
    ws3 = wb.create_sheet(title="Campaign Analysis")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:I2")
    ws3["A1"] = "CAMPAIGN PERFORMANCE AUDIT: TOP STARS & UNDERPERFORMERS"
    ws3["A1"].font = title_font
    ws3["A1"].fill = title_fill
    ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")

    ws3["A4"] = "Top 10 Most Profitable Campaigns"
    ws3["A4"].font = section_font

    camp_perf = df.groupby(["Campaign ID", "Campaign Name", "Marketing Channel", "Campaign Status"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index()
    camp_perf["ROAS"] = camp_perf["Revenue"] / camp_perf["Marketing Spend"]
    camp_perf["ROI"] = ((camp_perf["Revenue"] - camp_perf["Marketing Spend"]) / camp_perf["Marketing Spend"]) * 100
    camp_perf["CAC"] = camp_perf["Marketing Spend"] / camp_perf["Conversions"]

    top_10 = camp_perf.sort_values(by="Net Profit", ascending=False).head(10).reset_index(drop=True)

    headers3 = ["Campaign ID", "Campaign Name", "Channel", "Status", "Spend ($)", "Revenue ($)", "Net Profit ($)", "ROAS", "CAC ($)"]
    for col_idx, h in enumerate(headers3, 1):
        cell = ws3.cell(row=5, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    r_idx = 6
    for _, row in top_10.iterrows():
        ws3.cell(row=r_idx, column=1, value=row["Campaign ID"]).font = data_font
        ws3.cell(row=r_idx, column=2, value=row["Campaign Name"]).font = data_font
        ws3.cell(row=r_idx, column=3, value=row["Marketing Channel"]).font = data_font
        ws3.cell(row=r_idx, column=4, value=row["Campaign Status"]).font = data_font
        ws3.cell(row=r_idx, column=5, value=row["Marketing Spend"]).number_format = '$#,##0'
        ws3.cell(row=r_idx, column=6, value=row["Revenue"]).number_format = '$#,##0'
        ws3.cell(row=r_idx, column=7, value=row["Net Profit"]).number_format = '$#,##0'
        ws3.cell(row=r_idx, column=8, value=row["ROAS"]).number_format = '0.00"x"'
        ws3.cell(row=r_idx, column=9, value=row["CAC"]).number_format = '$#,##0.00'
        for c_idx in range(1, 10):
            cell = ws3.cell(row=r_idx, column=c_idx)
            cell.border = thin_border
            if r_idx % 2 == 0:
                cell.fill = zebra_fill
        r_idx += 1

    # Bottom 10 by ROAS
    r_idx += 2
    ws3.cell(row=r_idx, column=1, value="Lowest Performing Campaigns (Budget Optimization Opportunities)").font = section_font
    r_idx += 1
    for col_idx, h in enumerate(headers3, 1):
        cell = ws3.cell(row=r_idx, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    r_idx += 1
    bottom_10 = camp_perf.sort_values(by="ROAS", ascending=True).head(10).reset_index(drop=True)
    for _, row in bottom_10.iterrows():
        ws3.cell(row=r_idx, column=1, value=row["Campaign ID"]).font = data_font
        ws3.cell(row=r_idx, column=2, value=row["Campaign Name"]).font = data_font
        ws3.cell(row=r_idx, column=3, value=row["Marketing Channel"]).font = data_font
        ws3.cell(row=r_idx, column=4, value=row["Campaign Status"]).font = data_font
        ws3.cell(row=r_idx, column=5, value=row["Marketing Spend"]).number_format = '$#,##0'
        ws3.cell(row=r_idx, column=6, value=row["Revenue"]).number_format = '$#,##0'
        ws3.cell(row=r_idx, column=7, value=row["Net Profit"]).number_format = '$#,##0'
        ws3.cell(row=r_idx, column=8, value=row["ROAS"]).number_format = '0.00"x"'
        ws3.cell(row=r_idx, column=9, value=row["CAC"]).number_format = '$#,##0.00'
        for c_idx in range(1, 10):
            cell = ws3.cell(row=r_idx, column=c_idx)
            cell.border = thin_border
            if r_idx % 2 == 0:
                cell.fill = zebra_fill
        r_idx += 1

    # =========================================================================
    # TAB 4: MARKETING ATTRIBUTION MODEL COMPARISON
    # =========================================================================
    ws4 = wb.create_sheet(title="Attribution Analysis")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:K2")
    ws4["A1"] = "MULTI-TOUCH MARKETING ATTRIBUTION MODEL COMPARISON"
    ws4["A1"].font = title_font
    ws4["A1"].fill = title_fill
    ws4["A1"].alignment = Alignment(horizontal="center", vertical="center")

    headers4 = [
        "Marketing Channel",
        "First-Touch Rev ($)", "First-Touch Share",
        "Last-Touch Rev ($)", "Last-Touch Share",
        "Linear Rev ($)", "Linear Share",
        "Position-Based Rev ($)", "Position-Based Share",
        "Shift (Last - First) ($)", "Variance Type"
    ]
    for col_idx, h in enumerate(headers4, 1):
        cell = ws4.cell(row=4, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    r_idx = 5
    for _, row in df_attr[df_attr["Marketing Channel"] != "Total"].iterrows():
        shift = row["Last_Touch_Revenue"] - row["First_Touch_Revenue"]
        var_type = "Bottom-of-Funnel Closer" if shift > 0 else "Top-of-Funnel Introducer"
        
        ws4.cell(row=r_idx, column=1, value=row["Marketing Channel"]).font = data_font
        ws4.cell(row=r_idx, column=2, value=row["First_Touch_Revenue"]).number_format = '$#,##0'
        ws4.cell(row=r_idx, column=3, value=row["First_Touch_Revenue_Share_Pct"] / 100).number_format = '0.0%'
        ws4.cell(row=r_idx, column=4, value=row["Last_Touch_Revenue"]).number_format = '$#,##0'
        ws4.cell(row=r_idx, column=5, value=row["Last_Touch_Revenue_Share_Pct"] / 100).number_format = '0.0%'
        ws4.cell(row=r_idx, column=6, value=row["Linear_Revenue"]).number_format = '$#,##0'
        ws4.cell(row=r_idx, column=7, value=row["Linear_Revenue_Share_Pct"] / 100).number_format = '0.0%'
        ws4.cell(row=r_idx, column=8, value=row["Position_Based_Revenue"]).number_format = '$#,##0'
        ws4.cell(row=r_idx, column=9, value=row["Position_Based_Revenue_Share_Pct"] / 100).number_format = '0.0%'
        ws4.cell(row=r_idx, column=10, value=shift).number_format = '$#,##0;($#,##0)'
        ws4.cell(row=r_idx, column=11, value=var_type).font = Font(name=font_family, size=9, bold=True, color="1F497D" if shift > 0 else "C00000")

        for c_idx in range(1, 12):
            cell = ws4.cell(row=r_idx, column=c_idx)
            cell.border = thin_border
            if r_idx % 2 == 0:
                cell.fill = zebra_fill
        r_idx += 1

    # Total row
    tot_row = df_attr[df_attr["Marketing Channel"] == "Total"].iloc[0]
    ws4.cell(row=r_idx, column=1, value="Total Attributed Revenue").font = total_font
    ws4.cell(row=r_idx, column=2, value=tot_row["First_Touch_Revenue"]).number_format = '$#,##0'
    ws4.cell(row=r_idx, column=3, value=1.0).number_format = '0.0%'
    ws4.cell(row=r_idx, column=4, value=tot_row["Last_Touch_Revenue"]).number_format = '$#,##0'
    ws4.cell(row=r_idx, column=5, value=1.0).number_format = '0.0%'
    ws4.cell(row=r_idx, column=6, value=tot_row["Linear_Revenue"]).number_format = '$#,##0'
    ws4.cell(row=r_idx, column=7, value=1.0).number_format = '0.0%'
    ws4.cell(row=r_idx, column=8, value=tot_row["Position_Based_Revenue"]).number_format = '$#,##0'
    ws4.cell(row=r_idx, column=9, value=1.0).number_format = '0.0%'
    ws4.cell(row=r_idx, column=10, value=0.0).number_format = '$#,##0'
    ws4.cell(row=r_idx, column=11, value="Balanced").font = total_font

    for c_idx in range(1, 12):
        cell = ws4.cell(row=r_idx, column=c_idx)
        cell.font = total_font
        cell.fill = total_fill
        cell.border = total_border

    # =========================================================================
    # TAB 5: MONTHLY PERFORMANCE TRENDS & NATIVE CHART
    # =========================================================================
    ws5 = wb.create_sheet(title="Monthly Trends")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:I2")
    ws5["A1"] = "MONTHLY MARKETING FINANCIALS & MOM GROWTH"
    ws5["A1"].font = title_font
    ws5["A1"].fill = title_fill
    ws5["A1"].alignment = Alignment(horizontal="center", vertical="center")

    headers5 = ["Month", "Marketing Spend ($)", "Revenue ($)", "Net Profit ($)", "ROAS", "MoM Rev Growth (%)", "Conversions", "CAC ($)"]
    for col_idx, h in enumerate(headers5, 1):
        cell = ws5.cell(row=4, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    monthly_df = df.groupby(["Month", "Month_Name"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index().sort_values(by="Month")

    r_idx = 5
    prev_rev = None
    for _, row in monthly_df.iterrows():
        rev = row["Revenue"]
        growth = (rev - prev_rev) / prev_rev if prev_rev is not None else 0.0
        prev_rev = rev

        ws5.cell(row=r_idx, column=1, value=row["Month_Name"]).font = data_font
        ws5.cell(row=r_idx, column=2, value=row["Marketing Spend"]).number_format = '$#,##0'
        ws5.cell(row=r_idx, column=3, value=row["Revenue"]).number_format = '$#,##0'
        ws5.cell(row=r_idx, column=4, value=row["Net Profit"]).number_format = '$#,##0'
        ws5.cell(row=r_idx, column=5, value=row["Revenue"] / row["Marketing Spend"]).number_format = '0.00"x"'
        ws5.cell(row=r_idx, column=6, value=growth).number_format = '0.0%'
        ws5.cell(row=r_idx, column=7, value=row["Conversions"]).number_format = '#,##0'
        ws5.cell(row=r_idx, column=8, value=row["Marketing Spend"] / row["Conversions"]).number_format = '$#,##0.00'

        for c_idx in range(1, 9):
            cell = ws5.cell(row=r_idx, column=c_idx)
            cell.border = thin_border
            if r_idx % 2 == 0:
                cell.fill = zebra_fill
        r_idx += 1

    # Embed Native Excel Bar/Line Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Monthly Marketing Spend vs. Revenue (FY 2025)"
    chart.y_axis.title = "Amount (USD $)"
    chart.x_axis.title = "Month"
    chart.width = 16
    chart.height = 9

    data_ref = Reference(ws5, min_col=2, min_row=4, max_col=3, max_row=16)
    cats_ref = Reference(ws5, min_col=1, min_row=5, max_row=16)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    ws5.add_chart(chart, "A19")

    # Auto-adjust column widths for all sheets
    for ws in [ws1, ws2, ws3, ws4, ws5]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                # ignore merged cells spanning across
                if cell.coordinate in ws.merged_cells:
                    continue
                if cell.value:
                    val_str = str(cell.value)
                    max_len = max(max_len, len(val_str.split("\n")[0]))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    # Save workbook
    wb.save(output_path)
    print(f"Excel report successfully generated: {output_path}")


if __name__ == "__main__":
    create_excel_report()
