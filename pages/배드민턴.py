import streamlit as st
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page

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

st.success('[지도](%s)' % 'https://map.naver.com/v5/directions/-/14114858.818669442,4540450.617396284,%EC%97%90%EC%9D%B4%EC%9B%90%EB%AF%BC%ED%84%B4%20%EC%9D%BC%EC%82%B0%EC%A0%90,1328259034,PLACE_POI/-/transit?c=14114507.1137752,4540282.9324362,15,0,0,0,dh&isCorrectAnswer=true')

st.write("배드민턴")
if st.button('홈으로'):
    switch_page('club')