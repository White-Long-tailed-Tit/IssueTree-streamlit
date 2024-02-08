# app1.py와 app2.py 통합 코드 

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


#제목 
st.title("IssueTree Search")

#text input: 오류 메시지 input
search_text =st.text_input(
  '오류메시지 검색',
  placeholder='오류메시지를 입력해주세요 ',
  help='Help message goes here'
)

#부제목(결과)
st.subheader(
  'results'
)

## branch geemgaeun codes 

# 왼쪽 사이드바
st.sidebar.header('filter')
option1 = st.sidebar.checkbox('spring-boot-starter-data-jpa')
option2 = st.sidebar.checkbox('spring-boot-starter-data-jdbc')
option3 = st.sidebar.checkbox('lombok')
option4 = st.sidebar.checkbox('spring-boot-starter-test')

st.sidebar.write('')
st.sidebar.subheader('문제 해결이 되지 않았다면 !')
sos_button = st.sidebar.button('SOS')

# 세션 상태 초기화
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []

# 옵션이 변경될 때 세션 상태 업데이트
st.session_state.selected_options = []

if option1:
    st.session_state.selected_options.append('spring-boot-starter-data-jpa')
if option2:
    st.session_state.selected_options.append('spring-boot-starter-data-jdbc')
if option3:
    st.session_state.selected_options.append('lombok')
if option4:
    st.session_state.selected_options.append('spring-boot-starter-test')

# st.multiselect 초기화
options = st.multiselect(
    'filter',
    ['spring-boot-starter-data-jpa', 'spring-boot-starter-data-jdbc', 'lombok', 'spring-boot-starter-test'],
    default=st.session_state.selected_options
)


## branch 'kjy' codes


# 샘플 데이터프레임 생성
data = {'document': [
      "Exception in thread 'main' java.lang.UnsupportedClassVersionError.txt",
      "could not prepare statement; SQL; nested exception is org.hibernate.exception.SQLGrammarException.txt",
      "variable not initialized in the default constructor 에러, class lombok.javac.apt.lombokprocessor cannot access class .txt"
    ],
        'springboot version': [3.1, 2.2, 2.4],
        'library':['JPA','lombok','jdbc'],
        'date': ['2024.02.02', '2022.01.11', '2021.01.01'],
        }
df = pd.DataFrame(data)

# 입력한 텍스트를 포함하는 문서 필터링
filtered_df = df[df['document'].str.contains(search_text)]

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





