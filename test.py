import streamlit as st

st.title("ISSUE TREE")
st.text_input("오류 메시지를 입력해주세요.")

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

# st.multiselect 초기화
options = st.multiselect(
    'filter',
    checkbox_labels,
    default=[]
)


# 세션 상태 초기화
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []

# 옵션이 변경될 때 세션 상태 업데이트
st.session_state.selected_options = options

# st.sidebar.checkbox 업데이트
for label in checkbox_labels:
    checked = label in options
    st.sidebar.checkbox(label, value=checked, key=label)