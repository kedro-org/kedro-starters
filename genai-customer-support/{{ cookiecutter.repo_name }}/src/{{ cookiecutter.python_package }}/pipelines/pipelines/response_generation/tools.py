from typing import Callable

import pandas as pd
from sqlalchemy import text, Engine, Row
from langchain_core.tools import tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_lookup_docs(docs: pd.DataFrame, docs_matches: int = 3) -> Callable:
    @tool
    def lookup_docs(query: str) -> str:
        """Look up documentation to suggest a solution."""
        if docs.empty:
            return "No relevant documentation found."

        texts = docs["question"].astype(str) + " " + docs["answer"].astype(str)
        vectorizer = TfidfVectorizer().fit([query] + texts.tolist())
        vectors = vectorizer.transform([query] + texts.tolist())

        sims = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
        top_indices = sims.argsort()[::-1][:docs_matches]

        results = []
        for idx in top_indices:
            q = docs.iloc[idx]["question"]
            a = docs.iloc[idx]["answer"]
            score = sims[idx]
            results.append(f"Q: {q}\nA: {a}\n(similarity={score:.2f})")

        return "Relevant documentation found:\n" + "\n\n".join(results)

    return lookup_docs


def build_get_user_claims(db_engine: Engine) -> Callable:
    @tool
    def get_user_claims(user_id: int) -> list[dict]:
        """Fetch all claims for a given user from the DB."""
        query = text("""
            SELECT id, title, status, problem, solution, created_at
            FROM claim
            WHERE user_id = :user_id
            ORDER BY created_at DESC
        """)
        with db_engine.connect() as conn:
            result = conn.execute(query, {"user_id": user_id})
            # Row has `. _asdict()` in SQLAlchemy 1.4+ and 2.0
            return [row._asdict() for row in result]

    return get_user_claims


def build_create_claim(db_engine: Engine) -> Callable:
    @tool
    def create_claim(user_id: int, title: str, problem: str) -> dict:
        """Insert a new claim into the DB for a given user."""
        query = text("""
            INSERT INTO claim (user_id, title, status, problem)
            VALUES (:user_id, :title, 'Pending', :problem)
            RETURNING id, user_id, title, status, created_at
        """)
        with db_engine.begin() as conn:
            row: Row | None = conn.execute(
                query, {"user_id": user_id, "title": title, "problem": problem}
            ).fetchone()

            if row is None:
                raise RuntimeError("Failed to create claim — no row returned.")

            return row._asdict()

    return create_claim
