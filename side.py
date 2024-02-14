import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_tags import st_tags
import streamlit.components.v1 as components

def main_page():

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

    # 결과값이 없는 경우 처리
    if filtered_df.empty:
        st.write("We couldn't find anything :sob:")
        # sos 버튼
        st.subheader('need help?')
        st.button('SOS')
    else:
        # Configure grid options using GridOptionsBuilder
        builder = GridOptionsBuilder.from_dataframe(filtered_df)
        builder.configure_pagination(enabled=True)
        builder.configure_selection(selection_mode='single', use_checkbox=False)
        grid_options = builder.build()

        # Display AgGrid
        return_value = AgGrid(filtered_df, gridOptions=grid_options)
        if return_value['selected_rows']:
            doc_name = return_value['selected_rows'][0]['document']
            st.write(f"Selected System Name: {doc_name}")
        else:
            st.write("")

def dashboard(): # 대시보드 페이지 실행 함수
    iframeHTML = """
    <p 
        align="center"
        height="500"
        width="100%"
    >
        <iframe
        style="border:none"
        height="500"
        width="100%"
            src="https://smw-whiteeye.kb.us-west-2.aws.found.io:9243/app/dashboards#/view/14342cf1-162e-4a2c-b042-a8328b0232eb?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A60000)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))"> 
        </iframe>
    </p>
    """
    
    components.html(iframeHTML, height=500 )

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
