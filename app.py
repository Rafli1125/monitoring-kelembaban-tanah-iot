import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard Monitoring Kelembaban Tanah",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: white;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    .block-container {
        padding-top: 0rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }

    .main-header {
        background-color: #06182d;
        color: white;
        padding: 22px 32px;
        margin-left: -1.5rem;
        margin-right: -1.5rem;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .main-header h1 {
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 1px;
        margin: 0;
        text-align: center;
        width: 100%;
    }

    .header-icon {
        font-size: 34px;
        font-weight: 900;
        color: white;
    }

    .card {
        border: 1.5px solid #c8c8c8;
        border-radius: 8px;
        background-color: white;
        height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #06182d;
    }

    .card-title {
        font-size: 27px;
        font-weight: 900;
        margin-bottom: 22px;
        color: #06182d;
        text-align: center;
    }

    .card-value {
        font-size: 66px;
        font-weight: 900;
        line-height: 1;
        color: #06182d;
        text-align: center;
    }

    .online {
        color: #15823a;
    }

    .panel {
        border: 1.5px solid #c8c8c8;
        border-radius: 8px;
        background-color: white;
        padding: 28px 32px;
        min-height: 510px;
        margin-top: 24px;
    }

    .panel-title {
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 18px;
        color: #06182d;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        table-layout: fixed;
    }

    th {
        background-color: #06182d;
        color: white;
        font-size: 24px;
        font-weight: 900;
        padding: 18px 8px;
        border: 1px solid #c8c8c8;
        text-align: center;
    }

    td {
        color: #111827;
        font-size: 26px;
        font-weight: 800;
        padding: 18px 8px;
        border: 1px solid #c8c8c8;
        text-align: center;
    }

    @media screen and (max-width: 900px) {
        .main-header h1 {
            font-size: 22px;
        }

        .card-title {
            font-size: 20px;
        }

        .card-value {
            font-size: 44px;
        }

        th, td {
            font-size: 15px;
            padding: 10px 4px;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="header-icon">☰</div>
    <h1>Dashboard Monitoring Kelembaban Tanah</h1>
    <div class="header-icon">⌁</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">Kelembaban Tanah</div>
        <div class="card-value">42%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">Status Tanah</div>
        <div class="card-value">Lembab</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">Status Pompa</div>
        <div class="card-value">Mati</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-title">Koneksi Sistem</div>
        <div class="card-value online">Online</div>
    </div>
    """, unsafe_allow_html=True)

data = pd.DataFrame({
    "Waktu": ["08:00", "08:10", "08:20", "08:30", "08:40"],
    "Kelembaban": [25, 32, 38, 42, 45],
    "Status Tanah": ["Kering", "Lembab", "Lembab", "Lembab", "Lembab"],
    "Status Pompa": ["Aktif", "Mati", "Mati", "Mati", "Mati"]
})

left, right = st.columns(2)

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Grafik Kelembaban Tanah</div>', unsafe_allow_html=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["Waktu"],
        y=data["Kelembaban"],
        mode="lines+markers+text",
        text=[f"{v}%" for v in data["Kelembaban"]],
        textposition="top center",
        line=dict(color="#0b4ea2", width=4),
        marker=dict(size=12, color="#0b4ea2"),
        textfont=dict(size=16, color="#111827", family="Arial Black")
    ))

    fig.update_layout(
        height=390,
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            title=dict(text="Waktu", font=dict(size=20, color="#06182d", family="Arial Black")),
            tickfont=dict(size=16, color="#111827", family="Arial Black"),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text="Kelembaban (%)", font=dict(size=20, color="#06182d", family="Arial Black")),
            tickfont=dict(size=16, color="#111827", family="Arial Black"),
            range=[0, 60],
            dtick=10,
            ticksuffix="%",
            gridcolor="#d1d5db"
        ),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Riwayat Monitoring</div>', unsafe_allow_html=True)

    table_html = """
    <table>
        <thead>
            <tr>
                <th>Waktu</th>
                <th>Kelembaban</th>
                <th>Status Tanah</th>
                <th>Status Pompa</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>08:00</td><td>25%</td><td>Kering</td><td>Aktif</td></tr>
            <tr><td>08:10</td><td>32%</td><td>Lembab</td><td>Mati</td></tr>
            <tr><td>08:20</td><td>38%</td><td>Lembab</td><td>Mati</td></tr>
            <tr><td>08:30</td><td>42%</td><td>Lembab</td><td>Mati</td></tr>
            <tr><td>08:40</td><td>45%</td><td>Lembab</td><td>Mati</td></tr>
        </tbody>
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)