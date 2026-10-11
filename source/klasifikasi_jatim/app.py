"""
app.py - Aplikasi Streamlit Klasifikasi Tutupan Lahan Jawa Timur (XGBoost)

Jalankan lokal:
    streamlit run app.py

File yang dibutuhkan di folder data/:
    model_xgb.joblib, dataset_ekstraksi_tif_lengkap.csv, centroid_poligon.csv,
    hasil_rgba.png, meta.json, statistik_kelas.csv
"""

import json
from pathlib import Path

import folium
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from folium.raster_layers import ImageOverlay
from PIL import Image
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from streamlit_folium import st_folium

import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# KONFIGURASI
# ------------------------------------------------------------------
BASE = Path(__file__).resolve().parent
DATA = BASE / "data" if (BASE / "data").is_dir() else BASE

st.set_page_config(page_title="Klasifikasi LULC Jawa Timur", layout="wide")

# CSS kustom untuk tampilan dashboard yang bersih, elegan, dan estetik
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Judul Utama */
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.15rem;
        color: #0f172a;
    }
    .sub-caption {
        font-size: 0.92rem;
        color: #64748b;
        margin-bottom: 1.25rem;
    }

    /* Kartu Metrik Estetik */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .metric-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
    }
    .metric-title {
        font-size: 1.02rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.35rem;
    }
    .metric-desc {
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.5;
    }

    /* Kartu Kelas LULC */
    .class-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.9rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .class-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }

    /* Badge Bagian */
    .section-badge {
        display: inline-block;
        padding: 2px 9px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        background: #f1f5f9;
        color: #475569;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
        font-size: 0.9rem;
        padding: 8px 16px;
        border-radius: 6px;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        font-weight: 600;
        color: #0f172a !important;
        background-color: #f8fafc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

WARNA_KELAS = {
    "Sawah": "#FFD92F",
    "Bangunan": "#E41A1C",
    "Mangrove": "#8E44AD",
    "Hutan": "#2E7D32",
    "Laut": "#0D47A1",
    "Danau": "#4FC3F7",
}
NAMA_KELAS = ["Sawah", "Bangunan", "Danau", "Hutan", "Mangrove", "Laut"]  # urutan label 0-5
FITUR = ["B02", "B03", "B04", "B08", "B11", "NDVI", "NDWI", "NDBI"]


# ------------------------------------------------------------------
# FUNGSI PEMUAT DATA (di-cache supaya tidak dibaca ulang tiap interaksi)
# ------------------------------------------------------------------
@st.cache_resource
def muat_model():
    return joblib.load(DATA / "model_xgb.joblib")


@st.cache_data
def muat_hasil_peta():
    img = np.array(Image.open(DATA / "hasil_rgba.png").convert("RGBA"))
    with open(DATA / "meta.json") as f:
        meta = json.load(f)
    return img, meta


@st.cache_data
def muat_statistik():
    return pd.read_csv(DATA / "statistik_kelas.csv")


@st.cache_data
def muat_centroid():
    return pd.read_csv(DATA / "centroid_poligon.csv")


@st.cache_data
def evaluasi_model():
    """Evaluasi pada data uji (split yang sama seperti di notebook)."""
    paket = muat_model()
    model = paket["model"]

    df = pd.read_csv(DATA / "dataset_ekstraksi_tif_lengkap.csv")
    X, y = df[FITUR], df["label"]
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    y_pred = model.predict(X_test)
    laporan = classification_report(
        y_test, y_pred, target_names=NAMA_KELAS, output_dict=True, zero_division=0
    )
    cm = confusion_matrix(y_test, y_pred)
    return accuracy_score(y_test, y_pred), pd.DataFrame(laporan).T, cm, len(X_test)


# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="section-badge">METADATA</div>', unsafe_allow_html=True)
    st.subheader("Informasi Proyek")
    st.markdown("""
    **Dataset:** Sentinel-2A Level-2A  
    **Wilayah:** Provinsi Jawa Timur  
    **Model:** XGBoost Classifier  
    **Kerangka Kerja:** CRISP-DM  
    **Jumlah Kelas:** 6 Tutupan Lahan  
    """)
    st.divider()
    st.markdown('<div class="section-badge">FITUR PREDIKTOR</div>', unsafe_allow_html=True)
    st.markdown("""
    - **Pita Spektral:** B02, B03, B04, B08, B11
    - **NDVI:** Indeks Kerapatan Vegetasi
    - **NDWI:** Indeks Badan Air
    - **NDBI:** Indeks Kawasan Terbangun
    """)

# ------------------------------------------------------------------
# HALAMAN UTAMA
# ------------------------------------------------------------------
st.markdown('<div class="main-title">Klasifikasi Tutupan Lahan Jawa Timur</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-caption">Sentinel-2A + XGBoost | 6 Kelas: Sawah, Bangunan, Danau, Hutan, Mangrove, Laut</div>', unsafe_allow_html=True)

tab_bu, tab_peta, tab_stat, tab_eval, tab_manual = st.tabs(
    [
        "Business Understanding",
        "Peta Interaktif",
        "Statistik Luas",
        "Evaluasi Model",
        "Prediksi Manual",
    ]
)

# ---------------- TAB 0: BUSINESS UNDERSTANDING ----------------
with tab_bu:
    st.markdown('<div class="section-badge">CRISP-DM TAHAP 1</div>', unsafe_allow_html=True)
    st.subheader("Pemahaman Bisnis dan Konteks Masalah")
    st.markdown(
        "Pendekatan pemantauan tutupan lahan skala regional berbasis citra satelit multispektral "
        "dan machine learning mengadopsi metodologi standar industri **CRISP-DM** "
        "(*Cross-Industry Standard Process for Data Mining*)."
    )

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            """
            <div class="metric-card" style="border-top: 3px solid #eab308;">
                <div class="metric-tag" style="color: #ca8a04;">Sektor Pertanian</div>
                <div class="metric-title">Lumbung Pangan Nasional</div>
                <div class="metric-desc">
                    Memantau dan mengawal perlindungan Lahan Pertanian Pangan Berkelanjutan (LP2B) 
                    dari tekanan konversi sawah produktif menuju kawasan permukiman dan industri.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            """
            <div class="metric-card" style="border-top: 3px solid #ef4444;">
                <div class="metric-tag" style="color: #dc2626;">Sektor Tata Ruang</div>
                <div class="metric-title">Dinamika Urbanisasi</div>
                <div class="metric-desc">
                    Menyajikan pemetaan spasial terukur terkait laju ekspansi kawasan terbangun, 
                    jaringan infrastruktur, dan pusat pertumbuhan ekonomi baru di Jawa Timur.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            """
            <div class="metric-card" style="border-top: 3px solid #16a34a;">
                <div class="metric-tag" style="color: #15803d;">Sektor Lingkungan</div>
                <div class="metric-title">Konservasi Ekologis</div>
                <div class="metric-desc">
                    Mendukung pemantauan ekosistem kritis seperti kawasan hutan lindung dataran tinggi 
                    dan sabuk hijau mangrove pesisir guna mitigasi abrasi serta degradasi lingkungan.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. Latar Belakang dan Urgensi Masalah")
        st.markdown(
            """
            Provinsi Jawa Timur memiliki luas daratan ±47.800 km² dengan bentang alam yang sangat heterogen. 
            Pemantauan lahan berkala dengan survei lapangan konvensional menghadapi kendala nyata:
            - **Biaya dan Logistik Tinggi:** Memerlukan alokasi anggaran dan personel besar untuk menjangkau 38 kabupaten/kota.
            - **Keterlambatan Pembaruan (*Time-Lag*):** Pemetaan manual membutuhkan waktu berbulan-bulan hingga tahunan.
            - **Aksesibilitas Geografis:** Area curam lereng pegunungan dan hutan rawa pesisir sulit dijangkau secara terestrial.

            Integrasi penginderaan jauh satelit **Sentinel-2A** (resolusi 10–20 meter) dipadukan dengan 
            model **XGBoost** menghadirkan solusi pemantauan objektif, berkala, cepat, dan beresolusi tinggi.
            """
        )

        st.markdown("#### 2. Rumusan Masalah")
        st.markdown(
            """
            1. **Klasifikasi Multi-Kelas Spasial:** Bagaimana mendiskriminasi 6 kelas tutupan lahan (*Sawah, Bangunan, Danau, Hutan, Mangrove, Laut*) dari data reflektansi satelit?
            2. **Tumpang-Tindih Spektral (*Spectral Confusion*):** Bagaimana membedakan objek dengan profil spektrum mirip, seperti sesama kanopi hijau (*Hutan vs Mangrove*) atau badan air (*Danau vs Laut*)?
            3. **Efisiensi Komputasi Regional:** Bagaimana mengklasifikasikan jutaan piksel citra Sentinel-2A secara cepat dan akurat tanpa hambatan memori?
            """
        )

    with col2:
        st.markdown("#### 3. Tujuan Analisis")
        st.markdown(
            """
            - **Tujuan Kebijakan dan Perencanaan Wilayah:**
              - Menyediakan basis data faktual untuk Rencana Tata Ruang Wilayah (RTRW) Jawa Timur.
              - Mengawal perlindungan Lahan Pertanian Pangan Berkelanjutan (LP2B).
              - Memfasilitasi mitigasi abrasi dan konservasi ekosistem mangrove pesisir.
            - **Tujuan Teknis Data Science:**
              - Mengekstraksi 5 pita spektral Sentinel-2A (`B02, B03, B04, B08, B11`) dan 3 indeks biofisik (`NDVI, NDWI, NDBI`).
              - Melatih model XGBoost dengan hyperparameter optimal dan regularisasi ketat.
              - Melakukan inferensi *per-pixel* skala regional menggunakan teknik *spatial masking*.
              - Menyajikan hasil dalam dashboard interaktif Web GIS.
            """
        )

        st.markdown("#### 4. Kriteria Keberhasilan (*Success Criteria*)")
        kriteria_df = pd.DataFrame(
            {
                "Parameter": [
                    "Akurasi Keseluruhan (Overall Accuracy)",
                    "Macro F1-Score & Recall",
                    "Waktu Inferensi Skala Regional",
                    "Aksesibilitas Produk",
                ],
                "Target Kriteria": [
                    "≥ 90% pada subset data pengujian",
                    "≥ 0.85 (terutama kelas Mangrove & Danau)",
                    "Skala detik/menit dengan multi-threading",
                    "Peta web interaktif yang mandiri & responsif",
                ],
            }
        )
        st.dataframe(kriteria_df, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 5. Karakteristik 6 Kelas Tutupan Lahan (LULC)")
    cols_kelas = st.columns(6)
    deskripsi_kelas = {
        "Sawah": "Lahan pertanian padi aktif (fase genangan air dan vegetatif).",
        "Bangunan": "Permukiman, infrastruktur jalan, dan zona terbangun/industri.",
        "Danau": "Badan air tawar pedalaman (waduk, danau, telaga).",
        "Hutan": "Tutupan vegetasi pohon rapat di kawasan daratan/pegunungan.",
        "Mangrove": "Hutan bakau dan vegetasi pesisir payau pasang surut.",
        "Laut": "Perairan asin terbuka di pesisir dan laut lepas Jawa Timur.",
    }
    for col, nama in zip(cols_kelas, NAMA_KELAS):
        warna = WARNA_KELAS[nama]
        with col:
            st.markdown(
                f"""
                <div class="class-card" style="border-top: 3px solid {warna};">
                    <div style="font-weight: 600; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">
                        <span class="class-dot" style="background-color: {warna};"></span>{nama}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b; line-height: 1.45;">
                        {deskripsi_kelas[nama]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------- TAB 1: PETA ----------------
with tab_peta:
    img, meta = muat_hasil_peta()
    opasitas = st.slider("Opasitas lapisan klasifikasi", 0.0, 1.0, 0.65, 0.05)
    tampil_titik = st.checkbox("Tampilkan titik sampel ground truth", value=False)

    pusat = [(meta["lat_s"] + meta["lat_n"]) / 2, (meta["lon_w"] + meta["lon_e"]) / 2]
    peta = folium.Map(location=pusat, zoom_start=8, tiles=None, control_scale=True)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri",
        name="Esri Satellite",
        max_zoom=19,
        overlay=False,
    ).add_to(peta)
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap", overlay=False, show=False).add_to(peta)

    ImageOverlay(
        image=img,
        bounds=[[meta["lat_s"], meta["lon_w"]], [meta["lat_n"], meta["lon_e"]]],
        opacity=opasitas,
        name="Hasil Klasifikasi XGBoost",
        zindex=5,
    ).add_to(peta)

    if tampil_titik:
        cen = muat_centroid()
        for nama, warna in WARNA_KELAS.items():
            grup = folium.FeatureGroup(name=f"Titik Sampel: {nama}")
            for _, r in cen[cen["label_teks"].str.title() == nama].iterrows():
                folium.CircleMarker(
                    [r["lat_centroid"], r["lon_centroid"]],
                    radius=4, color="white", weight=1,
                    fill=True, fill_color=warna, fill_opacity=1,
                    popup=nama,
                ).add_to(grup)
            grup.add_to(peta)

    # Legenda
    item = "".join(
        f'<div style="margin:2px 0"><span style="display:inline-block;width:14px;height:14px;'
        f'background:{w};border:1px solid #333;margin-right:6px;vertical-align:middle"></span>{k}</div>'
        for k, w in WARNA_KELAS.items()
    )
    legenda = (
        '<div style="position:fixed;bottom:30px;left:30px;z-index:9999;'
        'background:rgba(255,255,255,0.95);padding:10px 14px;border:1px solid #888;'
        f'border-radius:6px;font:12px sans-serif;color:#000"><b>Legenda LULC</b><hr style="margin:5px 0">{item}</div>'
    )
    peta.get_root().html.add_child(folium.Element(legenda))
    folium.LayerControl(collapsed=False).add_to(peta)

    st_folium(peta, height=600, use_container_width=True, returned_objects=[])

# ---------------- TAB 2: STATISTIK ----------------
with tab_stat:
    stat = muat_statistik()
    st.subheader("Luas dan proporsi tiap kelas")

    kol1, kol2 = st.columns([1, 1])
    with kol1:
        tampil = stat.rename(columns={"Luas_km2": "Luas (km²)", "Persen": "Persen (%)"})
        st.dataframe(tampil, use_container_width=True, hide_index=True)
        st.download_button(
            "Unduh CSV",
            stat.to_csv(index=False).encode("utf-8"),
            file_name="statistik_kelas.csv",
            mime="text/csv",
        )
    with kol2:
        fig, ax = plt.subplots(figsize=(6, 4))
        warna = [WARNA_KELAS[k] for k in stat["Kelas"]]
        ax.bar(stat["Kelas"], stat["Luas_km2"], color=warna, edgecolor="#333")
        ax.set_ylabel("Luas (km²)")
        ax.set_title("Luas per kelas")
        plt.xticks(rotation=30)
        st.pyplot(fig)

# ---------------- TAB 3: EVALUASI ----------------
with tab_eval:
    st.subheader("Evaluasi XGBoost pada data uji")
    akurasi, laporan, cm, n_uji = evaluasi_model()

    c1, c2 = st.columns(2)
    c1.metric("Overall Accuracy", f"{akurasi * 100:.2f}%")
    c2.metric("Jumlah data uji", n_uji)

    st.markdown("**Classification Report**")
    st.dataframe(laporan.round(3), use_container_width=True)

    st.markdown("**Confusion Matrix**")
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(6))
    ax.set_yticks(range(6))
    ax.set_xticklabels(NAMA_KELAS, rotation=45, ha="right")
    ax.set_yticklabels(NAMA_KELAS)
    ax.set_xlabel("Kelas Prediksi")
    ax.set_ylabel("Kelas Aktual")
    for i in range(6):
        for j in range(6):
            ax.text(
                j, i, cm[i, j], ha="center", va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black",
            )
    fig.colorbar(im)
    st.pyplot(fig)

