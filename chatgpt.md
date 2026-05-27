# 1. Kanye West 챗봇 만들기

GPT Builder에서 kanye.rest API를 연동하여 Kanye West 스타일로 대화하는 챗봇을 만들어 보겠습니다. API를 활용해 명언을 랜덤으로 출력하고, 챗봇의 응답 스타일을 조정하여 Kanye West처럼 말하도록 설정해 봅니다.



## 지시사항

1. GPT Builder에서 ***\*구성 → 작업 → 새 작업 만들기\****를 클릭해서 작업 추가 화면을 열어주세요.
2. 작업 추가 화면 스키마에 [ActionsGPT](https://chatgpt.com/g/g-TYEliDU6A-actionsgpt)를 사용하여 kanye.rest API 스키마를 생성해주세요.
3. GPT Builder 왼쪽 패널의 `만들기` 탭에서 챗봇의 응답을 한국어로 설정합니다.
4. 설정을 마친 후 **`\**공유하기\**`**를 눌러 저장합니다. 사이드바에서 완성된 GPT를 선택하고 직접 활용해 봅니다.



***\*[지시사항 2번] 프롬프트\****

(ActionsGPT에 아래 프롬프트와 [kanye.rest API 도큐멘테이션](https://github.com/ajzbc/kanye.rest/blob/master/README.md)을 함께 입력하세요.)

```
I attached the documentation. 
Please make the spec as JSON for this apis.
```



***\*[지시사항 3번] 프롬프트\****

```
내가 등록한 actions로 카니예 웨스트 랜덤 어록을 보여주고 싶고, 
한국어로 재치있게 번역해서 보여줘.
```



#### ***\*Tips!\****

- 스키마를 붙여 넣었을 때 오류가 발생하면, ActionsGPT에게 오류를 복사해서 해결해 달라고 요청해 보세요.
- 채팅할 때 아래 와 같은 창이 뜨면 `항상 허용하기`를 클릭해 주세요.

![화면 캡처 2025-02-26 191720.png](https://cdn-api.elice.io/api-attachment/attachment/8bb8ff11b1904b49aba8137a2246cbd2/%ED%99%94%EB%A9%B4%20%EC%BA%A1%EC%B2%98%202025-02-26%20191720.png)



# 2. SerpAPI 연결하여 웹 검색하기

SerpAPI를 활용하여 웹에서 검색한 정보를 정리해서 알려주는 챗봇을 만듭니다. GPT Builder에서 작업(Action) 기능을 추가하고, API 키를 설정하여 검색 결과를 가져오는 방법을 실습합니다.



## 지시사항

1. [GPT 빌더](https://chat.openai.com/gpts)로 이동하고, ***\*구성 → 작업 → 새 작업 만들기\****를 클릭합니다.
2. 작업 추가 창이 열리면 ***\*스키마\**** 입력란을 찾습니다. ActionsGPT에서 스키마를 생성하기 위해 다음과 같이 프롬프트를 입력하고, 생성된 스키마를 복사하여 ***\*스키마 입력란\****에 붙여넣습니다.
3. 스키마에 `name: api_key`를 찾아서 description을 실제 나의 API key로 수정해 줍니다.
4. GPT의 지침과 설정을 작성하고 **`\**공유하기\**`** 버튼을 클릭하여 GPT를 저장합니다.

***\*[지시사항 2번] ActionsGPT 프롬프트\****

```
SerpAPI로 검색어를 입력하면, 구글 검색 결과를 정리해서 보여주는 GPTs를 만들거야. 
요청 URL과 파라미터 예시는 다음과 같아. 
https://serpapi.com/search.json?q=Coffee&location=Austin,+Texas,+United+States
```



#### ***\*Tips!\****

- 스키마를 붙여 넣었을 때 발생하는 오류는 나의 API key를 붙여 넣으면 사라집니다.
- Serp API 홈페이지(https://serpapi.com/)에 로그인하면 **`\**Your Account\**`** 페이지에서 본인의 API 키를 확인할 수 있습니다.
- 채팅할 때 아래 와 같은 창이 뜨면 `항상 허용하기`를 클릭해주세요.

![화면 캡처 2025-02-26 191720.png](https://cdn-api.elice.io/api-attachment/attachment/808a80676f74476395375dd99da50145/%ED%99%94%EB%A9%B4%20%EC%BA%A1%EC%B2%98%202025-02-26%20191720.png)



# 3. Sheety API로 나만의 주식 포트폴리오 챗봇 만들기

이 실습에서는 나의 주식 데이터를 구글 시트에 업로드하고, Sheety API를 사용해 챗봇과 연동하는 방법을 배웁니다. 이를 통해 주식 포트폴리오를 분석해주는 나만의 챗봇을 만들어 봅니다.



## 지시사항

1. [Google Sheets](https://docs.google.com/spreadsheets)에 접속해 새 시트를 만듭니다. 기존 엑셀 데이터를 업로드하려면 파일 → 가져오기 → 업로드를 선택하고, 파일을 선택한 후 가져오기를 완료합니다. 시트가 준비되면 우측 상단의 `공유` → `링크 복사`를 클릭합니다.
2. [Sheety API](https://dashboard.sheety.co/)에 접속해 `New Project`를 생성한 후, 앞에서 복사한 시트 URL을 입력합니다. 프로젝트 이름을 정한 후 `Create Project`를 클릭하면 API가 생성됩니다.
3. 생성된 프로젝트에서 `Authentication` → `API Key`를 Basic으로 선택하고 `Generate API Key`를 클릭하여 키를 발급받습니다.
4. 다음으로 GPT Builder에 접속하여 구성 → 작업 → 새 작업 만들기를 클릭합니다. 작업 추가 창에서 `인증` 유형을 API Key로 설정하고, 앞서 발급받은 API 키를 입력한 후 저장합니다. `스키마`에서는 [ActionsGPT](https://chatgpt.com/g/g-TYEliDU6A-actionsgpt)를 통해 생성한 스키마를 입력합니다.
5. 뒤로가기를 클릭하고 `만들기`와 `구성`탭에 원하는 설정을 입력합니다.
6. 설정이 완료되면 **`\**공유하기\**`**를 눌러 GPT를 사용할 수 있습니다.



***\*[지시사항 1번] 실습에서 사용한 엑셀 파일\****
[stock_data.xlsx](https://cdn-api.elice.io/api-attachment/attachment/a3f22457d4a64541a80999ab32634486/stock_data.xlsx)



***\*[지시사항 4번] 프롬프트\****
(다음 프롬프트를 본인의 프로젝트 URL과 함께 입력하세요.)

```
SheetyAPI를 GPTs에 연동할건데 스키마 만들어줘.
SheetyAPI 프로젝트 URL은 다음과 같아.
```



***\*[지시사항 5번] 프롬프트\****

```
주식 및 시장 추세에 대한 분석을 제공하는 챗봇을 만들거야. 
이름은 "주식 포트폴리오 분석기"로 하자.
그리고 이 챗봇은 다음과 같은 특징이 있어.

1. Sheety API를 통해 주식 포트폴리오 데이터에 대한 구글 스프레드시트에 연동하고,
GET 요청을 통해 시트 데이터를 가져오는 기능을 추가할 예정이다.
2. 사용자가 주식 포트폴리오 데이터 관련 질문을 하면 연동된 시트의 데이터를 기반으로 답변한다.
3. 사용자가 특정 주식에 대한 분석을 요청하면 웹 검색을 진행하여 답변한다.
4. 사용자와 한국어로 소통하는 것을 디폴트로 설정한다.
```



#### ***\*Tips!\****

- 스키마를 붙여 넣었을 때 발생하는 오류는 `인증`에 API key를 붙여 넣으면 사라집니다.
- 채팅할 때 아래 와 같은 창이 뜨면 `항상 허용하기`를 클릭해주세요.

![화면 캡처 2025-02-26 191720.png](https://cdn-api.elice.io/api-attachment/attachment/808a80676f74476395375dd99da50145/%ED%99%94%EB%A9%B4%20%EC%BA%A1%EC%B2%98%202025-02-26%20191720.png)