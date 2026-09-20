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

# Preprocessing dan Ekstraksi Fitur

## Preprocessing: Penanganan Missing Value, Outliers dan Interpolasi

Pada tahap _Data Understanding_, kita telah mengidentifikasi adanya _missing values_ dan _outliers_. Untuk menangani masalah ini dan mempersiapkan data agar bisa diekstrak fiturnya secara berkesinambungan, kita menerapkan pembersihan data menggunakan metode Rentang Interkuartil (IQR) dan mengisi kekosongan data menggunakan **interpolasi linier**.

### Deteksi Missing Value

Deteksi _missing value_ (data kosong atau hilang) bertujuan untuk mengidentifikasi seberapa banyak data yang tidak terekam dalam observasi. Mengetahui jumlah dan persentase kekosongan data sangat penting sebelum dilakukan proses penanganan (seperti interpolasi), agar kita dapat mengukur kualitas dataset secara keseluruhan.

```python
import pandas as pd

df = pd.read_csv("nama_file_polutan.csv")

missing_value = df['nama_kolom_polutan'].isna().sum()
total_data = len(df)
persentase_missing = (missing_value / total_data) * 100

print(f"Jumlah missing value: {missing_value}")
print(f"Total data: {total_data}")
print(f"Persentase data missing: {persentase_missing:.2f}%")
```

1. NO2

```{code-cell}
:tags: [hide-input]
import pandas as pd

df = pd.read_csv("./source/ekstraksi_fitur/NO2_Bangkalan_Terkini.csv")

missing_value = df['NO2'].isna().sum()
total_data = len(df)
persentase_missing = (missing_value / total_data) * 100

print(f"Jumlah missing value: {missing_value}")
print(f"Total data: {total_data}")
print(f"Persentase data missing: {persentase_missing:.2f}%")
```

2. CO

```{code-cell}
:tags: [hide-input]
import pandas as pd

df = pd.read_csv("./source/ekstraksi_fitur/CO_Bangkalan_Terkini.csv")

missing_value = df['CO'].isna().sum()
total_data = len(df)
persentase_missing = (missing_value / total_data) * 100

print(f"Jumlah missing value: {missing_value}")
print(f"Total data: {total_data}")
print(f"Persentase data missing: {persentase_missing:.2f}%")
```

3. SO2

```{code-cell}
:tags: [hide-input]
import pandas as pd

df = pd.read_csv("./source/ekstraksi_fitur/SO2_Bangkalan_Terkini.csv")

missing_value = df['SO2'].isna().sum()
total_data = len(df)
persentase_missing = (missing_value / total_data) * 100

print(f"Jumlah missing value: {missing_value}")
print(f"Total data: {total_data}")
print(f"Persentase data missing: {persentase_missing:.2f}%")
```

### Deteksi dan Visualisasi Outlier (Metode IQR)

Metode _Interquartile Range_ (IQR) digunakan untuk mengidentifikasi nilai-nilai yang menyimpang atau berada di luar batas kewajaran. Data polutan yang nilainya lebih rendah dari _lower bound_ atau lebih tinggi dari _upper bound_ diklasifikasikan sebagai outlier.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("nama_file_polutan.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['nama_kolom_polutan'].quantile(0.25)
Q3 = df['nama_kolom_polutan'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['nama_kolom_polutan'] < lower_bound) | (df['nama_kolom_polutan'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'nama_kolom_polutan']].head())
```

1. NO2

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/NO2_Bangkalan_Terkini.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['NO2'].quantile(0.25)
Q3 = df['NO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['NO2'] < lower_bound) | (df['NO2'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'NO2']].head())
```

2. CO

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/CO_Bangkalan_Terkini.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['CO'].quantile(0.25)
Q3 = df['CO'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['CO'] < lower_bound) | (df['CO'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'CO']].head())
```

3. SO2

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/SO2_Bangkalan_Terkini.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['SO2'].quantile(0.25)
Q3 = df['SO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['SO2'] < lower_bound) | (df['SO2'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'SO2']].head())
```

Visualisasi batas ambang IQR terhadap distribusi data untuk melihat outlier secara lebih jelas:

