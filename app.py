import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Monitoring Kelembaban Tanah",
    page_icon="🌱",
    layout="wide"
)

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
        padding-left: 1.6rem;
        padding-right: 1.6rem;
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
        margin-left: -1.6rem;
        margin-right: -1.6rem;
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

    .info-bar {
        background-color: #f8fafc;
        border: 1.5px solid #c8c8c8;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 18px;
        color: #06182d;
        font-size: 17px;
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
    }

    .card-title {
        font-size: 25px;
        font-weight: 900;
        margin-bottom: 22px;
        color: #06182d;
        text-align: center;
    }

    .card-value {
        font-size: 62px;
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
        margin-top: 16px;
        margin-bottom: 14px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #c8c8c8;
        border-radius: 8px;
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

    .footer-note {
        margin-top: 18px;
        padding: 12px 14px;
        background-color: #f8fafc;
        border-left: 5px solid #06182d;
        font-size: 16px;
        font-weight: 700;
        color: #06182d;
    }

    @media screen and (max-width: 900px) {
        .main-header h1 {
            font-size: 22px;
        }

        .header-icon {
            font-size: 26px;
        }

        .card-title {
            font-size: 18px;
        }

        .card-value {
            font-size: 40px;
        }

        .section-title {
            font-size: 23px;
        }
    }
</style>
""", unsafe_allow_html=True)


def clean_column_name(col):
    return str(col).strip().lower().replace("_", " ").replace("-", " ")


def find_column(df, keywords):
    normalized = {col: clean_column_name(col) for col in df.columns}
    for col, clean in normalized.items():
        for key in keywords:
            if key in clean:
                return col
    return None


def load_default_data():
    return pd.DataFrame({
        "Waktu": ["08:00", "08:10", "08:20", "08:30", "08:40"],
        "Kelembaban": [25, 32, 38, 42, 45]
    })


def prepare_dataset(raw_df):
    df = raw_df.copy()

    time_col = find_column(df, ["time", "waktu", "timestamp", "date"])
    moisture_col = find_column(df, [
        "soil moisture",
        "soil_moisture",
        "moisture",
        "kelembaban",
        "humidity soil",
        "soil humidity"
    ])

    if moisture_col is None:
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if len(numeric_cols) > 0:
            moisture_col = numeric_cols[0]
        else:
            return load_default_data(), "Kolom kelembaban tidak ditemukan. Dashboard memakai data contoh."

    result = pd.DataFrame()
    result["Kelembaban"] = pd.to_numeric(df[moisture_col], errors="coerce")
    result = result.dropna(subset=["Kelembaban"])

    if result.empty:
        return load_default_data(), "Data kelembaban kosong atau tidak valid. Dashboard memakai data contoh."

    if result["Kelembaban"].max() <= 1:
        result["Kelembaban"] = result["Kelembaban"] * 100

    result["Kelembaban"] = result["Kelembaban"].clip(lower=0, upper=100).round(0).astype(int)

    if time_col is not None:
        waktu = pd.to_datetime(df.loc[result.index, time_col], errors="coerce")
        if waktu.notna().sum() > 0:
            result["Waktu"] = waktu.dt.strftime("%H:%M")
        else:
            result["Waktu"] = [f"Data {i+1}" for i in range(len(result))]
    else:
        result["Waktu"] = [f"Data {i+1}" for i in range(len(result))]

    result = result[["Waktu", "Kelembaban"]].tail(10).reset_index(drop=True)
    return result, f"Dataset berhasil dibaca. Kolom kelembaban yang digunakan: {moisture_col}"


if "threshold" not in st.session_state:
    st.session_state.threshold = 30

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")


with st.sidebar:
    st.markdown("## Pengaturan Dashboard")

    uploaded_file = st.file_uploader(
        "Upload dataset Kaggle",
        type=["csv", "xlsx"]
    )

    threshold = st.slider(
        "Batas Tanah Kering (%)",
        min_value=10,
        max_value=70,
        value=30,
        step=1
    )

    status_koneksi = st.radio(
        "Status Koneksi",
        ["Online", "Offline"],
        index=0
    )

    pompa_manual = st.toggle(
        "Paksa Pompa Aktif",
        value=False
    )

    jumlah_data = st.slider(
        "Jumlah Data Grafik",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )

    if st.button("Perbarui Dashboard"):
        st.session_state.threshold = threshold
        st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
        st.rerun()

    if st.button("Reset Tampilan"):
        st.session_state.threshold = 30
        st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
        st.rerun()


if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            raw_data = pd.read_csv(uploaded_file)
        else:
            raw_data = pd.read_excel(uploaded_file)

        data, dataset_note = prepare_dataset(raw_data)
    except Exception as e:
        data = load_default_data()
        dataset_note = f"Dataset gagal dibaca. Dashboard memakai data contoh. Error: {e}"
else:
    data = load_default_data()
    dataset_note = "Belum ada dataset Kaggle yang di-upload. Dashboard memakai data contoh."

data = data.tail(jumlah_data).reset_index(drop=True)

kelembaban_akhir = int(data["Kelembaban"].iloc[-1])
status_tanah = "Kering" if kelembaban_akhir < threshold else "Lembab"

if pompa_manual:
    status_pompa = "Aktif"
else:
    status_pompa = "Aktif" if kelembaban_akhir < threshold else "Mati"

data["Status Tanah"] = data["Kelembaban"].apply(lambda x: "Kering" if x < threshold else "Lembab")
data["Status Pompa"] = data["Kelembaban"].apply(lambda x: "Aktif" if x < threshold else "Mati")
data["Kelembaban (%)"] = data["Kelembaban"].astype(str) + "%"

table_data = data[["Waktu", "Kelembaban (%)", "Status Tanah", "Status Pompa"]].copy()

st.markdown("""
<div class="main-header">
    <div class="header-icon">☰</div>
    <h1>Dashboard Monitoring Kelembaban Tanah</h1>
    <div class="header-icon">⌁</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="info-bar">
    Sumber Data: Dataset Kaggle / Data Simulasi &nbsp;&nbsp; | &nbsp;&nbsp;
    Batas Tanah Kering: {threshold}% &nbsp;&nbsp; | &nbsp;&nbsp;
    Update Terakhir: {st.session_state.last_update}
</div>
""", unsafe_allow_html=True)

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
    koneksi_class = "online" if status_koneksi == "Online" else "offline"
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Koneksi Sistem</div>
        <div class="card-value {koneksi_class}">{status_koneksi}</div>
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns(2)

with left:
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
        textfont=dict(size=15, color="#111827", family="Arial Black")
    ))

    fig.add_hline(
        y=threshold,
        line_dash="dash",
        line_color="#b91c1c",
        annotation_text=f"Batas {threshold}%",
        annotation_position="top left"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        xaxis=dict(
            title=dict(text="Waktu", font=dict(size=20, color="#06182d", family="Arial Black")),
            tickfont=dict(size=16, color="#111827", family="Arial Black"),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text="Kelembaban (%)", font=dict(size=20, color="#06182d", family="Arial Black")),
            tickfont=dict(size=16, color="#111827", family="Arial Black"),
            range=[0, 100],
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
    st.markdown('<div class="section-title">Riwayat Monitoring</div>', unsafe_allow_html=True)

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        height=430
    )

st.markdown(f"""
<div class="footer-note">
    {dataset_note}
</div>
""", unsafe_allow_html=True)
