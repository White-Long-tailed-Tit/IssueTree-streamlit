import streamlit as st
from streamlit_option_menu import option_menu

def main_page(): #메인페이지 
    st.title("IssueTree Search")

    search_text = st.text_input(
        '오류메시지 검색',
        placeholder='오류메시지를 입력해주세요 ',
        help='Help message goes here'
    )

    st.subheader('results')

def side(): #사이드바 실행 함수 
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'DashBoard','Settings'], 
            icons=['house','bar-chart', 'gear'], menu_icon="cast", default_index=0)

    if selected == "Home":
        main_page() #홈이 선택되면 main_page를 보여줌 
    elif selected == "DashBoard":
        st.write("Dashboard is selected")
    elif selected == "Settings":
        st.write("Settings is selected")


# import side from side.py 방식으로 불러와서 app.py에서 side() 사용하시면 됨 
