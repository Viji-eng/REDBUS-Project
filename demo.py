import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from datetime import time


# Database connection using SQLAlchemy
# Replace 'username', 'password', 'host', 'port', and 'database' with your actual credentials
engine = create_engine('mysql+pymysql://root:2510vihaan@127.0.0.1:3306/Redbus')

# Fetch data from the database
query = "SELECT * FROM bus_route"
data = pd.read_sql(query, engine)

# Streamlit app layout
st.title('Redbus Routes Data Filtering and Analysis')
# Display images
st.image(r"C:\Users\Admin\Desktop\redbusbooking.in_logo12.jpg", use_column_width=True)
# Bus service names with full forms
bus_services = [
    
    
    'KSRTC - Kerala State Road Transport Corporation',
    'APSRTC - Andhra Pradesh State Road Transport Corporation',
    'TSRTC - Telangana State Road Transport Corporation',
    'KTCL - Kadamba Transport Corporation Limited',
    'RSRTC - Rajasthan State Road Transport Corporation',
    'SBSTC - South Bengal State Transport Corporation',
    'HRTC - Haryana Road Transport Corporation',
    'ASTC - Assam State Transport Corporation',
    'UPSRTC - Uttar Pradesh State Road Transport Corporation'
    'WBSTC - West Bengal State Transport Corporation',
    
]
# Extract short names for identification
service_identifiers = [service.split(' - ')[0] for service in bus_services]
# Step 1: Select Bus Service
with st.form("bus_service_form"):
    selected_service = st.selectbox('Select Bus Service', bus_services)
    service_code = selected_service.split(' - ')[0]
    submitted_service = st.form_submit_button("Submit")

st.sidebar.markdown("#### BUS TYPES")
bus_type_seater = st.sidebar.checkbox("SEATER", key="bus_type_seater")
bus_type_sleeper = st.sidebar.checkbox("SLEEPER", key="bus_type_sleeper")
bus_type_ac = st.sidebar.checkbox("AC", key="bus_type_ac")
bus_type_nonac = st.sidebar.checkbox("NON AC", key="bus_type_nonac")
    
# Start time 
Start_time = st.sidebar.selectbox("Start_time", ("Any Time", "Before 6AM", "6AM to 12PM", "12PM to 6PM", "After 6PM"))
#End time
End_time = st.sidebar.selectbox("End_time", ( "Any Time", "Before 6AM", "6AM to 12PM", "12PM to 6PM", "After 6PM"))


# Filters
routename_filter = st.multiselect ('Select Routename:', options=data['Route_name'].unique())
price_filter = st.slider('Select Price Range:', min_value=int(data['Price'].min()), max_value=int(data['Price'].max()), value=(int(data['Price'].min()), int(data['Price'].max())))
Rating_filter = st.slider('Select Rating Range:', min_value=float(data['Rating'].min()), max_value=float(data['Rating'].max()), value=(float(data['Rating'].min()), float(data['Rating'].max())))
availability_filter = st.slider('Select Seat Available Range:', min_value=int(data['Seats_Available'].min()), max_value=int(data['Seats_Available'].max()), value=(int(data['Seats_Available'].min()), int(data['Seats_Available'].max())))

# Filter data based on user inputs
filtered_data = data
if selected_service:
    st.session_state['selected_service'] = selected_service
if routename_filter:
    filtered_data = filtered_data[filtered_data['Route_name'].isin(routename_filter)]
# Filter by bus type
if bus_type_seater:
    filtered_data = filtered_data[filtered_data["Bus_type"].str.contains(r'\bSEATER\b', case=False, regex=True)]
if bus_type_sleeper:
    filtered_data = filtered_data[filtered_data["Bus_type"].str.contains(r'\bSLEEPER\b', case=False, regex=True)]
if bus_type_ac:
    filtered_data = filtered_data[filtered_data["Bus_type"].str.contains(r'\bA[./]?C\b', case=False, regex=True) & 
                                  ~filtered_data["Bus_type"].str.contains(r'\bNON\b', case=False, regex=True)]
if bus_type_nonac:
    filtered_data = filtered_data[filtered_data["Bus_type"].str.contains(r'\bNON AC\b', case=False, regex=True)]    
        
if price_filter:
 filtered_data = filtered_data[(filtered_data['Price']>=price_filter[0])&(filtered_data['Price']<=price_filter[1])]
if Rating_filter: 
 filterd_data =  filtered_data[(filtered_data['Rating']>= Rating_filter[0])&(filtered_data['Rating']<= Rating_filter[1])]
if availability_filter: 
 filterd_data = filtered_data[(filterd_data['Seats_Available']>=availability_filter[0])&(filtered_data['Seats_Available']<=availability_filter[1])]  
 
if Start_time =="Before 6AM":
    dep_st_tm = time(0,0,0)
    dep_end_tm = time(6,0,0)
elif Start_time =="6AM to 12PM":
    dep_st_tm = time(6,0,1)
    dep_end_tm = time(12,0,0)
elif Start_time =="12PM to 6PM":
    dep_st_tm = time(12,0,1)
    dep_end_tm = time(18,0,0)
elif Start_time =="After 6PM":
    dep_st_tm = time(18,0,1)
    dep_end_tm = time(23,59,59)
else:
    dep_st_tm = time(0,0,0)
    dep_end_tm = time(23,59,59) 
    
if End_time =="Before 6AM":
    ari_st_tm = time(0,0,0)
    ari_end_tm = time(6,0,0)
elif End_time =="6AM to 12PM":
    ari_st_tm = time(6,0,1)
    ari_end_tm = time(12,0,0)
elif End_time =="12PM to 6PM":
    ari_st_tm = time(12,0,1)
    ari_end_tm = time(18,0,0)
elif End_time =="After 6PM":
    ari_st_tm = time(18,0,1)
    ari_end_tm = time(23,59,59)
else:
    ari_st_tm = time(0,0,0)
    ari_end_tm = time(23,59,59)    
    
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