import os
import sys
import streamlit as st
import pandas as pd


current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
for p in ['functions', 'src', 'template']:
    utils_path = os.path.join(parent_dir, p)
    sys.path.append(utils_path)

from utils import *
from chains import *


st.set_page_config(
    page_title="abstract",
    page_icon="🐹"
)


system_role = """
    You are a teacher who wants to provide step-by-step explanations tailored to the students' levels, so they can gradually solve the problems without giving up. 
    Please divide the given explanation into a process with at least 2 and at most 5 steps, depending on the length of the main content and the difficulty of the explanation.
    Each step must start with [1단계], [2단계], etc. 
    The answer should only appear at the end, and must not be mentioned in the stages like [1단계], [2단계]. 
    When dividing the steps, do not create new content that is unrelated to the explanation. 
    If the explanation is incorrect, it could lead the students to solve the problems incorrectly, so please make sure the LaTeX equations are correct. 
    """

explain_role = """
    You are a passionate and capable teacher who wants to help all students find mathematics enjoyable and encourage them not to give up even when it's tough. 
    You love your students very much, and they love you a lot too. 
    Your students are currently finding it difficult to understand math problems and explanations, even after reading them. 
    You want to kindly pinpoint the essentials of the problems and explain them in an easy-to-understand way for your beloved students. 
    Using the given Korean high school mathematics problems and explanations, please explain them in Korean in an easy-to-understand manner. 
    You must not create any wrong answers or incorrect explanations. 
    If the explanation is wrong, it could lead the students to solve the problems incorrectly, so please make sure the LaTeX equations are correct. 
    For a kind explanation, please try to end your sentences with '요' instead of '다'.
    """

split_role = """
    You are a teacher who wants to provide step-by-step explanations tailored to the students' levels, so they can gradually solve the problems without giving up. 
    Please divide the given explanation into a process with at least 2 and at most 5 steps, depending on the length of the main content and the difficulty of the explanation.
    Each step must start with [1단계], [1단계], etc. 
    The answer should only appear at [정답] at the end, and must not be mentioned in the stages like [1단계], [2단계]. 
    When dividing the steps, do not create new content that is unrelated to the explanation. 
    If the explanation is incorrect, it could lead the students to solve the problems incorrectly, so please make sure the LaTeX equations are correct. 
    Finally, for your beloved students, add encouraging words like '이를 이용하여 한 번 풀어볼까요?' at the end of each stage.
"""

question_role = """
    You are a passionate and capable teacher who wants all students to find mathematics enjoyable and to persevere without giving up, even when it's tough. 
    You deeply love your students, and they love you a lot too. 
    The students need to solve the given problems following the provided explanation steps, but they often struggle to understand these steps. 
    You want to help the students by asking them if they understand the key content required at each step. 
    It would be great if you could include the key content's latex formulas where possible. 
    For each step of the problem-solving process, create a minimum of 1 to a maximum of 3 questions about the key content. 
    If there are no questions to create, just skip with [질문 없음]. 
    Absolutely do not create questions unrelated to the explanation steps of the problem.
"""

# streamlit 사이드바 생성
with st.sidebar:
    choice = None
    explain_result = None
    split_result = None
    question_result = None
    final_result = None
    
    question_input = st.text_area("문제를 입력하세요")
    explanation_input = st.text_area("해설을 입력하세요")
    
    choice = st.selectbox(
        "답안 생성 타입을 선택해주세요",
        (
            "zero-shot",
            "few-shot",
        ),
        index=None,
    )
        
    if st.button('실행'):
        if question_input == "":
            raise ValueError("문제를 입력해야 합니다")
        if explanation_input == "":
            raise ValueError("해설을 입력해야 합니다")
        
        preprocessed_question = preprocessing_question(question_input)
        preprocessed_explanation = preprocessing_explanation(explanation_input)
        
        if choice == "zero-shot":
            explain_chain, split_chain, question_chain = get_chains(temperature=0.6, mode="zero-shot")
            
            with st.status("해설을 생성하는 중...") as status:
                explain_result = explain_chain.invoke({
                    "explain_role": explain_role,
                    "question": preprocessed_question,
                    "explanation": preprocessed_explanation,
                })

            with st.status("해설 단계를 나누는 중...") as status:
                split_result = split_chain.invoke({
                    "split_role": split_role,
                    "question": preprocessed_question,
                    "explanation": explain_result,
                })

            with st.status("단계별 질문을 생성하는 중...") as status:
                question_result = question_chain.invoke({
                    "question_role": question_role,
                    "question": preprocessed_question,
                    "steps": split_result,
                })
            
        else:
            final_chain = get_chains(temperature=0.5, mode="few-shot")
                       
            with st.status("해설을 생성하는 중...") as status:
                final_result = final_chain.invoke({
                    "system_role": system_role,
                    "question": preprocessed_question,
                    "explanation": preprocessed_explanation,
                })

        
# streamlit 페이지 생성
if choice is None:
    st.markdown(
        """
        ### 사용 방법
        1. [어드민 페이지](https://ai.matamath.net/admin/question)에서 원하는 문제를 선택한 후 문제의 개념/용어 태깅을 off한다
        2. 문제와 텍스트를 입력란에 복붙한다
        3. 답안 생성 타입을 선택한다
            * zero-shot: 답안 생성의 모든 과정을 chatGPT가 결정
            * few-shot: 예시 데이터와 같이 프롬프트(예시 데이터는 원길님이 제공해주셨습니다:smile:)
        4. 실행 버튼 클릭
        
        :heart: 개인적으로 답안 퀄리티는 few-shot이 좋은 것 같습니다!
            
        ---
        ### 앞으로 수정할 내용
        """
    )
    
    st.checkbox("latex rendering 수정")
    st.checkbox("few-shot 질문 생성")
    st.checkbox("퀄리티 측정 지표 생성")
    
    
    st.markdown("---")
    
    with st.expander("latex rendering 문제 기록"):
        st.markdown("__기록용입니다!!__")
        st.write(r"""
                주어진 유리함수를 정리하면 
                $$
                \begin{align*}y&=\dfrac{bx+4}{a-x}\\&=\dfrac{-b(a-x)+ab+4}{a-x}\\&\;=\dfrac{ab+4}{a-x}-b\end{align*}
                $$
                이 돼요.""")
        st.latex(r"\begin{align*}y&=\dfrac{bx+4}{a-x}\\&=\dfrac{-b(a-x)+ab+4}{a-x}\\&\;=\dfrac{ab+4}{a-x}-b\end{align*}")
    
    
    
elif choice == "zero-shot":
    tab1, tab2, tab3 = st.tabs(["답안", "단계", "질문"])
    with tab1:
        if explain_result:
            st.subheader('재생성된 답안:sunglasses:', divider='rainbow')
            render_latex_for_streamlit(explain_result.content.strip('"'))
    with tab2:
        if split_result:
            st.subheader('답안 단계별 분할:sunglasses:', divider='rainbow')
            render_latex_for_streamlit(split_result.content.strip('"'))
    with tab3:
        if question_result:
            st.subheader('단계별 질문:sunglasses:', divider='rainbow')
            render_latex_for_streamlit(question_result.content.strip('"'))
        
elif choice == "few-shot":
    if final_result:
        st.subheader('답안 단계별 분할:sunglasses:', divider='rainbow')
        st.markdown(final_result.content.strip('"'))
        # render_latex_for_streamlit(final_result.content.strip('"'))