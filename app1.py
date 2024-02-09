import streamlit as st
from streamlit_tags import st_tags

st.title("ISSUE TREE")
st.text_input("오류 메시지를 입력해주세요.")

# 왼쪽 사이드바
st.sidebar.header('asdf')

# filter
keywords = st_tags(
    ['spring-boot-starter-data-jpa', 'spring-boot-starter-data-jdbc', 'lombok', 'spring-boot-starter-test'],
    text='',
    label='Filter',
    suggestions=['spring-boot-starter-data-jpa', 'spring-boot-starter-data-jdbc', 'lombok', 'spring-boot-starter-test'],
    key='1')