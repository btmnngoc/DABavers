import streamlit as st
import plotly.express as px
from datetime import datetime
from utils.plotting import plot_financial_metrics
import pandas as pd
from pandas.api.types import CategoricalDtype
from data.loader import get_indicator_groups, load_financial_long_df

def clean_indicator_name(name):
    # Tùy logic bạn muốn xử lý cột, đây là ví dụ
    return name.strip().replace("_", " ").title()

def local_css():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] * { color: white !important; }
        [data-testid="stSidebar"] { background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%) !important; }
        .stRadio [role="radiogroup"] label {
            background-color: rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
            padding: 8px 12px !important;
            margin: 5px 0 !important;
        }
        .stRadio [role="radiogroup"] label:hover {
            background-color: rgba(255,255,255,0.2) !important;
        }
        .stRadio [role="radiogroup"] [data-baseweb="radio"]:checked+label {
            background-color: rgba(255,255,255,0.3) !important;
            font-weight: bold !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header():
    st.sidebar.markdown("""
    <div style="text-align:center">
        <h1 style="color:white">DABAVERSE</h1>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center; color:gray">
        <p>DABAFIN - Hệ thống phân tích đầu tư</p>
        <p>Dữ liệu cập nhật đến {datetime.now().strftime("%d/%m/%Y")}</p>
    </div>
    """, unsafe_allow_html=True)

def render_market_overview(data):
    st.header("📊 Tổng Quan Thị Trường")
   


def render_financial_health(data, stock):
    """Display financial health analysis for a stock"""
    st.markdown(
    f"""
    <h2 style='font-weight: 700; text-align: center;'>
        <span style='color: #0E6994;'>📈 SỨC KHOẺ TÀI CHÍNH -</span>
        <span style='color: #FD6200;'>{stock}</span>
    </h2>
    """,
    unsafe_allow_html=True
)
    # Load data
    from data.loader import load_financial_data, get_indicator_groups
    df = load_financial_data()
    indicator_groups = get_indicator_groups()

    # Filter for selected stock
    df_stock = df[df['StockID'] == stock]

    # Create tabs for each indicator group
    tabs = st.tabs(list(indicator_groups.keys()))

    for tab, (group_name, indicators) in zip(tabs, indicator_groups.items()):
        with tab:
            # Get data for current group
            sub = df_stock[df_stock['Indicator'].isin(indicators)]

            if sub.empty:
                st.warning(f"Không có dữ liệu cho nhóm {group_name}")
                continue

            # Display data table
            st.subheader(f"Bảng số liệu {group_name}")
            # Trong hàm show_financial_health()
            pivot_df = sub.pivot(index='Period', columns='Indicator', values='Value')
            pivot_df = pivot_df.sort_index()  # Thêm dòng này để sắp xếp theo thứ tự thời gian
            pivot_df.columns = [clean_indicator_name(col) for col in pivot_df.columns]
            st.dataframe(
                pivot_df.style.format("{:.2f}"),
                use_container_width=True,
                height=300
            )

            # Display interactive chart
            st.subheader(f"Biểu đồ {group_name}")
            fig = plot_financial_metrics(
                df,
                stock,
                {group_name: indicators}
            )

            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Không có dữ liệu để vẽ biểu đồ")



import plotly.graph_objects as go
from services.financial_utils import compute_rsi

def render_stock_movement(data, stock):
    st.markdown(
    f"""
    <h2 style='font-weight: 700; text-align: center;'>
        <span style='color: #0E6994;'>📊 BIẾN ĐỘNG CỔ PHIẾU  -</span>
        <span style='color: #FD6200;'>{stock}</span>
    </h2>
    """,
    unsafe_allow_html=True
)

    df = data.get(stock)
    if df is None or df.empty:
        st.warning(f"Không có dữ liệu cho {stock}")
        return

    df = df.copy()

    # === Chỉ báo kỹ thuật ===
    df['SMA_14'] = df['Closing Price'].rolling(window=14).mean()
    df['RSI_14'] = compute_rsi(df['Closing Price'], 14)
    df['EMA_12'] = df['Closing Price'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Closing Price'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal_Line']
    sma_20 = df['Closing Price'].rolling(window=20).mean()
    std_20 = df['Closing Price'].rolling(window=20).std()
    df['BB_upper'] = sma_20 + 2 * std_20
    df['BB_lower'] = sma_20 - 2 * std_20
    df['BB_middle'] = sma_20

    # === TABS ===
    tabs = st.tabs(["Bảng số liệu", "Bollinger Bands", "SMA/EMA", "MACD"])

    with tabs[0]:
        st.subheader("📋 Bảng kỹ thuật")
        display_cols = ['Date', 'Closing Price', 'SMA_14', 'EMA_12', 'EMA_26', 'MACD', 'Signal_Line', 'RSI_14', 'BB_upper', 'BB_middle', 'BB_lower']
        display_df = df[display_cols].set_index('Date')
        st.dataframe(display_df.style.format("{:.2f}"), use_container_width=True, height=300)

    with tabs[1]:
        st.subheader("📈 Bollinger Bands (Kênh biến động giá + Cảnh báo breakout)")

        fig = go.Figure()

        # 1. Vùng tô BB
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['BB_upper'],
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False,
            hoverinfo='skip',
            name='BB Upper'
        ))

        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['BB_lower'],
            fill='tonexty',
            fillcolor='rgba(132,208,208,0.2)',
            line=dict(color='rgba(0,0,0,0)'),
            name='Bollinger Band',
            hoverinfo='skip'
        ))

        # 2. Giá đóng cửa
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Closing Price'],
            name='Giá đóng cửa',
            line=dict(color='#0E6994', width=2)
        ))

        # 3. Đường giữa
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['BB_middle'],
            name='BB Middle',
            line=dict(color='#FD6200', width=2, dash='dot')
        ))

        # 4. Breakout trên
        breakout_up = df[df['Closing Price'] > df['BB_upper']]
        if not breakout_up.empty:
            fig.add_trace(go.Scatter(
                x=breakout_up['Date'],
                y=breakout_up['Closing Price'],
                mode='markers',
                name='Breakout ↑',
                marker=dict(color='green', symbol='triangle-up', size=10),
                hovertext='Vượt BB_upper - Tín hiệu tăng',
                hoverinfo='text'
            ))

        # 5. Breakout dưới
        breakout_down = df[df['Closing Price'] < df['BB_lower']]
        if not breakout_down.empty:
            fig.add_trace(go.Scatter(
                x=breakout_down['Date'],
                y=breakout_down['Closing Price'],
                mode='markers',
                name='Breakout ↓',
                marker=dict(color='red', symbol='triangle-down', size=10),
                hovertext='Rớt BB_lower - Tín hiệu giảm',
                hoverinfo='text'
            ))

        fig.update_layout(
            height=520,
            title="Bollinger Bands & Giá đóng cửa + Cảnh báo breakout",
            hovermode="x unified",
            legend=dict(orientation="h", y=1.2),
            margin=dict(t=60, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.subheader("📉 SMA & EMA")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Closing Price'], name='Giá đóng cửa', line=dict(color='#D8A100')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_14'], name='SMA 14', line=dict(color='#FD6200')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_12'], name='EMA 12', line=dict(color='#0E6994')))
        fig.update_layout(height=500, hovermode="x unified", legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        st.subheader("📊 MACD với vùng phân kỳ")

        fig = go.Figure()

        # Line MACD & Signal
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['MACD'],
            name='MACD', line=dict(color='#0E6994', width=2),
            mode='lines'
        ))

        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Signal_Line'],
            name='Signal', line=dict(color='#FD6200', width=2, dash='dot'),
            mode='lines'
        ))

        # Fill between MACD and Signal → tô màu
        for i in range(len(df) - 1):
            x_vals = [df['Date'].iloc[i], df['Date'].iloc[i + 1], df['Date'].iloc[i + 1], df['Date'].iloc[i]]
            y_macd = [df['MACD'].iloc[i], df['MACD'].iloc[i + 1], df['Signal_Line'].iloc[i + 1],
                      df['Signal_Line'].iloc[i]]
            color = 'rgba(46, 204, 113, 0.3)' if df['MACD'].iloc[i] > df['Signal_Line'].iloc[
                i] else 'rgba(231, 76, 60, 0.3)'

            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_macd,
                fill='toself',
                fillcolor=color,
                line=dict(color='rgba(255,255,255,0)'),  # không viền
                hoverinfo="skip",
                showlegend=False
            ))

        # Zero line
        fig.add_hline(y=0, line=dict(color='gray', dash='dot'))

        fig.update_layout(
            height=500,
            hovermode="x unified",
            legend=dict(orientation="h", y=1.2),
            margin=dict(t=60, b=40),
            title="MACD & Tín hiệu phân kỳ"
        )

        st.plotly_chart(fig, use_container_width=True)

