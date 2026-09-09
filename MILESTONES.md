# Goal-Driven Smart Campus Agent: 단계별 개발 지침서 (Milestones)

본 문서는 `PROJECT_PLAN.md` 기획서를 기반으로 하여, 시스템 아키텍처 및 세부 구현 단계를 구체화한 공식 개발 지침서이다. 각 단계는 엄격한 사전 검토, 가설 기반 테스트, 최소 단위 구현(YAGNI) 원칙에 따라 진행된다.

---

## Milestone 1: 데이터 스키마 정의 및 수집 파이프라인 (2026-09-01 ~ 2026-10-15)
- **달성 목표**:
  - 학사 요람(졸업 요건, 전공/교양 이수 체계, 선수과목 그래프) 및 비교과 프로그램 표준 JSON 스키마 정의
  - 학사 데이터 정형화(JSON/Markdown) 및 로컬 벡터 DB(Chroma/SQLite-Vec) 적재 파이프라인 구축
  - 단위 테스트를 통한 데이터 파싱 무결성 검증
- **예상 생성/수정 파일**:
  - `data/schema/curriculum_schema.json`: 학사/선수과목 스키마
  - `data/schema/extracurricular_schema.json`: 비교과 프로그램 스키마
  - `data/mock/sample_curriculum.json`: 검증용 모의 학사 데이터
  - `scripts/ingest.py`: 데이터 파싱 및 벡터 DB 적재 스크립트
  - `tests/test_data_pipeline.py`: 데이터 무결성 검증 테스트
- **트레이드오프 및 대안**:
  - *대안 1 (채택)*: 요람 문서를 사전에 정형 데이터(JSON)로 가공하여 벡터 DB에 적재. 웹 크롤링 차단 리스크와 데이터 오염을 방지하고 높은 신뢰도 확보.
  - *대안 2*: 실시간 웹 크롤러 중심. 최신성은 높으나 페이지 구조 변경 및 캡차 등으로 파이프라인 불안정성 야기.

---

## Milestone 2: 에이전트 코어 파이프라인 및 백엔드 기반 구축 (2026-10-16 ~ 2026-11-20)
- **달성 목표**:
  - LangGraph 기반 멀티 에이전트 상태 머신(StateGraph) 코어 구조 설계 (목표 분해기, 학사 조회 툴, 검증기)
  - FastAPI 기반 백엔드 API 서버 뼈대 및 세션/상태 관리 구현
- **예상 생성/수정 파일**:
  - `backend/app/main.py`: FastAPI 엔트리포인트
  - `backend/app/core/config.py`: 환경변수 및 설정
  - `backend/app/agents/state.py`: LangGraph State 정의
  - `backend/app/agents/graph.py`: 멀티 에이전트 워크플로우 정의
  - `backend/app/agents/tools/curriculum_retriever.py`: RAG 기반 학사 조회 도구
  - `tests/test_agent_workflow.py`: 에이전트 상태 전이 및 응답 테스트
- **트레이드오프 및 대안**:
  - *대안 1 (채택)*: Python FastAPI. LangGraph/LangChain과의 네이티브 호환성, 비동기 지원, OpenAPI 자동 생성.
  - *대안 2*: Node.js (NestJS). 프론트엔드와 언어 통일은 가능하나 Python 중심의 최신 LLM/RAG 라이브러리 활용 제한.

---

## Milestone 3: 역산(Backtracking) 로드맵 엔진 및 1차 웹 프로토타입 완성 (2026-11-21 ~ 2026-12-18)
- **달성 목표**:
  - 최종 목표로부터 잔여 학기를 역산하여 학기별 권장 이수 과목과 비교과 활동을 배치하는 DAG 기반 역산 알고리즘 구현
  - 타임라인 기반 로드맵 시각화 및 대화형 웹 UI 프로토타입 완성
  - **교내 행정 마감 준수**:
    - **2026. 12. 04.(금)**: 캡스톤디자인 과제개발비 카드 집행 완료 및 정산 서류 준비
    - **2026. 12. 18.(금)**: 1학기 과제개발 완료, 결과보고서 및 포트폴리오(1차 웹 프로토타입 결과물 파일) 제출
- **예상 생성/수정 파일**:
  - `backend/app/engine/backtracker.py`: 역산 로드맵 생성 엔진 (DAG 위상 정렬)
  - `backend/app/engine/rule_validator.py`: 필수 이수 요건 및 선수과목 위반 검증기
  - `frontend/src/components/Timeline.tsx`: 로드맵 시각화 컴포넌트
  - `frontend/src/components/ChatInterface.tsx`: 목표 입력 대화형 인터페이스
  - `tests/test_backtracker.py`: 역산 알고리즘 정합성 검증 테스트
- **트레이드오프 및 대안**:
  - *대안 1 (채택)*: 하이브리드 아키텍처. 목표 분해와 비교과 추천은 LLM이, 필수 학점 계산 및 선수과목 배치는 결정론적 알고리즘(DAG)이 전담하여 환각 차단.
  - *대안 2*: 순수 LLM 프롬프트 기반 생성. 구현은 쉬우나 학점 오차 및 선수과목 누락 등 신뢰성 저하.

---

## Milestone 4: 적응형 재계획(Re-planning) 엔진 및 웹 연동 (2026-12-19 ~ 2027-02-28)
- **달성 목표**:
  - 겨울방학 집중 개발: 과목 미이수, 계획 변경 등 학사 변동 발생 시 기이수 내역을 보존하며 잔여 학기 로드맵을 유연하게 재수립하는 Re-planning 로직 개발
  - 프론트엔드-백엔드-에이전트 전체 연동 및 알파 테스트 수행
- **예상 생성/수정 파일**:
  - `backend/app/engine/replanner.py`: 차분 계산 및 잔여 학기 재할당 로직
  - `backend/app/api/roadmap.py`: 로드맵 조회/수정 및 재계획 API
  - `frontend/src/components/ReplanModal.tsx`: 변동 상황 입력 뷰
  - `tests/test_replanner.py`: 재계획 시나리오 불변성 및 정합성 테스트

---

## Milestone 5: 시스템 고도화 및 교내 모의 테스트 (2027-03-01 ~ 2027-04-15)
- **달성 목표**:
  - 다양한 가상 학생 페르소나(1~4학년, 복수전공, 전과, 편입 등) 대상 로드맵 생성 정합성 100% 검증
  - 응답 지연 시간 최적화 및 벤치마크 지표 도출
- **예상 생성/수정 파일**:
  - `benchmarks/personas.json`: 모의 테스트 페르소나 데이터셋
  - `benchmarks/evaluate.py`: 정합성 및 성능 평가 러너
  - `benchmarks/report.md`: 검증 결과 보고서

---

## Milestone 6: 서비스 배포 및 결과 보고서 작성 (2027-04-16 ~ 2027-05-31)
- **달성 목표**:
  - 컨테이너화(Docker) 및 클라우드 호스팅 배포 완료
  - 최종 캡스톤디자인 결과 보고서 작성
- **예상 생성/수정 파일**:
  - `Dockerfile`, `docker-compose.yml`
  - `docs/FINAL_REPORT.md`: 최종 과제 결과 보고서
