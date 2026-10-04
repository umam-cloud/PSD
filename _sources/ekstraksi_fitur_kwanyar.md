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

## Penanganan Outlier, Melengkapi Tanggal, dan Interpolasi Data

Setelah mendeteksi keberadaan outlier, langkah selanjutnya adalah menandainya sebagai nilai kosong (`NaN`). Karena pada data deret waktu terdapat banyak tanggal yang terlewat, kita melengkapi rentang waktunya (dari tanggal terawal hingga terakhir). 

Dalam tahapan ini kita bisa menerapkan dua variasi interpolasi, yaitu **Interpolasi Linier** maupun **Interpolasi Polinomial Iteratif** (untuk membersihkan outlier secara berulang hingga benar-benar habis).

### 1. Metode Interpolasi Linier (Standard)
Metode ini mengisi nilai kosong secara linier (garis lurus) antar data yang ada. Di akhir proses, teknik _backward fill_ (`bfill`) serta _forward fill_ (`ffill`) dimanfaatkan guna mengatasi nilai kosong pada awalan dan akhiran.

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
df_polutan_Kwanyar.to_csv("namaPolutan_Bangkalan_final_linear.csv", index=False)
```

### Grafik setelah penanganan Outlier dan Penambahan Tanggal (Metode Linier)

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


### 2. Metode Interpolasi Polinomial Iteratif
Metode ini secara iteratif (berulang) akan mengecek batas IQR. Jika ada outlier baru setelah interpolasi sebelumnya, ia akan membersihkannya kembali dan melakukan interpolasi polinomial hingga data benar-benar bebas outlier.

```python
df['polutan_filled'] = df['polutan'].copy()

