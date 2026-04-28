import streamlit as st
from pyairtable import Api

def single_booking_assigner(primary_name, primary_email, primary_phone, age, gender, home_church, city_town, form_category):
    with st.spinner("Processing..."):
        api = Api(st.secrets["airtable"]["PAT"])
        base = api.base(st.secrets["airtable"]["BASE_ID"])
        bookings_table = base.table("Primary Reg Table")
        attendees_table = base.table("Secondary Reg Table")

        # 1. CREATE RECORD IN MAIN BOOKING
        booking_data = {
            "Full Name": primary_name,
            "Email ID": primary_email,
            "Contact Number": primary_phone
        }
        if age != "Please Choose Age": booking_data["Age"] = age
        if gender != "Please Choose Gender": booking_data["Gender"] = gender
        if home_church: booking_data["Home Church / Congregation"] = home_church
        if city_town: booking_data["City / Town"] = city_town
        if form_category: booking_data["Form Category"] = form_category

        booking_record = bookings_table.create(booking_data)

        booking_record_id = booking_record["id"]

        # 2. CREATE RECORD IN SECONDARY BOOKING
        primary_attendee_data = {
            "Name": primary_name,
            "Type": "Primary",
            "Attendance": True,
            "Primary Booking": [booking_record_id],
        }
        if age != "Please Choose Age": primary_attendee_data["Age"] = age
        if gender != "Please Choose Gender": primary_attendee_data["Gender"] = gender

        attendees_table.create(primary_attendee_data)

        return booking_record_id

def multiple_booking_assigner(primary_name, primary_email, primary_phone, age, gender, home_church, city_town, form_category, attendance, attendees):
    with st.spinner("Processing..."):
        api = Api(st.secrets["airtable"]["PAT"])
        base = api.base(st.secrets["airtable"]["BASE_ID"])
        bookings_table = base.table("Primary Reg Table")
        attendees_table = base.table("Secondary Reg Table")

        # 1. CREATE RECORD IN MAIN BOOKING
        booking_data = {
            "Full Name": primary_name,
            "Email ID": primary_email,
            "Contact Number": primary_phone
        }
        if age != "Please Choose Age": booking_data["Age"] = age
        if gender != "Please Choose Gender": booking_data["Gender"] = gender
        if home_church: booking_data["Home Church / Congregation"] = home_church
        if city_town: booking_data["City / Town"] = city_town
        if form_category: booking_data["Form Category"] = form_category

        booking_record = bookings_table.create(booking_data)

        booking_record_id = booking_record["id"]

        # 2. CREATE RECORD IN SECONDARY BOOKING
        primary_attendee_data = {
            "Name": primary_name,
            "Type": "Primary",
            "Attendance": attendance,
            "Primary Booking": [booking_record_id],
        }
        if age != "Please Choose Age": primary_attendee_data["Age"] = age
        if gender != "Please Choose Gender": primary_attendee_data["Gender"] = gender

        attendees_table.create(primary_attendee_data)

        for attendee in attendees:
            if attendee["name"]:
                attendee_data = {
                    "Name": attendee["name"],
                    "Type": "Additional",
                    "Attendance": True,
                    "Primary Booking": [booking_record_id],
                }
                if attendee["age"] != "Please Choose Age": attendee_data["Age"] = attendee["age"]
                if attendee["gender"] != "Please Choose Gender": attendee_data["Gender"] = attendee["gender"]
                
                attendees_table.create(attendee_data)

        return booking_record_id
