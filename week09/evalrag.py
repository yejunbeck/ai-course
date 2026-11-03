
import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
rows = con.execute(
    "SELECT id, name, embedding FROM facility"
).fetchall()
con.close()

names = [r[1] for r in rows]
V = np.stack([
    np.frombuffer(r[2], dtype=np.float32)
    for r in rows
])
V = V / np.linalg.norm(V, axis=1, keepdims=True)

# (질문, 정답 동아리 이름) - 총 10개
TESTS = [
    ("파이썬 공부하는 동아리 있어?", "파이썬 연구회"),
    ("코딩 테스트 준비하는 모임은?", "알고리즘 스터디"),
    ("웹사이트를 직접 만들어 보고 싶어", "웹 개발 동아리"),
    ("머신러닝과 딥러닝을 배우고 싶어", "인공지능 연구회"),
    ("게임을 직접 개발하는 동아리는?", "게임 개발 동아리"),
    ("영어로 대화 연습을 하고 싶어", "영어 회화 모임"),
    ("사진 찍는 취미를 함께하고 싶어", "사진 동아리"),
    ("축구를 같이 할 수 있는 모임은?", "축구 동아리"),
    ("주식 투자 공부를 하고 싶어", "투자 스터디"),
    ("봉사 활동에 참여하고 싶어", "봉사 동아리"),
]

hit1 = hit3 = 0

for q, want in TESTS:
    qv = np.array(
        ollama.embed(model="bge-m3", input=q).embeddings[0],
        dtype=np.float32
    )
    qv = qv / np.linalg.norm(qv)

    top = [
        names[i]
        for i in np.argsort(-(V @ qv))[:3]
    ]

    ok1 = top[0] == want
    ok3 = want in top

    hit1 += ok1
    hit3 += ok3

    mark = "O" if ok1 else ("△" if ok3 else "X")
    print(
        f"{mark} 질문: {q}\n"
        f"  검색 1위: {top[0]}\n"
        f"  정답: {want}\n"
        f"  상위 3개: {top}\n"
    )

print(f"\n1위 적중: {hit1}/{len(TESTS)} "
      f"({hit1 / len(TESTS) * 100:.1f}%)")
print(f"3위 안 적중: {hit3}/{len(TESTS)} "
      f"({hit3 / len(TESTS) * 100:.1f}%)")
