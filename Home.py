import streamlit as st
import re

# def replace_text(input_text):
#     # img 태그 제거
#     input_text = re.sub(r'<img[^>]*>', '', input_text)

#     # <br> 태그 제거
#     input_text = input_text.replace('<br>', '')

#     # <b> 태그 제거 (여는 태그와 닫는 태그 모두 제거)
#     input_text = re.sub(r'</?b>', '', input_text)

#     # [ ] -> $ $ 로 변경
#     input_text = input_text.replace('[', '$').replace(']', '$')

#     return input_text

st.set_page_config(
    page_title="Home",
    page_icon="🥕",
)

# 애플리케이션의 제목 설정
st.title('Chat bot 검증사이트')

# # 사이드바 생성
# sidebar = st.sidebar
# sidebar.header('문제/해설 입력')

# # 사이드바에 텍스트 입력 필드 추가
# question_input = sidebar.text_area('문제 입력')
# answer_input = sidebar.text_area('해설 입력')

# # HTML/CSS를 사용하여 테두리가 있는 텍스트 박스 생성
# st.markdown('<style>div.stTextInput>div{border:2px solid #4CAF50;}</style>', unsafe_allow_html=True)

# # 상단의 단일 텍스트 박스 추가
# text_box_1 = st.text_area("Prompt 입력 데이터(전처리", replace_text(question_input), height=100)
# text_box_2 = st.text_area("결과 1 raw data", "", height=100)
# text_box_3 = st.text_area("결과 2 latex", "", height=100)

# # 사이드바에 버튼 추가
# if sidebar.button('버튼 클릭'):
#     print(question_input)
#     print(answer_input)
#     print("TODO 전처리 및 결과 로직")


st.markdown(
    """
    ### 좌측 사이드 바에서 챗봇을 선택해주세요 :)
    """
)


