analisis file pada ekstraksi_fitur_kwanyar.md dan tambah kan pada bagian Penanganan Outlier, Melengkapi Tanggal, dan Interpolasi Data itu yang awalnya menggunakan interpolasi linear tambahkan dengan penanganan polynomial dengan contoh code:

```python
df['CO_filled'] = df['CO'].copy()

# Looping iteratif untuk membersihkan outlier sampai benar-benar habis
while True:
    # 1. Hitung ulang kuartil dan batas IQR berdasarkan data saat ini
    Q1 = df['CO_filled'].quantile(0.25)
    Q3 = df['CO_filled'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # 2. Deteksi lokasi outlier
    outliers = (df['CO_filled'] < lower_bound) | (df['CO_filled'] > upper_bound)

    # Jika sudah tidak ada outlier yang terdeteksi, hentikan perulangan
    if not outliers.any():
        break

    # 3. Mask nilai outlier menjadi NaN, lalu isi dengan interpolasi polinomial + bfill + ffill
    df['CO_filled'] = df['CO_filled'].mask(outliers)
    df['CO_filled'] = df['CO_filled'].interpolate(method='polynomial', order=1).bfill().ffill()

# 4. Simpan hasil akhir ke DataFrame baru dan ekspor ke CSV
df_CO = pd.DataFrame({"date": df['date'], "CO": df['CO_filled']})
df_CO.to_csv("CO_Bangkalan_final_polynomial.csv", index=False)
print("Data CO berhasil diproses dan disimpan ke CO_Bangkalan_final_polynomial.csv")
```

dan pada bagian ekstraksi fitur rubah yang awal nya melakukan ekstraksi satu persatu polutan menjadi dalam satu file tiga polutan lakukan di interpolasi linear maupun polynomial untuk code penggabungan file:

```python

import pandas as pd

# Memuat data yang telah diproses
df_no2 = pd.read_csv("NO2_Bangkalan_final.csv")
df_co = pd.read_csv("CO_Bangkalan_final.csv")
df_so2 = pd.read_csv("SO2_Bangkalan_final.csv")

dataframe_merged = pd.DataFrame({
    "date": df_no2['date'],
    "CO": df_co['CO'],
    "NO2": df_no2['NO2'],
    "SO2": df_so2['SO2']
})

dataframe_merged.to_csv("Polutan_Bangkalan_linear.csv", index=False)
print("Data polutan berhasil digabungkan dan disimpan ke Polutan_Bangkalan_linear.csv")
```

dan untuk code ekstraksi nya adalah:

```python
import pandas as pd
import numpy as np
import inspect
import tsfel.feature_extraction.features as tsfel_features

# ---------- 1. Muat 1 file CSV utama yang berisi semua polutan ----------
df = pd.read_csv('Polutan_Bangkalan_linear.csv')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

pollutants = ['NO2', 'SO2', 'CO']
fs = 1

# ---------- 2. Daftar 68 Fitur TSFEL ----------
FEATURE_LIST = """abs_energy auc autocorr average_power calc_centroid calc_max calc_mean
calc_median calc_min calc_std calc_var dfa distance ecdf ecdf_percentile ecdf_percentile_count
ecdf_slope entropy fundamental_frequency higuchi_fractal_dimension hist_mode human_range_energy
hurst_exponent interq_range kurtosis lempel_ziv lpcc max_frequency max_power_spectrum
maximum_fractal_length mean_abs_deviation mean_abs_diff mean_diff median_abs_deviation
median_abs_diff median_diff median_frequency mfcc mse negative_turning neighbourhood_peaks
petrosian_fractal_dimension pk_pk_distance positive_turning power_bandwidth rms skewness slope
spectral_centroid spectral_decrease spectral_distance spectral_entropy spectral_kurtosis
spectral_positive_turning spectral_roll_off spectral_roll_on spectral_skewness spectral_slope
spectral_spread spectral_variation spectrogram_mean_coeff sum_abs_diff wavelet_abs_mean
wavelet_energy wavelet_entropy wavelet_std wavelet_var zero_cross""".split()

print(f"Jumlah fitur per polutan: {len(FEATURE_LIST)}")
print(f"Total target fitur keseluruhan: {len(FEATURE_LIST) * len(pollutants)}")

# ---------- 3. Fungsi ekstraksi dan penyeragaman output  ----------
def to_scalar(result):
    if isinstance(result, dict) and "values" in result:
        result = result["values"]
    if isinstance(result, (list, tuple, np.ndarray)):
        arr = np.asarray(result, dtype=float)
        return float(np.nanmean(arr))
    return float(result)

def extract_one(fn_name, signal, fs):
    fn = getattr(tsfel_features, fn_name)
    params = inspect.signature(fn).parameters
    if "fs" in params:
        result = fn(signal, fs)
    else:
        result = fn(signal)
    return to_scalar(result)

# Dictionary untuk menampung seluruh hasil ekstraksi
combined_row = {}

# ---------- 4. Looping untuk membersihkan dan mengekstraksi tiap polutan ----------
for pollutant in pollutants:
    print(f"\n--- Memproses polutan: {pollutant} ---")

    df_poly = df[['date', pollutant]].copy()
    df_poly[pollutant] = pd.to_numeric(df_poly[pollutant], errors='coerce')

    # Handling outlier dengan IQR (sebagai safeguard tambahan)
    Q1 = df_poly[pollutant].quantile(0.25)
    Q3 = df_poly[pollutant].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_poly.loc[(df_poly[pollutant] < lower_bound) | (df_poly[pollutant] > upper_bound), pollutant] = np.nan

    # Interpolasi waktu dan cleaning
    df_clean = df_poly.set_index('date').interpolate(method='time').ffill().bfill()
    signal_1d = df_clean[pollutant].astype(float).values

    # Ekstraksi fitur dan beri prefix nama polutan (misal: NO2_abs_energy)
    for fn_name in FEATURE_LIST:
        feature_key = f"{pollutant}_{fn_name}"
        combined_row[feature_key] = extract_one(fn_name, signal_1d, fs)

# ---------- 5. Simpan ke DataFrame final ----------
extracted_features_final = pd.DataFrame([combined_row])
print(f"\nBerhasil! Total kolom akhir yang dihasilkan: {extracted_features_final.shape[1]}")

output_filename = 'Bangkalan_linear.csv'
extracted_features_final.to_csv(output_filename, index=False)
print(f"File berhasil disimpan sebagai: {output_filename}")
```

untuk directory file data:

data ekstraksi interpolasi linear = `source/ekstraksi_fitur/Bangkalan_linear.csv`
data polutan setelah interpolasi polynomial = `source/ekstraksi_fitur_polynomial/namaPolutan_Bangkalan_polynomial.csv`
data polutan interpolasi polynomial setelah digabung = `source/ekstraksi_fitur_polynomial/Polutan_Bangkalan_polynomial.csv`
data ekstraksi interpolasi polynomial = `source/ekstraksi_fitur_polynomial/Bangkalan_polynomial.csv`
