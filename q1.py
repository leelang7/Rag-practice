import datetime

from langchain.agents import AgentType, initialize_agent
from langchain.prompts import PromptTemplate
from langchain_community.tools import (
    DuckDuckGoSearchResults,
    DuckDuckGoSearchRun,
)
from langchain_openai import ChatOpenAI

# LLM 초기화
llm = ChatOpenAI(
    api_key="sk-",
    model="gpt-4o-mini",
)

# DuckDuckGo 검색 툴 초기화
search = DuckDuckGoSearchRun()

# 현재 시각 추가
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
SYSTEM_PROMPT = f"""너는 사용자에 질문에 답변하는 챗봇이야. 현재 시각은 {current_time}이야."""

# 에이전트 초기화 - ZERO_SHOT_REACT_DESCRIPTION 사용
agent = initialize_agent(
    tools=[search],
    llm=llm,
    agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"prefix": SYSTEM_PROMPT},
    handle_parsing_errors=True,
    verbose=True,
)

result = agent.invoke("어제 있었던 한국의 주요 뉴스를 요약해줘.")
print(result.get("output"))
