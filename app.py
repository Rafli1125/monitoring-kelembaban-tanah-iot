import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Monitoring Kelembaban Tanah",
    page_icon="🌱",
    layout="wide"
)

# =========================
# STYLE CSS
# =========================
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    .block-container {
        padding-top: 0rem;
        padding-left: 1.4rem;
        padding-right: 1.4rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #d1d5db;
    }

    .main-header {
        background-color: #06182d;
        color: white;
        padding: 26px 32px;
        margin-left: -1.4rem;
        margin-right: -1.4rem;
        margin-bottom: 22px;
        display: grid;
        grid-template-columns: 60px 1fr 60px;
        align-items: center;
    }

    .main-header h1 {
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 1px;
        text-align: center;
        margin: 0;
        color: white;
    }

    .header-icon {
        font-size: 34px;
        font-weight: 900;
        color: white;
        text-align: center;
    }

    .control-bar {
        background-color: #f8fafc;
        border: 1.5px solid #c8c8c8;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 18px;
        color: #06182d;
        font-size: 18px;
        font-weight: 800;
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
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 26px;
        font-weight: 900;
        margin-bottom: 22px;
        color: #06182d;
        text-align: center;
    }

    .card-value {
        font-size: 64px;
        font-weight: 900;
        line-height: 1;
        color: #06182d;
        text-align: center;
    }

    .online {
        color: #15823a;
    }

    .offline {
        color: #b91c1c;
    }

    .section-title {
        font-size: 31px;
        font-weight: 900;
        color: #06182d;
        margin-bottom: 18px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #c8c8c8;
        border-radius: 8px;
        background-color: white;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        margin-top: 4px;
    }

    th {
        background-color: #06182d;
        color: white;
        font-size: 22px;
        font-weight: 900;
        padding: 17px 8px;
        border: 1px solid #c8c8c8;
        text-align: center;
    }

    td {
        color: #111827;
        font-size: 24px;
        font-weight: 800;
        padding: 16px 8px;
        border: 1px solid #c8c8c8;
        text-align: center;
    }

    .footer-note {
        margin-top: 16px;
        padding: 12px 14px;
        background-color: #f8fafc;
        border-left: 5px solid #06182d;
        font-size: 16px;
        font-weight: 700;
        color: #06182d;
    }

    div.stButton > button {
        width: 100%;
        background-color: #06182d;
        color: white;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        font-weight: 800;
        padding: 10px 14px;
    }

    div.stButton > button:hover {
        background-color: #0b2a4a;
        color: white;
        border: none;
    }

    @media screen and (max-width: 900px) {
        .main-header {
            grid-template-columns: 40px 1fr 40px;
            padding: 20px 16px;
        }

        .main-header h1 {
            font-size: 22px;
        }

        .header-icon {
            font-size: 26px;
        }

        .card-title {
            font-size: 19px;
        }

        .card-value {
            font-size: 44px;
        }

        .section-title {
            font-size: 24px;
        }

        th, td {
            font-size: 14px;
            padding: 10px 4px;
        }
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "mode_data" not in st.session_state:
    st.session_state.mode_data = "Normal"

if "status_koneksi" not in st.session_state:
    st.session_state.status_koneksi = "Online"

if "pompa_manual" not in st.session_state:
    st.session_state.pompa_manual = False

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# =========================
# DATA SIMULASI
# =========================
data_normal = pd.DataFrame({
    "Waktu": ["08:00", "08:10", "08:20", "08:30", "08:40"],
    "Kelembaban": [25, 32, 38, 42, 45]
})

data_kering = pd.DataFrame({
    "Waktu": ["08:00", "08:10", "08:20", "08:30", "08:40"],
    "Kelembaban": [18, 21, 24, 25, 27]
})

data_lembab = pd.DataFrame({
    "Waktu": ["08:00", "08:10", "08:20", "08:30", "08:40"],
    "Kelembaban": [38, 41, 42, 45, 48]
})

# =========================
# SIDEBAR INTERAKTIF
# =========================
with st.sidebar:
    st.markdown("## Pengaturan Dashboard")

    mode = st.selectbox(
        "Mode Data",
        ["Normal", "Tanah Kering", "Tanah Lembab"],
        index=["Normal", "Tanah Kering", "Tanah Lembab"].index(st.session_state.mode_data)
    )

    threshold = st.slider(
        "Batas Tanah Kering (%)",
        min_value=10,
        max_value=60,
        value=30,
        step=1
    )

    koneksi = st.radio(
        "Status Koneksi",
        ["Online", "Offline"],
        index=0 if st.session_state.status_koneksi == "Online" else 1
    )

    kontrol_pompa = st.toggle(
        "Paksa Pompa Aktif",
        value=st.session_state.pompa_manual
    )

    if st.button("Perbarui Dashboard"):
        st.session_state.mode_data = mode
        st.session_state.status_koneksi = koneksi
        st.session_state.pompa_manual = kontrol_pompa
        st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
        st.rerun()

    if st.button("Reset Data"):
        st.session_state.mode_data = "Normal"
        st.session_state.status_koneksi = "Online"
        st.session_state.pompa_manual = False
        st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
        st.rerun()

# =========================
# PILIH DATA
# =========================
if st.session_state.mode_data == "Tanah Kering":
    data = data_kering.copy()
elif st.session_state.mode_data == "Tanah Lembab":
    data = data_lembab.copy()
else:
    data = data_normal.copy()

kelembaban_akhir = int(data["Kelembaban"].iloc[-2]) if st.session_state.mode_data == "Normal" else int(data["Kelembaban"].iloc[-1])

status_tanah = "Kering" if kelembaban_akhir < threshold else "Lembab"

if st.session_state.pompa_manual:
    status_pompa = "Aktif"
else:
    status_pompa = "Aktif" if kelembaban_akhir < threshold else "Mati"

data["Status Tanah"] = data["Kelembaban"].apply(lambda x: "Kering" if x < threshold else "Lembab")
data["Status Pompa"] = data["Kelembaban"].apply(lambda x: "Aktif" if x < threshold else "Mati")
data["Kelembaban Teks"] = data["Kelembaban"].astype(str) + "%"

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-header">
    <div class="header-icon">☰</div>
    <h1>Dashboard Monitoring Kelembaban Tanah</h1>
    <div class="header-icon">⌁</div>
</div>
""", unsafe_allow_html=True)

# =========================
# CONTROL BAR
# =========================
st.markdown(f"""
<div class="control-bar">
    Mode Data: {st.session_state.mode_data} &nbsp;&nbsp; | &nbsp;&nbsp;
    Batas Tanah Kering: {threshold}% &nbsp;&nbsp; | &nbsp;&nbsp;
    Update Terakhir: {st.session_state.last_update}
</div>
""", unsafe_allow_html=True)

# =========================
# CARD UTAMA
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Kelembaban Tanah</div>
        <div class="card-value">{kelembaban_akhir}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Status Tanah</div>
        <div class="card-value">{status_tanah}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Status Pompa</div>
        <div class="card-value">{status_pompa}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    koneksi_class = "online" if st.session_state.status_koneksi == "Online" else "offline"
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Koneksi Sistem</div>
        <div class="card-value {koneksi_class}">{st.session_state.status_koneksi}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# GRAFIK DAN TABEL
# =========================
left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown('<div class="section-title">Grafik Kelembaban Tanah</div>', unsafe_allow_html=True)

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

        fig.add_hline(
            y=threshold,
            line_dash="dash",
            line_color="#b91c1c",
            annotation_text=f"Batas {threshold}%",
            annotation_position="top left"
        )

        fig.update_layout(
            height=390,
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False,
            xaxis=dict(
                title=dict(
                    text="Waktu",
                    font=dict(size=20, color="#06182d", family="Arial Black")
                ),
                tickfont=dict(size=16, color="#111827", family="Arial Black"),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(
                    text="Kelembaban (%)",
                    font=dict(size=20, color="#06182d", family="Arial Black")
                ),
                tickfont=dict(size=16, color="#111827", family="Arial Black"),
                range=[0, 60],
                dtick=10,
                ticksuffix="%",
                gridcolor="#d1d5db"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True
            }
        )

with right:
    with st.container(border=True):
        st.markdown('<div class="section-title">Riwayat Monitoring</div>', unsafe_allow_html=True)

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
        """

        for _, row in data.iterrows():
            table_html += f"""
                <tr>
                    <td>{row["Waktu"]}</td>
                    <td>{row["Kelembaban Teks"]}</td>
                    <td>{row["Status Tanah"]}</td>
                    <td>{row["Status Pompa"]}</td>
                </tr>
            """

        table_html += """
            </tbody>
        </table>
        """

        st.markdown(table_html, unsafe_allow_html=True)

# =========================
# CATATAN BAWAH
# =========================
st.markdown("""
<div class="footer-note">
    Dashboard ini menampilkan simulasi monitoring kelembaban tanah berbasis IoT, meliputi nilai kelembaban tanah, status tanah, status pompa, koneksi sistem, grafik, dan riwayat monitoring.
</div>
""", unsafe_allow_html=True)
