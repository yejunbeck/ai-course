import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

docs = [
    "카메라 전원을 켜려면 상단의 전원 스위치를 ON 위치로 돌린다",
    "사진을 촬영하려면 셔터 버튼을 반누름하여 초점을 맞춘 후 끝까지 누른다",
    "배경을 흐리게 촬영하려면 조리개 값을 낮게 설정한다",
    "어두운 곳에서 사진을 밝게 촬영하려면 ISO 감도를 높인다",
    "동영상을 촬영하려면 동영상 모드로 전환한 후 동영상 촬영 버튼을 누른다",
    "촬영한 사진은 재생 버튼을 눌러 카메라 화면에서 확인할 수 있다",
]
D = np.stack([emb(d) for d in docs])          # 문서 10개를 미리 벡터로 (10 x 1024)

def search(question, k=3):
    q = emb(question)
    sims = D @ q / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))   # 문서 10개와의 코사인을 한 번에
    for i in np.argsort(-sims)[:k]:
        print(f"   {sims[i]:.3f}  {docs[i]}")

for question in ["카메라 전원을 어떻게 켜?", "사진은 어떻게 찍어?", "배경을 흐리게 찍으려면 어떻게 해?",
                 "어두운 곳에서 사진을 밝게 찍으려면?", "동영상은 어떻게 촬영해?"]:
    print("Q:", question)
    search(question)
