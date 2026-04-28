import streamlit as st
from contextlib import contextmanager
from modules import airtable_functions
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

st.title("Single Booking")

# Checking for booking success status in session state
if st.session_state.get("booking_success_single"):
    st.success("Booked!")

    del st.session_state.booking_success_single

    if st.button("Close Message & Refresh", type="secondary", width="stretch", key="single_refresh_button"):
        st.rerun()
else:
    FORM_CATEGORY = "Single" # Differentiates between Single or Multiple Booking

    with st.form("singe_booking_form", clear_on_submit=False, enter_to_submit=False):
        NAME = st.text_input("Name *", placeholder="Enter your name", icon=":material/id_card:")
        EMAIL = st.text_input("Email *", placeholder="Enter your email", icon=":material/mail:", help="Please enter the correct email.")
        NUMBER = st.text_input("Mobile Number (All countries supported!) *", placeholder="Enter your mobile number (e.g.: +447xxxxxxxxx)", icon=":material/call:", help="Please enter the correct mobile number in the provided format without spaces.")

        age_options = ["Please Choose Age", "Below 6", "6-12", "13-19", "20-25", "26-35", "36-50", "50+"]
        AGE = st.selectbox("Age Group *", options=age_options, placeholder="Choose one of the age groups")

        gender_options = ["Please Choose Gender", "Male", "Female", "Prefer not to say"]
        GENDER = st.selectbox("Gender *", options=gender_options, placeholder="Choose one of the genders")

        HOME_CHURCH = st.text_input("Home Church / Congregation *", placeholder="Enter your Home Church or Congregation", icon=":material/church:")
        CITY_TOWN = st.text_input("City / Town *", placeholder="Enter your Town or City", icon=":material/location_city:")

        single_submitted = st.form_submit_button("Submit Booking")

    @st.dialog("Confirm Booking", width="small")
    def show_single_confirm_dialog(name, email, number, age, gender, home_church, city_town, form_category):
        st.write(f"Are you sure you want to confirm the booking for **{name}**?")

        with st_horizontal():
            if st.button("Confirm", type="primary", width="stretch", key="single_confirm_button"):
                try:
                    airtable_functions.single_booking_assigner(name, email, number, age, gender, home_church, city_town, form_category)

                    st.session_state.booking_success_single = True
                    st.rerun()

                except Exception as e:
                    st.exception(e)

            if st.button("Cancel", type="secondary", width="stretch", key="single_cancel_button"):
                st.rerun()

    if single_submitted:
        if not NAME or not EMAIL or not NUMBER or AGE == "Please Choose Age" or GENDER == "Please Choose Gender" or not HOME_CHURCH or not CITY_TOWN:
            st.error("Please enter all the information!")
        elif not mobile_number_verifier("".join(NUMBER.split())):
            st.error("Please enter a valid mobile number in the example format, +447xxxxxxxxx, without spaces!")   
        else:
            show_single_confirm_dialog(NAME.strip().title(), EMAIL.strip(), "".join(NUMBER.split()), AGE, GENDER, HOME_CHURCH.strip(), CITY_TOWN.strip().title(), FORM_CATEGORY)
