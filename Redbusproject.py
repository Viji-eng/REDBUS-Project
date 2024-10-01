import streamlit as st
import pymysql
import pandas as pd
#connect to MySql database
def get_connection():
    return pymysql.connect(host='127.0.0.1',user='root',passwd='2910vvvi',database='redbus_data') 

#Function  to Fetch route names starting with a specified letter
def fetch_Route_name(connection,starting_letter):
    query=f"SELECT DISTINCT Route_name FROM bus_route WHERE Route_name LIKE '{starting_letter}%' ORDER BY Route_name"
    Route_name= pd.read_sql(query, connection)['Route_name'].tolist()
    return Route_name
    

#Function to fetch data from Mysql database on slected Route_name and price sort by orde
def fetch_data(connection,Route_name,price_sort_order):
    price_sort_order_sql="ASC" if price_sort_order=="Low to High" else 'DESC'
    query=f"SELECT * FROM bus_route WHERE Route_name=%s ORDER BY Rating DESC, PRICE{price_sort_order_sql}"
    df= pd.read_sql(query,connection,params=(Route_name,))
    return df
   
def filter_data(df,rating,Bus_type):
    filter_df=df[df['Rating'].isin(rating)&df['Bus_type'].isin(Bus_type)]
    return filter_df

#Main Streamlit  App
def main():
   
    st.header('REDBUS ONLINE BUS TICKET BOOKING')

    connection=get_connection()

    try:
        starting_letter=st.sidebar.text_input('Enter starting letter of Route name','A')

        if starting_letter:
            Route_name=fetch_Route_name(connection,starting_letter.upper())
            
            if Route_name:
                selected_route=st.sidebar.radio('Select Route Name',Route_name)

                if selected_route:
                    #sidebar for sorting price
                    price_sort_order=st.sidebar.selectbox('sort by price',['Low to High','High to Low'])

                    
                    data = fetch_data(connection,selected_route,price_sort_order)

                    if not data.empty:
                        st.write(f"### Data for Route:{selected_route}")
                        st.write(data)

                        # Filter by Rating and Bus_type
                        Rating=data['Rating'].unique().tolist()
                        selected_rating=st.multiselect('Filter by Rating',Rating)

                        Bus_type=data['Bus_type'].unique.tolist()
                        selected_Bus_type=st.multiselect('Filter by Bus_type',Bus_type)

                        if selected_rating and selected_Bus_type:
                            filter_data=filter_data(data,selected_rating,selected_Bus_type)
                            #Display filtered data table
                            st.write(f"### Filtered Data for Rating: {selected_rating} and Bus_type:{selected_Bus_type}")
                            st.write(filter_data)

                    else:
                        st.write(f"No data found for route:{selected_route} with the specified price sort order.")
                else:
                    st.write("No route found starting with specified letter.")
    finally:
        connection.close()

if __name__ =='__main__':
    main()        
                    



                                             
                                             
                                
