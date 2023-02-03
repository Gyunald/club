import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
import streamlit_authenticator as stauth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

if not firebase_admin._apps:
    cred = credentials.Certificate('imi-club-firebase-adminsdk-83dcu-9b2da08252.json')
    app = firebase_admin.initialize_app(cred)

st.session_state.clear()

empty = st.empty()
nickname = st.text_input('닉네임 입력(추후 회원기능 도입)')

if 'nickname' not in st.session_state:
    st.session_state.nickname = nickname
st.write(st.session_state.nickname)
db = firestore.client()


def img(img):
     return st.image(img,use_column_width=True)

def expander(title):
    return st.expander(title, expanded=False)


# data = {
#     u'stringExample': u'Hello, World!',
#     u'booleanExample': True,
#     u'numberExample': 3.14159265,
#     u'dateExample': datetime.datetime.now(tz=datetime.timezone.utc),
#     u'arrayExample': [5, True, u'hello'],
#     u'nullExample': None,
#     u'objectExample': {
#         u'a': 5,
#         u'b': True
#     }
# }

# C

# res = collection.document('배드민턴').get().to_dict()

# # R
# res = collection.get() # returns a list

# for i in res:
#     st.write(i.to_dict())

# # U
# res = collection.document('A01').update({
#     'State': 'Chennai',
#     'age': 21
# })

# # D
# res = collection.document('A01').delete() 

if nickname:
    empty.empty()
    # st.header('IMI Critical Engineering Club')
    with expander('dynamic'):
        c1, c2, c3 = st.columns([1,1,1])

        with c1:
            img('https://cdn.pixabay.com/photo/2021/03/02/19/26/snowshoes-6063630_960_720.jpg')
            if st.button('배드민턴'):
                switch_page('배드민턴')
            
        with c2:
            img('https://cdn.pixabay.com/photo/2019/01/21/13/58/table-tenis-3946115_960_720.jpg')
            if st.button('탁구'):
                switch_page('탁구')

        with c3:
            img('https://cdn.pixabay.com/photo/2018/03/08/20/36/ball-3209809_960_720.jpg')
            if st.button('풋살'):
                switch_page('풋살')

    with expander('static'):
        c4, c5, c6 = st.columns([1,1,1])

        with c4:
            img('https://cdn.pixabay.com/photo/2015/11/20/08/17/meat-1052571_960_720.jpg')
            if st.button('파티'):
                switch_page('파티')

        with c5:
            img('https://cdn.pixabay.com/photo/2016/04/23/20/21/smart-1348189_960_720.jpg')
            if st.button('카풀'):
                switch_page('카풀')
