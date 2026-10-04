---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Clustering K-Means

Dokumen ini menyajikan tahapan analisis pengelompokan spasial (*spatial clustering*) dari dataset gabungan **3 polutan udara** (NO2, CO, SO2) yang telah diekstraksi menjadi fitur gabungan terpusat (multi-polutan). Pada tahapan ini seluruh polutan diproses dalam satu tabel sehingga menghasilkan 204 fitur (`68 fitur x 3 polutan`) untuk tiap daerah observasi.

Tujuan dari tahapan ini adalah untuk mengeksekusi pengelompokan area (*clustering*) guna menemukan daerah mana saja yang memiliki tren dan profil pencemaran campuran (*multi-pollutant*) yang identik. Eksperimen ini memadukan validasi di **Python (Scikit-Learn)** dan visualisasi alur di **KNIME Analytics Platform**.

## 1. Eksperimen Analisis Silhouette Menggunakan KNIME

Proses segmentasi klaster juga divalidasi dan divisualisasikan secara komprehensif menggunakan **KNIME Analytics Platform** dengan fokus pada perbandingan performa antar skenario reduksi dimensi secara paralel.

```{figure} ./img/clustering_knime/struktur.png
---
name: workflow-kmeans-knime
align: center
width: 90%
---
Visualisasi Struktur Alur Kerja (Workflow) Multi-Polutan pada KNIME
```
*(Catatan: Anda dapat memperbarui direktori gambar di atas dengan tangkapan layar spesifik dari struktur KNIME milik Anda).*

### 1.1 Penjelasan Alur Percabangan (*Pipeline*) KNIME

Berdasarkan *workflow* yang telah Anda susun, tahapan analisis dirancang tanpa blok *looping*, melainkan didistribusikan secara linier dan eksplisit:

1. **MySQL Connector $\rightarrow$ DB Table Selector $\rightarrow$ DB Reader:**
   Menarik seluruh data ekstraksi gabungan multi-polutan (**204 kolom fitur**) dari basis data langsung menuju memori KNIME agar bisa diolah secara lokal.

2. **Jalur Reduksi Dimensi (PCA):**
   Data dari *DB Reader* langsung disebar secara paralel ke 4 (empat) cabang utama:
   * **Jalur Tanpa PCA (Baseline)**: Murni menggunakan 204 fitur mentah asli tanpa dikompresi.
   * **Jalur PCA 203 Dimensi**: Mempertahankan seluruh struktur matriks tetapi membuang redundansi linear satu kolom terakhir.
   * **Jalur PCA 74 Dimensi**: Kompresi moderat (menghilangkan lebih dari setengah dimensi bervarians kecil).
   * **Jalur PCA 37 Dimensi**: Kompresi maksimal berdasarkan *Maximum Rank*.

3. **Node K-Means (Paralel) & Evaluasi Silhouette:**
   Setiap ujung jalur PCA dibagi paralel menuju **3 node k-Means**. Parameter K-Means pada masing-masing jalur disetel statis berturut-turut pada **$k=2$, $k=4$, dan $k=7$**. 
   Setiap *output k-Means* dievaluasi langsung menggunakan node **Silhouette Coefficient** (untuk melihat skor ketajaman batas klaster) dan node **Scatter Plot** (untuk memvisualisasikan data).

### 1.2 Interpretasi Hasil Clustering dan Kesimpulan

Dari eksperimen tersebut, terdapat dua penemuan krusial yang diamati dari skor evaluasi Silhouette Coefficient.

#### A. Fenomena Konsistensi Hasil pada Seluruh Skenario Dimensi (PCA)

Berdasarkan hasil eksperimen di KNIME, output pengelompokan (*clustering*) untuk nilai $K$ yang sama memberikan nilai metrik Silhouette yang **persis sama**, baik pada jalur data mentah (tanpa PCA), PCA 203, PCA 74, maupun PCA 37. Mengapa hal ini bisa terjadi?

* **Derajat Kebebasan Matematis (*Maximum Rank*)**: Jumlah daerah pengamatan (*rows*) yang dikelompokkan hanya berjumlah **37 area**. Secara perhitungan *linear algebra*, seberapapun banyaknya fitur yang kita miliki (204 kolom), matriks tersebut hanya bisa memiliki varians efektif maksimum sebesar 37 (*rank* = 37).
* **Zero Loss of Information**: Ketika KNIME mereduksi data dari 204 dimensi ke 37 dimensi, algoritma PCA berhasil **menyimpan 100% informasi struktural (*varians utama*)** tanpa terpotong sama sekali. Sisanya hanyalah "ruang kosong" atau redundansi. 
* Kesimpulannya, K-Means membaca proporsi jarak Euclidian yang sama persis di antara ke-37 titik data tersebut, baik di ruang 37 dimensi maupun 204 dimensi, sehingga susunan klaster dan skor *Silhouette*-nya tidak berubah sama sekali. Namun, komputasi pada PCA 37 jauh lebih ringan dan efisien.

