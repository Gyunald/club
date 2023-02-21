
import streamlit as st
from datetime import datetime,timedelta
from streamlit_server_state import server_state, server_state_lock, no_rerun
from streamlit_extras.switch_page_button import switch_page
empty = st.empty()
if 'nickname' not in st.session_state:
    nickname = st.text_input('닉네임 입력(추후 회원기능 도입)')
    st.session_state.nickname = nickname
else:
    nickname = empty.text_input('닉네임 입력(추후 회원기능 도입)',value=st.session_state.nickname)
    st.session_state.nickname = nickname
nickname = st.session_state.nickname
st.write(f"### Hi, {nickname}🎈")
e =st.empty()
if nickname:
    switch_page('chat')
