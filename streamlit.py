import streamlit as st
import pandas as pd
import mysql.connector

# Function to fetch distinct route names from MySQL
def get_route_names():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Knkjs@29",
        database="redbus",
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT route_name FROM redbus")  # Assuming 'route_name' is the column name
    names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return names

# Function to fetch data from MySQL based on filters
def fetch_data(bus_type=None, route_name=None, price_min=None, price_max=None, rating=None, seats_available=None):
    try:
        # Connect to your MySQL database
        db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Knkjs@29",
            database="redbus",
            auth_plugin='mysql_native_password'
        )

        # Define the SQL query
        query = "SELECT ID, busname, bustype, route_name, route_link, departing_time, duration, reaching_time, price, rating, seats_available FROM redbus WHERE 1=1"
        params = []

        # Apply filters based on user inputs
        if bus_type:
            if bus_type.lower() == 'ac':
                query += " AND bustype LIKE %s"
                params.append('%A/C%')
            elif bus_type.lower() == 'nonac':
                query += " AND bustype LIKE %s"
                params.append('%NON A/C%')
            elif bus_type.lower() == 'sleeper':
                query += " AND bustype LIKE %s"
                params.append('%Sleeper%')
            elif bus_type.lower() == 'seater':
                query += " AND bustype LIKE %s"
                params.append('%Seater%')
        if route_name:
            query += " AND route_name LIKE %s"
            params.append('%' + route_name + '%')
        if price_min is not None:
            query += " AND price >= %s"
            params.append(price_min)
        if price_max is not None:
            query += " AND price <= %s"
            params.append(price_max)
        if rating is not None:
            query += " AND rating >= %s"  # Adjusted to include ratings equal to or greater than the selected rating
            params.append(rating)
        if seats_available:
            query += " AND seats_available > 0"

        # Execute the query
        cursor = db_connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()

        # Close cursor and database connection
        cursor.close()
        db_connection.close()

        return data

    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return None

# Streamlit UI
def main():
    st.title('Redbus List')
    
    # Sidebar filters
    st.sidebar.header('Filters')
    bus_type = st.sidebar.selectbox('Bus Type', ['', 'AC', 'Non-AC', 'Sleeper', 'Seater'])
    route_names = get_route_names()
    route_name = st.sidebar.selectbox('Route Name', [''] + route_names)
    price_min = st.sidebar.number_input('Minimum Price', value=0, min_value=0)
    price_max = st.sidebar.number_input('Maximum Price', value=10000, min_value=0)
    rating = st.sidebar.selectbox('Star Rating', ['', 1, 2, 3, 4, 5])
    seats_available = st.sidebar.checkbox('Available Seats Only')

    # Fetch data based on filters
    if st.sidebar.button('Apply Filters'):
        filtered_data = fetch_data(
            bus_type.lower() if bus_type != '' else None,
            route_name if route_name != '' else None,
            price_min if price_min != 0 else None,
            price_max if price_max != 10000 else None,
            rating if rating != '' else None,
            seats_available
        )

        # Display filtered data in cards
        st.subheader('Search Results:')
        if filtered_data:
            for row in filtered_data:
                st.write(f"**Route:** {row[3]} - {row[1]} ({row[2]})")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    st.write(f"Departure Time: {row[5]}")
                    st.write(f"Duration: {row[6]}")
                with col2:
                    st.write(f"Reaching Time: {row[7]}")
                    st.write(f"Price: {row[8]}")
                with col3:
                    st.write(f"Rating: {row[9]}")
                    st.write(f"Seats Available: {row[10]}")
                st.write(f"[Book Now]({row[4]})")
                st.write("---")
        else:
            st.write('No data found for the selected filters.')

if __name__ == '__main__':
    main()










