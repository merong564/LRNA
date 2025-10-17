"""
SQLite DB 핸들러 모듈
- 주행 전략과 근거를 기록 및 조회합니다.
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "driving_log.db")

def init_db():
    """DB 테이블 생성"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()                          # 커서 생성
    # 커리 생성
    cursor.execute("""                              
        CREATE TABLE IF NOT EXISTS driving_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detections TEXT,
            strategy TEXT,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_record(detections: list, strategy: str, reason: str):
    """주행 전략 기록 추가"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO driving_log (detections, strategy, reason) VALUES (?, ?, ?)",
        (json.dumps(detections, ensure_ascii=False), strategy, reason)
    )
    conn.commit()
    conn.close()

def fetch_latest_record():
    """가장 최근 주행 전략 조회"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT detections, strategy, reason, timestamp FROM driving_log ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "detections": json.loads(row[0]),
            "strategy": row[1],
            "reason": row[2],
            "timestamp": row[3]
        }
    else:
        return None

def fetch_all_records():
    """전체 로그 조회"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, detections, strategy, reason, timestamp FROM driving_log ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "detections": json.loads(r[1]),
            "strategy": r[2],
            "reason": r[3],
            "timestamp": r[4]
        } for r in rows
    ]