```python
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("nama_file_polutan.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['nama_kolom_polutan'].quantile(0.25)
Q3 = df['nama_kolom_polutan'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['nama_kolom_polutan'] < lower_bound) | (df['nama_kolom_polutan'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['nama_kolom_polutan'], label="nama_kolom_polutan", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['nama_kolom_polutan'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data nama_kolom_polutan (Metode IQR)")
plt.xlabel("Tanggal")
plt.ylabel("Kadar nama_kolom_polutan")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

1. NO2

```{code-cell}
:tags: [hide-input]
df = pd.read_csv("./source/ekstraksi_fitur/NO2_Bangkalan_Terkini.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['NO2'].quantile(0.25)
Q3 = df['NO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['NO2'] < lower_bound) | (df['NO2'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['NO2'], label="NO2", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['NO2'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data NO2 (Metode IQR)")
plt.xlabel("Tanggal")
plt.ylabel("Kadar NO2")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

2. CO

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/CO_Bangkalan_Terkini.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['CO'].quantile(0.25)
Q3 = df['CO'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['CO'] < lower_bound) | (df['CO'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['CO'], label="CO", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['CO'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data CO (Metode IQR)")
plt.xlabel("Tanggal")
plt.ylabel("Kadar CO")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

3. SO2

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/SO2_Bangkalan_Terkini.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['SO2'].quantile(0.25)
Q3 = df['SO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['SO2'] < lower_bound) | (df['SO2'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['SO2'], label="SO2", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['SO2'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data SO2 (Metode IQR)")
plt.xlabel("Tanggal")
plt.ylabel("Kadar SO2")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

### Penanganan Outlier, Melengkapi Tanggal, dan Interpolasi Data

Setelah mendeteksi keberadaan outlier, langkah selanjutnya adalah menandainya sebagai nilai kosong (`NaN`). Karena pada data deret waktu terdapat banyak tanggal yang terlewat, kita melengkapi rentang waktunya (dari tanggal terawal hingga terakhir). Kemudian, metode interpolasi linier diterapkan pada keseluruhan dataset untuk mengisi nilai kosong (`NaN`) tersebut. Di akhir proses, teknik _backward fill_ (`bfill`) serta _forward fill_ (`ffill`) dimanfaatkan guna mengatasi nilai kosong pada bagian pinggir atau awalan dan akhiran rangkaian data yang tidak bisa diinterpolasi linier.

```python
# Tandai outlier menjadi NaN
df['polutan_cleaned'] = df['polutan'].mask(
    (df['polutan'] < lower_bound) | (df['polutan'] > upper_bound)
)

# Memasukkan data ke dalam rentang tanggal yang lengkap
df = df.set_index('date')
rentang_tanggal_lengkap = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
df_lengkap = df.reindex(rentang_tanggal_lengkap)

# interpolasi linier pada NaN yang sudah dibuat (dari outlier & reindex)
df_lengkap['polutan_filled'] = df_lengkap['polutan_cleaned'].interpolate(method='linear')
df_lengkap['polutan_filled'] = df_lengkap['polutan_filled'].bfill().ffill()

# Kembalikan index menjadi kolom
df_lengkap.index.name = 'date'
df_lengkap.reset_index(inplace=True)

# Simpan data yang telah dibersihkan dan diinterpolasi ke file CSV baru
df_polutan_Kwanyar = pd.DataFrame({
    "date": df_lengkap['date'],
    "polutan": df_lengkap['polutan_filled']
})
df_polutan_Kwanyar.to_csv("nama_hasil_file_polutan_cleaned.csv", index=False)
```

Grafik setelah penanganan Outlier dan Penambahan Tanggal

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("nama_file_polutan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['nama_kolom_polutan'].quantile(0.25)
Q3 = df['nama_kolom_polutan'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['nama_kolom_polutan'] < lower_bound) | (df['nama_kolom_polutan'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'nama_kolom_polutan']].head())
```

1. NO2

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/NO2_Bangkalan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['NO2'].quantile(0.25)
Q3 = df['NO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['NO2'] < lower_bound) | (df['NO2'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'NO2']].head())
```

2. CO

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/CO_Bangkalan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['CO'].quantile(0.25)
Q3 = df['CO'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['CO'] < lower_bound) | (df['CO'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'CO']].head())
```

3. SO2

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/ekstraksi_fitur/SO2_Bangkalan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['SO2'].quantile(0.25)
Q3 = df['SO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter outlier
outliers_iqr = df[(df['SO2'] < lower_bound) | (df['SO2'] > upper_bound)]

print("Jumlah Outlier (IQR):", len(outliers_iqr))
print(outliers_iqr[['date', 'SO2']].head())
```

Visualisasi batas ambang IQR terhadap distribusi data untuk melihat outlier secara lebih jelas:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("nama_file_polutan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['nama_kolom_polutan'].quantile(0.25)
Q3 = df['nama_kolom_polutan'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['nama_kolom_polutan'] < lower_bound) | (df['nama_kolom_polutan'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['nama_kolom_polutan'], label="nama_kolom_polutan", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['nama_kolom_polutan'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data nama_kolom_polutan (Metode IQR) - Setelah Penanganan")
plt.xlabel("Tanggal")
plt.ylabel("Kadar nama_kolom_polutan")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

1. NO2

```{code-cell}
:tags: [hide-input]
df = pd.read_csv("./source/ekstraksi_fitur/NO2_Bangkalan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['NO2'].quantile(0.25)
Q3 = df['NO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['NO2'] < lower_bound) | (df['NO2'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['NO2'], label="NO2", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['NO2'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data NO2 (Metode IQR) - Setelah Penanganan")
plt.xlabel("Tanggal")
plt.ylabel("Kadar NO2")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

2. CO

```{code-cell}
:tags: [hide-input]
df = pd.read_csv("./source/ekstraksi_fitur/CO_Bangkalan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['CO'].quantile(0.25)
Q3 = df['CO'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['CO'] < lower_bound) | (df['CO'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['CO'], label="CO", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['CO'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data CO (Metode IQR) - Setelah Penanganan")
plt.xlabel("Tanggal")
plt.ylabel("Kadar CO")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

3. SO2

```{code-cell}
:tags: [hide-input]
df = pd.read_csv("./source/ekstraksi_fitur/SO2_Bangkalan_final.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Hitung IQR
Q1 = df['SO2'].quantile(0.25)
Q3 = df['SO2'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['SO2'] < lower_bound) | (df['SO2'] > upper_bound)]

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['SO2'], label="SO2", linewidth=1)

plt.scatter(outliers_iqr['date'], outliers_iqr['SO2'],
            color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data SO2 (Metode IQR) - Setelah Penanganan")
plt.xlabel("Tanggal")
plt.ylabel("Kadar SO2")
plt.legend()
plt.tight_layout()
plt.xticks(
    ticks=[df['date'].iloc[0], df['date'].iloc[-1]],
    labels=[df['date'].iloc[0].strftime('%Y-%m-%d'),
            df['date'].iloc[-1].strftime('%Y-%m-%d')]
)
plt.show()
```

### Visualisasi Gabungan Timeseries (NO2, CO, SO2)

Berikut adalah visualisasi yang menampilkan ketiga polutan secara bersamaan dalam satu gambar (dengan subplot agar skala tiap polutan tidak saling bertabrakan) setelah melalui proses pembersihan data:

```{code-cell}
:tags: [hide-input]
import pandas as pd
import matplotlib.pyplot as plt

# Memuat ketiga data final
df_no2 = pd.read_csv("./source/ekstraksi_fitur/NO2_Bangkalan_final.csv")
df_co = pd.read_csv("./source/ekstraksi_fitur/CO_Bangkalan_final.csv")
df_so2 = pd.read_csv("./source/ekstraksi_fitur/SO2_Bangkalan_final.csv")

# Pastikan format tanggal sama
df_no2['date'] = pd.to_datetime(df_no2['date'])
df_co['date'] = pd.to_datetime(df_co['date'])
df_so2['date'] = pd.to_datetime(df_so2['date'])

# Menggabungkan ketiga data berdasarkan tanggal
df_gabungan = df_no2[['date', 'NO2']].merge(df_co[['date', 'CO']], on='date', how='outer')
df_gabungan = df_gabungan.merge(df_so2[['date', 'SO2']], on='date', how='outer')
df_gabungan.set_index('date', inplace=True)

# Membuat visualisasi gabungan (satu grafik / overlay)
# Catatan: Karena rentang nilai tiap polutan mungkin berbeda jauh, garis yang bernilai kecil bisa terlihat lebih rata.
df_gabungan.plot(figsize=(15, 7), title="Visualisasi Timeseries Tiga Polutan (NO2, CO, SO2) dalam 1 Grafik", grid=True, color=['red', 'gold', 'green'])

plt.xlabel("Tanggal")
plt.ylabel("Kadar Polutan")
plt.tight_layout()
plt.show()
```

## Ekstraksi Fitur Deret Waktu (Time Series)

Dengan data deret waktu polutan udara yang konsisten (tanpa tanggal hilang dan tanpa _outlier_), kita dapat melangkah ke ekstraksi berbagai fitur statistik, temporal, maupun spektral. Fitur-fitur ini sangat berguna sebagai parameter *input* yang merepresentasikan karakteristik *trend* harian polutan ke dalam model _machine learning_ maupun _deep learning_.

Kita akan memanfaatkan modul pustaka Python bernama `tsfel` (_Time Series Feature Extraction Library_) guna mempermudah proses komputasi serta standarisasi ragam tipe fitur.

Berikut adalah sintaks kode implementasi untuk mengekstraksi sebanyak 68 fitur otomatis pada deret data NO₂ (dan berlaku perlakuan serupa untuk unsur polutan lainnya):

```python
import pandas as pd
import numpy as np
import inspect
import tsfel.feature_extraction.features as tsfel_features

# ---------- 1. Muat data yang sudah dibersihkan ----------
df = pd.read_csv('nama_file_polutan_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

target_pollutant = 'nama_polutan'

# Pastikan data di-casting ke tipe numerik.
df[target_pollutant] = pd.to_numeric(df[target_pollutant], errors='coerce')

# Interpolasi terakhir untuk berjaga-jaga apabila terdapat sisa format nan
df_clean = df.set_index('date').interpolate(method='time').ffill().bfill()
fs = 1
signal_1d = df_clean[target_pollutant].astype(float).values

# ---------- 2. Inisiasi 68 Daftar Fitur TSFEL ----------
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

print("Jumlah fitur yang diminta:", len(FEATURE_LIST))

# ---------- 3. Fungsi ekstraksi dan penyeragaman output  ----------

# Fungsi bantuan (helper) merubah output multivariat TSFEL menjadi float tunggal/skalar
def to_scalar(result):
    if isinstance(result, dict) and "values" in result:
        result = result["values"]
    if isinstance(result, (list, tuple, np.ndarray)):
        arr = np.asarray(result, dtype=float)
        return float(np.nanmean(arr))
    return float(result)

# Fungsi map pemanggilan fungsi TSFEL 
def extract_one(fn_name, signal, fs):
    fn = getattr(tsfel_features, fn_name)
    params = inspect.signature(fn).parameters
    if "fs" in params:
        result = fn(signal, fs)
    else:
        result = fn(signal)
    return to_scalar(result)

# Lakukan ekstraksi iteratif pada fitur
row = {}
for fn_name in FEATURE_LIST:
    row[fn_name] = extract_one(fn_name, signal_1d, fs)

extracted_features_final = pd.DataFrame([row])

print(f"Berhasil! Jumlah fitur yang diekstrak pada {target_pollutant}: {extracted_features_final.shape[1]}")

# Export hasil ke file CSV
extracted_features_final.to_csv(f'nama_hasil_ekstraksi_fitur_TSFEL.csv', index=False)
```

Data hasil ekstraksi fitur menggunakan TSFEL

1. NO2

```{code-cell}
:tags: [hide-input]
df = pd.read_csv("./source/Ekstraksi_fitur/NO2_Kwanyar_TSFEL.csv")
df.head(5)
```

2. CO

```{code-cell}
:tags: [hide-input]
df = pd.read_csv("./source/Ekstraksi_fitur/CO_Kwanyar_TSFEL.csv")
df.head(5)
```

3. SO2

```{code-cell}
:tags: [hide-input]
df = pd.read_csv("./source/Ekstraksi_fitur/SO2_Kwanyar_TSFEL.csv")
df.head(5)
```