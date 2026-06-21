from paddleocr import PaddleOCR
import numpy as np

from app.interfaces.ocr_engine_base import OCREngineBase

class PaddleEngine(OCREngineBase):

    def __init__(self, lang: str = "korean", use_gpu: bool = False):
        self._ocr = PaddleOCR(
            use_angle_cls=True, # 문서 기울기 방향 자동 감지
            lang=lang,          # 언어 : korean , 한글모델 자동 다운로드
            use_gpu=use_gpu,
        )

    def recognize(self, frame: np.ndarray) -> list[dict]:
        raw = self._ocr.ocr(frame, cls=True)    # PaddleOCR 실행 

        results = []
        if not raw or not raw[0]:               # 안식 결과 없으면 빈 리스트 반환
            return results
        
        for line in raw[0]:
            bbox, (text, confidence) = line     # PaddleOCR 출력 구조 언패킹
            results.append({
                "text": text,
                "confidence": float(confidence),
                "bbox": bbox,
            })
        
        return results