#### B. Tabel Hasil Eksperimen Silhouette (Jalur Fitur Linier) 

Berikut merupakan ringkasan matriks nilai Silhouette Coefficient yang didapatkan dari ujung *pipeline* untuk setiap cabang pengujian:

| Jalur Node | Jumlah Klaster ($k$) | Silhouette **203 Dimensi** | Silhouette **74 Dimensi** | Silhouette **37 Dimensi** | Status Evaluasi |
| :---: | :---: | :---: | :---: | :---: | :--- |
| `Node 1` | **$k = 2$** | **`0.822`** | **`0.822`** | **`0.822`** | **Klaster Optimal (Tertinggi)** |
| `Node 2` | **$k = 4$** | `0.659` | `0.659` | `0.659` | Mulai terjadi pemecahan zona transisi |
| `Node 3` | **$k = 7$** | `0.582` | `0.582` | `0.582` | *Over-segmentation* ekstrem (klaster terlalu kecil) |

#### C. Tabel Hasil Eksperimen Silhouette (Jalur Fitur Polinomial)

Sama halnya dengan jalur linier, dataset yang diekstraksi secara polinomial juga dievaluasi. Transformasi polinomial ini biasanya menangkap interaksi non-linier antar polutan, sehingga memberikan skor yang sedikit berbeda secara matematis namun tetap konsisten secara *pattern*:

| Jalur Node | Jumlah Klaster ($k$) | Silhouette **203 Dimensi** | Silhouette **74 Dimensi** | Silhouette **37 Dimensi** | Status Evaluasi |
| :---: | :---: | :---: | :---: | :---: | :--- |
| `Node 1` | **$k = 2$** | **`0.634`** | **`0.634`** | **`0.634`** | **Klaster Optimal (Tertinggi)** |
| `Node 2` | **$k = 4$** | `0.466` | `0.466` | `0.466` | Mulai terjadi pemecahan zona transisi |
| `Node 3` | **$k = 7$** | `0.537` | `0.537` | `0.537` | *Over-segmentation* ekstrem (klaster terlalu kecil) |

#### D. Evaluasi Kualitas Klaster Terbaik ($k=2$, $k=4$, $k=7$)

Evaluasi *Silhouette Coefficient* mengukur seberapa padat suatu klaster dan seberapa jauh jaraknya dari klaster lain. Semakin mendekati angka **1.0**, semakin baik dan solid pemisahannya. 

Baik pada jalur data fitur **Linier** maupun **Polinomial**, keduanya secara absolut menempatkan $K=2$ sebagai konfigurasi paling solid. Berikut adalah interpretasi visualisasi dan analisis mendalam dari ketiga pengujian jumlah klaster di atas:

**1. Hasil untuk $K = 7$**
```{figure} ./img/clustering_knime/linear_k7.png
---
name: silhouette-linier-k7
align: center
width: 60%
---
Hasil Silhouette Coefficient Linier untuk k=7 (Skor Keseluruhan: 0.582)
```
```{figure} ./img/clustering_knime/polynomial_k7.png
---
name: silhouette-poli-k7
align: center
width: 60%
---
Hasil Silhouette Coefficient Polinomial untuk k=7 (Skor Keseluruhan: 0.537)
```
Pada pembagian 7 klaster, skor keseluruhan (*Overall*) anjlok ke angka **0.582** (Linier) dan **0.537** (Polinomial). Hal ini terjadi karena pemecahan wilayah terlalu banyak (*over-segmentation*). Daerah-daerah dengan sedikit perbedaan dipaksa pisah menjadi klaster terisolasi sehingga kepadatan klaster (*kohesi*) menjadi sangat lemah.

**2. Hasil untuk $K = 4$**
```{figure} ./img/clustering_knime/linear_k4.png
---
name: silhouette-linier-k4
align: center
width: 60%
---
Hasil Silhouette Coefficient Linier untuk k=4 (Skor Keseluruhan: 0.659)
```
```{figure} ./img/clustering_knime/polynomial_k4.png
---
name: silhouette-poli-k4
align: center
width: 60%
---
Hasil Silhouette Coefficient Polinomial untuk k=4 (Skor Keseluruhan: 0.466)
```
Pada $k=4$, pemisahan wilayah pada fitur Linier mulai membaik dengan skor **0.659**, namun fitur Polinomial justru mencatatkan penurunan tajam menjadi **0.466**. Meski mulai terbentuk segmen yang relevan, masih terdapat banyak irisan antar batas zona (klaster transisi) sehingga jarak separasinya belum ideal.

