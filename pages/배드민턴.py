import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_extras.switch_page_button import switch_page
from streamlit_lottie import st_lottie
from firebase_admin import firestore

@st.experimental_memo
def load_lottie(url:str):
    r = requests.get(url)

    if r.status_code != 200:
        return None
    return r.json()

lottie_url = 'https://assets6.lottiefiles.com/packages/lf20_5edeys7f.json'
lottie_json = load_lottie(lottie_url)

st_lottie(
    lottie_json,
    speed=1,
    # reverse='Ture',
    loop=True,
    quality='low',
    width=200
    )

empty = st.empty()
if 'nickname' not in st.session_state:
    nickname = empty.text_input('닉네임 입력(추후 회원기능 도입)')
    st.session_state.nickname = nickname
    empty.empty()
else:
    nickname = empty.text_input('닉네임 입력(추후 회원기능 도입)',value=st.session_state.nickname)
    st.session_state.nickname = nickname
    empty.empty()

db = firestore.client()

nickname = st.session_state.nickname
if nickname :
    st.write(f"Hi, {nickname}🎈")
    with st.form("my_form",clear_on_submit=True):
        date = st.date_input('date').strftime('%Y-%m-%d')
        time = st.time_input('time',value=datetime.time(17,45)).strftime('%H:%M')
        # name = st.text_input('name',value='')
        # age = st.number_input('age',value=30, step=1 )
        # part = st.text_input('part',value='가공')
        # phone = st.text_input('phone',value='010-')
        place = st.selectbox('place', ['고양팩토스타디움','파주시 배드민턴 전용구장'])
        # place = st.text_input('title')
        data = { f"{date}-{place}" : {
            '시간' : time,
            '날짜' : date,
            '장소' : place,
            '참가자' : [],
            '참여' : {},
            '불참' : {},
            '작성자' : nickname,
            # '부서/나이/연락처' : [part,age,phone]
        }}

        submitted = st.form_submit_button('등록')
        date_check = data[f"{date}-{place}"]['날짜'] +'-'+ data[f"{date}-{place}"]['장소']
        if submitted :
            if date_check not in db.collection('activity').document('배드민턴').get().to_dict():
                db.collection('activity').document('배드민턴').update(data)
            else:
                st.warning('이미 같은장소에 모임이 있습니다.')

    st.write('---')
    rerun = st.button('새로고침')

    if rerun:        
        st.experimental_rerun()

    def disabled_참():
        st.session_state.disabled_참 = True
        st.session_state.disabled_불참 = False
    def disabled_불참():
        st.session_state.disabled_참 = False
        st.session_state.disabled_불참 = True

    c = st.columns(3)
    doc_ref = db.collection('activity').document('배드민턴')
    doc = doc_ref.get().to_dict()
    doc_time = (datetime.datetime.utcnow()+datetime.timedelta(hours=9)).strftime('%Y-%m-%d-%H:%M')

    for i,j in zip(range(len(c)), sorted(doc.keys(),reverse=True)):
        doc_document = doc[j]
        doc_list = doc_document['참가자']
        standard = (datetime.datetime.utcnow()+datetime.timedelta(hours=9)).strftime('%Y-%m-%d') > doc_document['날짜']
        k = f"disabled_{j}"
        if k not in st.session_state:
            st.session_state[k] = False

        if len(doc_list) == 2:
            st.session_state[k] = True
            if nickname in doc_list:
                st.session_state[k] = False

        if standard:
            st.session_state[k] = True

        with c[i]:
            with st.form(j):
                st.header(f"{doc_document['날짜']}")
                st.header(f"{doc_document['시간']}")
                st.subheader(f"{doc_document['장소']}")
                참 = st.form_submit_button('참여',on_click=disabled_참, disabled=st.session_state[k])
                불참 = st.form_submit_button('불참', on_click=disabled_불참, disabled=st.session_state[k])
                if doc_document['작성자'] == nickname:
                    삭제 = st.form_submit_button('삭제')
                    if 삭제:
                        check = st.text_input('렬루?',placeholder="'y' 치고 클릭").lower()
                        if check == 'y':
                            doc_ref.update({f"{doc_document['날짜']}-{doc_document['장소']}" : firestore.DELETE_FIELD})
                            st.experimental_rerun()
                if 참 :
                    if len(doc_list) < 2:
                        doc_application = doc_document['참여']
                        if nickname not in doc_list:
                            doc_list.append(nickname)
                            doc_application[nickname] = doc_time
                        doc_ref.update(doc)
                        st.balloons()

                if 불참:
                    doc_cancel = doc_document['불참']
                    doc_cancel[nickname] = doc_time
                    if nickname in doc_list :
                        doc_list.remove(nickname)
                    doc_ref.update(doc)

                if len(doc_list) == 2:
                    st.error(f"{len(doc_list)}/2 명")
                    if nickname in doc_list:
                        st.session_state.disabled_불참 = False
                    else:
                        st.session_state.disabled_참 = True
                        st.session_state.disabled_불참 = True
                else:
                    st.info(f"{len(doc_list)}/2 명")
                st.error(doc_list)
                st.success('[🚕 네이버지도](%s)' % f'https://map.naver.com/v5/directions/-/14114397.866921965,4540303.012815246,%EA%B3%A0%EC%96%91%ED%8C%A9%ED%86%A0%EC%8A%A4%ED%83%80%EB%94%94%EC%9B%80,1966063934,PLACE_POI/-/transit?c=14111433.1227196,4538425.9290852,12.89,0,0,0,dh')
                st.warning('[🚗 카카오맵](%s)' % 'https://map.kakao.com/?map_type=TYPE_MAP&target=car&rt=%2C%2C454120%2C1173003&rt1=&rt2=%EC%95%BC%EB%8B%B9%EC%97%AD&rtIds=%2C&rtTypes=%2C')

    logout = st.button('로그아웃')
    if logout:
        st.session_state.clear()
        # st.experimental_rerun()
        switch_page('club')

if st.button('홈으로'):
    switch_page('club')
