import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.write("파티")
if st.button('홈으로'):
    switch_page('club')