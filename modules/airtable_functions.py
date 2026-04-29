import streamlit as st
from pyairtable import Api
import time

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

        if age in ["13-19", "20-25", "26-35", "36-50", "50+"]:
            primary_attendee_data["Booking Price"] = 50

        attendees_table.create(primary_attendee_data)

        # 3. FETCH RELEVANT DETAILS OF THE MAIN RECORD WITH RETRIES
        fields = {}
        for _ in range(10): # 10 retries
            primary_record = bookings_table.get(booking_record_id)
            fields = primary_record.get("fields", {})
            if fields.get("Total Booking Price", 0) > 0:
                break
            time.sleep(3)

        # 4. UPDATE THE SYSTEM VARIABLE IN THE MAIN RECORD FOR CONFIRMATION
        bookings_table.update(booking_record_id, {"Price Calculation Status (System Field)": True})

        return fields.get("Registration Code"), fields.get("Form Category"), fields.get("Total Booking Price")

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

        calculated_total_price = 0
        if attendance == True and age in ["13-19", "20-25", "26-35", "36-50", "50+"]:
            primary_attendee_data["Booking Price"] = 50
            calculated_total_price += 50

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
                
                if attendee["age"] in ["13-19", "20-25", "26-35", "36-50", "50+"]:
                    attendee_data["Booking Price"] = 50
                    calculated_total_price += 50
                
                attendees_table.create(attendee_data)

        # 3. FETCH RELEVANT DETAILS OF THE MAIN RECORD WITH RETRIES
        fields = {}
        for _ in range(10): # 10 retries
            primary_record = bookings_table.get(booking_record_id)
            fields = primary_record.get("fields", {})
            if fields.get("Total Booking Price", 0) == calculated_total_price:
                break
            time.sleep(3)

        # 4. UPDATE THE SYSTEM VARIABLE IN THE MAIN RECORD FOR CONFIRMATION
        bookings_table.update(booking_record_id, {"Price Calculation Status (System Field)": True})

        return fields.get("Registration Code"), fields.get("Form Category"), fields.get("Total Booking Price")
