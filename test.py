import streamlit as st

# 애플리케이션의 제목 설정
st.title('Chat bot 검증사이트')

# 사이드바 생성
sidebar = st.sidebar
sidebar.header('문제/해설 입력')

# 사이드바에 옵션 추가
option = sidebar.selectbox(
    'Version 선택',
    ('version 1', 'version 2')
)

# 메인 페이지에 선택된 옵션 표시
st.write(f'선택한 옵션: {option}')

# 사이드바에 텍스트 입력 필드 추가
question_input = sidebar.text_area('문제 입력')
answer_input = sidebar.text_area('해설 입력')

# 메인 페이지에 사용자 입력 표시
st.write(f'Prompt 입력 데이터(전처리): {question_input}')

# 사이드바에 버튼 추가
if sidebar.button('버튼 클릭'):
    print("TODO 전처리 및 결과 로직")
