# Goal-Driven Smart Campus Agent (목표 역산형 스마트 캠퍼스 에이전트)

> 학생의 최종 진로 및 학업 목표로부터 졸업 요건과 선수과목을 역산(Backtracking)하여 맞춤형 로드맵을 수립하고, 교내 학사 일정 및 프로그램을 연계·추천하는 지능형 AI 자율 에이전트 플랫폼

---

## 1. 프로젝트 개요 (Overview)
대학 생활 중 많은 학생들이 구체적인 진로 목표(예: 특정 직무 취업, 대학원 진학 등)를 세우더라도, 이를 달성하기 위해 어떤 전공/교양 과목을 순서대로 이수해야 하는지, 어떤 비교과 활동(특강, 멘토링, 공모전 등)에 참여해야 하는지 체계적으로 파악하기 어렵습니다.

**Goal-Driven Smart Campus Agent**는 학생이 설정한 최종 목표를 기반으로 필요 요건을 역산(Backtracking)하여 단계별 최적 로드맵을 자동 수립하고, 학사 변동(과목 미이수, 수강신청 실패, 진로 변경 등) 발생 시 능동적으로 대안을 재계획(Re-planning)해주는 풀스택 AI 에이전트 서비스입니다.

---

## 2. 주요 핵심 기능 (Key Features)

1. **목표 기반 역산 로드맵 생성 (Goal Backtracking Engine)**
   - 최종 목표에 필요한 역량 및 졸업 요건을 분석하여 잔여 학기별 최적의 이수 테크트리 생성
   - DAG(방향성 비순환 그래프) 및 위상 정렬 알고리즘 기반 선수과목 위반 없는 확정적 스케줄링

2. **LangGraph 기반 멀티 에이전트 워크플로우 (Multi-Agent RAG System)**
   - 목표 분해기(Goal Decomposer), 학사/비교과 데이터 조회 툴(Curriculum Retriever), 검증기(Rule Validator)의 유기적 협업
   - 교내 학사 요람, 졸업 요건, 비교과 공지 벡터 DB 적재 및 고신뢰 RAG 검색

3. **적응형 동적 재계획 (Adaptive Re-planning)**
   - F학점, 수강 실패, 휴학 등 예기치 못한 학사 변동 시 기이수 내역을 보존하며 잔여 학기 스케줄 자동 재조정

4. **웹 기반 반응형 대시보드 & 타임라인 시각화**
   - 학기별 커리어 로드맵 인터랙티브 타임라인 제공
   - 맞춤 추천 캘린더 및 실시간 AI 대화 인터페이스

---

## 3. 기술 스택 (Tech Stack)

- **AI / Agent Core:** LangChain, LangGraph, OpenAI / Anthropic / Gemini LLM
- **Vector DB / RAG:** Chroma / SQLite-Vec
- **Backend:** Python 3.11+, FastAPI, Pydantic, Uvicorn
- **Frontend:** React, TypeScript, Vite, Tailwind CSS (또는 바닐라 CSS)
- **Database / Cache:** SQLite / PostgreSQL

---

## 4. 디렉토리 구조 (Project Structure)

```text
├── AGENTS.md               # 에이전트 시스템 프롬프트 및 코딩 원칙
├── PROJECT_PLAN.md         # 프로젝트 공식 기획서
├── MILESTONES.md           # 단계별 개발 지침서 (로드맵)
├── CHANGELOG.md            # 작업 변경 이력 로그
├── README.md               # 프로젝트 소개 및 가이드
├── data/                   # 학사/비교과 데이터 스키마 및 모의 데이터
│   ├── schema/
│   └── mock/
├── backend/                # FastAPI 백엔드 및 에이전트 코어
│   └── app/
│       ├── agents/         # LangGraph 워크플로우
│       ├── engine/         # 역산 및 재계획 알고리즘
│       └── api/            # REST API 엔드포인트
└── frontend/               # 웹 대시보드 프론트엔드
```

---

## 5. 마일스톤 및 일정 요약 (Roadmap)

**전체 개발·검증·결과물 준비 완료: 2026.12.17 / 최종 제출: 2026.12.18**

- **Milestone 1 (2026.09.01 ~ 2026.10.09):** 요구사항 정리, 학교 API 제공 여부 확인 및 대체 문서 수집·DB 구축
- **Milestone 2 (2026.10.10 ~ 2026.10.23):** AI 에이전트·백엔드 기반 및 학사 정보 조회 기능 구축
- **Milestone 3 (2026.10.24 ~ 2026.11.06):** 목표 역산 로드맵·학사 규칙 검증 및 웹 화면 구현
- **Milestone 4 (2026.11.07 ~ 2026.11.20):** 적응형 재계획·웹 연동 및 전체 기능 통합
- **Milestone 5 (2026.11.21 ~ 2026.12.04):** 통합 검증·사용자 피드백 및 오류 수정
- **Milestone 6 (2026.12.05 ~ 2026.12.17):** 최종 검증, 배포·시연 준비, 결과보고서·포트폴리오 완성
- **2026.12.18:** 완성된 최종 결과물 제출

재계획을 포함한 모든 개발과 제출 준비를 기한 내 완료한다. 학교 API 제공 여부를 먼저 확인하고, 미제공 또는 정보 부족 시 학교·학과 문서와 교칙 등을 수집하여 DB를 구축한다. 자료 수집·활용 범위는 교수님 피드백을 반영한다.

교수님 검토용 전체 개발계획서는 `docs/Smart Campus Agent 전체 개발계획서.md`를 참고한다.
