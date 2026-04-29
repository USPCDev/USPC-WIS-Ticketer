import streamlit as st
from contextlib import contextmanager
from modules import airtable_functions, expander_functions
import phonenumbers
import re

def mobile_number_verifier(mobile_number):
    try:
        # Enforce format: +<country_code><number> (digits only, no spaces)
        if not re.match(r"^\+\d+$", mobile_number):
            return False
        
        # Double check with phonenumbers
        # Passing None for region allows auto-detection from international format
        parsed = phonenumbers.parse(mobile_number, None)
        return phonenumbers.is_valid_number(parsed)
    
    except:
        return False

horizontal_style="""<style class="hide-element">
                        .element-container:has(.hide-element) {
                            display: none;
                        }
                        div[data-testid="stVerticalBlock"]:has(> .element-container .horizontal-marker) {
                            display: flex;
                            flex-direction: row !important;
                            flex-wrap: wrap;
                            gap: 0.5rem;
                            align-items: baseline;
                        }
                        div[data-testid="stVerticalBlock"]:has(> .element-container .horizontal-marker) div {
                            width: max-content !important;
                        }
                    </style>"""

@contextmanager
def st_horizontal():
    st.markdown(horizontal_style, unsafe_allow_html=True)
    with st.container():
        st.markdown('<span class="hide-element horizontal-marker"></span>', unsafe_allow_html=True)
        yield

with st_horizontal():
    if st.button(":material/arrow_back_ios_new:", type="primary", help="Back to Home Page"):
        st.switch_page("home.py")

    if st.button("Switch to **Single** Booking"):
        st.switch_page("pages/single_main.py")

expander_functions.info_expander("multiple_map")

st.title("Multiple Booking")

# Checking for booking success status in session state
if st.session_state.get("booking_success_multiple"):
    st.success(f"##### Thank you for placing an order, **{st.session_state.booked_primary_name_multiple}**!\nYour order details will be sent to your email, **{st.session_state.booked_primary_email_multiple}**, shortly. If you haven't received any order confirmation email, please contact the support team whose numbers are provided in the homepage. Please pay the required *amount* using the correct *reference*, as provided below, in the mentioned bank details. Thank you once again!\n##### Order Summary:\nBooking Type: **{st.session_state.booked_booking_type_multiple}**\n\nReference No.: **{st.session_state.booked_order_id_multiple}**\n\nPrice: **£{st.session_state.booked_booking_price_multiple}.00**\n##### Bank Details:\nAccount Name: **United Shalom Pentecostal Church (Charity/Business)**\n\nAccount No.: **51553690**\n\nSort Code: **40-31-30**\n\nOnce payment has been made, our back office team will verify it, and upon successful verification, your seat will be confirmed.")

    del st.session_state.booking_success_multiple
    del st.session_state.booked_primary_name_multiple
    del st.session_state.booked_primary_email_multiple
    del st.session_state.booked_order_id_multiple
    del st.session_state.booked_booking_type_multiple
    del st.session_state.booked_booking_price_multiple

    if st.button("Close Message & Refresh", type="secondary", width="stretch", key="multiple_refresh_button"):
        st.rerun()
