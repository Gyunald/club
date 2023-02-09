import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_extras.switch_page_button import switch_page
from firebase_admin import firestore

@st.experimental_memo
def load_lottie(url:str):
    r = requests.get(url)

    if r.status_code != 200:
        return None
    return r.json()

lottie_url = 'https://assets6.lottiefiles.com/packages/lf20_5edeys7f.json'
lottie_json = load_lottie(lottie_url)

# st_lottie(
#     lottie_json,
#     speed=1,
#     # reverse='Ture',
#     loop=True,
#     quality='low',
#     width=200
#     )

db = firestore.client()
n = st.session_state.nickname
st.error('회장 화면')
st.write(f"Hi, {n}🎈")

with st.form("my_form",clear_on_submit=False):
    date = st.date_input('date').strftime('%Y-%m-%d')
    time = st.time_input('time',value=datetime.time(17,45)).strftime('%H:%M')
    # name = st.text_input('name',value='')
    # age = st.number_input('age',value=30, step=1 )
    # part = st.text_input('part',value='가공')
    # phone = st.text_input('phone',value='010-')
    place = st.selectbox('place', ['고양팩토스타디움','파주시 배드민턴 전용구장'])
    data = { date : {
        '시간' : time,
        '날짜' : date,
        '장소' : place,
        '참가자' : [],
        '참여' : {},
        '불참' : {},
        # '부서/나이/연락처' : [part,age,phone]
    }}

    submitted = st.form_submit_button('등록')

    if submitted :        
        db.collection('activity').document('배드민턴').update(data)


st.write('---')
st.error('회원 화면')

def disabled_참():
    st.session_state.disabled_참 = True
    st.session_state.disabled_불참 = False
def disabled_불참():
    st.session_state.disabled_참 = False
    st.session_state.disabled_불참 = True

c = st.columns(3)
doc_ref = db.collection('activity').document('배드민턴')
doc = doc_ref.get().to_dict()
doc_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')

for i,j in zip(range(len(c)), sorted(doc.keys(),reverse=True)):
    doc_document = doc[j]
    doc_list = doc_document['참가자']
    standard = datetime.datetime.utcnow().strftime('%Y-%m-%d') > doc_document['날짜']
    k = f"disabled_{j}"
    if k not in st.session_state:
        st.session_state[k] = False
        st.session_state[k] = False

    if len(doc_list) == 2:
        st.session_state[k] = True
        st.session_state[k] = True
        if n in doc_list:
            st.session_state[k] = False

    if standard:
        st.session_state[k] = True
        st.session_state[k] = True
        if n in doc_list:
            st.session_state[k] = False

    with c[i]:
        with st.form(j):
            st.header(f"{doc_document['날짜']}")
            st.header(f"{doc_document['시간']}")
            st.header(f"{doc_document['장소']}")
            참 = st.form_submit_button('참여',on_click=disabled_참, disabled=st.session_state[k])
            불참 = st.form_submit_button('불참', on_click=disabled_불참, disabled=st.session_state[k])
            if 참 :
                if len(doc_list) < 2:
                    doc_application = doc_document['참여']
                    if n not in doc_list:
                        doc_list.append(n)
                        doc_application[n] = doc_time
                    doc_ref.update(doc)
                    st.balloons()

            if 불참:
                doc_cancel = doc_document['불참']
                doc_cancel[n] = doc_time
                if n in doc_list :
                    doc_list.remove(n)
                doc_ref.update(doc)
                st.snow()

            if len(doc_list) == 2:
                st.error(f"{len(doc_list)}/2 명")
                if n in doc_list:
                    st.session_state.disabled_불참 = False
                else:
                    st.session_state.disabled_참 = True
                    st.session_state.disabled_불참 = True
            else:
                st.info(f"{len(doc_list)}/2 명")
            st.error(doc_list)
            st.success('[네이버지도](%s)' % f'https://map.naver.com/v5/directions/-/14114397.866921965,4540303.012815246,%EA%B3%A0%EC%96%91%ED%8C%A9%ED%86%A0%EC%8A%A4%ED%83%80%EB%94%94%EC%9B%80,1966063934,PLACE_POI/-/transit?c=14111433.1227196,4538425.9290852,12.89,0,0,0,dh')
            st.warning('[카카오맵](%s)' % 'https://map.kakao.com/link/to/고양팩토스타디움,37.722334,126.791838')

if st.button('홈으로'):
    switch_page('club')
