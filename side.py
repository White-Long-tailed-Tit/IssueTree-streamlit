import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu
from streamlit_tags import st_tags
import streamlit.components.v1 as components
import es_con 
import sos
import json
import re 

def main_page():
    #title
    st.markdown("<h1 style='text-align: center; color: black;'>IssueTree Search</h1>", unsafe_allow_html=True)

    data=es_con.connect() #elasticsearch 연결 후 전체 데이터 목록 
    
    df = pd.DataFrame(data)

    #text input: 오류 메시지 input
    search_text = st.text_input(
        '오류메시지 검색',
        placeholder='오류메시지를 입력해주세요 ',
        help='Help message goes here'
    )
    # 입력된 문자열을 raw string으로 변환
    search_text = r'''{}'''.format(search_text)

    #options = df['document'].unique().tolist()

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
    filtered_df = df[df['issue'].str.contains(search_text)]

    # 추가한 태그에 따라 필터링
    if len(tag_library) > 0:
        filtered_df = filtered_df[filtered_df['stack'].apply(lambda x: any(tag.lower() in x.lower() for tag in tag_library))]

    if len(tag_springbootversion) > 0:
        filtered_df = filtered_df[filtered_df['version'].astype(str).apply(lambda x: any(tag.lower() in x.lower() for tag in tag_springbootversion))]

    a_date_start = datetime.datetime.combine(a_date[0], datetime.datetime.min.time())
    a_date_end = datetime.datetime.combine(a_date[1], datetime.datetime.max.time())
    #filtered_df = filtered_df[pd.to_datetime(filtered_df['lastModifiedDate']).between(a_date_start, a_date_end)]

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

        # 에러 메시지 parsing
        package, file_path, isLine,line =sos.parsing(search_text)
        author_name=None
        author_email=None
        
        

        if not(package==None or file_path==None): #패키지명 파싱 가능한 경우
            # GitHub 저장소 정보
            owner = 'White-Long-tailed-Tit'
            repo = 'IssueTree-Spring'
            branch = 'main'
            token = ''

            if isLine: #라인 넘버 추출 가능한 오류 메시지인 경우 
                blame_data=sos.get_git_blame_line(owner, repo, file_path, token, branch)
                # JSON 문자열을 파이썬 딕셔너리로 변환
                blame_data_dict = json.loads(blame_data)

                # line 값이 있는지 확인하고 해당하는 author의 name과 email 추출
                for range_data in blame_data_dict['data']['repository']['object']['blame']['ranges']:
                    if line >= range_data['startingLine'] and line <= range_data['endingLine']:
                        author_name = range_data['commit']['author']['name']
                        author_email = range_data['commit']['author']['email']
                        print("Author Name:", author_name)
                        print("Author Email:", author_email)
                        break
            else: #라인 넘버 추출 x, 패키지명만 가능한 경우 
                final_commit_data=sos.get_bit_blame(owner, repo, file_path, token, branch)
                final_commit_dict=json.loads(final_commit_data)

                author_name = final_commit_dict['author']
                author_email = final_commit_dict['email']

                print("Author:", author_name)
                print("Email:", author_email)
            

        with st.expander('**Request Body**'):
            with st.form('Request Body'):
                reporter_name=st.text_input('Reporter Name')
                package_input=st.text_input('Package Name',value=package)
                error_msg=st.text_input('Error Message',value=search_text)
                manager=st.text_input('Manager Github Id',value=author_name)
                comment=st.text_input('Comment')
                stack=st.text_input('Stack')
                version=st.text_input('Version')
              
                #submit button
                submitted = st.form_submit_button('SOS')
                if submitted:
                    sos.send_form(reporter_name,package_input,error_msg,manager,comment,
                              stack,version)


    else:
        selection = dataframe_with_selections(df)
        if selection['selected_rows'] is not None and not selection['selected_rows'].empty:
            doc_name = selection['selected_rows'].iloc[0]['issue']
            st.write(f"Selected Document: {doc_name}")


def dashboard(): # 대시보드 페이지 실행 함수
    #title
    st.markdown("<h1 style='text-align: center; color: black; width: 100%;'>Dashboard</h1>", unsafe_allow_html=True)

    iframeHTML = """
    <p 
        style="border:none; width:100%; height:800px;" 
        align="center"
    >
        <iframe
        style="border:none"
        height="100%"
        width="100%"
            src="https://smw-whiteeye.kb.us-west-2.aws.found.io:9243/app/dashboards#/view/14342cf1-162e-4a2c-b042-a8328b0232eb?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A60000)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))"> 
        </iframe>
    </p>
    """
    
    components.html(iframeHTML, height=4000, width=1000 )

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