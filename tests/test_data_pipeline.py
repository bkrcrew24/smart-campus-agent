"""
tests/test_data_pipeline.py

Milestone 1 데이터 파이프라인 무결성 검증 테스트.

검증 항목:
  1. JSON Schema 유효성: 모의 데이터가 정의된 스키마를 만족하는지 확인
  2. 선수과목 순환 참조(Cycle) 부재: DAG 구조의 무결성 보장
  3. ingest.py의 Document 변환 함수 정합성: 필수 필드 존재 여부 확인

실행: pytest tests/test_data_pipeline.py -v
"""

import json
import os
import sys

import pytest

# 프로젝트 루트를 sys.path에 추가하여 scripts 모듈을 임포트 가능하게 한다.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from scripts.ingest import (
    build_course_documents,
    build_extracurricular_documents,
    load_json,
)

DATA_DIR = os.path.join(ROOT_DIR, "data", "mock")
SCHEMA_DIR = os.path.join(ROOT_DIR, "data", "schema")

CURRICULUM_PATH = os.path.join(DATA_DIR, "sample_curriculum.json")
EXTRACURRICULAR_PATH = os.path.join(DATA_DIR, "sample_extracurricular.json")
CURRICULUM_SCHEMA_PATH = os.path.join(SCHEMA_DIR, "curriculum_schema.json")
EXTRACURRICULAR_SCHEMA_PATH = os.path.join(SCHEMA_DIR, "extracurricular_schema.json")


# ---------------------------------------------------------------------------
# 픽스처
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def curriculum():
    return load_json(CURRICULUM_PATH)


@pytest.fixture(scope="session")
def extracurricular():
    return load_json(EXTRACURRICULAR_PATH)


@pytest.fixture(scope="session")
def curriculum_schema():
    return load_json(CURRICULUM_SCHEMA_PATH)


@pytest.fixture(scope="session")
def extracurricular_schema():
    return load_json(EXTRACURRICULAR_SCHEMA_PATH)


# ---------------------------------------------------------------------------
# 1. JSON Schema 유효성 검증
# ---------------------------------------------------------------------------

class TestSchemaValidation:
    """모의 데이터가 JSON Schema 규격을 만족하는지 검증한다."""

    def test_curriculum_schema_has_required_keys(self, curriculum_schema):
        """curriculum_schema.json에 필수 최상위 키가 존재해야 한다."""
        assert "properties" in curriculum_schema
        assert "department" in curriculum_schema["properties"]
        assert "graduation_requirements" in curriculum_schema["properties"]
        assert "courses" in curriculum_schema["properties"]

    def test_extracurricular_schema_has_required_keys(self, extracurricular_schema):
        """extracurricular_schema.json에 programs 키가 존재해야 한다."""
        assert "properties" in extracurricular_schema
        assert "programs" in extracurricular_schema["properties"]

    def test_curriculum_data_has_department(self, curriculum):
        """학사 데이터에 학과 정보가 포함되어야 한다."""
        assert "department" in curriculum
        dept = curriculum["department"]
        for key in ("id", "name", "college"):
            assert key in dept, f"department에 '{key}' 필드가 없습니다."

    def test_curriculum_data_has_graduation_requirements(self, curriculum):
        """학사 데이터에 졸업 요건이 포함되어야 한다."""
        gr = curriculum.get("graduation_requirements", {})
        assert "total_credits" in gr
        assert "breakdown" in gr
        breakdown = gr["breakdown"]
        for key in ("major_required", "major_elective", "general_required", "general_elective"):
            assert key in breakdown, f"breakdown에 '{key}' 필드가 없습니다."

    def test_curriculum_data_has_courses(self, curriculum):
        """학사 데이터에 교과목 목록이 비어 있지 않아야 한다."""
        courses = curriculum.get("courses", [])
        assert len(courses) > 0, "교과목 목록이 비어 있습니다."

    def test_each_course_has_required_fields(self, curriculum):
        """모든 교과목에 필수 필드가 존재해야 한다."""
        required_fields = ("id", "name", "credits", "category", "year", "semester")
        for course in curriculum["courses"]:
            for field in required_fields:
                assert field in course, f"과목 '{course.get('id', '?')}'에 '{field}' 필드가 없습니다."

    def test_extracurricular_data_has_programs(self, extracurricular):
        """비교과 데이터에 프로그램 목록이 비어 있지 않아야 한다."""
        programs = extracurricular.get("programs", [])
        assert len(programs) > 0, "비교과 프로그램 목록이 비어 있습니다."

    def test_each_program_has_required_fields(self, extracurricular):
        """모든 비교과 프로그램에 필수 필드가 존재해야 한다."""
        required_fields = ("id", "name", "category", "target_year")
        for prog in extracurricular["programs"]:
            for field in required_fields:
                assert field in prog, f"프로그램 '{prog.get('id', '?')}'에 '{field}' 필드가 없습니다."


