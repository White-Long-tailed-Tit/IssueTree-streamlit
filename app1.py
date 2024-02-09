import streamlit as st
import pandas as pd
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_tags import st_tags

# 샘플 데이터프레임 생성
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

#제목 
st.title("IssueTree Search")

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
            key='2',
            )

    min_date = datetime.datetime(2010,1,1)
    max_date = datetime.date.today()
    a_date = st.date_input("date",(min_date, max_date))

    if len(a_date) != 2:
        st.stop()

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