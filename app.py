import streamlit as st
import requests
from datetime import datetime
import pandas as pd

'''
# 🚖 TaxiFareModel Front
'''

st.markdown('''
Enter your trip details to get the predicted taxi fare...
''')

'''
## 📝 Enter Trip Details
'''

# 1. Input controls for data entry
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Pickup Location")
    pickup_longitude = st.number_input(
        "Longitude (Pickup Longitude)",
        value=-73.950655,
        format="%.6f"
    )
    pickup_latitude = st.number_input(
        "Latitude (Pickup Latitude)",
        value=40.783282,
        format="%.6f"
    )

with col2:
    st.subheader("📍 Dropoff Location")
    dropoff_longitude = st.number_input(
        "Longitude (Dropoff Longitude)",
        value=-73.984365,
        format="%.6f"
    )
    dropoff_latitude = st.number_input(
        "Latitude (Dropoff Latitude)",
        value=40.769802,
        format="%.6f"
    )

# Date, time and passenger count
col3, col4 = st.columns(2)

with col3:
    pickup_date = st.date_input("📅 Pickup Date", datetime(2014, 7, 6))
    pickup_time = st.time_input("⏰ Pickup Time", datetime(2014, 7, 6, 19, 18))

with col4:
    passenger_count = st.number_input(
        "👥 Passenger Count",
        min_value=1,
        max_value=8,
        value=2
    )

# Combine date and time
pickup_datetime = f"{pickup_date} {pickup_time.strftime('%H:%M:%S')}"

'''
## 🚀 Get Predicted Fare
'''

# 2. Build data to send to API
params = {
    'pickup_datetime': pickup_datetime,
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': passenger_count
}

# 🔄 Test multiple API URLs
api_urls = [
    'https://taxifare.lewagon.ai/predict',  # Ready API
    'http://localhost:8081/predict',        # Local API
    'http://localhost:8080/predict'         # Alternative local API
]

url = None
for api_url in api_urls:
    try:
        test_response = requests.get(api_url, params=params, timeout=2)
        if test_response.status_code == 200:
            url = api_url
            st.success(f"✅ Connected to: {api_url}")
            break
    except:
        continue

if url is None:
    st.error("❌ Cannot connect to any API server")
    st.info("💡 Try running the API locally or use the ready link")
else:
    if st.button("💰 Calculate Fare"):
        st.write("📞 Connecting to server...")

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                prediction = response.json()
                fare = prediction.get("fare")

                if fare is not None:
                    st.success(f"💵 Predicted Fare: **${fare:.2f}**")

                    # Display additional information
                    col5, col6 = st.columns(2)
                    with col5:
                        st.metric("💰 Fare", f"${fare:.2f}")
                    with col6:
                        # Calculate approximate distance
                        distance = ((dropoff_latitude - pickup_latitude)**2 +
                                  (dropoff_longitude - pickup_longitude)**2)**0.5 * 111
                        st.metric("📏 Approximate Distance", f"{distance:.2f} km")

                    # Display additional details
                    with st.expander("📋 View Response Details"):
                        st.json(prediction)

                    # Display entered data
                    with st.expander("📝 Trip Input Data"):
                        st.write(f"**📅 Date & Time:** {pickup_datetime}")
                        st.write(f"**📍 Pickup:** {pickup_latitude:.4f}, {pickup_longitude:.4f}")
                        st.write(f"**📍 Dropoff:** {dropoff_latitude:.4f}, {dropoff_longitude:.4f}")
                        st.write(f"**👥 Passengers:** {passenger_count}")

                else:
                    st.error("❌ Fare value not found in server response")

            else:
                st.error(f"❌ API request failed. Status code: {response.status_code}")
                st.info("💡 Server might be unavailable or link incorrect")

        except requests.exceptions.Timeout:
            st.error("⏰ Connection timeout to server")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to server")
            st.info("💡 Make sure the API is running at: " + url)
        except Exception as e:
            st.error(f"🚨 Unexpected error: {e}")

'''
## 🗺️ Location Map
'''

# Show locations on map
if st.checkbox('🗺️ Show Map'):
    # Create DataFrame for map
    map_data = pd.DataFrame({
        'lat': [pickup_latitude, dropoff_latitude],
        'lon': [pickup_longitude, dropoff_longitude],
        'location': ['Pickup', 'Dropoff']
    })

    st.map(map_data)

    # Display precise coordinates
    st.markdown("### 📍 Precise Coordinates:")
    col7, col8 = st.columns(2)

    with col7:
        st.info(f"**Pickup Location:**\n- Latitude: {pickup_latitude:.6f}\n- Longitude: {pickup_longitude:.6f}")

    with col8:
        st.info(f"**Dropoff Location:**\n- Latitude: {dropoff_latitude:.6f}\n- Longitude: {dropoff_longitude:.6f}")

'''
## ℹ️ Usage Information
'''

st.markdown('''
### 💡 Tips:
- **Default coordinates** are for locations in New York (from Times Square to Central Park)
- **You can modify any value** to get a different price
- **Approximate distance** is calculated for comparison only

### 🎯 Coordinate Examples:
- **🏙️ Manhattan:** -73.9662, 40.7831
- **✈️ JFK Airport:** -73.7781, 40.6413
- **🗽 Statue of Liberty:** -74.0445, 40.6892

### 🔗 Useful Links:
- [📚 Streamlit Documentation](https://docs.streamlit.io)
- [🚖 TaxiFare API](https://taxifare.lewagon.ai)
''')

# Add footer
st.markdown("---")
st.caption("🚀 Developed with Streamlit and FastAPI")