**3. Hasil untuk $K = 2$ (Klaster Terbaik)**
```{figure} ./img/clustering_knime/linear_k2.png
---
name: silhouette-linier-k2
align: center
width: 60%
---
Hasil Silhouette Coefficient Linier untuk k=2 (Skor Keseluruhan: 0.822)
```
```{figure} ./img/clustering_knime/polynomial_k2.png
---
name: silhouette-poli-k2
align: center
width: 60%
---
Hasil Silhouette Coefficient Polinomial untuk k=2 (Skor Keseluruhan: 0.634)
```
**Nilai $K=2$ terbukti sebagai konfigurasi *clustering* terbaik pada kedua skenario.** Dengan nilai agregat *Overall* mencapai **0.822** (Linier) dan **0.634** (Polinomial).
Secara geografis dan polusi, ini menandakan bahwa 37 daerah observasi secara alamiah terpolarisasi dengan sangat kuat dan tegas ke dalam dua kelompok besar saja: **Zona Tinggi Polutan** dan **Zona Rendah Polutan** (Background). Memecah mereka lebih dari dua kelompok hanya akan merusak batas solid tersebut. Fitur polinomial menangkap interaksi non-linier antar polutan, sehingga meskipun skornya lebih rendah, struktur klaster utamanya tetap bersepakat pada binerisasi (K=2).


## 2. Pemetaan Segmentasi Wilayah

Berikut adalah visualisasi spasial dari pembagian daerah menggunakan konfigurasi klaster terbaik (=2$). Peta interaktif ini diproyeksikan langsung dari koordinat 37 daerah observasi berdasarkan hasil pelabelan *k-Means* di KNIME.

### A. Peta Klaster (Fitur Linier)

