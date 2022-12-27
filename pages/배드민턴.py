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

st.success('[네이버지도](%s)' % 'https://map.naver.com/v5/directions/-/14114397.866921965,4540303.012815246,%EA%B3%A0%EC%96%91%ED%8C%A9%ED%86%A0%EC%8A%A4%ED%83%80%EB%94%94%EC%9B%80,1966063934,PLACE_POI/-/transit?c=14111433.1227196,4538425.9290852,12.89,0,0,0,dh')

st.warning('[카카오맵](%s)' % 'https://map.kakao.com/link/to/고양팩토스타디움,37.722334,126.791838')

st.write("배드민턴")
if st.button('홈으로'):
    switch_page('club')
