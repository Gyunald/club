import pandas as pd
import streamlit as st
from datetime import datetime, timedelta, time
import requests
from streamlit_extras.switch_page_button import switch_page
from firebase_admin import firestore


st.set_page_config(
    page_title="😎",
    # initial_sidebar_state="collapsed",
)

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

if 'type_참' not in st.session_state:
    st.session_state.type_참 = ''
    st.session_state.type_불참 = ''

db = firestore.client()

nickname = st.session_state.nickname
now_date = (datetime.utcnow()+timedelta(hours=9))
max_date = now_date.replace(year=now_date.year+1,month=1,day=1) - timedelta(days=1)

if nickname :
    if st.session_state.club != '' :
        st.write(f"### Hi, {nickname}🎈")
        with st.expander('모임생성'):
            with st.form("my_form",clear_on_submit=True):
                club = st.selectbox('클럽',[st.session_state.club])
                date = st.date_input('날짜',value=now_date,min_value=now_date,max_value=max_date).strftime('%m-%d')
                times = st.time_input('시간',value= time(17,30)).strftime('%H:%M')

                empty = st.empty()
                place = empty.selectbox('장소',st.session_state.place,help='장소를 직접 입력하려면 장소추가 버튼을 누르세요.')
                people = st.number_input('정원',value=10,max_value=30,help='최대인원 30명')
                button_place = st.form_submit_button('장소추가',use_container_width=True)
                button_place_del = st.form_submit_button('장소삭제',use_container_width=True)
                if button_place:
                    place = empty.text_input('place',placeholder='장소를 정확하게 입력하세요.',max_chars=30,help='장소추가 버튼을 한번 더 누르세요.')
                    if place != '' and place not in st.session_state.place:
                        st.session_state.place.append(place)
                        place = empty.selectbox('place',st.session_state.place,key='place_append')
                        st.experimental_rerun()

                if button_place_del:
                    if place not in st.session_state.place:
                        st.session_state.place.remove(place)
                        st.experimental_rerun()

                data = { f"{date}-{place}" : {
                    '시간' : times,
                    '날짜' : date,
                    '장소' : place,
                    '참가목록' : [],
                    '인원수' : 0,
                    '불참가목록' : [],
                    '참여' : {},
                    '불참' : {},            
                    '작성자' : nickname,
                }}
                doc_ref = st.session_state.doc_ref.document(club)

                submitted = st.form_submit_button('모임등록',use_container_width=True,type='primary')
                date_check = data[f"{date}-{place}"].get('날짜') +'-'+ data[f"{date}-{place}"].get('장소')

                if submitted :
                    if date_check not in doc_ref.get().to_dict() :
                        st.warning('모임이 생성되었습니다.')
                        doc_ref.update(data)

                    else:
                        st.warning('이미 같은장소에 모임이 있습니다.')

#         st.write('---')
        # rerun = st.button('새로고침')

        # if rerun:
        #     st.experimental_rerun()

        c = st.columns(3)    
        doc = doc_ref.get().to_dict()
        doc_time = now_date.strftime('%Y-%m-%d-%H:%M')

        for i,j in zip(range(len(c)), sorted(doc.keys(),reverse=True)):
            doc_document = doc[j]
            doc_list = doc_document.get('참가목록')
            doc_list_non = doc_document.get('불참가목록')
            standard = now_date.strftime('%m-%d') > doc_document['날짜']
            
            k = f"disabled_{j}"
            if k not in st.session_state:
                st.session_state[k] = False

            if doc_document['인원수'] == people:
                st.session_state[k] = True
                if nickname in doc_list:
                    st.session_state[k] = False

            if standard:
                st.session_state[k] = True

            if nickname in doc_list:
                st.session_state.type_참 = 'primary'
                st.session_state.type_불참 = 'secondary'
                
            elif nickname in doc_list_non:
                st.session_state.type_참 = 'secondary'
                st.session_state.type_불참 = 'primary'

            else: 
                st.session_state.type_참 = 'secondary'
                st.session_state.type_불참 = 'secondary'

            with c[i]:
                with st.form(j):
                    st.write(f"##### {doc_document.get('날짜')} 🏸 {doc_document.get('시간')}")
                    st.write(f"{doc_document.get('장소')}")
                    
                    참 = st.form_submit_button('참여',on_click=disabled_참, disabled=st.session_state[k],use_container_width=True, type= st.session_state.type_참)
                    불참 = st.form_submit_button('불참', on_click=disabled_불참, disabled=st.session_state[k],use_container_width=True,type= st.session_state.type_불참)
                    if doc_document.get('작성자') == nickname:
                        삭제 = st.form_submit_button('삭제',use_container_width=True,type='primary')
                        if 삭제:
                            check = st.text_input('렬루?',placeholder="'y' 치고 클릭").lower()
                            if check == 'y':
                                doc_ref.update({f"{doc_document.get('날짜')}-{doc_document.get('장소')}" : firestore.DELETE_FIELD})
                                st.experimental_rerun()
                    if 참 :
                        if doc_document['인원수'] < people:
                            doc_application = doc_document.get('참여')
                            if nickname not in doc_list:
                                doc_list.append(nickname)
                                doc_document['인원수'] +=1
                                doc_application[nickname] = doc_time
                                if nickname in doc_list_non:
                                    doc_list_non.remove(nickname)
                            doc_ref.update(doc)
                            st.experimental_rerun()

                    if 불참:
                        doc_cancel = doc_document.get('불참')
                        if nickname not in doc_list_non :
                            doc_list_non.append(nickname)                        
                            doc_cancel[nickname] = doc_time
                            if nickname in doc_list:
                                doc_list.remove(nickname)
                                doc_document['인원수'] -=1
                        doc_ref.update(doc)
                        st.experimental_rerun()
                        
                    with st.expander('인원'):
                        if not doc_list:
                            st.info('🙈')
                        else:
                            st.info(doc_list)
                        
                        if not doc_list_non:
                            st.error('🙉')
                        else:
                            st.error(doc_list_non)

                    if doc_document['인원수'] == people:
                        st.error(f"{doc_document['인원수']}/{people} 명")
                        if nickname in doc_list:
                            st.session_state.disabled_불참 = False
                        else:
                            st.session_state.disabled_참 = True
                            st.session_state.disabled_불참 = True
                    else:
                        st.info(f"{doc_document['인원수']}/{people} 명")
                        
                    word = doc_document.get('장소').replace(' ','')
                    st.success('[🚕 네이버지도](%s)' % f"https://map.naver.com/v5/search/{word}")
                    st.warning('[🚗 카카오맵](%s)' % f'https://map.kakao.com/link/search/{word}')
                    
        logout = st.button('로그아웃',type='primary')
        if logout:
            st.session_state.clear()
            switch_page('home')
    else:
        st.warning('홈에서 클럽을 선택하세요.')
else:
        st.warning('홈에서 로그인하세요.')

if st.button('홈으로'):
    switch_page('home')
