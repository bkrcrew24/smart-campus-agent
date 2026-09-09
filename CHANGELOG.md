# 변경 이력 (CHANGELOG)

## [2026-09-10]
- **대상 파일:** `data/schema/curriculum_schema.json`, `data/schema/extracurricular_schema.json`, `data/mock/sample_curriculum.json`, `data/mock/sample_extracurricular.json`, `scripts/ingest.py`, `tests/test_data_pipeline.py`
- **수정 이유:** Milestone 1 구현 - 학사/비교과 데이터 표준 스키마 정의, 모의 데이터셋 구축, 벡터 DB 적재 파이프라인 및 무결성 검증 테스트 작성
- **변경 내용:**
  - JSON Schema 2개 생성 (교과목/졸업요건 스키마, 비교과 스키마)
  - 컴퓨터소프트웨어학과 기준 1~4학년 교과목(22개, 선수과목 DAG 포함) 및 비교과 프로그램(10개) 모의 데이터 구축
  - ChromaDB 적재 스크립트 (`scripts/ingest.py`) 작성
  - pytest 기반 무결성 검증 테스트 14개 작성 및 전부 통과 확인 (14/14 passed)

## [2026-09-09]
- **대상 파일:** `.gitignore`, `파일/` 디렉토리
- **수정 이유:** 교내 내부 행정 서식 문서의 GitHub 원격 노출 차단
- **변경 내용:** `.gitignore`에 `파일/` 추가 및 Git 인덱스에서 캐시 삭제(`git rm -r --cached "파일"`), 로컬 파일 보존 유지

- **대상 파일:** `MILESTONES.md`, `PROJECT_PLAN.md`, `README.md`
- **수정 이유:** 교내 캡스톤디자인 1학기 공식 마감일(12/18) 및 예산 카드 사용 마감일(12/4) 준수를 위한 일정 동기화
- **변경 내용:** Milestone 2(10/16~11/20), Milestone 3(11/21~12/18, 1차 결과보고서/포트폴리오 제출 및 예산 정산), Milestone 4(12/19~2/28, 겨울방학 Re-planning 개발)로 기간 및 산출물 목표 조정

- **대상 파일:** `AGENTS.md`
- **수정 이유:** 에이전트 필수 참조 문서 목록 확장
- **변경 내용:** 기획서(`PROJECT_PLAN.md`) 외에 지침서(`MILESTONES.md`) 및 개요(`README.md`)를 필수 참조 문서로 추가

- **대상 파일:** `README.md`
- **수정 이유:** 이모티콘 사용 금지 원칙 준수를 위해 문서 헤더 정제
- **변경 내용:** 모든 섹션 헤더에서 이모티콘을 제거하고 번호 체계로 통일

- **대상 파일:** `README.md`, `.gitignore`
- **수정 이유:** 프로젝트 소개 문서 작성, 버전 관리 설정 및 GitHub 원격 저장소 연동
- **변경 내용:** 프로젝트 개요/아키텍처/기술스택/로드맵을 담은 `README.md` 및 `.gitignore` 생성, GitHub 비공개 저장소(`bkrcrew24/goal-driven-smart-campus-agent`) 연동 및 초기 푸시 완료

- **대상 파일:** `MILESTONES.md`
- **수정 이유:** 기획서 기반 단계별 개발 지침서(마일스톤 로드맵) 공식 문서화
- **변경 내용:** 1~6단계 마일스톤 목표, 예상 생성 파일, 기술적 트레이드오프를 정의한 `MILESTONES.md` 신규 생성

- **대상 파일:** `CLAUDE.md`, `AGENTS.md`
- **수정 이유:** 에이전트 작업 가이드라인 파일명을 표준 컨벤션으로 변경
- **변경 내용:** `CLAUDE.md`를 삭제하고 규칙 내용을 담은 `AGENTS.md` 신규 생성 및 내부 참조 문구 수정
