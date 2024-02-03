import streamlit as st
from tkinter.tix import COLUMN
from pyparsing import empty

st.title("IssueTree")
# 왼쪽 사이드바 생성
st.sidebar.header('filter')

# 체크박스 추가
option1 = st.sidebar.checkbox('lombok', True)
option2 = st.sidebar.checkbox('spring-boot-starter-data-jpa')

# 체크박스의 값을 사용하여 다른 작업 수행
if option1:
    st.write('lombok이 선택되었습니다.')

if option2:
    st.write('spring-boot-starter-data-jpa가 선택되었습니다.')

st.text_input(
  '오류메시지 검색',
  placeholder='오류메시지를 입력해주세요 ',
  help='Help message goes here'
)


st.subheader(
  'results'
)

st.selectbox(
  '정렬',
  ('해결순','최신순'),
  help='Help message goes here'
)