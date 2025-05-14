from data.loader import load_real_data
from views.analysis import handle_analysis_menu
from views.components import render_sidebar_header, render_footer, local_css, render_sidebar_footer
from data.loader import load_stock_transaction_data
import streamlit as st

st.header('DABAFIN - PHÂN TÍCH TÀI CHÍNH DOANH NGHIỆP')

def main():
    local_css()
    data = load_real_data()
    render_sidebar_header()
    render_sidebar_footer()
    # 🔁 Thêm dữ liệu phân tích kỹ thuật
    transaction_data = load_stock_transaction_data()
    data.update(transaction_data)  # Hợp nhất vào dict `data`

    menu_option = st.sidebar.radio("MENU CHÍNH", ["Phân tích", "Dự đoán", "Tối ưu đầu tư"])
    st.sidebar.markdown("---")

    if menu_option == "Phân tích":
        handle_analysis_menu(data)
    elif menu_option == "Dự đoán":
        st.warning('Chuc nang dang duoc xay dung')
    elif menu_option == "Tối ưu đầu tư":
        st.write('hi')
    render_footer()

if __name__ == "__main__":
    main()

