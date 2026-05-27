import datetime
import warnings
from pillow import Image  # 사진 데이터 확인용 (선택사항)

# 경고 메시지 방지
warnings.filterwarnings("ignore", category=DeprecationWarning)

from pymongo import MongoClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# ==========================================
# 1. 로컬 MongoDB 초기화 및 샘플 데이터 삽입
# ==========================================
print("DB 🔗 로컬 MongoDB에 연결하는 중...")
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["LocalAssistantDB"]

# 컬렉션 세팅
trips_col = db["trips"]       # 출장 기록
expenses_col = db["expenses"] # 지출 내역
photos_col = db["photos"]     # 사진 메타데이터

def init_sample_data():
    """테스트를 위한 로컬 MongoDB 데이터 적재"""
    # 기존 데이터 초기화 (테스트용)
    trips_col.delete_many({})
    expenses_col.delete_many({})
    photos_col.delete_many({})

    # 1. 출장 기록 데이터
    trips_col.insert_many([
        {"destination": "부산", "purpose": "AI 로봇 프로젝트 기술 미팅", "start_date": "2026-05-10", "end_date": "2026-05-12", "status": "완료"},
        {"destination": "대전", "purpose": "정부 공공데이터 AI 공모전 멘토링", "start_date": "2026-05-20", "end_date": "2026-05-21", "status": "완료"},
        {"destination": "광주", "purpose": "Vision AI 산업용 CCTV 고도화 미팅", "start_date": "2026-06-02", "end_date": "2026-06-04", "status": "예정"}
    ])

    # 2. 지출 내역 데이터
    expenses_col.insert_many([
        {"item": "KTX 열차표 (서울->부산)", "amount": 59800, "category": "교통비", "date": "2026-05-10"},
        {"item": "부산 광안리 횟집 (업체 식사)", "amount": 120000, "category": "식비(접대)", "date": "2026-05-11"},
        {"item": "대전역 성심당 빵 구입", "amount": 28000, "category": "식비", "date": "2026-05-21"},
        {"item": "연구실 소모품 (개발용 웹캠)", "amount": 85000, "category": "소모품비", "date": "2026-05-25"}
    ])

    # 3. 사진 데이터 (로컬 파일 경로 및 메타데이터 관리)
    photos_col.insert_many([
        {"file_name": "robot_test.jpg", "file_path": "./photos/robot_test.jpg", "description": "부산 미팅 중 로봇 플랫폼 구동 테스트 스크린샷", "date": "2026-05-11"},
        {"file_name": "daejeon_dinner.jpg", "file_path": "./photos/daejeon_dinner.jpg", "description": "대전 출장 멘토링 끝나고 학생들과 저녁 식사", "date": "2026-05-20"},
        {"file_name": "cctv_optical.jpg", "file_path": "./photos/cctv_optical.jpg", "description": "연구실 외주 프로젝트 CCTV 카메라 렌즈 화각 점검 사진", "date": "2026-05-26"}
    ])
    print("DB ✅ 샘플 데이터(출장/지출/사진)가 MongoDB에 성공적으로 저장되었습니다.")

# 샘플 데이터 초기화 실행
init_sample_data()


# ==========================================
# 2. LLM 및 라우팅 쿼리 파서 정의
# ==========================================
# 무료 티어인 gemini-1.5-flash 활용
llm = ChatGoogleGenerativeAI(
    google_api_key="AIzaSy...",  # 본인의 구글 API 키 입력
    model="gemini-1.5-flash",
    temperature=0
)

# 사용자의 의도를 분석하기 위한 Pydantic 데이터 구조 정의
class IntentRouter(BaseModel):
    target_collection: str = Field(description="사용자가 요청한 데이터 종류. 'trips', 'expenses', 'photos' 중 하나여야 합니다.")
    search_keyword: str = Field(description="MongoDB에서 검색할 핵심 키워드(예: '부산', 'KTX', 'CCTV'). 없을 경우 빈 문자열('')")

router_parser = JsonOutputParser(pydantic_object=IntentRouter)

