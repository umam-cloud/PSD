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

# Klasifikasi Spasial Tutupan Lahan Jawa Timur (6 Kelas)

Bagian ini mendokumentasikan tahapan akuisisi citra satelit optik **Sentinel-2A (Level-2A)** melalui **openEO** menggunakan agregasi spasial (*Spatial Aggregation*) langsung di server cloud, ekstraksi indeks spektral, hingga pemodelan klasifikasi *Multiclass* (6 kelas tutupan lahan) menggunakan algoritma **Random Forest**.

## Instalasi Library Yang Digunakan

```bash
pip install geopandas openeo pandas scikit-learn matplotlib seaborn
```

## 1. Desain Pengamatan (Ground Truth) 6 Kelas

Pengambilan sampel dilakukan secara spasial menggunakan data vektor (`Shapefile` / `GeoJSON` zip) yang mencakup wilayah Jawa Timur. Terdapat 6 kelas tutupan lahan yang diklasifikasikan:

| Kelas Target | Kode Label | Karakteristik Objek |
| :--- | :---: | :--- |
| **Sawah** | `0` | Petak lahan pertanian padi aktif. |
| **Bangunan** | `1` | Permukiman, infrastruktur jalan, dan kawasan terbangun perkotaan. |
| **Danau** | `2` | Badan air darat tawar, seperti danau atau waduk. |
| **Hutan** | `3` | Area dengan tutupan pohon rapat di daratan (hutan primer/sekunder). |
| **Mangrove** | `4` | Hutan bakau/vegetasi pesisir pantai. |
| **Laut** | `5` | Perairan laut lepas atau wilayah perairan pesisir. |

```{code-cell} ipython3
import geopandas as gpd
import openeo
import pandas as pd
import json

# ==============================================================================
# 1. BACA FILE ZIP DAN BERI LABEL OTOMATIS
# ==============================================================================
gdf_sawah = gpd.read_file("sawah.zip").to_crs("EPSG:4326")
gdf_bangunan = gpd.read_file("bangunan.zip").to_crs("EPSG:4326")
gdf_danau = gpd.read_file("danau.zip").to_crs("EPSG:4326")
gdf_hutan = gpd.read_file("hutan.zip").to_crs("EPSG:4326")
gdf_mangrove = gpd.read_file("mangrove.zip").to_crs("EPSG:4326")
gdf_laut = gpd.read_file("laut.zip").to_crs("EPSG:4326")

gdf_sawah["label_teks"], gdf_sawah["label"] = "Sawah", 0
gdf_bangunan["label_teks"], gdf_bangunan["label"] = "Bangunan", 1
gdf_danau["label_teks"], gdf_danau["label"] = "Danau", 2
gdf_hutan["label_teks"], gdf_hutan["label"] = "Hutan", 3
gdf_mangrove["label_teks"], gdf_mangrove["label"] = "Mangrove", 4
gdf_laut["label_teks"], gdf_laut["label"] = "Laut", 5

# Gabungkan menjadi 1 GeoDataFrame
gdf_gabungan = gpd.GeoDataFrame(
    pd.concat([gdf_sawah, gdf_bangunan, gdf_danau, gdf_hutan, gdf_mangrove, gdf_laut], ignore_index=True),
    crs="EPSG:4326"
)

# Buang geometri kosong
gdf_gabungan = gdf_gabungan.dropna(subset=["geometry"]).reset_index(drop=True)
geojson_gabungan = json.loads(gdf_gabungan.to_json())

print(f"Total sampel gabungan 6 kelas: {len(gdf_gabungan)}")
```

## 2. Akuisisi & Ekstraksi Nilai Piksel Cloud via openEO

Berbeda dengan akuisisi lokasi sempit yang seringkali mengunduh citra utuh `.tif` berukuran besar, pada pemetaan skala regional (Provinsi Jawa Timur), kita dapat memanfaatkan metode **Spatial Aggregation**. 

Melalui fungsi `aggregate_spatial`, ekstraksi nilai pantulan (*reflectance*) Sentinel-2A dihitung langsung oleh *server cloud* (Data Space Copernicus). Model mengekstrak nilai spektral 5 band (*Blue, Green, Red, NIR, SWIR*) di titik-titik lokasi (poligon) tanpa perlu mengunduh file mentahnya, menghemat ratusan Gigabyte memori.

```{code-cell} ipython3
# ==============================================================================
# 2. AMBIL BATAS KOORDINAT GABUNGAN (BOUNDING BOX)
# ==============================================================================
minx, miny, maxx, maxy = gdf_gabungan.total_bounds
bbox = {
    "west": float(minx), "south": float(miny),
    "east": float(maxx), "north": float(maxy),
}

# ==============================================================================
# 3. KONEKSI KE OPENEO & PROSES SPATIAL AGGREGATION
# ==============================================================================
conn = openeo.connect("openeo.dataspace.copernicus.eu")
conn.authenticate_oidc()

datacube = conn.load_collection(
    "SENTINEL2_L2A",
    spatial_extent=bbox,
    temporal_extent=["2026-06-01", "2026-09-30"],
    bands=["B02", "B03", "B04", "B08", "B11"],
    max_cloud_cover=10,
)

# Mengambil median agregasi temporal bebas awan
composite_s2 = datacube.median_time()

print("Meminta ekstraksi nilai piksel dari server OpenEO...")
aggregated_data = composite_s2.aggregate_spatial(geometries=geojson_gabungan, reducer="mean")

# Data akan turun dalam format JSON yang jauh lebih ringan
hasil_json = "hasil_ekstraksi_jatim.json"
aggregated_data.download(hasil_json, format="JSON")
print("Ekstraksi spasial selesai!")
```

