
## Domain TSFEL

Pustaka TSFEL membagi fitur deret waktu menjadi tiga domain utama untuk menganalisis data dari berbagai perspektif: **Statistik (Statistical)**, **Waktu (Temporal)**, dan **Frekuensi (Spectral)**. Berikut adalah penjelasan untuk setiap domain beserta fitur-fitur yang terdapat di dalamnya:

### 1. Domain Statistical
Domain statistik mengekstrak metrik kuantitatif dan karakteristik sebaran serta bentuk distribusi dari sinyal deret waktu tanpa mempertimbangkan urutan kemunculan waktunya. Fitur-fitur ini sangat baik untuk mengetahui rentang, kecenderungan memusat, dan variasi data.

* **`calc_max`, `calc_min`, `calc_mean`, `calc_median`**: Nilai maksimum, minimum, rata-rata, dan median dari deret waktu polutan.
  
  $$ \mu = \frac{1}{N} \sum_{i=1}^N x_i $$

* **`calc_std`, `calc_var`**: Standar deviasi dan varians yang mengukur tingkat penyebaran atau fluktuasi sinyal.
  
  $$ \sigma = \sqrt{\frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2} $$

* **`ecdf`, `ecdf_percentile`, `ecdf_percentile_count`, `ecdf_slope`**: Metrik berdasarkan _Empirical Cumulative Distribution Function_ (ECDF) yang menggambarkan distribusi probabilitas kumulatif dari sinyal.
  
  $$ \hat{F}(t) = \frac{1}{N} \sum_{i=1}^N \mathbf{1}_{x_i \le t} $$

* **`hist_mode`**: Nilai kemunculan terbanyak (modus) dalam histogram data.

* **`interq_range`**: _Interquartile Range_ (IQR), mengukur rentang data di antara kuartil atas (Q3) dan kuartil bawah (Q1).
  
  $$ IQR = Q_3 - Q_1 $$

* **`kurtosis`**: Tingkat kelancipan (_peakedness_) dari distribusi data polutan dibandingkan dengan distribusi normal.
  
  $$ K = \frac{\frac{1}{N} \sum_{i=1}^N (x_i - \mu)^4}{\sigma^4} $$

* **`skewness`**: Ukuran ketidaksimetrisan (kemiringan) dari distribusi data polutan.
  
  $$ S = \frac{\frac{1}{N} \sum_{i=1}^N (x_i - \mu)^3}{\sigma^3} $$

* **`mean_abs_deviation`, `median_abs_deviation`**: Rata-rata deviasi absolut dan median deviasi absolut yang memberikan ukuran kekokohan (_robustness_) sebaran data dari rata-rata atau mediannya.
  
  $$ MAD = \frac{1}{N} \sum_{i=1}^N |x_i - \mu| $$

* **`rms`**: _Root Mean Square_ (RMS), ukuran besaran rata-rata kuadrat dari sinyal, mencerminkan energi rata-rata data.
  
  $$ RMS = \sqrt{\frac{1}{N} \sum_{i=1}^N x_i^2} $$

### 2. Domain Temporal
Domain temporal mengevaluasi sinyal dari segi urutan waktunya. Fitur ini sangat krusial untuk menemukan siklus, tren linier, kompleksitas atau tingkat kekacauan (_chaos_) pada data, serta autokorelasi dari suatu titik waktu ke waktu lainnya.

* **`abs_energy`**: Total energi absolut yang dikandung oleh sinyal seiring berjalannya waktu.
  
  $$ E = \sum_{i=1}^N |x_i|^2 $$

* **`auc`**: _Area Under the Curve_ (AUC), total luas area di bawah kurva sinyal polutan, dihitung dengan aturan trapesium.
  
  $$ AUC = \sum_{i=1}^{N-1} \frac{|x_{i+1} + x_i|}{2} $$

* **`autocorr`**: Autokorelasi, seberapa kuat sinyal polutan saat ini berkorelasi dengan waktu-waktu sebelumnya.
  
  $$ R(\tau) = \frac{1}{(N-\tau)\sigma^2} \sum_{i=1}^{N-\tau} (x_i - \mu)(x_{i+\tau} - \mu) $$

* **`average_power`**: Rata-rata kekuatan sinyal dalam domain waktu.
  
  $$ P = \frac{1}{N} \sum_{i=1}^N x_i^2 $$