# Looping iteratif untuk membersihkan outlier sampai benar-benar habis
while True:
    # 1. Hitung ulang kuartil dan batas IQR berdasarkan data saat ini
    Q1 = df['polutan_filled'].quantile(0.25)
    Q3 = df['polutan_filled'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # 2. Deteksi lokasi outlier
    outliers = (df['polutan_filled'] < lower_bound) | (df['polutan_filled'] > upper_bound)

    # Jika sudah tidak ada outlier yang terdeteksi, hentikan perulangan
    if not outliers.any():
        break

    # 3. Mask nilai outlier menjadi NaN, lalu isi dengan interpolasi polinomial + bfill + ffill
    df['polutan_filled'] = df['polutan_filled'].mask(outliers)
    df['polutan_filled'] = df['polutan_filled'].interpolate(method='polynomial', order=1).bfill().ffill()

# 4. Simpan hasil akhir ke DataFrame baru dan ekspor ke CSV
df_polutan_Kwanyar = pd.DataFrame({"date": df['date'], "polutan": df['polutan_filled']})
df_polutan_Kwanyar.to_csv("namaPolutan_Bangkalan_polynomial.csv", index=False)
print("Data polutan berhasil diproses dan disimpan ke namaPolutan_Bangkalan_polynomial.csv")
```

### Grafik setelah penanganan Outlier dan Penambahan Tanggal (Metode Polinomial Iteratif)

Karena menggunakan metode iteratif, maka pada data hasil polinomial seharusnya jumlah outlier yang tersisa menjadi 0 (atau jauh lebih sedikit) karena IQR akan terus mengecil hingga tidak ada nilai yang di luar kewajaran.

1. NO2 (Polinomial)

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/Ekstraksi_fitur_polynomial/NO2_Bangkalan_final_polynomial.csv")
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

print("Jumlah Outlier (IQR) - Polynomial:", len(outliers_iqr))

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['NO2'], label="NO2 (Polynomial)", linewidth=1, color='blue')

if len(outliers_iqr) > 0:
    plt.scatter(outliers_iqr['date'], outliers_iqr['NO2'], color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='cyan',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data NO2 (Metode IQR) - Setelah Penanganan Polinomial")
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

2. CO (Polinomial)

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/Ekstraksi_fitur_polynomial/CO_Bangkalan_final_polynomial.csv")
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

print("Jumlah Outlier (IQR) - Polynomial:", len(outliers_iqr))

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['CO'], label="CO (Polynomial)", linewidth=1, color='orange')

if len(outliers_iqr) > 0:
    plt.scatter(outliers_iqr['date'], outliers_iqr['CO'], color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='green', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='cyan',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data CO (Metode IQR) - Setelah Penanganan Polinomial")
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

3. SO2 (Polinomial)

```{code-cell}
:tags: [hide-input]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./source/Ekstraksi_fitur_polynomial/SO2_Bangkalan_final_polynomial.csv")
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

print("Jumlah Outlier (IQR) - Polynomial:", len(outliers_iqr))

plt.figure(figsize=(15,5))
plt.plot(df['date'], df['SO2'], label="SO2 (Polynomial)", linewidth=1, color='green')

if len(outliers_iqr) > 0:
    plt.scatter(outliers_iqr['date'], outliers_iqr['SO2'], color='red', marker='o', label="Outliers")

plt.axhline(upper_bound, color='orange', linestyle='dashed', label="Upper Bound (IQR)")
plt.axhline(lower_bound, color='blue',   linestyle='dashed', label="Lower Bound (IQR)")

plt.title("Deteksi Outlier Data SO2 (Metode IQR) - Setelah Penanganan Polinomial")
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

### Visualisasi Gabungan Timeseries (NO2, CO, SO2) - Linier

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

### Visualisasi Gabungan Timeseries (NO2, CO, SO2) - Polinomial

Berikut adalah visualisasi dari gabungan ketiga polutan yang diproses menggunakan metode Polinomial Iteratif:

```{code-cell}
:tags: [hide-input]
import pandas as pd
import matplotlib.pyplot as plt

# Memuat ketiga data final polinomial
df_no2_poly = pd.read_csv("./source/Ekstraksi_fitur_polynomial/NO2_Bangkalan_final_polynomial.csv")
df_co_poly = pd.read_csv("./source/Ekstraksi_fitur_polynomial/CO_Bangkalan_final_polynomial.csv")
df_so2_poly = pd.read_csv("./source/Ekstraksi_fitur_polynomial/SO2_Bangkalan_final_polynomial.csv")

# Pastikan format tanggal sama
df_no2_poly['date'] = pd.to_datetime(df_no2_poly['date'])
df_co_poly['date'] = pd.to_datetime(df_co_poly['date'])
df_so2_poly['date'] = pd.to_datetime(df_so2_poly['date'])

# Menggabungkan ketiga data berdasarkan tanggal
df_gabungan_poly = df_no2_poly[['date', 'NO2']].merge(df_co_poly[['date', 'CO']], on='date', how='outer')
df_gabungan_poly = df_gabungan_poly.merge(df_so2_poly[['date', 'SO2']], on='date', how='outer')
df_gabungan_poly.set_index('date', inplace=True)

# Membuat visualisasi gabungan (satu grafik / overlay)
df_gabungan_poly.plot(figsize=(15, 7), title="Visualisasi Timeseries Tiga Polutan (NO2, CO, SO2) dalam 1 Grafik - Polinomial", grid=True, color=['blue', 'orange', 'green'])

plt.xlabel("Tanggal")
plt.ylabel("Kadar Polutan")
plt.tight_layout()
plt.show()
```

## Ekstraksi Fitur Deret Waktu (Time Series)

Dengan data deret waktu polutan udara yang konsisten (tanpa tanggal hilang dan tanpa _outlier_), kita dapat melangkah ke ekstraksi berbagai fitur statistik, temporal, maupun spektral. Pada versi ini, kita tidak lagi mengekstraksi polutan secara terpisah, melainkan **menggabungkannya terlebih dahulu ke dalam satu file**, agar hasil ekstraksi menghasilkan satu baris data panjang yang mewakili kondisi ketiga polutan sekaligus.

### 1. Penggabungan File Data Tiga Polutan
Baik menggunakan interpolasi linier maupun polinomial, kita gabungkan ketiga file hasil pembersihan ke dalam satu dataset.

#### Penggabungan File Linier

```{code-cell}
import pandas as pd

# Memuat data yang telah diproses (linear)
df_no2 = pd.read_csv("./source/ekstraksi_fitur/NO2_Bangkalan_final.csv")
df_co = pd.read_csv("./source/ekstraksi_fitur/CO_Bangkalan_final.csv")
df_so2 = pd.read_csv("./source/ekstraksi_fitur/SO2_Bangkalan_final.csv")

dataframe_merged = pd.DataFrame({
    "date": df_no2['date'],
    "CO": df_co['CO'],
    "NO2": df_no2['NO2'],
    "SO2": df_so2['SO2']
})

dataframe_merged.to_csv("Polutan_Bangkalan_linear.csv", index=False)
print("Data polutan berhasil digabungkan dan disimpan ke Polutan_Bangkalan_linear.csv")
```

#### Penggabungan File Polinomial

```{code-cell}
import pandas as pd

# Memuat data yang telah diproses (polinomial)
df_no2 = pd.read_csv("./source/ekstraksi_fitur_polynomial/NO2_Bangkalan_final_polynomial.csv")
df_co = pd.read_csv("./source/ekstraksi_fitur_polynomial/CO_Bangkalan_final_polynomial.csv")
df_so2 = pd.read_csv("./source/ekstraksi_fitur_polynomial/SO2_Bangkalan_final_polynomial.csv")

dataframe_merged_poly = pd.DataFrame({
    "date": df_no2['date'],
    "CO": df_co['CO'],
    "NO2": df_no2['NO2'],
    "SO2": df_so2['SO2']
})

dataframe_merged_poly.to_csv("Polutan_Bangkalan_polynomial.csv", index=False)
print("Data polutan polinomial berhasil digabungkan dan disimpan ke Polutan_Bangkalan_polynomial.csv")
```

### 2. Ekstraksi Fitur TSFEL Terpusat

Kita memanfaatkan pustaka Python `tsfel` (_Time Series Feature Extraction Library_) guna mempermudah proses komputasi serta standarisasi ragam tipe fitur. Kode di bawah ini akan secara otomatis melakukan _looping_ ekstraksi pada setiap polutan di file gabungan, menambahkan prefiks pada nama kolom (misal: `NO2_abs_energy`), dan menggabungkannya ke dalam 1 baris DataFrame final.

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

1. Hasil Ekstraksi Fitur Linier

```{code-cell}
:tags: [hide-input]
df_ekstraksi_cek = pd.read_csv("source/Ekstraksi_fitur/Bangkalan_linear.csv")
df_ekstraksi_cek.head(5)
```

2. Hasil Ekstraksi Fitur Polinomial

```{code-cell}
:tags: [hide-input]
df_ekstraksi_cek_poly = pd.read_csv("./source/Ekstraksi_fitur_polynomial/Bangkalan_polynomial.csv")
df_ekstraksi_cek_poly.head(5)
```