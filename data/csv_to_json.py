"""slam_dunk_quiz_100.csv を Realtime Database インポート用の JSON に変換する。

使い方:  python3 data/csv_to_json.py
出力:    data/quizzes.json  （{"quizzes": [...]} 形式）
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "slam_dunk_quiz_100.csv"
DST = HERE / "quizzes.json"

quizzes = []
with SRC.open(encoding="utf-8-sig", newline="") as f:
    for i, row in enumerate(csv.DictReader(f), start=2):
        choices = [row[f"選択肢{n}"].strip() for n in range(1, 5)]
        answer = row["正解"].strip()
        if answer not in choices:
            raise SystemExit(f"{i}行目: 正解「{answer}」が選択肢にありません")
        quizzes.append({
            "difficulty": int(row["難易度"]),
            "question": row["問題"].strip(),
            "choices": choices,
            "answer": answer,
        })

DST.write_text(json.dumps({"quizzes": quizzes}, ensure_ascii=False, indent=2), encoding="utf-8")

counts = {d: sum(q["difficulty"] == d for q in quizzes) for d in range(1, 11)}
print(f"{len(quizzes)}問を書き出しました -> {DST}")
print("難易度別:", counts)
