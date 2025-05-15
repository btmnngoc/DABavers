from views.components import render_financial_health, render_stock_movement, render_sector_indicators
import streamlit as st
csv_path = "Bản sao 6.5 (his) financialreport_metrics_Nhóm ngành_Công nghệ thông tin (of FPT_CMG)_processed.csv"

def handle_analysis_menu(data):
    analysis_type = st.sidebar.radio("LOẠI PHÂN TÍCH", [
        "Tổng quan", 
        "Sức khỏe tài chính doanh nghiệp", 
        "Biến động cổ phiếu doanh nghiệp"
    ])

    if analysis_type == "Tổng quan":
        render_sector_indicators(csv_path)
    elif analysis_type == "Sức khỏe tài chính doanh nghiệp":
        stock = st.sidebar.radio("CHỌN MÃ", ["FPT", "CMG"])
        render_financial_health(data, stock)
    elif analysis_type == "Biến động cổ phiếu doanh nghiệp":
        stock = st.sidebar.radio("CHỌN MÃ", ["FPT", "CMG"])
        render_stock_movement(data, stock)


import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import re
from data.loader import load_financial_long_df

indicator_groups = {
    'Khả năng sinh lời': [
        'Tỷ suất sinh lợi trên tổng tài sản bình quân (ROAA)\n%',
        'Tỷ suất lợi nhuận trên vốn chủ sở hữu bình quân (ROEA)\n%',
        'Tỷ suất lợi nhuận gộp biên\n%',
        'Tỷ suất sinh lợi trên doanh thu thuần\n%'
    ],
    'Khả năng thanh toán': [
        'Tỷ số thanh toán hiện hành (ngắn hạn)\nLần',
        'Tỷ số thanh toán nhanh\nLần',
        'Tỷ số thanh toán bằng tiền mặt\nLần'
    ],
    'Đòn bẩy tài chính': [
        'Tỷ số Nợ trên Tổng tài sản\n%',
        'Tỷ số Nợ trên Vốn chủ sở hữu\n%'
    ],
    'Hiệu quả hoạt động': [
        'Vòng quay tổng tài sản (Hiệu suất sử dụng toàn bộ tài sản)\nVòng',
        'Vòng quay hàng tồn kho\nVòng',
        'Vòng quay phải thu khách hàng\nVòng'
    ],
    'Chỉ số thị trường': [
        'Chỉ số giá thị trường trên thu nhập (P/E)\nLần',
        'Chỉ số giá thị trường trên giá trị sổ sách (P/B)\nLần',
        'Beta\nLần'
    ]
}

custom_palette = ['#004c97', '#f2a900', '#f45d01', '#7ec8e3']
sns.set_style("whitegrid")
sns.set_palette(sns.color_palette(custom_palette))

plt.rcParams.update({
    'figure.figsize': (14, 6),
    'axes.titlesize': 18,
    'axes.labelsize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'font.family': 'DejaVu Sans',
    'lines.linewidth': 2.5,
    'lines.markersize': 8
})

def extract_unit(indicator_list):
    units = set()
    for ind in indicator_list:
        match = re.search(r'\n(.+)', ind)
        if match:
            units.add(match.group(1))
    return ', '.join(units) if units else ''

def show_financial_analysis():
    df_long = load_financial_long_df()

    st.subheader("📊 Phân tích theo nhóm chỉ số tài chính")
    selected_group = st.selectbox("Chọn nhóm chỉ số", list(indicator_groups.keys()))
    indicators = indicator_groups[selected_group]

    sub = df_long[df_long['Indicator'].isin(indicators)]

    if sub.empty:
        st.warning("Không có dữ liệu cho nhóm này.")
        return

    pivot_df = sub.pivot(index='Period', columns='Indicator', values='Value')
    pivot_df.columns = [i.split('\n')[0] for i in pivot_df.columns]
    st.dataframe(pivot_df.style.format("{:.2f}"), use_container_width=True)

    fig, ax = plt.subplots()
    for idx, indicator in enumerate(indicators):
        line_data = sub[sub['Indicator'] == indicator]
        if not line_data.empty:
            sns.lineplot(
                data=line_data,
                x='Period',
                y='Value',
                label=indicator.split('\n')[0],
                color=custom_palette[idx % len(custom_palette)],
                marker='o',
                ax=ax
            )

    ax.set_title(selected_group, loc='center', fontweight='bold')
    ax.set_xlabel("Kỳ báo cáo")
    ax.set_ylabel(f"Giá trị ({extract_unit(indicators)})")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(title='Chỉ số', loc='upper left')
    st.pyplot(fig)
