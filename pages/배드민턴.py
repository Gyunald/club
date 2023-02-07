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
        '참석자' : [],
        '신청자' : [],
        '취소자' : [],
        # '부서/나이/연락처' : [part,age,phone]
    }}

    submitted = st.form_submit_button('등록')

    if submitted :        
        db.collection('activity').document('배드민턴').update(data)


st.write('---')
st.error('회원 화면')

def disabled_True():
    st.session_state.disabled_True = True
    st.session_state.disabled_False = False
def disabled_False():
    st.session_state.disabled_True = False
    st.session_state.disabled_False = True

if "disabled_True" not in st.session_state:
    st.session_state.disabled_True = False
    
if "disabled_False" not in st.session_state:
    st.session_state.disabled_False = False

for i in range(1,2):
    c1,c2,c3= st.columns([i,i,i])

if 'count' not in st.session_state:
    st.session_state.count = 0
if 'participant' not in st.session_state:
    st.session_state.participant = []

with c1:
    doc_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    
    with st.form('output_form',):
        st.header(f'{date}-{time}')
        st.header(f'{place}')
        참 = st.form_submit_button('참석',on_click=disabled_True, disabled=st.session_state.disabled_True)
        불참 = st.form_submit_button('불참', on_click=disabled_False, disabled=st.session_state.disabled_False)

        if 참 :
            st.session_state.count +=1
            st.session_state.participant.append(n)
            
            doc_ref = db.collection('activity').document('배드민턴')
            doc = doc_ref.get().to_dict()
            doc_document = doc['2023-02-08']
            doc_list = doc_document['참석자']
            doc_application = doc_document['신청자']
            doc_list.append(f"{n}, {doc_time}")
            doc_application.append(f"{n}, {doc_time}")
            doc_ref.update(doc)

            
        elif 불참:
            # if st.session_state.count > 0 and n in st.session_state.participant :
            st.session_state.count -=1
            st.session_state.participant.remove(n)
            # st.session_state.nickname
            doc_ref = db.collection('activity').document('배드민턴')
            doc = doc_ref.get().to_dict()
            doc_document = doc['2023-02-08']
            doc_list = doc_document['참석자']
            doc_cancel = doc_document['취소자']
            doc_cancel.append(f"{n}, {doc_time}")
            doc_list.pop()
            doc_ref.update(doc)

        if st.session_state.count == 2:
            st.error(f"{st.session_state.count}/2 명")
            # st.session_state.nickname
        else:
            st.info(f"{st.session_state.count}/2 명")
        st.error(st.session_state.participant)
        st.success('[네이버지도](%s)' % f'https://map.naver.com/v5/directions/-/14114397.866921965,4540303.012815246,%EA%B3%A0%EC%96%91%ED%8C%A9%ED%86%A0%EC%8A%A4%ED%83%80%EB%94%94%EC%9B%80,1966063934,PLACE_POI/-/transit?c=14111433.1227196,4538425.9290852,12.89,0,0,0,dh')
        st.warning('[카카오맵](%s)' % 'https://map.kakao.com/link/to/고양팩토스타디움,37.722334,126.791838')

# a =db.collection('activity').document('배드민턴').get().to_dict()['2023-02-06']['장소/시간'][1]
# a =db.collection('activity').document('배드민턴').get().to_dict()
# for i in a :
#     # st.write(i)
#     st.write(f"가입일 : {a[i]['이름']} : >>> {a[i]['가입일/생성일'][0]}")

if st.button('홈으로'):
    switch_page('club')