```{code-cell} ipython3
:tags: [hide-input]

import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap
import warnings
warnings.filterwarnings('ignore')

# 1. BACA FILE CSV HASIL CLUSTERING (LINIER)
df_linier = pd.read_csv('./source/cluster_daerah/hasil_clustering_linear.csv')

# Standarisasi penamaan label klaster menjadi 'Cluster 0' dan 'Cluster 1'
if 'Cluster' in df_linier.columns:
    df_linier['Cluster_Label'] = df_linier['Cluster'].astype(str).apply(
        lambda x: f"Cluster {x.split('_')[-1]}" if "cluster_" in x.lower() else x
    )
else:
    df_linier['Cluster_Label'] = 'Cluster 0' # fallback

# 2. KAMUS KOORDINAT KECAMATAN/DAERAH
kamus_koordinat = {
    "baron": (-7.6033, 112.0601),          
    "sreseh": (-7.1983, 113.0805),         
    "banyu ajuh": (-7.1585, 112.7280),     
    "banyuajuh": (-7.1620, 112.7310),      
    "kamal": (-7.1662, 112.7214),          
    "labang": (-7.1294, 112.7936),         
    "kwanyar": (-7.1604, 112.8569),        
    "kecamatan bangkalan": (-7.0325, 112.7450), 
    "bangkalan": (-7.0455, 112.7351),      
    "gresik": (-7.1566, 112.6555),         
    "paciran": (-6.8767, 112.3414),        
    "jabon": (-7.5419, 112.7686),          
    "widang": (-6.9850, 112.1647),         
    "kalianget": (-7.0519, 113.9408),      
    "kota sumenep": (-7.0086, 113.8617),   
    "sumenep": (-7.0167, 113.8542),        
    "tikala": (1.4820, 124.8540),          
    "wonokromo": (-7.3006, 112.7383),      
    "surabaya": (-7.2575, 112.7521),       
    "pilangkenceng": (-7.4931, 111.6664),  
    "madiun": (-7.6298, 111.5239),         
    "sidoarjo": (-7.4478, 112.7183),       
    "tuban": (-6.8976, 112.0463),          
    "lamongan": (-7.1193, 112.4167),       
    "sampang": (-7.1872, 113.2394),        
    "pamekasan": (-7.1568, 113.4746),      
    "malang": (-7.9666, 112.6326),         
    "denpasar": (-8.6705, 115.2126),       
    "jakarta": (-6.2088, 106.8456),        
}

def cari_koordinat(nama_daerah, idx):
    nama_lower = str(nama_daerah).lower()
    for kata_kunci, (lat, lon) in kamus_koordinat.items():
        if kata_kunci in nama_lower:
            np.random.seed(idx * 42)
            offset_lat = np.random.uniform(-0.015, 0.015)
            offset_lon = np.random.uniform(-0.015, 0.015)
            return lat + offset_lat, lon + offset_lon
    return -7.2500 + (idx * 0.02), 112.7500 + (idx * 0.02)

if "latitude" not in df_linier.columns or "longitude" not in df_linier.columns:
    coords = [cari_koordinat(row["daerah"], i) for i, row in df_linier.iterrows()]
    df_linier["latitude"] = [c[0] for c in coords]
    df_linier["longitude"] = [c[1] for c in coords]

# 3. FUNGSI RENDER PETA FOLIUM
def render_peta_knime(df_data, nama_dataset="PCA-37", k_val=2, sil_score=0.822):
    m = folium.Map(location=[-7.2, 113.0], zoom_start=8, tiles=None, control_scale=True)
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap (default)").add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Esri Street Map"
    ).add_to(m)
    
    palet_warna = {"Cluster 0": "#e53935", "Cluster 1": "#1e88e5"}
    unique_clusters = sorted(df_data["Cluster_Label"].unique())
    fg_dict = {}
    
    for c_name in unique_clusters:
        fg = folium.FeatureGroup(name=c_name, show=True)
        fg.add_to(m)
        fg_dict[c_name] = fg

    df_sorted = df_data.sort_values(by="Cluster_Label", ascending=True)

    for idx, row in df_sorted.iterrows():
        c_name = row["Cluster_Label"]
        c_num = c_name.split()[-1]
        short_code = f"C{c_num}"
        color = palet_warna.get(c_name, "#e53935")
        z_idx = 1000 if c_name == "Cluster 1" else 100

        icon_html = f"""
        <div style="background-color: {color}; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-family: Arial, sans-serif; font-size: 10px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.45);">{short_code}</div>
        """

        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px; min-width: 160px;">
            <b>{row['daerah']}</b><hr style="margin: 4px 0;">
            <b>Klaster:</b> {c_name} ({short_code})<br>
            <b>Koordinat:</b> {row['latitude']:.4f}, {row['longitude']:.4f}
        </div>
        """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            icon=folium.DivIcon(html=icon_html, icon_size=(30, 30), icon_anchor=(15, 15)),
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['daerah']} ({short_code})",
            z_index_offset=z_idx
        ).add_to(fg_dict[c_name])

    MiniMap(toggle_display=True, position="bottomright").add_to(m)
    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    counts = df_data["Cluster_Label"].value_counts()
    item_legenda_html = ""
    for c_name in unique_clusters:
        jml = counts.get(c_name, 0)
        color = palet_warna.get(c_name, "#e53935")
        item_legenda_html += f"""
        <div style="display: flex; align-items: center; margin-bottom: 6px; font-size: 13px; color: #333;">
            <span style="display:inline-block; width: 14px; height: 14px; border-radius: 50%; background-color: {color}; margin-right: 10px;"></span>
            <span>{c_name} &mdash; {jml} wilayah</span>
        </div>
        """

    legend_card_html = f"""
    <div style="position: fixed; bottom: 45px; left: 20px; z-index: 9999; background-color: white; padding: 16px 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.18); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; min-width: 240px;">
        <div style="font-size: 15px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px;">Segmentasi Cluster</div>
        <div style="font-size: 12px; color: #777; margin-bottom: 12px;">Dataset: {nama_dataset} | k={k_val} | Sil={sil_score:.3f}</div>
        {item_legenda_html}
        <div style="font-size: 11px; color: #999; margin-top: 10px;">Klik marker untuk detail</div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_card_html))
    return m

# Tampilkan Peta Linier
peta_linier = render_peta_knime(df_linier, nama_dataset="Linier (PCA-37)", k_val=2, sil_score=0.822)
peta_linier
```

### B. Peta Klaster (Fitur Polinomial)

```{code-cell} ipython3
:tags: [hide-input]

# 1. BACA FILE CSV HASIL CLUSTERING (POLINOMIAL)
df_poli = pd.read_csv('./source/cluster_daerah/hasil_clustering_polynomial.csv')

if 'Cluster' in df_poli.columns:
    df_poli['Cluster_Label'] = df_poli['Cluster'].astype(str).apply(
        lambda x: f"Cluster {x.split('_')[-1]}" if "cluster_" in x.lower() else x
    )
else:
    df_poli['Cluster_Label'] = 'Cluster 0'

if "latitude" not in df_poli.columns or "longitude" not in df_poli.columns:
    coords = [cari_koordinat(row["daerah"], i) for i, row in df_poli.iterrows()]
    df_poli["latitude"] = [c[0] for c in coords]
    df_poli["longitude"] = [c[1] for c in coords]

# Tampilkan Peta Polinomial
peta_poli = render_peta_knime(df_poli, nama_dataset="Polinomial (PCA-37)", k_val=2, sil_score=0.634)
peta_poli
```

