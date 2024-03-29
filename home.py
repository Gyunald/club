# import pandas as pd
# import streamlit as st
# import datetime
# import requests
# from streamlit_extras.switch_page_button import switch_page
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# st.set_page_config(
#     page_title="😎",
# )

# st.cache_resource()
# def img(img):
#     img = st.image(img,use_column_width=True)
#     return img

# def expander(title):
#     return st.expander(title, expanded=True)

# if not firebase_admin._apps:
#     cred = credentials.Certificate({
#     "type": st.secrets.type,
#     "project_id": st.secrets.project_id,
#     "private_key_id": st.secrets.private_key_id,
#     "private_key": st.secrets.private_key,
#     "client_email": st.secrets.client_email,
#     "client_id": st.secrets.client_id,
#     "auth_uri": st.secrets.auth_uri,
#     "token_uri": st.secrets.token_uri,
#     "auth_provider_x509_cert_url": st.secrets.auth_provider_x509_cert_url,
#     "client_x509_cert_url": st.secrets.client_x509_cert_url
#     })
#     app = firebase_admin.initialize_app(cred)

# empty = st.empty()

# if 'club' not in st.session_state:
#     st.session_state.club = ''

# if 'nickname' not in st.session_state:
#     nickname = st.text_input('닉네임 입력(추후 회원기능 도입)')
#     st.session_state.nickname = nickname
    
# else:
#     nickname = empty.text_input('닉네임 입력(추후 회원기능 도입)',value=st.session_state.nickname)
#     st.session_state.nickname = nickname

# nickname = st.session_state.nickname

# st.write(f"### Hi, {nickname}🎈")
# db = firestore.client()

# if nickname:
#     empty.empty()
# #     st.write('# IMI CE Korea Club')
#     st.write('# Club')
#     with expander('dynamic'):
#         c = st.columns(3)
#         with c[0]:
#             img('https://cdn.pixabay.com/photo/2021/03/02/19/26/snowshoes-6063630_960_720.jpg')
#             if st.button('배드민턴',use_container_width=True) :
#                 st.session_state.club = '배드민턴'
#                 st.session_state.place = ['고양 팩토 스타디움','파주시 배드민턴 전용구장']
#                 st.session_state.doc_ref = db.collection('dynamic')
#                 switch_page('club')
            
#         with c[1]:
#             img('https://cdn.pixabay.com/photo/2019/01/21/13/58/table-tenis-3946115_960_720.jpg')
#             if st.button('탁구',use_container_width=True):
#                 st.session_state.club = '탁구'
#                 st.session_state.place = ['문산 국민체육센터']
#                 st.session_state.doc_ref = db.collection('dynamic')
#                 switch_page('club')

#         with c[2]:
#             img('https://cdn.pixabay.com/photo/2018/03/08/20/36/ball-3209809_960_720.jpg')
#             if st.button('축구',use_container_width=True):
#                 st.session_state.club = '축구'
#                 st.session_state.place = ['당동리 풋살구장','FC 파주 풋살장']
#                 st.session_state.doc_ref = db.collection('dynamic')
#                 switch_page('club')

#     with expander('static'):
#         c = st.columns(3)
#         with c[0]:
#             img('https://cdn.pixabay.com/photo/2015/05/26/23/52/technology-785742_960_720.jpg')
#             if st.button('코딩',use_container_width=True):
#                 st.session_state.club = '코딩'
#                 st.session_state.place = ['스타벅스','폴바셋']
#                 st.session_state.doc_ref = db.collection('static')
#                 switch_page('club')

#         with c[1]:

#             img('https://cdn.pixabay.com/photo/2017/12/17/21/44/drink-3025022__340.jpg')
#             if st.button('독서',use_container_width=True):
#                 st.session_state.club = '독서'
#                 st.session_state.place = ['폴바셋', '스타벅스']
#                 st.session_state.doc_ref = db.collection('static')
#                 switch_page('club')                

#         with c[2]:
#             img('https://cdn.pixabay.com/photo/2021/10/31/07/23/instrument-6756414__340.jpg')
#             if st.button('기타',use_container_width=True):
#                 st.session_state.club = '기타'
#                 st.session_state.place = ['연습실']
#                 st.session_state.doc_ref = db.collection('static')
#                 switch_page('club')
                
#     with expander('etc'):
#         c = st.columns(3)
#         with c[0]:
#             img('https://cdn.pixabay.com/photo/2017/06/21/09/19/spoon-2426623__340.jpg')
#             if st.button('모임',use_container_width=True):
#                 st.session_state.club = '모임'                
#                 st.session_state.doc_ref = db.collection('static')
#                 switch_page('club')

