import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# Database connection using SQLAlchemy
# Replace 'username', 'password', 'host', 'port', and 'database' with your actual credentials
engine = create_engine('mysql+pymysql://root:2910vvvi@127.0.0.1:3306/Redbus_data')

# Fetch data from the database
query = "SELECT * FROM bus_route"
data = pd.read_sql(query, engine)

# Streamlit app layout
st.title('Redbus Routes Data Filtering and Analysis')

# Display images
st.image(r"C:\Users\Admin\Desktop\redbus-logo-5B2A75C4DA-seeklogo.com.png", use_column_width=True)

# Filters
busname_filter = st.multiselect('Select Bus_name:', options=data['Bus_name'].unique())
bustype_filter=st.multiselect('Select Bus_type:',options=data['Bus_type'].unique())
routename_filter = st.multiselect ('Select Routename:', options=data['Route_name'].unique())
price_filter = st.slider('Select Price Range:', min_value=int(data['Price'].min()), max_value=int(data['Price'].max()), value=(int(data['Price'].min()), int(data['Price'].max())))
Rating_filter = st.slider('Select Rating Range:', min_value=float(data['Rating'].min()), max_value=float(data['Rating'].max()), value=(float(data['Rating'].min()), float(data['Rating'].max())))
availability_filter = st.slider('Select Seat Available Range:', min_value=int(data['Seats_Available'].min()), max_value=int(data['Seats_Available'].max()), value=(int(data['Seats_Available'].min()), int(data['Seats_Available'].max())))

# Filter data based on user inputs
filtered_data = data

if busname_filter:
    filtered_data = filtered_data[filtered_data['Bus_name'].isin(busname_filter)]

if bustype_filter:
    filtered_data= filtered_data[filtered_data['Bus_type'].isin(bustype_filter)] 



if routename_filter:
    filtered_data = filtered_data[filtered_data['Route_name'].isin(routename_filter)]

filtered_data = filtered_data[(filtered_data['Price'] >= price_filter[0]) & (filtered_data['Price'] <= price_filter[1])]
filtered_data = filtered_data[(filtered_data['Rating'] >= Rating_filter[0]) & (filtered_data['Rating'] <= Rating_filter[1])]
filtered_data = filtered_data[(filtered_data['Seats_Available'] >= availability_filter[0]) & (filtered_data['Seats_Available'] <= availability_filter[1])]

# Display filtered data
st.write('Filtered Data:')
st.dataframe(filtered_data)

# Add a download button to export the filtered data
if not filtered_data.empty:
    st.download_button(
        label="Download Filtered Data",
        data=filtered_data.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.warning("No data available with the selected filters.")
