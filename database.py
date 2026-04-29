from __future__ import annotations

import hashlib
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "marketplace.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL DEFAULT '',
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'buyer',
                is_subscription INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                phone TEXT NOT NULL DEFAULT '',
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                media TEXT NOT NULL DEFAULT '',
                is_featured INTEGER NOT NULL DEFAULT 0,
                clicks INTEGER NOT NULL DEFAULT 0,
                whatsapp_clicks INTEGER NOT NULL DEFAULT 0,
                calls INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'General',
                price REAL NOT NULL DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS banner_ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media TEXT NOT NULL,
                target_url TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(vendor_id) REFERENCES users(id)
            );
            """
        )

        # Lightweight migrations for existing installations.
        user_columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
        if "first_name" not in user_columns:
            conn.execute("ALTER TABLE users ADD COLUMN first_name TEXT NOT NULL DEFAULT ''")
        if "is_subscription" not in user_columns:
            conn.execute("ALTER TABLE users ADD COLUMN is_subscription INTEGER NOT NULL DEFAULT 0")
        ads_columns = {row["name"] for row in conn.execute("PRAGMA table_info(ads)").fetchall()}
        if "whatsapp_clicks" not in ads_columns:
            conn.execute("ALTER TABLE ads ADD COLUMN whatsapp_clicks INTEGER NOT NULL DEFAULT 0")
        if "calls" not in ads_columns:
            conn.execute("ALTER TABLE ads ADD COLUMN calls INTEGER NOT NULL DEFAULT 0")
        if "is_active" not in ads_columns:
            conn.execute("ALTER TABLE ads ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1")

        owner_email = "samzinovpro@gmail.com"
        owner_hash = hashlib.sha256("!n0v.".encode("utf-8")).hexdigest()
        conn.execute(
            """
            INSERT OR IGNORE INTO users(first_name, full_name, email, password_hash, role, is_subscription)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("Samuel", "Samuel Moussavou", owner_email, owner_hash, "admin", 1),
        )
        conn.execute(
            """
            UPDATE users
            SET first_name = ?, full_name = ?, role = ?, is_subscription = 1
            WHERE email = ?
            """,
            ("Samuel", "Samuel Moussavou", "admin", owner_email),
        )

        existing_banner = conn.execute("SELECT COUNT(*) AS n FROM banner_ads").fetchone()["n"]
        if existing_banner == 0:
            conn.execute(
                """
                INSERT INTO banner_ads(media, target_url, expires_at)
                VALUES (?, ?, ?)
                """,
                (
                    "https://images.unsplash.com/photo-1556741533-6e6a62bd8b49?auto=format&fit=crop&w=1200&q=80",
                    "https://example.com",
                    (date.today() + timedelta(days=30)).isoformat(),
                ),
            )

        # Seed starter marketplace vendors/listings inspired by the legacy app.
        seeds = [
            {
                "first_name": "Elijah",
                "full_name": "Elijah Shoe World",
                "email": "elijah.shoeworld@biliwaka.local",
                "phone": "256775000101",
                "title": "Elijah Shoe World",
                "description": "Quality men and women shoes, office shoes, sneakers, and school shoes at fair prices.",
                "price": 85000,
                "category": "Fashion",
                "media": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=900&q=80",
                "location_hint": "Kampala",
            },
            {
                "first_name": "Mafashid",
                "full_name": "Mafashid Collections",
                "email": "mafashid.collections@biliwaka.local",
                "phone": "256775000102",
                "title": "Mafashid Collections",
                "description": "Trendy shoe collections with new arrivals weekly, including casual, official, and party footwear.",
                "price": 95000,
                "category": "Fashion",
                "media": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
                "location_hint": "Kampala",
            },
            {
                "first_name": "Sarah",
                "full_name": "Sarahs Touch Salon",
                "email": "sarahstouchsalon@gmail.com",
                "phone": "256775000103",
                "title": "Sarahs Touch Salon",
                "description": "Professional salon services: braiding, hair treatment, manicure, pedicure, and bridal touch-ups.",
                "price": 40000,
                "category": "Beauty",
                "media": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=900&q=80",
                "location_hint": "Nalumunye",
            },
        ]
        default_hash = hashlib.sha256("welcome123".encode("utf-8")).hexdigest()
        for seed in seeds:
            conn.execute(
                """
                INSERT OR IGNORE INTO users(first_name, full_name, email, password_hash, role, is_subscription)
                VALUES (?, ?, ?, ?, 'vendor', 1)
                """,
                (
                    seed["first_name"],
                    seed["full_name"],
                    seed["email"],
                    default_hash,
                ),
            )
            seller = conn.execute("SELECT id FROM users WHERE email = ?", (seed["email"],)).fetchone()
            existing_ad = conn.execute("SELECT id FROM ads WHERE title = ? AND user_id = ?", (seed["title"], seller["id"])).fetchone()
            if not existing_ad:
                conn.execute(
                    """
                    INSERT INTO ads(
                        user_id, phone, title, description, media, is_featured, clicks, whatsapp_clicks, calls, is_active,
                        created_at, expires_at, category, price
                    )
                    VALUES (?, ?, ?, ?, ?, 1, 0, 0, 0, 1, ?, ?, ?, ?)
                    """,
                    (
                        seller["id"],
                        seed["phone"],
                        seed["title"],
                        f"{seed['description']} Location: {seed['location_hint']}.",
                        seed["media"],
                        date.today().isoformat(),
                        (date.today() + timedelta(days=45)).isoformat(),
                        seed["category"],
                        seed["price"],
                    ),
                )