else:
    FORM_CATEGORY = "Multiple" # Differentiates between Single or Multiple Booking

    with st.form("multiple_booking_form", clear_on_submit=False, enter_to_submit=False):
        st.subheader("Primary Contact Details", divider="grey")

        PRIMARY_NAME = st.text_input("Name *", placeholder="Enter your name", icon=":material/id_card:")
        PRIMARY_EMAIL = st.text_input("Email *", placeholder="Enter your email", icon=":material/mail:", help="Please enter the correct email.")
        PRIMARY_NUMBER = st.text_input("Mobile Number (All countries supported!) *", placeholder="Enter your mobile number (e.g.: +447xxxxxxxxx)", icon=":material/call:", help="Please enter the correct mobile number in the provided format without spaces.")

        age_options = ["Please Choose Age", "Below 6", "6-12", "13-19", "20-25", "26-35", "36-50", "50+"]
        AGE = st.selectbox("Age Group *", options=age_options, placeholder="Choose one of the age groups")

        gender_options = ["Please Choose Gender", "Male", "Female", "Prefer not to say"]
        GENDER = st.selectbox("Gender *", options=gender_options, placeholder="Choose one of the genders")

        HOME_CHURCH = st.text_input("Home Church / Congregation *", placeholder="Enter your Home Church or Congregation", icon=":material/church:")
        CITY_TOWN = st.text_input("City / Town *", placeholder="Enter your Town or City", icon=":material/location_city:")

        ATTENDANCE = st.checkbox("**Are you attending the event?**")
        
        st.divider()
        
        st.subheader("Additional Participants", divider="grey")
        
        attendee_tabs = st.tabs(["**Attendee 1**", "**Attendee 2**", "**Attendee 3**", "**Attendee 4**", "**Attendee 5**", "**Attendee 6**"])
        ATTENDEES = []
        for i, tab in enumerate(attendee_tabs):
            with tab:
                st.markdown(f"##### Attendee {i+1} Details:")

                ATTENDEE_NAME = st.text_input(f"Name *", placeholder="Enter the name", icon=":material/id_card:", key=f"attendee_name_{i}")

                age_options = ["Please Choose Age", "Below 6", "6-12", "13-19", "20-25", "26-35", "36-50", "50+"]
                ATTENDEE_AGE = st.selectbox("Age Group *", options=age_options, key=f"attendee_age_{i}")

                gender_options = ["Please Choose Gender", "Male", "Female", "Prefer not to say"]
                ATTENDEE_GENDER = st.selectbox("Gender *", options=gender_options, key=f"attendee_gender_{i}")

                ATTENDEES.append({
                    "name": ATTENDEE_NAME,
                    "age": ATTENDEE_AGE,
                    "gender": ATTENDEE_GENDER
                })

        multiple_submitted = st.form_submit_button("Submit Booking")

    @st.dialog("Confirm Booking", width="small")
    def show_multiple_confirm_dialog(primary_name, primary_email, primary_phone, age, gender, home_church, city_town, form_category, attendance, validated_attendees):
        st.write(f"Are you sure you want to confirm the booking for **{primary_name}**?")

        with st_horizontal():
            if st.button("Confirm", type="primary", width="stretch", key="multiple_confirm_button"):
                try:
                    order_id, booking_type, booking_price = airtable_functions.multiple_booking_assigner(primary_name, primary_email, primary_phone, age, gender, home_church, city_town, form_category, attendance, validated_attendees)

                    st.session_state.booking_success_multiple = True
                    st.session_state.booked_primary_name_multiple = primary_name
                    st.session_state.booked_primary_email_multiple = primary_email
                    st.session_state.booked_order_id_multiple = order_id
                    st.session_state.booked_booking_type_multiple = booking_type
                    st.session_state.booked_booking_price_multiple = booking_price
                    st.rerun()

                except Exception as e:
                    st.exception(e)

            if st.button("Cancel", type="secondary", width="stretch", key="multiple_cancel_button"):
                st.rerun()

    if multiple_submitted:
        if not PRIMARY_NAME or not PRIMARY_EMAIL or not PRIMARY_NUMBER or AGE == "Please Choose Age" or GENDER == "Please Choose Gender" or not HOME_CHURCH or not CITY_TOWN:
            st.error("Please complete the primary contact details.")
        elif not mobile_number_verifier("".join(PRIMARY_NUMBER.split())):
            st.error("Please enter a valid mobile number in the example format, +447xxxxxxxxx, without spaces!")
        else:
            # Attendee validation
            is_valid = True
            VALIDATED_ATTENDEES = []
            has_data = False
            
            for ATT in ATTENDEES:
                # If name is filled, or age is selected, or gender is selected, treat as attendee
                AGE_FILLED = ATT["age"] != "Please Choose Age"
                GENDER_FILLED = ATT["gender"] != "Please Choose Gender"
                
                if ATT["name"] or AGE_FILLED or GENDER_FILLED:
                    has_data = True
                    if not (ATT["name"] and AGE_FILLED and GENDER_FILLED):
                        st.error(f"Please fill all the required fields (Name, Age, Gender) for Attendee {ATTENDEES.index(ATT)+1}!")
                        is_valid = False
                        break
                    VALIDATED_ATTENDEES.append(ATT)
            
            if is_valid and not has_data:
                st.error("Please add at least one attendee or toggle off additional participants.")
                is_valid = False
            
            if is_valid:
                show_multiple_confirm_dialog(PRIMARY_NAME.strip().title(), PRIMARY_EMAIL.strip(), "".join(PRIMARY_NUMBER.split()), AGE, GENDER, HOME_CHURCH.strip(), CITY_TOWN.strip().title(), FORM_CATEGORY, ATTENDANCE, VALIDATED_ATTENDEES)
