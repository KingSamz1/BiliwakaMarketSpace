from __future__ import annotations

import hashlib
import sqlite3
from typing import Optional

from database import get_connection


def hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def register_user(full_name: str, email: str, password: str, role: str = "buyer") -> tuple[bool, str]:
    email = email.strip().lower()
    if not full_name.strip() or not email or not password:
        return False, "All fields are required."

    first_name = full_name.strip().split()[0]
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO users(first_name, full_name, email, password_hash, role, is_subscription)
                VALUES (?, ?, ?, ?, ?, 0)
                """,
                (first_name, full_name.strip(), email, hash_password(password), role),
            )
        return True, "Registration successful."
    except sqlite3.IntegrityError:
        return False, "Email already exists."


def login_user(email: str, password: str) -> Optional[dict]:
    email = email.strip().lower()
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, first_name, full_name, email, role, is_subscription, password_hash
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if not row:
        return None
    if row["password_hash"] != hash_password(password):
        return None

    return {
        "id": row["id"],
        "first_name": row["first_name"],
        "full_name": row["full_name"],
        "email": row["email"],
        "role": row["role"],
        "is_subscription": bool(row["is_subscription"]),
    }
