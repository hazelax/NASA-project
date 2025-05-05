import streamlit as st 
import pandas as pd
import pymysql 


st.title(":rocket: NASA Asteroid Tracker :star:")


cols = st.columns(2)

slider_1=cols[0].slider("Min Magnitude",min_value=13.80,max_value=32.61)
slider_2=cols[1].slider("Relative_velocity_kmph_Range",min_value=1418.21,max_value=173071.83)

st.write(slider_1,slider_2)

cols = st.columns(2)

slider_3=cols[0].slider("Min Estimated Diameter(km)",min_value=0.00,max_value=4.62)
slider_4=cols[1].slider("Astronomical Unit",min_value=1418.21,max_value=173071.83)

st.write(slider_3,slider_4)

st.slider("Max Estimated Diameter(km)",min_value=0.00,max_value=10.33)

cols = st.columns(3)

text_1=cols[0].text_input('Start Date')
text_2=cols[1].text_input('End Date')
text_3=cols[2].text_input('Only show Potentially Hazardous')

st.write(text_1,text_2,text_3)

st.sidebar.title("Asteroid Approaches")


if "page" not in st.session_state:
    st.session_state["page"] = "Home"



    

def get_db_connection():
    return connection
connection = pymysql.connect(
       
                  host = "localhost",
                  user = 'root',
                  password = "Fedo_ria@0304",
                  database = 'astro'
              )

cursor = connection.cursor()

def get_filtered_data():
    conn = get_db_connection()
    query = f"""
    SELECT * FROM asteroids
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df


if st.button("Filter"):
    filtered_data = get_filtered_data()  # type: ignore # Pass arguments
    st.dataframe(filtered_data) 

def run_query(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


    
Quiz = {
    "1. Count how many times each asteroid has approached Earth": "SELECT name, COUNT(*) AS approach_count FROM asteroids GROUP BY name;",
    "2. Average velocity of each asteroid over multiple approaches": "SELECT name, AVG(relative_velocity) AS avg_velocity FROM asteroids GROUP BY name;",
    "3. List top 10 fastest asteroids": "SELECT name, MAX(relative_velocity) AS max_velocity FROM asteroids ORDER BY max_velocity DESC LIMIT 10;",
    "4. Find potentially hazardous asteroids that have approached Earth more than 3 times": "SELECT name FROM asteroids WHERE hazardous = 1 GROUP BY name HAVING COUNT(*) > 3;",
    "5. Find the month with the most asteroid approaches": "SELECT MONTH(close_approach_date) AS month, COUNT(*) AS count FROM asteroids GROUP BY month ORDER BY count DESC LIMIT 1;",
    "6. Get the asteroid with the fastest ever approach speed": "SELECT name, MAX(relative_velocity) FROM asteroids;",
    "7. Sort asteroids by maximum estimated diameter (descending)": "SELECT name, estimated_diameter_max FROM asteroids ORDER BY estimated_diameter_max DESC;",
    "8. An asteroid whose closest approach is getting nearer over time": "SELECT name FROM asteroids ORDER BY close_approach_date ASC LIMIT 1;",
    "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth": "SELECT name, close_approach_date, miss_distance FROM asteroids ORDER BY miss_distance ASC;",
    "10. List names of asteroids that approached Earth with velocity > 50,000 km/h": "SELECT name FROM asteroids WHERE relative_velocity > 50000;",
    "11. Count how many approaches happened per month": "SELECT MONTH(close_approach_date) AS month, COUNT(*) FROM asteroids GROUP BY month;",
    "12. Find asteroid with the highest brightness (lowest magnitude value)": "SELECT name FROM asteroids ORDER BY magnitude ASC LIMIT 1;",
    "13. Get number of hazardous vs non-hazardous asteroids": "SELECT hazardous, COUNT(*) FROM asteroids GROUP BY hazardous;",
    "14. Find asteroids that passed closer than the Moon (lesser than 1 LD)": "SELECT name, close_approach_date, miss_distance FROM asteroids WHERE miss_distance < 1;",
    "15. Find asteroids that came within 0.05 AU": "SELECT asteroid_name FROM asteroids WHERE miss_distance < 0.05;"
}


if st.sidebar.button("Filter Criteria"):
    st.session_state["page"] = "Filter"

if st.sidebar.button("Questions"):
    st.session_state["page"] = "Questions"

if st.session_state["page"] == "Questions":
    st.write("## NASA Asteroid Questions")
    selected_question = st.selectbox("Select a question", list(Quiz.keys()))
    
    # Execute the corresponding SQL query
    query = Quiz[selected_question]
    result_df = run_query(query)
    st.dataframe(result_df)  
    
elif st.session_state["page"] == "Questions":
    st.write("## NASA Asteroid Questions")
    selected_question = st.selectbox("Select a question", list(Quiz.keys()))
    st.write("**SQL Query for Analysis:**")
    st.code(Quiz[selected_question], language="sql")

else:
    st.write("Use the sidebar to navigate.")


    