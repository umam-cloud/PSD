"""
precompute.py
Jalankan SEKALI di komputer kamu (bukan di Streamlit Cloud).

Fungsi: membaca TIF Sentinel-2 + model XGBoost, memprediksi semua piksel,
lalu menyimpan hasilnya ke folder data/ :
  - hasil_rgba.png       -> gambar hasil klasifikasi (dipakai overlay peta)
  - meta.json            -> batas koordinat peta
  - statistik_kelas.csv  -> jumlah piksel, luas (km2), dan persen tiap kelas

Cara pakai:
    python precompute.py
"""

import json
import math
from pathlib import Path

import geopandas as gpd
import joblib
import numpy as np
import pandas as pd
import rasterio
from PIL import Image
from rasterio.features import rasterize
from rasterio.warp import transform_bounds

# ------------------------------------------------------------------
# KONFIGURASI (sesuaikan jika nama file kamu berbeda)
# ------------------------------------------------------------------
DATA = Path("./data")
FILE_TIF = DATA / "sentinel2_6kelas_visual_full.tif"
FILE_GEOJSON = DATA / "jawa_timur_provinsi.geojson"
FILE_MODEL = DATA / "model_xgb.joblib"

# Gambar hasil diperkecil jika sisi terpanjangnya lebih dari ini,
# supaya peta web tidak berat. Statistik tetap dihitung dari resolusi penuh.
MAX_DIM = 3000

WARNA_KELAS = {
    "Sawah": "#FFD92F",
    "Bangunan": "#E41A1C",
    "Mangrove": "#8E44AD",
    "Hutan": "#2E7D32",
    "Laut": "#0D47A1",
    "Danau": "#4FC3F7",
}


def hex_ke_rgb(h):
    h = h.lstrip("#")
    return [int(h[i : i + 2], 16) for i in (0, 2, 4)]


# ------------------------------------------------------------------
# 1. Muat model
# ------------------------------------------------------------------
print("Memuat model...")
paket = joblib.load(FILE_MODEL)
model = paket["model"]
fitur = paket["fitur"]
encoder = paket["encoder"]

# ------------------------------------------------------------------
# 2. Baca raster & hitung indeks
# ------------------------------------------------------------------
print("Membaca raster...")
with rasterio.open(FILE_TIF) as src:
    H, W = src.height, src.width
    B02, B03, B04, B08, B11 = [src.read(i).astype(np.float32) for i in range(1, 6)]
    lon_w, lat_s, lon_e, lat_n = transform_bounds(src.crs, "EPSG:4326", *src.bounds)
    transform_tif = src.transform
    crs_tif = src.crs

    # Ukuran 1 piksel dalam km (untuk menghitung luas)
    res_x, res_y = src.res
    if crs_tif.is_geographic:
        lat_tengah = (lat_s + lat_n) / 2
        km_x = res_x * 111.32 * math.cos(math.radians(lat_tengah))
        km_y = res_y * 110.57
    else:
        km_x, km_y = res_x / 1000, res_y / 1000
    luas_piksel_km2 = km_x * km_y

np.seterr(divide="ignore", invalid="ignore")
NDVI = np.nan_to_num((B08 - B04) / (B08 + B04), nan=0.0, posinf=0.0, neginf=0.0)
NDWI = np.nan_to_num((B03 - B08) / (B03 + B08), nan=0.0, posinf=0.0, neginf=0.0)
NDBI = np.nan_to_num((B11 - B08) / (B11 + B08), nan=0.0, posinf=0.0, neginf=0.0)

# ------------------------------------------------------------------
# 3. Masking daratan
# ------------------------------------------------------------------
print("Membuat masker daratan...")
prov = gpd.read_file(FILE_GEOJSON)
if prov.crs != crs_tif:
    prov = prov.to_crs(crs_tif)

mask_daratan = rasterize(
    [(geom, 1) for geom in prov.geometry],
    out_shape=(H, W),
    transform=transform_tif,
    fill=0,
    dtype=np.uint8,
)

# ------------------------------------------------------------------
# 4. Prediksi
# ------------------------------------------------------------------
print("Memprediksi piksel daratan (bisa beberapa menit)...")
df_pred = pd.DataFrame(
    {
        "B02": B02.flatten(), "B03": B03.flatten(), "B04": B04.flatten(),
        "B08": B08.flatten(), "B11": B11.flatten(),
        "NDVI": NDVI.flatten(), "NDWI": NDWI.flatten(), "NDBI": NDBI.flatten(),
    }
)

mask_flat = mask_daratan.flatten()
valid_data = B02.flatten() > 0
idx_daratan_valid = (mask_flat == 1) & valid_data
idx_laut_valid = (mask_flat == 0) & valid_data

preds_num = model.predict(df_pred[idx_daratan_valid][fitur])
preds_teks = encoder.inverse_transform(preds_num)
preds_teks = np.array([str(p).title() for p in preds_teks])

# ------------------------------------------------------------------
# 5. Warnai (RGBA)
# ------------------------------------------------------------------
print("Membuat gambar hasil...")
rgba_flat = np.zeros((H * W, 4), dtype=np.uint8)

rgba_flat[idx_laut_valid, :3] = hex_ke_rgb(WARNA_KELAS["Laut"])
rgba_flat[idx_laut_valid, 3] = 225

posisi_daratan = np.where(idx_daratan_valid)[0]
for kelas, warna in WARNA_KELAS.items():
    if kelas == "Laut":
        continue
    posisi = posisi_daratan[preds_teks == kelas]
    rgba_flat[posisi, :3] = hex_ke_rgb(warna)
    rgba_flat[posisi, 3] = 225

rgba_img = rgba_flat.reshape((H, W, 4))

# ------------------------------------------------------------------
# 6. Statistik (dari resolusi penuh)
# ------------------------------------------------------------------
jumlah = {k: int((preds_teks == k).sum()) for k in WARNA_KELAS if k != "Laut"}
jumlah["Laut"] = int(idx_laut_valid.sum())

stat = pd.DataFrame({"Kelas": list(jumlah.keys()), "Piksel": list(jumlah.values())})
stat["Luas_km2"] = (stat["Piksel"] * luas_piksel_km2).round(2)
stat["Persen"] = (stat["Piksel"] / stat["Piksel"].sum() * 100).round(2)

# ------------------------------------------------------------------
# 7. Simpan (gambar diperkecil jika terlalu besar)
# ------------------------------------------------------------------
langkah = max(1, math.ceil(max(H, W) / MAX_DIM))
img_kecil = rgba_img[::langkah, ::langkah]
Image.fromarray(img_kecil, mode="RGBA").save(DATA / "hasil_rgba.png", optimize=True)

with open(DATA / "meta.json", "w") as f:
    json.dump({"lat_s": lat_s, "lon_w": lon_w, "lat_n": lat_n, "lon_e": lon_e}, f)

stat.to_csv(DATA / "statistik_kelas.csv", index=False)

print("\nSelesai! File tersimpan di folder data/:")
print(" - hasil_rgba.png, meta.json, statistik_kelas.csv")
print(stat.to_string(index=False))
