import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_rfm_hourly_df(df):
    rfm_season_df = df.groupby(by="season", as_index=False).agg({
        "dteday" : "max",
        "id" : "nunique",
        "count" : "sum"
    })

    rfm_season_df.columns =['season','max_date','frequency','monetary']
    type_mappings = {1 : 'Semi', 2 : 'Panas', 3 : 'Gugur', 4 : 'Dingin'}
    rfm_season_df['season'] = rfm_season_df['season'].map(type_mappings)
    
    rfm_season_df['max_date'] = pd.to_datetime(rfm_season_df['max_date']).dt.date
    last_date = pd.to_datetime(hours_cleaned_df['dteday']).dt.date.max()
    rfm_season_df['recency'] = rfm_season_df['max_date'].apply(lambda x: (last_date - x).days)
 
    rfm_season_df.drop("max_date", axis=1, inplace=True)
    return rfm_season_df


# Order data by dteday and convert dteday to datetime
col_date = 'dteday'
hours_cleaned_df = pd.read_csv('hours_cleaned.csv')
hours_cleaned_df.sort_values(by=col_date, inplace=True)
hours_cleaned_df.reset_index(inplace=True)

hours_cleaned_df[col_date] = pd.to_datetime(hours_cleaned_df[col_date])

# Create filter component
min_date = hours_cleaned_df[col_date].min()
max_date = hours_cleaned_df[col_date].max()
 



with st.sidebar:
    # Add logo
    st.image("https://cdn.vectorstock.com/i/1000x1000/25/95/bicycle-bike-logo-vector-22962595.webp")
    
    # Get start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value= max_date,
        value= [min_date, max_date]
    )

# filter df by date and load df
ranged_df = hours_cleaned_df[(hours_cleaned_df[col_date] >= str(start_date)) & 
                (hours_cleaned_df[col_date] <= str(end_date))]

rfm_hourly_df = create_rfm_hourly_df(ranged_df)

# dasboard main section
st.header('Dashboard Pesepeda Ceria 2011 :chart_with_upwards_trend:')
st.subheader('Rekap Tahun 2011')

col1, col2 = st.columns(2)

with col1:
    total_rentals_in21011 = hours_cleaned_df['count'].sum()
    st.metric("Total Peminjam di 2011", total_rentals_in21011)

with col2:
    total_rentas_ranged = ranged_df['count'].sum()
    st.metric("Total Peminjam filtered", total_rentas_ranged)

# Distribution section
st.subheader('Distribusi Jumlah Peminjam Sepeda')
fig, ax = plt.subplots(figsize=(12,5))
sns.pointplot(data=hours_cleaned_df, x='hour', y='count', hue='season',palette='Set1', ax=ax)

ax.set(
    title='Jumlah Peminjam Sepeda Berdasarkan Musim di Tahun 2011', 
    xlabel='Jam Peminjaman',
    ylabel='Total Peminjam')

season_handles = ax.get_legend_handles_labels()[0]
ax.legend(season_handles, ['Semi','Panas','Gugur','Dingin'],title='Musim')
st.pyplot(fig)

# Section Hourly Total Rental
st.subheader('Distribusi Jumlah Data berdasarkan Jam')
fig, ax = plt.subplots(figsize=(11,5))
sns.pointplot(data=hours_cleaned_df, x='hour', y='count', ax=ax)
ax.set(title='Jumlah Peminjam Sepeda Tiap Jamnya di Tahun 2011',
       xlabel='Jam Peminjaman',
       ylabel='Total Peminjam')
st.pyplot(fig)

# rfm section
st.subheader('Musim terbaik menggunakan RFM Analisis berasarkan parameter musim')
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_hourly_df.recency.mean(), 1)
    st.metric("Rata-Rata Kebaruan (hari)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_hourly_df.frequency.mean(), 2)
    st.metric("Rata-Rata Frekuensi", value=avg_frequency)
 
with col3:
    avg_monetary = round(rfm_hourly_df.monetary.mean(), 2)
    st.metric("Rata-Rata Total Peminjam", value=avg_monetary)


fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
 
sns.barplot(y="recency", x="season", data=rfm_hourly_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('Musim')
ax[0].set_title("Berdasarkan Kebaruan (Hari)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)
 
sns.barplot(y="frequency", x="season", data=rfm_hourly_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('Musim')
ax[1].set_title("Berdasarkan Frekuensi", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
 
sns.barplot(y="monetary", x="season", data=rfm_hourly_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel('Musim')
ax[2].set_title("Berdasrkan Total Peminjam", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
 
#plt.suptitle("Musim Terbaik berasarkan RFM Parameters (season)", fontsize=20)
#plt.show()

st.pyplot(fig)

st.caption('Copyright (c) Pesepeda Santai 2023')
