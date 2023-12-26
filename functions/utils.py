import re
import pandas as pd
import streamlit as st
from datetime import datetime


class SaveResult:
    def __init__(self):
        self.iter = 0
        self.save_dict = {}
    
    def save(self, purpose: str, template: str, result: str):
        temp = {
            "timestamp": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "purpose": purpose,
            "template": template,
            "result": result
        }
        self.save_dict[self.iter] = temp
        self.iter += 1
        
    def get(self):
        return pd.DataFrame(self.save_dict).T


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        st.session_state["message"].append({"message": message, "role": role})
       
        
def paint_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], save=False)


def preprocessing_question(input):
    # html 태그 제거
    input = re.sub(r"<b>|</b>|<br>|</br>", "", input)

    # 레이텍 함수 치환
    input = re.sub(r"\[|\]", "$$", input)

    # [3pt], [5pt] 등의값 제거
    input = re.sub(r"\[\d+pt\]", "", input)

    # 이미지 제거
    input = re.sub(r"#\[[^\]]+\]#", "", input)
    
    # 유니코드 화살표 변환
    input = re.sub(r"unicode{x27AD}", "rightarrow", input)
    
    # 레이텍 align 함수 치환
    input = re.sub(r"(\\begin{align\*}.+?\\end{align\*})", r"$$\1$$", input, flags=re.DOTALL)

    # 마지막에 \n 및 띄어쓰기 정리
    input = input.replace("\n", "").rstrip().lstrip()
    
    return input



def preprocessing_explanation(input):
    # html 태그 제거
    input = re.sub(r"<b>|</b>|<br>|</br>", "", input)

    # [3pt], [5pt] 등의값 제거
    input = re.sub(r"\\?\[\d+pt\]", "", input)
    
    # 레이텍 함수 치환
    # input = re.sub(r"\[|\]", "$", input)
    input = input.replace('\[', '$$').replace('\]', '$$')

    # 이미지 제거
    input = re.sub(r"#\[[^\]]+\]#", "", input)
    
    # 유니코드 화살표 변환
    input = re.sub(r"unicode{x27AD}", "rightarrow", input)

    # 마지막에 \n 및 띄어쓰기 정리
    input = input.replace("\n", "").rstrip().lstrip()
    
    return input


def render_latex_for_streamlit(text):
    """
    주어진 텍스트 내의 LaTeX 수식을 포함하여 Streamlit에 맞게 렌더링하는 함수입니다.
    (1) \begin{align*} 후 엔터
    (2) \begin{align*} ... \end{align*}이 한 줄
    (3) \begin{align*} ... \end{align*}이 한 줄 + 한글

    :param text: 처리할 전체 텍스트
    """
    # align* 환경이 시작되었는지 추적
    in_align_block = False
    align_block = ""

    lines = text.split('\n')
    for line in lines:
        # 한 줄로 나오는 경우
        if line.startswith("$$") and line.endswith("$$"):
            if line[2:].startswith('\x08'):
                st.latex(r"\b" + line[3:])
        elif r"\begin{align*}" in line:
            in_align_block = True
            align_block += line + '\n'
        elif r"\end{align*}" in line:
            in_align_block = False
            align_block += line
            st.latex(align_block)
            align_block = ""
        elif in_align_block:
            align_block += line + '\n'
        else:
            st.markdown(line)