## 3. Fitur Spektral dan Ekstraksi Indeks Turunan

Selain menggunakan ke-5 Pita Utama (`B02, B03, B04, B08, B11`), proses diskriminasi *Multiclass* (6 Kelas) sangat memerlukan penekanan terhadap jenis objek tertentu dengan kalkulasi Indeks Spektral:

1. **NDVI (Normalized Difference Vegetation Index):** `(B08 - B04) / (B08 + B04)` 
   Sangat ideal dalam membedakan kerapatan *Vegetasi* seperti Sawah, Hutan, dan Mangrove dibandingkan non-vegetasi.
2. **NDWI (Normalized Difference Water Index):** `(B03 - B08) / (B03 + B08)` 
   Berguna mendeteksi pantulan air (*Badan Air*), sehingga mudah membedakan Danau dan Laut dengan daratan.
3. **NDBI (Normalized Difference Built-up Index):** `(B11 - B08) / (B11 + B08)` 
   Sangat peka terhadap pantulan dari bangunan dan lahan terbuka. Kunci bagi model mengenali Bangunan secara spesifik.

```{code-cell} ipython3
import numpy as np

# Buka hasil agregasi spasial dari OpenEO
with open(hasil_json, 'r') as f:
    data_openeo = json.load(f)

extracted_rows = []
for item in data_openeo:
    try:
        # Menangani dimensi JSON nested
        if isinstance(item, list) and len(item) > 0 and isinstance(item[0], list):
            vals = item[0]
        else:
            vals = item
        extracted_rows.append({
            "B02": vals[0], "B03": vals[1], "B04": vals[2], 
            "B08": vals[3], "B11": vals[4]
        })
    except Exception:
        # Apabila ada data kosong
        extracted_rows.append({
            "B02": np.nan, "B03": np.nan, "B04": np.nan, 
            "B08": np.nan, "B11": np.nan
        })

df_features = pd.DataFrame(extracted_rows)
# Menggabungkan fitur ekstraksi satelit dengan label ground truth
df_final = pd.concat([df_features, gdf_gabungan[['label_teks', 'label']]], axis=1).dropna().reset_index(drop=True)

# Ekstraksi Indeks Spektral (Epsilon digunakan untuk menghindari pembagian 0)
eps = 1e-8
df_final['NDVI'] = (df_final['B08'] - df_final['B04']) / (df_final['B08'] + df_final['B04'] + eps)
df_final['NDWI'] = (df_final['B03'] - df_final['B08']) / (df_final['B03'] + df_final['B08'] + eps)
df_final['NDBI'] = (df_final['B11'] - df_final['B08']) / (df_final['B11'] + df_final['B08'] + eps)

# Bersihkan nilai Infinity akibat operasi pembagian
df_final = df_final.replace([np.inf, -np.inf], np.nan).dropna()
df_final.to_csv("dataset_sentinel2_jatim.csv", index=False)

display(df_final.head())
```

## 4. Hasil Evaluasi Klasifikasi *Multiclass* (Random Forest)

Dataset dievaluasi menggunakan *Stratified Train-Test Split* (80% Data Pelatihan, 20% Data Pengujian). 
Algoritma *Random Forest* digunakan karena sifat ensemble-nya (*Decision Trees* paralel) dapat membuat batas keputusan non-linear yang handal di tengah data satelit berskala besar yang terkadang memiliki *overlapping signatures* (misalnya: warna Mangrove yang mirip dengan Hutan hijau).

```{code-cell} ipython3
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix

fitur_kolom = ['B02', 'B03', 'B04', 'B08', 'B11', 'NDVI', 'NDWI', 'NDBI']
X = df_final[fitur_kolom]
y = df_final['label']
nama_kelas = ['Sawah', 'Bangunan', 'Danau', 'Hutan', 'Mangrove', 'Laut']

# Pemisahan dataset secara merata proporsional
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Data Pelatihan: {len(X_train)} Sampel")
print(f"Data Pengujian: {len(X_test)} Sampel")

# Pelatihan Model Random Forest (100 Pohon)
model_rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model_rf.fit(X_train, y_train)

# Melakukan Prediksi
y_pred = model_rf.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=nama_kelas))
```

### Visualisasi Model: Confusion Matrix & Kontribusi Fitur
Grafik *Confusion Matrix* di bawah menunjukkan sejauh mana model rentan terhadap misklasifikasi pada kelas tertentu. Sedangkan *Feature Importance* menjabarkan Pita Satelit / Indeks mana yang paling berpengaruh krusial saat pohon keputusan memilih label suatu lahan.

```{code-cell} ipython3
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# 1. Confusion Matrix Plot
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=nama_kelas, yticklabels=nama_kelas)
axes[0].set_title('Confusion Matrix - Klasifikasi 6 Kelas', fontweight="bold")
axes[0].set_xlabel('Prediksi (Predicted)')
axes[0].set_ylabel('Aktual (Actual)')

# 2. Plot Tingkat Kepentingan Fitur
importances = model_rf.feature_importances_
indices = np.argsort(importances)
axes[1].barh(range(len(indices)), importances[indices], color='#3498db', edgecolor='black')
axes[1].set_yticks(range(len(indices)))
axes[1].set_yticklabels([fitur_kolom[i] for i in indices])
axes[1].set_xlabel('Nilai Kepentingan (Importance)')
axes[1].set_title('Kontribusi Fitur Sentinel-2A terhadap Keputusan', fontweight="bold")

plt.tight_layout()
plt.savefig("evaluasi_klasifikasi_jatim.png", dpi=300)
plt.show()
```
