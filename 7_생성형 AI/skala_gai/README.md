# SKALA  

AI 서비스 개발을 위해 필요한 기술 요소를 학습 및 실습 하기 위한 자료 입니다. 

## 📚 출처

- [langchain-ai](https://github.com/langchain-ai/langchain) 📖
- [OpenAI API Reference](https://platform.openai.com/docs/introduction) 🤖


## 환경 구성 

**Notion 가이드** 따라 로컬 환경에 환경을 구성해 주시기 바랍니다. 

환경의 기본 구성 항목은 다음과 같습니다. 
- Python 3.11 (recommended using Python 3.11.9 or 3.11.11) 
- Visual Studio Code 

`.env` 파일에는 5개 정보가 담겨지도록 작성 합니다. (`.env_sample` 참고) 
(1) OPEN_API_KEY=sk-...
(2) LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
(3) LANGCHAIN_TRACING_V2=false
(4) LANGCHAIN_PROJECT=SKALA
(5) LANGCHAIN_API_KEY=ls_...


## 소스 코드 

소스 코드는 지속적으로 업데이트 됩니다. 과정 안내에 따라 Notion 교재 경로 통해 확인 바랍니다. 


## Open AI 요금표 
[Ref] https://openai.com/api/pricing/

- 구성 : 모델 | Input Cost | Output Cost
- Cost는 1K token당 달러 

- GPT 3.5 Turbo 
    - gpt-3.5-turbo-0125 | 0.0005 | 0.0015 
    - gpt-3.5-turbo-instruct | 0.0015 | 0.0020 
- GPT-4
    - gpt-4 | 0.03 | 0.06
    - gpt-4-32k | 0.06 | 0.12 
- GPT-4 Turbo 
    - gpt-4-0125-preview | 0.01 | 0.03
    - gpt-4-1106-preview | 0.01 | 0.03
- Embedding Models (per 1K token)
    - text-embedding-3-small : 0.00002
    - text-embedding-3-large : 0.00013 
    - ada v2 : 0.00010



## (참고) LangChain 밋업 2024 Q1 발표자료

- [RAG - 우리가 절대 쉽게 원하는 결과물을 얻을 수 없는 이유 - 테디노트](https://aifactory.space/task/2719/discussion/830)
- [프름프트 흐름과 LLM 모델 평가 - 이재석님](https://aifactory.space/task/2719/discussion/831)
- [인공지능을 통한 게임 제작 파이프라인의 변화 - 김한얼님](https://aifactory.space/task/2719/discussion/834)
- [OpenAI SORA 살짝 맛보기 - 박정현님](https://aifactory.space/task/2719/discussion/839)
- [Semantic Kernel로 만드는 AI Copilot - 이종인님](https://aifactory.space/task/2719/discussion/835)
- [Streamlit 과 langchain으로 나만의 웹서비스 개발하기 - 최재혁님](https://aifactory.space/task/2719/discussion/832)
- [Llama2-koen을 만들기까지 - 최태균님](https://aifactory.space/task/2719/discussion/836)
- [올바른 한국어 언어 모델 평가를 위해: HAE-RAE Bench, KMMLU - 손규진님](https://aifactory.space/task/2719/discussion/833)
- [랭체인 네이버 기사 크롤링 - 우성우님](https://aifactory.space/task/2719/discussion/829)
- [Gemma와 LangChain을 이용한 SQL 체인만들기 - 김태영님](https://aifactory.space/task/2719/discussion/841)
