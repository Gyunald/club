import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_extras.switch_page_button import switch_page

from firebase_admin import firestore

@st.cache_data()
def load_lottie(url:str):
    r = requests.get(url)

    if r.status_code != 200:
        return None
    return r.json()

def disabled_참():
    st.session_state.disabled_참 = True
    st.session_state.disabled_불참 = False
def disabled_불참():
    st.session_state.disabled_참 = False
    st.session_state.disabled_불참 = True
    
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
        club = st.selectbox('club',[st.session_state.club])
        date = st.date_input('날짜',(datetime.datetime.utcnow()+datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
        time = st.time_input('시간',value= datetime.time(17,45)).strftime('%H:%M')

        empty = st.empty()
        place = empty.selectbox('장소',st.session_state.place)
        button_place = st.form_submit_button('장소추가',use_container_width=True)
        button_place_del = st.form_submit_button('장소삭제',use_container_width=True)
        if button_place:
            place = empty.text_input('place',placeholder='장소 직접입력 후 리스트에 추가')
            if place != '' and place not in st.session_state.place:
                st.session_state.place.append(place)
                place = empty.selectbox('place',st.session_state.place,key='place_append')
                st.experimental_rerun()

        if button_place_del:
            if place not in st.session_state.place:
                st.session_state.place.remove(place)
                st.experimental_rerun()
        data = { f"{date}-{place}" : {
            '시간' : time,
            '날짜' : date,
            '장소' : place,
            '참가자' : [],
            '참여' : {},
            '불참' : {},
            '작성자' : nickname,
        }}
        doc_ref = st.session_state.doc_ref.document(club)

        submitted = st.form_submit_button('모임등록',use_container_width=True,type='primary')
        date_check = data[f"{date}-{place}"].get('날짜') +'-'+ data[f"{date}-{place}"].get('장소')

        if submitted :
            if date_check not in doc_ref.get().to_dict():
                doc_ref.update(data)
                
            else:
                st.warning('이미 같은장소에 모임이 있습니다.')

    st.write('---')
    rerun = st.button('새로고침')

    if rerun:
        st.experimental_rerun()

    c = st.columns(3)    
    doc = doc_ref.get().to_dict()
    doc_time = (datetime.datetime.utcnow()+datetime.timedelta(hours=9)).strftime('%Y-%m-%d-%H:%M')

    for i,j in zip(range(len(c)), sorted(doc.keys(),reverse=True)):
        doc_document = doc[j]
        doc_list = doc_document.get('참가자')
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
                st.header(f"{doc_document.get('날짜')}")
                st.header(f"{doc_document.get('시간')}")
                st.subheader(f"{doc_document.get('장소')}")
                참 = st.form_submit_button('참여',on_click=disabled_참, disabled=st.session_state[k],use_container_width=True,type='primary')
                불참 = st.form_submit_button('불참', on_click=disabled_불참, disabled=st.session_state[k],use_container_width=True)
                if doc_document.get('작성자') == nickname:
                    삭제 = st.form_submit_button('삭제',use_container_width=True,type='primary')
                    if 삭제:
                        check = st.text_input('렬루?',placeholder="'y' 치고 클릭").lower()
                        if check == 'y':
                            doc_ref.update({f"{doc_document.get('날짜')}-{doc_document.get('장소')}" : firestore.DELETE_FIELD})
                            st.experimental_rerun()
                if 참 :
                    if len(doc_list) < 2:
                        doc_application = doc_document.get('참여')
                        if nickname not in doc_list:
                            doc_list.append(nickname)
                            doc_application[nickname] = doc_time
                        doc_ref.update(doc)
                        st.balloons()

                if 불참:
                    doc_cancel = doc_document.get('불참')
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
                place_naver = doc_document.get('장소').replace(' ','')
                place_kakao = doc_document.get('장소').replace(' ','')
                url_naver = f'https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start=126.7626527103602,37.763437024584206,&&goal=126.791850394664,37.7224135020587'
                url_kakao = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={place_kakao}"
                headers_naver = {
                    'X-NCP-APIGW-API-KEY-ID' : 'foqwb8f3u4',
                    'X-NCP-APIGW-API-KEY' : 'Ntqm83lBU8FPINuJ0kOnn5GAhf4xhQUARhwVupgx'}
                
                headers_kakao = {"Authorization" : "KakaoAK 5112b33d653427be0da4daf5aac8a437"}
                
                res_naver = requests.get(url_naver,headers=headers_naver).json()
                res_kakao = requests.get(url_kakao,headers=headers_kakao).json()['documents'][0]
                x,y = res_kakao['y'], res_kakao['x']
                
                st.success('[🚕 네이버지도](%s)' % f"https://map.naver.com/v5/directions/-/{y},{x},{place_kakao},,PLACE_POI/-/car?c=16.22,0,0,0,dh&isCorrectAnswer=true")
                st.warning('[🚗 카카오맵](%s)' % f'https://map.kakao.com/link/to/{place_kakao},{x},{y}')

    logout = st.button('로그아웃',type='primary')
    if logout:
        st.session_state.clear()
        switch_page('home')

if st.button('홈으로'):
    switch_page('home')
