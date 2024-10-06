import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe


def create_casual_df(df):
    
	casual_df = df[['dteday', 'casual']]   
	return casual_df

def create_registered_df(df):
    
	registered_df = df[['dteday', 'registered']]   
	return registered_df

def create_cnt_df(df):
    
	cnt_df = df[['dteday', 'cnt']]    
	return cnt_df

def create_casualhour_df(df):
    
	casualhour_df = df[['dteday', 'hr', 'casual']]
	return casualhour_df

def create_registeredhour_df(df):
    
	registeredhour_df = df[['dteday', 'hr', 'registered']]
	return registeredhour_df

def create_cnthour_df(df):
    
	cnthour_df = df[['dteday', 'hr', 'cnt']]    
	return cnthour_df

def create_temp_df(df):
	temp_df = df[['temp', 'casual', 'registered', 'cnt']]
	return temp_df


# Load cleaned data
day1_df = Path(__file__).parents[1]/"dashboard/day1.csv"
hour1_df = Path(__file__).parents[1]/'dashboard/hour1.csv'

day1_df = pd.read_csv(day1_df)
hour1_df = pd.read_csv(hour1_df)

day1_df['dteday'] = pd.to_datetime(day1_df['dteday'], format='%Y-%m-%d', errors='coerce')
hour1_df['dteday'] = pd.to_datetime(hour1_df['dteday'], format='%Y-%m-%d', errors='coerce')

# Filter data
min_date = day1_df["dteday"].min()
max_date = day1_df["dteday"].max()

with st.sidebar:
	st.image("https://img.freepik.com/premium-vector/bike-sharing-rental-service-logo-icon-with-bicycle_116137-6024.jpg")
    # Mengambil start_date & end_date dari date_input
    
	start_date, end_date = st.date_input(
        
		label='Rentang Waktu',min_value=min_date,
        
		max_value=max_date,
        
		value=[min_date, max_date]
    
	)

main_df = day1_df[(day1_df["dteday"] >= str(start_date)) & 
                (day1_df["dteday"] <= str(end_date))]

mainhour_df = hour1_df[(hour1_df["dteday"] >= str(start_date)) & 
                (hour1_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
casual_df = create_casual_df(main_df)
registered_df = create_registered_df(main_df)
cnt_df = create_cnt_df(main_df)

casualhour_df = create_casualhour_df(mainhour_df)
registeredhour_df = create_registeredhour_df(mainhour_df)
cnthour_df = create_cnthour_df(mainhour_df)

temp_df = create_temp_df(main_df)


# plot number of daily users
st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Daily Users')

col1, col2, col3 = st.columns(3)

with col1:
    total_casual = casual_df.casual.sum()
    st.metric("Total Casual", value=total_casual)

with col2:
    total_registered = registered_df.registered.sum()
    st.metric("Total Registered", value=total_registered)

with col3:
    total_cnt = cnt_df.cnt.sum()
    st.metric("Total Count", value=total_cnt)

fig1, ax1 = plt.subplots(figsize=(16, 8))
ax1.plot(
    casual_df["dteday"],
    casual_df["casual"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax1.tick_params(axis='y', labelsize=20)
ax1.tick_params(axis='x', labelsize=15)

ax1.set_title("Casual Users Over Time", fontsize=20)
ax1.set_xlabel("Date", fontsize=15)
ax1.set_ylabel("Casual Users", fontsize=15)



fig2, ax2 = plt.subplots(figsize=(16, 8))
ax2.plot(
    registered_df["dteday"],
    registered_df["registered"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax2.tick_params(axis='y', labelsize=20)
ax2.tick_params(axis='x', labelsize=15)

ax2.set_title("Registered Users Over Time", fontsize=20)
ax2.set_xlabel("Date", fontsize=15)
ax2.set_ylabel("Registered Users", fontsize=15)



fig3, ax3 = plt.subplots(figsize=(16, 8))
ax3.plot(
    cnt_df["dteday"],
    cnt_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax3.tick_params(axis='y', labelsize=20)
ax3.tick_params(axis='x', labelsize=15)

ax3.set_title("Total Users Over Time", fontsize=20)
ax3.set_xlabel("Date", fontsize=15)
ax3.set_ylabel("Total Users", fontsize=15)

max_ylim = max(ax1.get_ylim()[1], ax2.get_ylim()[1], ax3.get_ylim()[1])

ax1.set_ylim(top=max_ylim)
ax2.set_ylim(top=max_ylim)
ax3.set_ylim(top=max_ylim)

st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)

# Average users
st.subheader("Rata-Rata User Setiap Jam")



fig, axes = plt.subplots(1, 3, figsize=(20, 6))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='hr' , y='casual', data=casualhour_df, ax=axes[0])
axes[0].set_title('Average Casual Users per Hour')
axes[0].set_xlabel('Hour')
axes[0].set_ylabel('Average Casual Users')

sns.barplot(x='hr', y='registered', data=registeredhour_df, ax=axes[1])
axes[1].set_title('Average Registered Users per Hour')
axes[1].set_xlabel('Hour')
axes[1].set_ylabel('Average Registered Users')

sns.barplot(x='hr', y='cnt', data=cnthour_df, ax=axes[2])
axes[2].set_title('Average Total Users per Hour')
axes[2].set_xlabel('Hour')
axes[2].set_ylabel('Average Total Users')

max_ylim = max(ax.get_ylim()[1] for ax in axes)
for ax in axes:
  ax.set_ylim(top=max_ylim)

st.pyplot(fig)

# Temperature
st.subheader("Pengaruh Suhu Terhadap Jumlah Users")

temp_df['temp_bins'] = pd.cut(temp_df['temp'], bins=10)

temp_casual = temp_df.groupby('temp_bins')['casual'].sum()
temp_registered = temp_df.groupby('temp_bins')['registered'].sum()
temp_cnt = temp_df.groupby('temp_bins')['cnt'].sum()

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

axes[0].plot(temp_casual.index.astype(str), temp_casual.values)
axes[0].set_title('Temperature vs Sum of Casual Users')
axes[0].set_xlabel('Temperature Bins')
axes[0].set_ylabel('Sum of Casual Users')
axes[0].tick_params(axis='x', rotation=45)

axes[1].plot(temp_registered.index.astype(str), temp_registered.values)
axes[1].set_title('Temperature vs Sum of Registered Users')
axes[1].set_xlabel('Temperature Bins')
axes[1].set_ylabel('Sum of Registered Users')
axes[1].tick_params(axis='x', rotation=45)

axes[2].plot(temp_cnt.index.astype(str), temp_cnt.values)
axes[2].set_title('Temperature vs Sum of Total Users')
axes[2].set_xlabel('Temperature Bins')
axes[2].set_ylabel('Sum of Total Users')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
max_ylim = max(ax.get_ylim()[1] for ax in axes)
for ax in axes:
  ax.set_ylim(top=max_ylim)

st.pyplot(fig)

st.caption('By Christoforus Stanislaus')
