import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

st.title('Bike Sharing Dashboard')

st.write('Dashboard analisis penyewaan sepeda berdasarkan cuaca dan waktu')
#Ringkasan data umum
st.subheader('Ringkasan Data')

st.markdown('###  Data Harian (day_df)')
col1, col2, col3 = st.columns(3)

col1.metric('Total Penyewaan', int(day_df['cnt'].sum()))
col2.metric('Rata-rata Harian', int(day_df['cnt'].mean()))
col3.metric('Max Harian', int(day_df['cnt'].max()))

st.markdown('Data Per Jam (hour_df)')
col4, col5, col6 = st.columns(3)

col4.metric('Total Penyewaan', int(hour_df['cnt'].sum()))
col5.metric('Rata-rata per Jam', int(hour_df['cnt'].mean()))
col6.metric('Max per Jam', int(hour_df['cnt'].max()))

#Visualisasi Pertanyaan 1
st.subheader('🌦️ Penyewaan Berdasarkan Cuaca data day_df dan hour_df')

col1, col2 = st.columns(2)

weather_map = {
    1: 'Sangat Baik',
    2: 'Baik',
    3: 'Kurang Baik',
    4: 'Buruk'
}

# DAY
day_df['weather_label'] = day_df['weathersit'].map(weather_map)
day_group = day_df.groupby('weather_label')['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(x='weather_label', y='cnt', data=day_group, ax=ax1)
ax1.set_title('Rata-rata Penyewaan (Harian)')
ax1.set_xlabel('Kondisi Cuaca')
ax1.set_ylabel('Rata-rata Penyewaan')

col1.pyplot(fig1)

# HOUR
hour_df['weather_label'] = hour_df['weathersit'].map(weather_map)
hour_group = hour_df.groupby('weather_label')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(x='weather_label', y='cnt', data=hour_group, ax=ax2)
ax2.set_title('Rata-rata Penyewaan (Per Jam)')
ax2.set_xlabel('Kondisi Cuaca')
ax2.set_ylabel('Rata-rata Penyewaan')

col2.pyplot(fig2)


#Visualisasi Pertanyaan 2
st.subheader('⏰ Pola Penyewaan Berdasarkan jam dan kategori waktu')

col3, col4 = st.columns(2)

fig3, ax3 = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=hour_df, ax=ax3)
ax3.set_title('sebaran rata-rata penyewaan sepeda')
ax3.set_xlabel('Jam')
ax3.set_ylabel('rata-rata penyewaan')

col3.pyplot(fig3)


def kategori_waktu(hour):
    if 5 <= hour <= 10:
        return 'Pagi'
    elif 11 <= hour <= 14:
        return 'Siang'
    elif 15 <= hour <= 18:
        return 'Sore'
    else:
        return 'Malam'

hour_df['kategori_waktu'] = hour_df['hr'].apply(kategori_waktu)

kelompok_waktu = hour_df.groupby('kategori_waktu')['cnt'].mean().reset_index()

order = ['Pagi', 'Siang', 'Sore', 'Malam']

fig4, ax4 = plt.subplots()
sns.barplot(x='kategori_waktu', y='cnt', data=kelompok_waktu, order=order, ax=ax4)

ax4.set_xlabel('Kategori Waktu')
ax4.set_ylabel('Rata-rata Penyewaan')

col4.pyplot(fig4)

#Insight
st.markdown('---')
st.write(f"""
 **Insight:**
- Penyewaan tertinggi terjadi pada waktu 17.00
- Semakin baik kondisi cuacanya semakin banyak pula penyewa sepeda
- Penyewaan meningkat pada sore hari (aktivitas pulang kerja ataupun berolahraga)
- Cuaca buruk menurunkan jumlah penyewaan secara signifikan
""")