# ---------------------------------------------------------------------------
# 2. 선수과목 DAG 순환 참조(Cycle) 검증
# ---------------------------------------------------------------------------

class TestPrerequisiteDAG:
    """선수과목 그래프가 DAG(방향성 비순환 그래프)인지 검증한다."""

    @staticmethod
    def _build_adj(courses: list) -> dict:
        """과목 ID -> 선수과목 ID 집합의 인접 리스트를 반환한다."""
        return {c["id"]: set(c.get("prerequisites", [])) for c in courses}

    @staticmethod
    def _has_cycle(adj: dict) -> bool:
        """DFS 기반 순환 감지. 순환이 있으면 True를 반환한다."""
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in adj.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.discard(node)
            return False

        for node in adj:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def test_no_cycle_in_prerequisites(self, curriculum):
        """선수과목 그래프에 순환 참조가 없어야 한다."""
        courses = curriculum["courses"]
        adj = self._build_adj(courses)
        assert not self._has_cycle(adj), "선수과목 그래프에 순환 참조가 감지되었습니다."

    def test_all_prerequisites_exist(self, curriculum):
        """선수과목으로 참조된 과목 ID가 실제 교과목 목록에 존재해야 한다."""
        courses = curriculum["courses"]
        course_ids = {c["id"] for c in courses}
        for course in courses:
            for prereq_id in course.get("prerequisites", []):
                assert prereq_id in course_ids, (
                    f"과목 '{course['id']}'의 선수과목 '{prereq_id}'가 교과목 목록에 존재하지 않습니다."
                )

    def test_total_credits_breakdown_matches(self, curriculum):
        """졸업 요건 breakdown 합계가 total_credits와 일치해야 한다."""
        gr = curriculum["graduation_requirements"]
        bd = gr["breakdown"]
        total = sum(bd[k] for k in bd)
        assert total == gr["total_credits"], (
            f"breakdown 합계({total})가 total_credits({gr['total_credits']})와 다릅니다."
        )


# ---------------------------------------------------------------------------
# 3. Document 변환 함수 정합성 검증
# ---------------------------------------------------------------------------

class TestDocumentBuilder:
    """ingest.py의 Document 변환 함수 출력 필드를 검증한다."""

    def test_course_documents_have_required_fields(self, curriculum):
        """build_course_documents()의 반환 문서에 id, text, metadata가 있어야 한다."""
        docs = build_course_documents(curriculum)
        assert len(docs) == len(curriculum["courses"])
        for doc in docs:
            assert "id" in doc
            assert "text" in doc
            assert "metadata" in doc
            assert doc["id"].startswith("course_")
            meta = doc["metadata"]
            assert meta["type"] == "course"
            for field in ("course_id", "name", "credits", "category", "year", "semester"):
                assert field in meta, f"metadata에 '{field}' 필드가 없습니다."

    def test_extracurricular_documents_have_required_fields(self, extracurricular):
        """build_extracurricular_documents()의 반환 문서에 id, text, metadata가 있어야 한다."""
        docs = build_extracurricular_documents(extracurricular)
        assert len(docs) == len(extracurricular["programs"])
        for doc in docs:
            assert "id" in doc
            assert "text" in doc
            assert "metadata" in doc
            assert doc["id"].startswith("ext_")
            meta = doc["metadata"]
            assert meta["type"] == "extracurricular"
            for field in ("program_id", "name", "category"):
                assert field in meta, f"metadata에 '{field}' 필드가 없습니다."

    def test_course_document_text_contains_name(self, curriculum):
        """변환된 교과목 문서 텍스트에 과목명이 포함되어야 한다."""
        docs = build_course_documents(curriculum)
        for doc, course in zip(docs, curriculum["courses"]):
            assert course["name"] in doc["text"]
