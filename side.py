import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu
from streamlit_tags import st_tags
import streamlit.components.v1 as components

def main_page():
    #title
    st.markdown("<h1 style='text-align: center; color: black;'>IssueTree Search</h1>", unsafe_allow_html=True)


    data = {
        'document': [
            "Exception in thread 'main' java.lang.UnsupportedClassVersionError.txt",
            "could not prepare statement; SQL; nested exception is org.hibernate.exception.SQLGrammarException.txt",
            "variable not initialized in the default constructor 에러, class lombok.javac.apt.lombokprocessor cannot access class .txt"
        ],
        'springboot version': [3.1, 2.2, 2.4],
        'library': ['JPA', 'lombok', 'jdbc'],
        'date': ['2024.02.02', '2022.01.11', '2021.01.01'],
    }
    df = pd.DataFrame(data)

    #text input: 오류 메시지 input
    search_text = st.text_input(
        '오류메시지 검색',
        placeholder='오류메시지를 입력해주세요 ',
        help='Help message goes here'
    )

    options = df['document'].unique().tolist()

    #filter
    with st.expander('Filter'):
        col1, col2 = st.columns(2)

        with col1:
            tag_springbootversion = st_tags(
                text='',
                label='springboot version',
                key='1'
                )
            
        with col2:
            tag_library = st_tags(
                text='',
                label='library',
                key='2'
                )
        
        min_date = datetime.datetime(2010,1,1)
        max_date = datetime.date.today()
        a_date = st.date_input("date",(min_date, max_date), key='d_key')
        if len(a_date) != 2:
            st.stop()

        # 날짜 초기화 버튼
        def reset():
            st.session_state.d_key = (min_date, max_date)  

        st.button('reset the date', on_click=reset)
        

    # 입력한 텍스트를 포함하는 문서 필터링
    filtered_df = df[df['document'].str.contains(search_text)]

    # 추가한 태그에 따라 필터링
    if len(tag_library) > 0:
        filtered_df = filtered_df[filtered_df['library'].apply(lambda x: any(tag.lower() in x.lower() for tag in tag_library))]

    if len(tag_springbootversion) > 0:
        filtered_df = filtered_df[filtered_df['springboot version'].astype(str).apply(lambda x: any(tag.lower() in x.lower() for tag in tag_springbootversion))]

    a_date_start = datetime.datetime.combine(a_date[0], datetime.datetime.min.time())
    a_date_end = datetime.datetime.combine(a_date[1], datetime.datetime.max.time())
    filtered_df = filtered_df[pd.to_datetime(filtered_df['date']).between(a_date_start, a_date_end)]

    #부제목(결과)
    st.subheader('results')

    def dataframe_with_selections(df):
        df_with_selections = df.copy()
        df_with_selections.insert(0, "Select", False)
        edited_df = st.data_editor(
            df_with_selections,
            width=1500,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
        )
        selected_rows = df[edited_df.Select]
        return {"selected_rows": selected_rows}

    # 결과값이 없는 경우 처리
    if filtered_df.empty:
        st.write("We couldn't find anything :sob:")
        # sos 버튼
        st.subheader('need help?')
        with st.expander('**Request Body**'):
            with st.form('Request Body'):
                st.text_input('Reporter Name')
                st.text_input('Package Name')
                st.text_input('Error Message')
                st.text_input('Manager Github Id')
                st.text_input('Comment')
                st.text_input('Stack')
                st.text_input('Version')

                #submit button
                submitted = st.form_submit_button('SOS')

    else:
        selection = dataframe_with_selections(df)
        if selection['selected_rows'] is not None and not selection['selected_rows'].empty:
            doc_name = selection['selected_rows'].iloc[0]['document']
            st.write(f"Selected Document: {doc_name}")


def dashboard(): # 대시보드 페이지 실행 함수
    #title
    st.markdown("<h1 style='text-align: center; color: black; width: 100%;'>Dashboard</h1>", unsafe_allow_html=True)

    iframe_src = "https://smw-whiteeye.kb.us-west-2.aws.found.io:9243/app/dashboards#/view/14342cf1-162e-4a2c-b042-a8328b0232eb?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A60000)%2Ctime%3A(from%3Anow-1M%2Cto%3Anow))&show-top-menu=true&show-query-input=true&show-time-filter=true"
    components.iframe(iframe_src, height=950, scrolling=True)

def side(): #사이드바 실행 함수 
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'DashBoard','Settings'], 
            icons=['house','bar-chart', 'gear'], menu_icon="cast", default_index=0)

    if selected == "Home":
        main_page() #홈이 선택되면 main_page를 보여줌 
    elif selected == "DashBoard":
        dashboard()
    elif selected == "Settings":
        st.write("Settings is selected")



# import side from side.py 방식으로 불러와서 app.py에서 side() 사용하시면 됨 