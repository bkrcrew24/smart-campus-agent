"""
scripts/ingest.py

학사/비교과 JSON 데이터를 파싱하여 ChromaDB 벡터 DB에 적재하는 스크립트.
사용법: python scripts/ingest.py [--data-dir DATA_DIR] [--db-dir DB_DIR]

Milestone 1 산출물 (MILESTONES.md 기준)
"""

import argparse
import json
import os
import sys


def load_json(filepath: str) -> dict:
    """JSON 파일을 읽어 dict로 반환한다."""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def build_course_documents(curriculum: dict) -> list[dict]:
    """
    교과목 데이터를 ChromaDB에 적재할 Document 형식으로 변환한다.

    Returns:
        List of {"id": str, "text": str, "metadata": dict}
    """
    docs = []
    for course in curriculum.get("courses", []):
        # RAG 검색 대상 텍스트: 과목명 + 설명 + 역량 키워드를 자연어로 결합
        skills_text = ", ".join(course.get("skills", []))
        prereqs_text = ", ".join(course.get("prerequisites", [])) or "없음"
        text = (
            f"과목명: {course['name']}\n"
            f"이수구분: {course['category']}\n"
            f"개설학기: {course['year']}학년 {course['semester']}학기\n"
            f"학점: {course['credits']}학점\n"
            f"선수과목: {prereqs_text}\n"
            f"설명: {course.get('description', '')}\n"
            f"역량: {skills_text}"
        )
        docs.append({
            "id": f"course_{course['id']}",
            "text": text,
            "metadata": {
                "type": "course",
                "course_id": course["id"],
                "name": course["name"],
                "credits": course["credits"],
                "category": course["category"],
                "year": course["year"],
                "semester": course["semester"],
                "prerequisites": json.dumps(course.get("prerequisites", []), ensure_ascii=False),
                "skills": json.dumps(course.get("skills", []), ensure_ascii=False),
            },
        })
    return docs


def build_extracurricular_documents(ext_data: dict) -> list[dict]:
    """
    비교과 프로그램 데이터를 ChromaDB Document 형식으로 변환한다.

    Returns:
        List of {"id": str, "text": str, "metadata": dict}
    """
    docs = []
    for prog in ext_data.get("programs", []):
        skills_text = ", ".join(prog.get("skills", []))
        careers_text = ", ".join(prog.get("related_careers", []))
        target_year_text = ", ".join(str(y) for y in prog.get("target_year", []))
        text = (
            f"프로그램명: {prog['name']}\n"
            f"유형: {prog['category']}\n"
            f"권장학년: {target_year_text}학년\n"
            f"운영주체: {prog.get('host', '')}\n"
            f"졸업인증여부: {'예' if prog.get('is_graduation_requirement') else '아니오'}\n"
            f"설명: {prog.get('description', '')}\n"
            f"역량: {skills_text}\n"
            f"관련진로: {careers_text}"
        )
        docs.append({
            "id": f"ext_{prog['id']}",
            "text": text,
            "metadata": {
                "type": "extracurricular",
                "program_id": prog["id"],
                "name": prog["name"],
                "category": prog["category"],
                "target_year": json.dumps(prog.get("target_year", []), ensure_ascii=False),
                "semester": prog.get("semester", 0),
                "is_graduation_requirement": prog.get("is_graduation_requirement", False),
                "skills": json.dumps(prog.get("skills", []), ensure_ascii=False),
                "related_careers": json.dumps(prog.get("related_careers", []), ensure_ascii=False),
            },
        })
    return docs


def ingest_to_chroma(documents: list[dict], db_dir: str, collection_name: str) -> None:
    """
    Document 목록을 ChromaDB 컬렉션에 업서트(upsert)한다.
    chromadb 패키지가 설치되어 있지 않으면 ImportError를 발생시킨다.
    """
    try:
        import chromadb
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
    except ImportError as exc:
        raise ImportError(
            "chromadb 패키지가 설치되어 있지 않습니다. "
            "'pip install chromadb sentence-transformers'를 실행하세요."
        ) from exc

    embedding_fn = SentenceTransformerEmbeddingFunction(
        model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS"
    )
    client = chromadb.PersistentClient(path=db_dir)
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
    )

    ids = [doc["id"] for doc in documents]
    texts = [doc["text"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]

    collection.upsert(ids=ids, documents=texts, metadatas=metadatas)
    print(f"[ingest] '{collection_name}' 컬렉션에 {len(documents)}개 문서 적재 완료 (db: {db_dir})")


def main() -> None:
    parser = argparse.ArgumentParser(description="학사/비교과 JSON 데이터를 벡터 DB에 적재합니다.")
    parser.add_argument(
        "--data-dir",
        default="data/mock",
        help="JSON 데이터 파일이 위치한 디렉토리 (기본값: data/mock)",
    )
    parser.add_argument(
        "--db-dir",
        default="chroma_db",
        help="ChromaDB 영속화 디렉토리 (기본값: chroma_db)",
    )
    args = parser.parse_args()

    curriculum_path = os.path.join(args.data_dir, "sample_curriculum.json")
    extracurricular_path = os.path.join(args.data_dir, "sample_extracurricular.json")

    if not os.path.exists(curriculum_path):
        print(f"[오류] 학사 데이터 파일을 찾을 수 없습니다: {curriculum_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(extracurricular_path):
        print(f"[오류] 비교과 데이터 파일을 찾을 수 없습니다: {extracurricular_path}", file=sys.stderr)
        sys.exit(1)

    curriculum = load_json(curriculum_path)
    extracurricular = load_json(extracurricular_path)

    course_docs = build_course_documents(curriculum)
    ext_docs = build_extracurricular_documents(extracurricular)

    print(f"[ingest] 교과목 {len(course_docs)}개, 비교과 {len(ext_docs)}개 문서 변환 완료.")

    ingest_to_chroma(course_docs, args.db_dir, "curriculum")
    ingest_to_chroma(ext_docs, args.db_dir, "extracurricular")


if __name__ == "__main__":
    main()
