
# import streamlit as st
# from datetime import datetime,timedelta
# from streamlit_server_state import server_state, server_state_lock, no_rerun
# from streamlit_extras.switch_page_button import switch_page
# empty = st.empty()
# if 'nickname' not in st.session_state:
#     nickname = st.text_input('닉네임 입력(추후 회원기능 도입)')
#     st.session_state.nickname = nickname
# else:
#     nickname = empty.text_input('닉네임 입력(추후 회원기능 도입)',value=st.session_state.nickname)
#     st.session_state.nickname = nickname
# nickname = st.session_state.nickname
# st.write(f"### Hi, {nickname}🎈")
# e =st.empty()
# if nickname:
#     switch_page('chat')


import streamlit as st
from datetime import datetime,timedelta
from streamlit_server_state import server_state, server_state_lock, no_rerun

def on_message_input():
    new_message_text = st.session_state["message_input"]
    
#     st.session_state["message_input"] = ""
    
    server_state["user"] = [nickname]

    if not new_message_text:
        return

    new_message_packet = {
        "nickname": nickname,
        "text": new_message_text,
        "time": (datetime.utcnow()+timedelta(hours=9)).strftime('%H:%M:%S')
    }

    with server_state_lock["chat_messages"]:
            server_state["chat_messages"] = server_state["chat_messages"] + [
                f"{new_message_packet['nickname']} : {new_message_packet['text']} \n {new_message_packet['time']}"
            ]
empty = st.empty()      
if 'nickname' not in st.session_state:
    nickname = st.text_input('Nickname)')
    st.session_state.nickname = nickname
nickname = st.session_state.nickname

if nickname :
    empty = st.empty()
    st.write(f"### Hi, {nickname}🎈")

    with server_state_lock["chat_messages"]:    
        if "chat_messages" not in server_state:
            server_state["chat_messages"] = []

    if "user" not in server_state:
        server_state["user"] = []

    else:
        if nickname not in server_state["user"]:
            server_state["user"] = [nickname] + server_state["user"]

    if st.button('claer'): 
        server_state["chat_messages"] = []

    if st.button('session_clear'): 
        st.session_state.clear()
        server_state.clear()

    st.info('\n'.join(set(server_state["user"])))
    st.text_input("Message",key="message_input",on_change=on_message_input)

    st.text_area('Chat','\n'.join(server_state["chat_messages"][::-1]), height=150)

    st.write(server_state.chat_messages)
    st.write(st.session_state.message_input)
    st.write(server_state.user)
