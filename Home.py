import streamlit as st

# 애플리케이션의 제목 설정
st.title('Chat bot 검증사이트')

# 사이드바 생성
sidebar = st.sidebar
sidebar.header('문제/해설 입력')

# 사이드바에 텍스트 입력 필드 추가
question_input = sidebar.text_area('문제 입력')
answer_input = sidebar.text_area('해설 입력')


# 상단의 단일 텍스트 박스 추가
text_box_top = st.text_area("Prompt 입력 데이터(전처리", "", height=100)

# HTML/CSS를 사용하여 테두리가 있는 텍스트 박스 생성
st.markdown('<style>div.stTextInput>div{border:2px solid #4CAF50;}</style>', unsafe_allow_html=True)

# 두 개의 열 생성
col1, col2 = st.columns(2)

# 첫 번째 열에 테두리가 있는 텍스트 박스 추가
with col1:
    text_box1 = st.text_area("결과 1 raw data", "", height=100)

# 두 번째 열에 테두리가 있는 텍스트 박스 추가
with col2:
    text_box2 = st.text_area("결과 2 latex", "", height=100)


# 사이드바에 버튼 추가
if sidebar.button('버튼 클릭'):
    print("TODO 전처리 및 결과 로직")
