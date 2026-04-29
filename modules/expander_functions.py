import streamlit as st
from streamlit_folium import st_folium
import folium

def info_expander(map_key):
    with st.expander("**Very Important Info (Click here to open)!**", icon=":material/info:", expanded=False):

        VENUE_DETAILS_TAB, REGISTRATION_FEES_TAB, EVENT_INFO_TAB, SUPPORT_TEAM_TAB = st.tabs(["Venue Details", "Registration Fees", "Important Info", "Support Contact"], width="stretch")

        with VENUE_DETAILS_TAB:
            st.subheader("Venue Details", divider="grey")

            VENUE_MAP_CONTAINER = st.container(border=True)
            with VENUE_MAP_CONTAINER:

                vog_venue_map = folium.Map(location=[53.39634376884467, -2.2864225004874528])
                folium.Marker(
                    [53.39634376884467, -2.2864225004874528],
                    popup="USPC Manchester",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(vog_venue_map)

                st_folium(vog_venue_map, zoom=15, width="stretch", height=300, key=f"st_folium_map{map_key}")

            EMPTY_COL_1, MAP_BUTTON_COLUMN, EMPTY_COL_2 = st.columns([2, 2, 2], gap="small", vertical_alignment="center")
            with MAP_BUTTON_COLUMN:
                st.link_button("Open Maps", url="https://maps.app.goo.gl/eNzkAJ3viGYF6sF79", icon=":material/explore:", width="stretch")

            VENUE_DETAILS_CONTAINER = st.container(border=False)
            with VENUE_DETAILS_CONTAINER:
                st.markdown("#### :material/stadium: Venue: *USPC Manchester, Wythenshawe*")
                st.markdown("#### :material/signpost: Street: *89 Floatshall Rd*")
                st.markdown("#### :material/map_search: Postcode: *M23 1JB*")
                st.markdown("#### :material/location_city: City: *Manchester*")

                st.divider()

                st.markdown("#### :material/calendar_month: Date: *Mon, 20th July - Wed, 22nd July, 2026*")

        with REGISTRATION_FEES_TAB:
            st.subheader("Tariff Details", divider="grey")
            AGES_13_AND_ABOVE_COLUMN, AGES_12_AND_UNDER_COLUMN = st.columns([1, 1], gap="small", vertical_alignment="center")

            with AGES_13_AND_ABOVE_COLUMN:
                st.metric("Ages 13 & Above", value="£50", border=True)

            with AGES_12_AND_UNDER_COLUMN:
                st.metric("Ages 12 & Under", value="Free", border=True)

        with EVENT_INFO_TAB:
            st.subheader("Important Info", divider="grey")

            st.markdown("#### Welcome to Christians Elite - Wisdom Camp 2026!")

            st.markdown("*Note: For planning purposes, all attendees must be registered, including children 12 and under. The registration fee covers all meals for the duration of the camp. There are no additional event fees.*")

            st.markdown("##### Event Details:")

            st.markdown("* **Dates:** Monday, 20 July - Wednesday, 22 July 2026")
            st.markdown("* **Venue:** United Shalom Pentecostal Church, 89 Floatshall Road, Manchester, M23 1JB, UK")
            st.markdown("* **Contact:** +44 7550634734")

            st.markdown("##### Registration Fees:")

            st.markdown("* **Ages 13+:** £50 per person")
            st.markdown("* **Ages 12 & Under:** Free")

            st.markdown("##### Payment Details:")

            st.markdown("* **Account Name:** United Shalom Pentecostal Church (Charity/Business)")
            st.markdown("* **Sort Code:** 40-31-30")
            st.markdown("* **Account No:** 51553690")
            st.markdown("* **Payment Reference:** Please use the reference code assigned to you once you have booked (The reference code will be shown on the booking acknowledgment message as well as in your provided email).")

            st.markdown("##### Accommodation:")

            st.markdown("Please use booking.com or airbnb and book early for affordable accommodation options near the conference venue.")

        with SUPPORT_TEAM_TAB:
            st.subheader("Support Contact", divider="grey")
            st.link_button("+447550634734", icon=":material/call:", url="tel:+447550634734", width="stretch")
