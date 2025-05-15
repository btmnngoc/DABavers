from data.loader import load_real_data
from views.analysis import handle_analysis_menu
from views.components import render_sidebar_header, render_footer, local_css
from data.loader import load_stock_transaction_data
import streamlit as st

st.header('DABAFIN - PHÂN TÍCH TÀI CHÍNH DOANH NGHIỆP')

def main():
    local_css()
    data = load_real_data()
    render_sidebar_header()
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

    st.sidebar.markdown("---")
    st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 0.85rem; color: gray; margin-top: 20px;'>
        © 2025 DABAFIN | Phân tích tài chính doanh nghiệp
    </div>
    """,
    unsafe_allow_html=True
)


if __name__ == "__main__":
    main()

