import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


# 문서 목록
documents = [
    "Exception in thread 'main' java.lang.UnsupportedClassVersionError.txt",
    "could not prepare statement; SQL; nested exception is org.hibernate.exception.SQLGrammarException.txt",
    "variable not initialized in the default constructor 에러, class lombok.javac.apt.lombokprocessor cannot access class .txt"
]

st.title("IssueTree Search")

search_text =st.text_input(
  '오류메시지 검색',
  placeholder='오류메시지를 입력해주세요 ',
  help='Help message goes here'
)

st.subheader(
  'results'
)

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
    st.write("No row selected")





# # 데이터프레임을 표로 표시
# st.dataframe(filtered_df)