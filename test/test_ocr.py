import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import numpy as np
from app.core.paddle_engine import PaddleEngine

engine = PaddleEngine()

if len(sys.argv) > 1:
    img = cv2.imread(sys.argv[1])
    if img is None:
        print(f"이미지를 읽을 수 없어요. : {sys.arvg[1]}")
        sys.exit(1)
else:
    img = np.ones((300,600,3), dtype=np.uint8)*255  # 흰 이미지 (텍스트 없음)
    print("이미지 없이 실행 했어요. - 빈 이미지로 PaddleOCR 로딩만 확인했어요. ")
    
# print(type(engine._ocr.predict(img)))
# print(engine._ocr.predict(img))
results = engine.recognize(img)
print(f"\n인식 결과 : {len(results)}개 입니다.")
for r in results:
    print(f" {r['text']} (신뢰도 : {r['confidence']:.2f})")

