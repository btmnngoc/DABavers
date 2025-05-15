from views.components import render_financial_health, render_stock_movement
import streamlit as st

def handle_analysis_menu(data):
    analysis_type = st.sidebar.radio("LOẠI PHÂN TÍCH", [
        "Tổng quan", 
        "Sức khỏe tài chính doanh nghiệp", 
        "Biến động cổ phiếu doanh nghiệp"
    ])

    if analysis_type == "Tổng quan":
        st.write('hellu cả nhà, mình là minh ngọc đây')
    elif analysis_type == "Sức khỏe tài chính doanh nghiệp":
        stock = st.sidebar.radio("CHỌN MÃ", ["FPT", "CMG"])
        render_financial_health(data, stock)
    elif analysis_type == "Biến động cổ phiếu doanh nghiệp":
        stock = st.sidebar.radio("CHỌN MÃ", ["FPT", "CMG"])
        render_stock_movement(data, stock)



