import streamlit as st
from streamlit_option_menu import option_menu

def main_page():
    st.title("IssueTree Search")

    search_text = st.text_input(
        '오류메시지 검색',
        placeholder='오류메시지를 입력해주세요 ',
        help='Help message goes here'
    )

    st.subheader('results')

def main():
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'DashBoard','Settings'], 
            icons=['house','bar-chart', 'gear'], menu_icon="cast", default_index=0)

    if selected == "Home":
        main_page()
    elif selected == "DashBoard":
        st.write("Dashboard is selected")
    elif selected == "Settings":
        st.write("Settings is selected")

if __name__ == "__main__":
    main()