router_prompt = ChatPromptTemplate.from_template("""
사용자의 질문을 분석하여 어떤 MongoDB 컬렉션을 조회해야 하는지, 그리고 검색 키워드는 무엇인지 JSON 구조로 분류해줘.

[컬렉션 규칙]
- 출장, 미팅, 방문, 일정 관련: 'trips'
- 지출, 금액, 비용, 영수증, 구매 관련: 'expenses'
- 사진, 이미지, 스크린샷 관련: 'photos'

현재 시각: {current_time}

[사용자 질문]
{question}

{format_instructions}
""")

router_chain = router_prompt | llm | router_parser


# ==========================================
# 3. 데이터 연계 및 최종 답변 체인 구축
# ==========================================
answer_prompt = ChatPromptTemplate.from_template("""
너는 로컬 MongoDB 데이터베이스와 연계된 지능형 개인 비서 AI 시스템이야.
현재 시각은 {current_time}이야.

사용자의 질문과 MongoDB에서 직접 조회한 데이터 원본(Context)을 바탕으로 자연스럽고 친절하게 답변해줘.
만약 사진 관련 요청이고 데이터가 존재한다면 반드시 파일 경로(file_path)를 언급해줘.

[MongoDB 조회 데이터 (Context)]
{db_context}

[사용자 질문]
{question}
""")

answer_chain = answer_prompt | llm | StrOutputParser()


# ==========================================
# 4. 실 통합 실행 함수
# ==========================================
def run_local_assistant_system(user_question):
    print(f"\nUser 💬: {user_question}")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Step 1: LLM을 통해 어떤 데이터베이스를 뒤질지 의도(Intent) 분석
    try:
        route_result = router_chain.invoke({
            "current_time": current_time,
            "question": user_question,
            "format_instructions": router_parser.get_format_instructions()
        })
    except Exception as e:
        print(f"⚠️ 의도 분석 실패: {e}")
        return

    target_col = route_result.get("target_collection")
    keyword = route_result.get("search_keyword")
    
    print(f"AI 🧠 [라우팅 완료] 대상 컬렉션: '{target_col}' | 검색 키워드: '{keyword}'")

    # Step 2: 분석된 의도를 기반으로 로컬 MongoDB 실제 쿼리 수행
    db_context = []
    if target_col == "trips":
        # 키워드가 있으면 목적지나 목적에서 검색, 없으면 전체 조회
        query = {"$or": [{"destination": {"$regex": keyword}}, {"purpose": {"$regex": keyword}}]} if keyword else {}
        db_context = list(trips_col.find(query, {"_id": 0}))
    elif target_col == "expenses":
        query = {"$or": [{"item": {"$regex": keyword}}, {"category": {"$regex": keyword}}]} if keyword else {}
        db_context = list(expenses_col.find(query, {"_id": 0}))
    elif target_col == "photos":
        query = {"$or": [{"file_name": {"$regex": keyword}}, {"description": {"$regex": keyword}}]} if keyword else {}
        # 최근 사진 순으로 정렬하기 위해 파이썬 정렬 처리 혹은 쿼리 가능
        db_context = list(photos_col.find(query, {"_id": 0}))

    print(f"DB 🔍 [조회된 데이터 수]: {len(db_context)}건")

    # Step 3: 조회된 데이터를 데이터 원본(Context)으로 주입하여 최종 자연어 답변 생성
    final_response = answer_chain.invoke({
        "current_time": current_time,
        "db_context": str(db_context),
        "question": user_question
    })

    print(f"AI 🤖:\n{final_response}\n")


# ==========================================
# 5. 각 시나리오별 시스템 모의 테스트 실행
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*40 + "\n🚀 로컬 연계 Assistant 시스템 테스트 시작\n" + "="*40)
    
    # 시나리오 1: 출장 기록 연동 테스트
    run_local_assistant_system("지난번에 대전 출장 갔다 왔던 일정이 언제였지?")
    
    # 시나리오 2: 지출 내역 연동 테스트
    run_local_assistant_system("최근에 돈 지출한 내역들 전부 보여줘")
    
    # 시나리오 3: 최근 사진 메타데이터 연동 및 경로 표출 테스트
    run_local_assistant_system("연구실에서 CCTV 카메라 점검하면서 찍었던 최근 사진 찾아줘")