* **`calc_centroid`**: Titik pusat (centroid) sinyal di sepanjang sumbu waktu.
  
  $$ C_t = \frac{\sum_{i=1}^N t_i x_i}{\sum_{i=1}^N x_i} $$

* **`dfa`**: _Detrended Fluctuation Analysis_ (DFA), untuk mengukur dependensi jangka panjang atau fraktalitas sinyal, didefinisikan dengan kemiringan kurva $\log(F(n))$ terhadap $\log(n)$.

* **`distance`**: Total jarak lintasan pergerakan titik data dari awal hingga akhir.
  
  $$ D = \sum_{i=1}^{N-1} |x_{i+1} - x_i| $$

* **`entropy`**: Skalar entropi yang mengukur tingkat ketidakteraturan, ketidakpastian, atau kerumitan pada deret waktu, dihitung dengan Shannon Entropy.
  
  $$ H = - \sum p(x) \log p(x) $$

* **`higuchi_fractal_dimension`, `petrosian_fractal_dimension`**: Dimensi fraktal yang digunakan untuk menilai seberapa bergerigi atau kompleks sinyal secara matematis (misal formula Petrosian).
  
  $$ D = \frac{\log_{10}(N)}{\log_{10}(N) + \log_{10}\left(\frac{N}{N+0.4N_{Z}}\right)} $$

* **`hurst_exponent`**: Mengevaluasi apakah deret waktu memiliki tren memori jangka panjang.
  
  $$ E\left[\frac{R(n)}{S(n)}\right] \sim c n^H $$

* **`lempel_ziv`**: Tingkat kompresibilitas atau kekayaan pola pada sinyal (kompleksitas deterministik).

* **`maximum_fractal_length`**: Panjang maksimal fraktal dari skala waktu yang bervariasi.

* **`mean_abs_diff`, `mean_diff`, `median_abs_diff`, `median_diff`**: Rata-rata dan median dari selisih atau selisih absolut antar data yang berurutan. Menggambarkan laju perubahan data harian.
  
  $$ Mean\ Diff = \frac{1}{N-1} \sum_{i=1}^{N-1} (x_{i+1} - x_i) $$

* **`mse`**: _Mean Squared Error_, parameter rata-rata kesalahan kuadrat dari sinyal terkait model rata-ratanya.
  
  $$ MSE = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2 $$

  **Contoh Perhitungan Manual MSE (Data NO2):**

  Sebagai ilustrasi perhitungan manual tanpa menggunakan *library* apapun, mari kita ambil data deret waktu dari `NO2_Bangkalan_final.csv`. Terdapat total data sebanyak $N = 365$. Beberapa nilai harian pertamanya adalah:
  
  $$ x_1 = 0.000010716 $$
  $$ x_2 = 0.000010840 $$
  $$ x_3 = 0.000010965 $$
  $$ \dots \text{hingga observasi ke } x_{365} $$

  **Langkah 1: Menghitung Rata-rata ($\mu$)**
  Apabila nilai dari seluruh kolom observasi ditambahkan dan dibagi 365, kita dapatkan nilai rata-ratanya:
  
  $$ \mu = \frac{x_1 + x_2 + x_3 + \dots + x_{365}}{365} $$
  $$ \mu \approx 0.00002782 $$

  **Langkah 2: Menghitung Nilai MSE**
  Masukkan seluruh data observasi ke dalam rumus MSE dengan mengurangi tiap nilai terhadap rata-rata, mengkuadratkannya, lalu mencari nilai rata-ratanya:
  
  $$ MSE = \frac{(x_1 - \mu)^2 + (x_2 - \mu)^2 + \dots + (x_{365} - \mu)^2}{365} $$
  $$ MSE = \frac{(0.000010716 - 0.00002782)^2 + (0.000010840 - 0.00002782)^2 + \dots}{365} $$
  
  Hasil akhir dari perhitungan di atas akan menghasilkan nilai MSE:
  
  $$ MSE \approx 2.0154 \times 10^{-10} $$

* **`negative_turning`, `positive_turning`**: Jumlah titik belok di mana tren data berubah dari naik ke turun (negatif) dan turun ke naik (positif).

* **`neighbourhood_peaks`**: Memonitor titik-titik puncak di suatu lingkup observasi berdekatan.

* **`pk_pk_distance`**: Jarak dari lembah terendah ke puncak tertinggi (_Peak-to-Peak_).
  
  $$ D_{pk-pk} = \max(x) - \min(x) $$

