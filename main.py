import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
import random

# Create a connection to the SQLite database
conn = sqlite3.connect('birthdays.db')
c = conn.cursor()

# Create the "birthdays" table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS birthdays (
        name TEXT,
        date TEXT
    )
''')
conn.commit()

# Random birthday wishes
birthday_wishes = [
    "May your birthday be filled with joy and happiness!",
    "Wishing you a fantastic birthday and an amazing year ahead!",
    "May all your birthday wishes come true!",
    # Add more birthday wishes here
]

# Random belated birthday wishes
belated_birthday_wishes = [
    "Wishing you a belated happy birthday! Sorry for the delay.",
    "Happy belated birthday! I hope it was a special one.",
    "Better late than never! Belated birthday wishes to you!",
    # Add more belated birthday wishes here
]

# Streamlit configuration
st.title("Birthday Reminder")

# Home page
page = st.sidebar.selectbox("Select an option", ["Check Birthday", "Add Birthday", "Upcoming Birthdays"])

if page == "Check Birthday":
    st.header("Check Your Birthday")

    # User input for name and date
    name = st.text_input("Enter your name")
    min_date = date(1950, 1, 1)
    max_date = date.today()
    date_val = st.date_input("Enter your birthday", min_value=min_date, max_value=max_date)

    if st.button("Check"):
        # Query the database for the given name and date
        c.execute("SELECT * FROM birthdays WHERE name = ? AND date = ?", (name, date_val))
        result = c.fetchone()

        if result is not None:
            # Check if the birthday is in the current year
            today = date.today()
            current_year_birthday = date(today.year, date_val.month, date_val.day)
            days_to_birthday = (current_year_birthday - today).days

            if days_to_birthday > 0:
                st.success(random.choice(birthday_wishes))
                st.info(f"You have {days_to_birthday} days to celebrate your birthday!")
            elif days_to_birthday == 0:
                st.success("Happy Birthday, {}!".format(name))
                st.audio("hbd.mp3", format="audio/mp3")
            else:
                st.success(random.choice(belated_birthday_wishes))
        else:
            st.warning("Your birthday is not found. Please add your birthday below.")

        if st.button("Clear"):
            st.text_input("Enter your name", value="")
            st.date_input("Enter your birthday", value=date.today(), min_value=min_date, max_value=max_date)
            st.empty()

if page == "Add Birthday":
    st.header("Add Your Birthday")

    # User input for name and date
    name = st.text_input("Enter your name")
    min_date = date(1950, 1, 1)
    max_date = date.today()
    date_val = st.date_input("Enter your birthday", min_value=min_date, max_value=max_date)

    if st.button("Add"):
        # Insert the name and date into the database
        c.execute("INSERT INTO birthdays (name, date) VALUES (?, ?)", (name, date_val))
        conn.commit()
        st.success("Your birthday has been added!")

if page == "Upcoming Birthdays":
    st.header("Upcoming Birthdays")
    today = date.today()
    c.execute("SELECT * FROM birthdays")
    results = c.fetchall()

    upcoming_birthdays = []
    for result in results:
        b_date = datetime.strptime(result[1], "%Y-%m-%d").date()
        if b_date.month >= today.month and b_date.day >= today.day:
            upcoming_birthdays.append((result[0], b_date))

    if len(upcoming_birthdays) > 0:
        upcoming_birthdays.sort(key=lambda x: (x[1].month, x[1].day))
        for name, birthday in upcoming_birthdays:
            st.write(f"{name}: {birthday.strftime('%B %d')}")
    else:
        st.info("No upcoming birthdays found.")

# Close the database connection
conn.close()
