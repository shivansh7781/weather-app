import base64
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

API_KEY = "6471d7e31c0f559de42d100975d58c5b"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.title("Real-time Weather App")


sns.set(style="whitegrid")


location = st.text_input("Enter a city name:", "LUCKNOW")


st.subheader("Live Weather Map")


def update_map():
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        
        st.subheader(f"Weather in {location}")
        st.write(f"Temperature: {data['main']['temp']}°C")
        st.write(f"Description: {data['weather'][0]['description']}")
        st.write(f"Humidity: {data['main']['humidity']}%")
        st.write(f"Pressure: {data['main']['pressure']} hPa")

        
        fig = go.Figure()
        fig.add_trace(go.Scattergeo(
            lon=[data['coord']['lon']],
            lat=[data['coord']['lat']],
            mode='markers+text',
            marker={'size': 20, 'color': 'red'},
            text=[data['weather'][0]['main']],
            hoverinfo='text'
        ))

        fig.update_geos(
            resolution=50,
            showland=True,
            landcolor="lightgray",
            showcoastlines=True,
            coastlinecolor="black",
            projection_type="mercator"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("City not found. Please check the name and try again.")


if st.button("Get Weather"):
    with st.spinner("Fetching weather data..."):
        update_map()
 