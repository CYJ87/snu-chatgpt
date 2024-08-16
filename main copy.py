import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

st.title("나만의 챗GPT")

# 메시지를 저장할 list 를 생성합니다.
if "messages" not in st.session_state:
    st.session_state.messages = []


# 채팅 메시지에 새로운 메시지를 추가하는 함수
def add_message(role, message):
    # 메시지 list 에 새로운 대화(메시지)를 추가합니다.
    st.session_state.messages.append(ChatMessage(role=role, content=message))


# 이전의 대화기록을 모두 출력하는 함수
def print_message():
    for message in st.session_state.messages:
        # 대화를 출력
        st.chat_message(message.role).write(message.content)


# 체인 생성
def create_chain():
    # 사용자의 프롬프트를 정의
    #     prompt = PromptTemplate.from_template(
    #         """당신은 친절한 AI 어시스턴트입니다. 사용자의 질문에 친절하게 답변해 주세요.

    # 질문: {question}"""
    #     )
    prompt = load_prompt("prompts/SNS.yaml", encoding="utf-8")
    # LLM 정의(OpenAI ChatGPT)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # 체인 생성
    chain = prompt | llm | StrOutputParser()
    return chain


# 이전 대화 기록을 모두 출력
print_message()

# 채팅 입력창
user_input = st.chat_input("궁금한 내용을 입력해 주세요.")

# 만약에 유저가 채팅을 입력하면
if user_input:
    st.chat_message("user").write(user_input)

    # 체인 생성
    chain = create_chain()

    # chain 을 실행서 ai_answer 를 받습니다.
    answer = chain.stream(user_input)

    with st.chat_message("ai"):
        # 빈 공간을 만듬
        chat_container = st.empty()

        # ai 의 답변을 출력
        ai_answer = ""

        # 스트리밍 출력
        for token in answer:
            ai_answer += token
            chat_container.markdown(ai_answer)

    # 답변을 출력
    # st.chat_message("ai").write(ai_answer)

    # 대화를 추가
    add_message("user", user_input)
    # ai 의 답변을 추가
    add_message("ai", ai_answer)
