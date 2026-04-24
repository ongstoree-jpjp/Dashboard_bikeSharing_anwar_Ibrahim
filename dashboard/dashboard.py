import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Load data
day_df = pd.read_csv('Data/day.csv')

#layout halaman
st.set_page_config(layout="wide")
st.title("BIKE SHARING DASHBOARD")

#Sidebar filter
st.sidebar.header(" Filter Data")

# pilihan tahun
year_map = {0: 2011, 1: 2012}
year_options = list(year_map.values())

selected_year_labels = st.sidebar.multiselect(
    "Pilih Tahun",
    options=year_options,
    default=year_options
)

# Mapping balik ke kode asli (0 / 1)
selected_year = [
    k for k, v in year_map.items() if v in selected_year_labels
]

# FILTER CUACA
weather_map = {
    1: "Cerah",
    2: "Mendung",
    3: "Hujan Ringan"
}

weather_options = list(weather_map.values())

selected_weather_labels = st.sidebar.multiselect(
    "Pilih Cuaca",
    options=weather_options,
    default=weather_options
)

# Mapping balik ke angka
selected_weather = [
    k for k, v in weather_map.items() if v in selected_weather_labels
]

#Validasi filter
if not selected_year:
    st.warning("Silakan pilih minimal satu tahun")
    st.stop()

if not selected_weather:
    st.warning("Silakan pilih minimal satu kondisi cuaca")
    st.stop()

#filtering data
filtered_df = day_df[
    (day_df["yr"].isin(selected_year)) &
    (day_df["weathersit"].isin(selected_weather))
].copy()

filtered_df["weather_label"] = filtered_df["weathersit"].map(weather_map)

#Ringkasan data
st.markdown("---")
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(filtered_df["cnt"].sum()))
col2.metric("Rata-rata Harian", int(filtered_df["cnt"].mean()))
col3.metric("Max Harian", int(filtered_df["cnt"].max()))

#Visualisasi 1
st.markdown("---")
st.subheader("Perbandingan Working Day vs Holiday")

workingday_map = {
    0: "Hari Libur",
    1: "hari Kerja"
}

filtered_df["day_type"] = filtered_df["workingday"].map(workingday_map)

group_day = (
    filtered_df.groupby("day_type")["cnt"]
    .mean()
    .reset_index()
)

sns.set_style("whitegrid")

fig1, ax1 = plt.subplots()
sns.barplot(data=group_day, x="day_type", y="cnt", ax=ax1)
ax1.set_xlabel("Tipe Hari")
ax1.set_ylabel("Rata-rata Penyewaan Sepeda")
ax1.set_title("Rata-rata Penyewaan: Working Day vs Holiday")

st.pyplot(fig1)

#Visualisasi 2
st.markdown("---")
st.subheader("Pengaruh Cuaca terhadap Penyewaan")

group_weather = (
    filtered_df.groupby("weather_label")["cnt"]
    .mean()
    .reset_index()
)

fig2, ax2 = plt.subplots()
sns.barplot(data=group_weather, x="weather_label", y="cnt", ax=ax2)
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan Sepeda")
ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")

st.pyplot(fig2)

#insight
st.markdown("---")
st.subheader("Insight")

st.write("""
- rata-rata jumlah penyewaan sepeda pada hari kerja sedikit lebih tinggi dibandingkan hari libur selama periode 2011–2012. Namun, perbedaan tersebut tidak terlalu signifikan. Hal ini menunjukkan bahwa sepeda tidak hanya digunakan untuk aktivitas commuting pada hari kerja, tetapi juga cukup banyak digunakan untuk aktivitas rekreasi pada hari libur. Oleh karena itu penyedia harus tetap mempertahankan kesediaan sepeda baik di hari kerja maupun hari libur.
- Berdasarkan analisis kondisi cuaca, jumlah penyewaan sepeda tertinggi terjadi pada kondisi cuaca cerah dan menurun pada kondisi mendung serta hujan ringan. Hal ini menunjukkan bahwa cuaca memiliki pengaruh signifikan terhadap minat pengguna dalam menyewa sepeda. Dari analisis ini , penyedia dapat menyesuaikan strategi operasional dengan menambah jumlah sepeda saat cuaca cerah serta memberikan promo ketika kondisi cuaca kurang baik untuk meningkatkan jumlah penyewa ketika cuaca kurang baik
- Gunakan filter untuk eksplorasi lebih dalam
""")