* **`slope`**: Kemiringan tren data linear secara keseluruhan (naik/turun), yang merupakan koefisien $a$ dari regresi linear $x_i = a t_i + b$.

* **`sum_abs_diff`**: Total akumulasi jumlah perbedaan absolut dari satu titik waktu ke waktu berikutnya.
  
  $$ \sum_{i=1}^{N-1} |x_{i+1} - x_i| $$

* **`zero_cross`**: Seberapa sering sinyal menyilang nilai nol (atau memotong garis _baseline_).
  
  $$ \sum_{i=1}^{N-1} \mathbf{1}_{(x_i \cdot x_{i+1} < 0)} $$

### 3. Domain Spectral
Domain spektral memproses deret waktu dengan mentransformasikannya ke dalam ranah frekuensi (menggunakan algoritma spektrum fourier atau dekomposisi wavelet). Fitur pada domain ini sangat bagus untuk menganalisis sifat periodik dan kepadatan osilasi gelombang yang tersembunyi.

* **`fundamental_frequency`**: Frekuensi dasar yang paling menonjol dalam sinyal, menandakan siklus polutan terkuat.
  
  $$ f_0 = \arg\max_f S(f) $$

* **`max_frequency`**: Frekuensi tertinggi yang dicatat pada analisis spektrum.

* **`median_frequency`**: Frekuensi median pembagi tengah total daya pada spektrum sinyal polutan.

* **`human_range_energy`**: Energi sinyal dalam rentang frekuensi tertentu (lebih spesifik untuk pergerakan frekuensi pada rentang manusia).

* **`lpcc`, `mfcc`**: _Linear Prediction Cepstral Coefficients_ dan _Mel-Frequency Cepstral Coefficients_, representasi padat terkait spektrum sinyal yang biasa digunakan dalam pemrosesan suara, berguna memetakan tekstur frekuensi polutan.

* **`max_power_spectrum`**: Nilai daya (energi) tertinggi pada frekuensi dominan dalam seluruh pita spektrum.
  
  $$ \max(S(f)) $$

* **`power_bandwidth`**: Lebar pita frekuensi tempat sebagian besar energi sinyal difokuskan.

* **`spectral_centroid`**: Titik berat frekuensi, mengindikasikan apakah energi spektrum lebih condong ke frekuensi tinggi atau rendah.
  
  $$ C_s = \frac{\sum_{k} f_k S(k)}{\sum_{k} S(k)} $$

* **`spectral_decrease`, `spectral_slope`**: Pengukuran tren seberapa curam/cepat daya spektrum menurun pada frekuensi tinggi.

* **`spectral_distance`**: Ukuran jarak antara profil frekuensi berdekatan (kestabilan spektrum).

* **`spectral_entropy`**: Entropi spektral, seberapa datar atau bervariasi distribusi energi pada keseluruhan pita frekuensi.
  
  $$ H_s = - \sum_{k} P_k \log P_k \quad \text{dimana} \quad P_k = \frac{S(k)}{\sum S(k)} $$

* **`spectral_kurtosis`, `spectral_skewness`**: Parameter bentuk untuk kurva densitas spektrum (menilai kelancipan dan kemiringan pita spektral), analog dengan momen statistik pada distribusi daya spektrum.

* **`spectral_positive_turning`**: Jumlah belokan (titik naik) pada plot kepadatan spektral frekuensi.

* **`spectral_roll_off`, `spectral_roll_on`**: Titik frekuensi di mana presentase mayoritas daya (misal 95%) telah terkonsentrasi; berguna untuk penyaringan sinyal bising/noise.

* **`spectral_spread`, `spectral_variation`**: Penyebaran atau lebar pita variasi spektrum di sekeliling _centroid_, diukur menggunakan ragam (_variance_) spektrum.

* **`spectrogram_mean_coeff`**: Rata-rata tingkat magnitudo atau koefisien yang diambil dari keseluruhan hasil matriks spektrogram waktu-frekuensi.

* **`wavelet_abs_mean`, `wavelet_energy`, `wavelet_entropy`, `wavelet_std`, `wavelet_var`**: Parameter dari hasil Transformasi Wavelet (rata-rata mutlak, energi, entropi, standar deviasi, dan varians koefisien wavelet), berguna untuk mengungkap struktur waktu dan frekuensi secara simultan yang dapat berubah-ubah.
