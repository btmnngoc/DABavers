from views.components import render_financial_health, render_stock_movement, render_sector_indicators
import streamlit as st
from pandas.api.types import CategoricalDtype  # THÊM VÀO


def handle_analysis_menu(data):
    analysis_type = st.sidebar.radio("LOẠI PHÂN TÍCH", [
        "Tổng quan", 
        "Sức khỏe tài chính doanh nghiệp", 
        "Biến động cổ phiếu doanh nghiệp"
    ])

    if analysis_type == "Tổng quan":
        render_sector_indicators('assets/data/financial_metrics_it_processed.csv', sector_name="Ngành CNTT")
    elif analysis_type == "Sức khỏe tài chính doanh nghiệp":
        stock = st.sidebar.radio("CHỌN MÃ", ["FPT", "CMG"])
        render_financial_health(data, stock)
    elif analysis_type == "Biến động cổ phiếu doanh nghiệp":
        stock = st.sidebar.radio("CHỌN MÃ", ["FPT", "CMG"])
        render_stock_movement(data, stock)

