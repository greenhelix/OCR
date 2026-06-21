# PaddleOCR 3.x 공식 라이브러리
from paddleocr import PaddleOCR
# numpy: 카메라에서 넘어오는 이미지 프레임은 numpy 배열 형태 (H x W x 3, BGR)
import numpy as np

# 이 클래스가 구현해야 할 인터페이스(계약) — recognize() 메서드 구현을 강제함
from app.interfaces.ocr_engine_base import OCREngineBase


class PaddleEngine(OCREngineBase):
    """
    PaddleOCR 3.x 기반 한글 OCR 구현체.
    OCREngineBase를 상속하므로 다른 OCR 엔진으로 교체 시 이 클래스만 바꾸면 됨.
    """

    def __init__(self, lang: str = "korean", device: str = "cpu"):
        """
        lang   : 인식 언어. "korean" 지정 시 한글 모델(korean_PP-OCRv5_mobile_rec) 자동 다운로드.
        device : "cpu" 또는 "gpu". Windows NVIDIA GPU 환경에서는 "gpu" 지정.
                 Mac(Apple Silicon)은 NVIDIA GPU 없으므로 항상 "cpu".
        """
        self._ocr = PaddleOCR(
            lang=lang,
            device=device,
            use_doc_orientation_classify=True,  # 문서 전체 방향 감지 (0°/90°/180°/270° 보정)
            use_textline_orientation=True,       # 텍스트 줄 단위 방향 감지 (기울어진 줄 보정)
        )

    def recognize(self, frame: np.ndarray) -> list[dict]:
        """
        이미지 프레임을 받아 인식된 텍스트 목록을 반환.

        반환 형태:
            [
                {
                    "text": "인식된 텍스트",
                    "confidence": 0.95,       # 0.0 ~ 1.0, 높을수록 정확
                    "bbox": [[x1,y1], ...]    # 텍스트 영역 꼭짓점 4개 좌표
                },
                ...
            ]
        """
        # predict()는 PaddleOCR 3.x 공식 메서드 (구버전의 ocr()는 deprecated)
        raw = self._ocr.predict(frame)

        results = []
        if not raw:                             # 인식 결과 없으면 빈 리스트 반환
            return results

        for item in raw:
            # 3.x 출력은 딕셔너리 형태
            # rec_texts : 인식된 텍스트 문자열 목록
            # rec_scores: 각 텍스트의 신뢰도 (0.0 ~ 1.0)
            # dt_polys  : 각 텍스트 영역의 꼭짓점 좌표 (numpy 배열, shape: N x 4 x 2)
            for text, score, bbox in zip(item['rec_texts'], item['rec_scores'], item['dt_polys']):
                results.append({
                    "text": text,
                    "confidence": float(score),
                    "bbox": bbox.tolist() if hasattr(bbox, 'tolist') else bbox,
                })

        return results