def render_sector_indicators(data, sector_name="Ngành Công nghệ thông tin"):
    st.markdown(
    f"""
    <h2 style='font-weight: 700; text-align: center;'>
        <span style='color: #0E6994;'>📊 CHỈ SỐ TÀI CHÍNH THỊ TRƯỜNG  -</span>
        <span style='color: #FD6200;'>{sector_name}</span>
    </h2>
    """,
    unsafe_allow_html=True
)
    df_long = load_financial_long_df()

    indicator_groups = get_indicator_groups()
    # Tạo tabs
    tabs = st.tabs(list(indicator_groups.keys()))


    for tab, (group_name, indicator) in zip(tabs, indicator_groups.items()):
        with tab:
            sub = df_long[df_long['Indicator'].isin(indicator)]

            if sub.empty:
                st.warning(f"Không có dữ liệu cho nhóm {group_name}")
                continue

            st.subheader(f"Bảng số liệu - {group_name}")
            pivot_df = sub.pivot(index='Period', columns='Indicator', values='Value')
            pivot_df = pivot_df.sort_index()
            pivot_df.columns = [clean_indicator_name(col) for col in pivot_df.columns]
            st.dataframe(
                pivot_df.style.format("{:.2f}"),
                use_container_width=True,
                height=300
            )

            st.subheader(f"Biểu đồ - {group_name}")
            fig = plot_financial_metrics(df_long, stock=sector_name, indicator_group={group_name: indicators})
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Không có dữ liệu để vẽ biểu đồ")
import streamlit as st

def render_brand_title():
    st.markdown(
        """
        <div style='text-align: center; line-height: 1.4;'>
            <div style='font-size: 2.8rem; font-weight: 900; color: #f06428;'>DABAFIN</div>
            <div style='font-size: 1.8rem; font-weight: 600; color: #1f4e79;'>PHÂN TÍCH TÀI CHÍNH DOANH NGHIỆP</div>
        </div>
        """,
        unsafe_allow_html=True
    )