# ---------------- TAB 4: PREDIKSI MANUAL ----------------
with tab_manual:
    st.subheader("Prediksi kelas dari nilai band")
    st.write("Masukkan nilai reflektansi band Sentinel-2 (sesuai skala yang dipakai saat training).")

    paket = muat_model()
    model, encoder = paket["model"], paket["encoder"]

    k1, k2, k3, k4, k5 = st.columns(5)
    b02 = k1.number_input("B02 (Blue)", value=0.05, format="%.4f")
    b03 = k2.number_input("B03 (Green)", value=0.08, format="%.4f")
    b04 = k3.number_input("B04 (Red)", value=0.06, format="%.4f")
    b08 = k4.number_input("B08 (NIR)", value=0.35, format="%.4f")
    b11 = k5.number_input("B11 (SWIR)", value=0.20, format="%.4f")

    if st.button("Prediksi"):
        def indeks(a, b):
            return (a - b) / (a + b) if (a + b) != 0 else 0.0

        ndvi = indeks(b08, b04)
        ndwi = indeks(b03, b08)
        ndbi = indeks(b11, b08)

        x = pd.DataFrame([[b02, b03, b04, b08, b11, ndvi, ndwi, ndbi]], columns=FITUR)
        pred = model.predict(x)
        kelas = str(encoder.inverse_transform(pred)[0]).title()

        st.success(f"Prediksi kelas: **{kelas}**")
        st.write(f"NDVI = {ndvi:.3f} | NDWI = {ndwi:.3f} | NDBI = {ndbi:.3f}")

        proba = model.predict_proba(x)[0]
        nama = [str(n).title() for n in encoder.inverse_transform(np.arange(len(proba)))]
        st.bar_chart(pd.Series(proba, index=nama, name="Probabilitas"))
