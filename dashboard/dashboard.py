import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.patches import Patch

# Mengatur style Seaborn
sns.set(style='darkgrid')

# Tittle dashboard
st.header('Bike-Sharing Dashboard')

# Memuat Data
df = pd.read_csv("dashboard/day_clean.csv")

# Mengubah tipe data kolom date
df['date'] = pd.to_datetime(df['date'])
df['weekday'] = df['date'].dt.day_name()

# Sidebar untuk logo dan filter date
with st.sidebar:
    st.image("dashboard/bike.jpg", use_column_width=True) 
    st.header('Filter Data')
    
    min_date = df['date'].min()
    max_date = df['date'].max()
    start_date, end_date = st.date_input(
        'Select date range:',
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter dataframe berdasarkan date range
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Analisis 1: Total rental sepeda berdasarkan musim
sum_season = filtered_df.groupby("season")["total_user"].sum().sort_values(ascending=False).reset_index()

st.subheader('Total Penyewaan Sepeda Berdasarkan Musim')
st.dataframe(sum_season, use_container_width=True) 

fig, ax = plt.subplots(figsize=(12, 6))  
sns.barplot(x="season", y="total_user", data=sum_season, color="#71797E", ax=ax)
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_xlabel("Musim")
ax.set_title("Total Penyewaan Sepeda Berdasarkan Musim", fontsize=20)
st.pyplot(fig)

# Analisis 2: Total rental sepeda paling berdasarkan hari
sum_day = filtered_df.groupby("weekday")["total_user"].sum().reset_index()

# Urutan hari 
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sum_day['weekday'] = pd.Categorical(sum_day['weekday'], categories=order, ordered=True)
sum_day = sum_day.sort_values('weekday')

st.subheader('Total Penyewaan Sepeda Berdasarkan Hari')
st.dataframe(sum_day, use_container_width=True)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="weekday", y="total_user", data=sum_day, color="#A9A9A9", ax=ax, order=order)
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_xlabel("Hari")
ax.set_title("Total Penyewaan Sepeda Berdasarkan Hari", fontsize=20)
st.pyplot(fig)

# Analysis Lanjutan Clustering : Pelanggan Kasual & Terdaftar berdasarkan musim
seasonal_grouping = filtered_df.groupby("season")[["casual_user", "registered_user"]].sum().reset_index()

seasonal_grouping.rename(columns={"casual_user": "Casual", "registered_user": "Registered"}, inplace=True)

seasonal_melted = seasonal_grouping.melt(id_vars="season", value_vars=["Casual", "Registered"],
                                        var_name="Tipe Pengguna", value_name="Jumlah Penyewaan")

st.subheader('Total Penyewaan Sepeda Berdasarkan Musim dan Tipe Pelanggan')
st.dataframe(seasonal_grouping, use_container_width=True)

fig, ax = plt.subplots(figsize=(10, 6))
colors = {"Casual": "#A9A9A9", "Registered": "#71797E"}
sns.barplot(
    data=seasonal_melted,
    y="season", x="Jumlah Penyewaan", hue="Tipe Pengguna",
    palette=[colors["Casual"], colors["Registered"]],
    ax=ax
)
ax.set_xlabel("Total Penyewaan")
ax.set_ylabel("Musim")
ax.set_title("Total Penyewaan Sepeda Berdasarkan Musim untuk Pelanggan Casual dan Registered", fontsize=20)
legend_labels = [Patch(color=colors["Casual"], label="Casual"),
                 Patch(color=colors["Registered"], label="Registered")]
ax.legend(handles=legend_labels, title="Tipe Pelanggan")
ax.grid(axis="x", linestyle="--", alpha=0.7)
st.pyplot(fig)


# Tambahkan di bawah seluruh visualisasi atau di akhir halaman Streamlit

st.markdown("### Kesimpulan:")
st.markdown("""
1. Musim dengan penyewaan terbanyak terjadi pada musim Gugur, diikuti oleh musim Panas dan Dingin. Sedangkan penyewaan terendah tercatat pada musim Semi. Hal ini menunjukkan bahwa faktor musim berpengaruh signifikan terhadap minat pelanggan dalam menyewa sepeda.

2. Hari dengan penyewaan terbanyak pada hari Jumat, diikuti oleh Kamis dan Sabtu. Sementara itu, hari Minggu memiliki tingkat penyewaan paling rendah. Pola ini mengindikasikan bahwa layanan bike-sharing lebih diminati pada hari kerja menjelang akhir pekan dibandingkan hari libur.

3. Clustering berdasarkan tipe pelanggan dan musim:
  * Pelanggan tetap (registered) menunjukkan pola penggunaan yang stabil di sepanjang musim, dengan dominasi jumlah penyewaan dibandingkan pelanggan casual.
  * Pelanggan tidak terdaftar (casual) cenderung lebih terpengaruh oleh musim, dengan peningkatan signifikan pada musim Panas, kemungkinan besar disebabkan oleh cuaca yang mendukung aktivitas luar ruangan.
  * Musim Gugur dan Panas merupakan periode dengan penyewaan tertinggi untuk kedua tipe pelanggan.
""")

st.markdown("### Saran:")
st.markdown("""
1. **Strategi Promosi Musiman**  
  Untuk meningkatkan penyewaan di musim dengan jumlah peminjaman rendah seperti musim Panas dan musim Dingin, perusahaan dapat menerapkan program diskon atau event khusus yang menarik bagi pelanggan, terutama untuk pelanggan casual yang sensitif terhadap kondisi musim.

2. **Target Marketing untuk Pelanggan Casual**  
  Karena pelanggan casual lebih dipengaruhi oleh musim, perusahaan dapat membuat iklan yang fokus pada kenyamanan dan keamanan bersepeda di semua musim. Misalnya, menyediakan perlengkapan tambahan seperti jaket atau panduan rute aman saat musim dingin.

3. **Meningkatkan Kepercayaan Pelanggan Registered**  
  Mengingat pelanggan tetap sudah menunjukkan pola penggunaan yang stabil, perusahaan bisa memberikan reward seperti poin yang dapat ditukar dengan gratis sewa atau merchandise untuk mempertahankan loyalitas mereka.
""")


# Footer
st.caption('Copyright © Rahma Aulia')