#         with c[1]:
#             img('https://cdn.pixabay.com/photo/2016/04/23/20/21/smart-1348189_960_720.jpg')
#             if st.button('카풀',use_container_width=True):
#                 st.session_state.club = '카풀'
#                 st.session_state.doc_ref = db.collection('static')
#                 switch_page('club')

#     logout = st.button('로그아웃',type='primary')
#     if logout:
#         st.session_state.clear()
#         switch_page('club')
from pymongo import MongoClient
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


client = MongoClient('mongodb+srv://bigstar:dEiGez5PcMko8bPv@cluster0.pyaolr0.mongodb.net/?retryWrites=true&w=majority')
db = client.club

st.set_page_config(
    page_title="😎",
)

st.cache_resource()
def img(img):
    img = st.image(img,use_column_width=True)
    return img

def expander(title):
    return st.expander(title, expanded=True)

empty = st.empty()

if 'club' not in st.session_state:
    st.session_state.club = ''

if 'nickname' not in st.session_state:
    nickname = st.text_input('닉네임 입력(추후 회원기능 도입)')
    st.session_state.nickname = nickname
    
else:
    nickname = empty.text_input('닉네임 입력(추후 회원기능 도입)',value=st.session_state.nickname)
    st.session_state.nickname = nickname

nickname = st.session_state.nickname

st.write(f"### Hi, {nickname} 🎈")

if nickname:
    empty.empty()
    st.write('# Club')
    with expander('dynamic'):
        c = st.columns(3)
        with c[0]:
            img('https://cdn.pixabay.com/photo/2021/03/02/19/26/snowshoes-6063630_960_720.jpg')
            if st.button('배드민턴',use_container_width=True) :
                st.session_state.club = '배드민턴'
                st.session_state.place = ['고양 팩토 스타디움','파주시 배드민턴 전용구장']
                st.session_state.doc_ref = db.배드민턴
                switch_page('club')
            
        with c[1]:
            img('https://cdn.pixabay.com/photo/2019/01/21/13/58/table-tenis-3946115_960_720.jpg')
            if st.button('탁구',use_container_width=True):
                st.session_state.club = '탁구'
                st.session_state.place = ['문산 국민체육센터']
                st.session_state.doc_ref = db.탁구
                switch_page('club')

        with c[2]:
            img('https://cdn.pixabay.com/photo/2018/03/08/20/36/ball-3209809_960_720.jpg')
            if st.button('축구',use_container_width=True):
                st.session_state.club = '축구'
                st.session_state.place = ['당동리 풋살구장','FC 파주 풋살장']
                st.session_state.doc_ref = db.축구
                switch_page('club')

    with expander('static'):
        c = st.columns(3)
        with c[0]:
            img('https://cdn.pixabay.com/photo/2015/05/26/23/52/technology-785742_960_720.jpg')
            if st.button('코딩',use_container_width=True):
                st.session_state.club = '코딩'
                st.session_state.place = ['스타벅스','폴바셋']
                st.session_state.doc_ref = db.코딩
                switch_page('club')

        with c[1]:
            img('https://cdn.pixabay.com/photo/2017/12/17/21/44/drink-3025022__340.jpg')
            if st.button('독서',use_container_width=True):
                st.session_state.club = '독서'
                st.session_state.place = ['폴바셋', '스타벅스']
                st.session_state.doc_ref = db.독서
                switch_page('club')                

        with c[2]:
            img('https://cdn.pixabay.com/photo/2021/10/31/07/23/instrument-6756414__340.jpg')
            if st.button('기타',use_container_width=True):
                st.session_state.club = '기타'
                st.session_state.place = ['연습실']
                st.session_state.doc_ref = db.기타
                switch_page('club')
                
    with expander('etc'):
        c = st.columns(3)
        with c[0]:
            img('https://cdn.pixabay.com/photo/2017/06/21/09/19/spoon-2426623__340.jpg')
            if st.button('모임',use_container_width=True):
                st.session_state.club = '모임'                
                st.session_state.doc_ref = db.모임
                switch_page('club')

        with c[1]:
            img('https://cdn.pixabay.com/photo/2016/04/23/20/21/smart-1348189_960_720.jpg')
            if st.button('카풀',use_container_width=True):
                st.session_state.club = '카풀'
                st.session_state.doc_ref = db.카풀
                switch_page('club')

    logout = st.button('로그아웃',type='primary')
    if logout:
        st.session_state.clear()
        switch_page('club')
