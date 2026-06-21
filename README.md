# OCR 문서 자동입력 시스템

USB 카메라 또는 스마트폰 IP카메라로 A4 문서를 촬영하여 한글 텍스트를 인식하고 PC에 자동 입력하는 프로그램.

---

## 목표

- 인쇄체 + 필기체 모두 인식
- 특정 문서 양식에 맞춰 PaddleOCR fine-tuning (양식별 모델 분리)
- Mac / Windows 11 양쪽 지원
- 양식 추가 시 코드 수정 없이 yaml + 모델 파일 추가만으로 확장

---

## 기술 스택

| 항목 | 선택 |
|---|---|
| 언어 | Python 3.11 |
| 카메라 캡처 | OpenCV (cv2.VideoCapture) |
| OCR | PaddleOCR PP-OCRv4 (korean) |
| 자동입력 | pyautogui (Mac: 접근성 권한 필요) |
| UI | PySide6 (미정) |
| 패키징 | PyInstaller |

---

## 디렉토리 구조

```
ocr-docu/
├── main.py                      # 조립만 담당 (30줄 이내)
├── app/
│   ├── interfaces/              # 추상 클래스 (계약)
│   │   ├── camera_base.py
│   │   ├── ocr_engine_base.py
│   │   ├── corrector_base.py
│   │   └── typer_base.py
│   ├── core/                    # 구현체
│   │   ├── camera_usb.py
│   │   ├── camera_ip.py
│   │   ├── camera_factory.py
│   │   ├── preprocess.py
│   │   └── paddle_engine.py
│   ├── correction/
│   │   ├── confidence_filter.py
│   │   ├── hangul_rules.py
│   │   └── dict_corrector.py
│   ├── output/
│   │   ├── typer_mac.py
│   │   └── typer_win.py
│   ├── pipeline/
│   │   ├── steps.py             # 각 단계 클래스
│   │   └── runner.py            # OCRPipeline, build_pipeline()
│   ├── config.py                # load_profile() — yaml 로드
│   └── ui/
│       └── main_window.py
├── profiles/                    # 문서 양식별 설정
│   └── default.yaml
├── models/
│   ├── base/                    # PaddleOCR 기본 모델
│   └── finetuned/               # 양식별 fine-tuned 모델
├── docs/
│   └── dev_rules.md             # 개발 규칙
└── requirements.txt
```

---

## 아키텍처

Hexagonal Architecture (Ports & Adapters) + Pipeline 패턴 조합.

```
[Camera Source]          [OCR Engine]         [Output]
USB / IP Camera  →  PaddleOCR / TrOCR  →  Mac / Windows
      ↑                    ↑                    ↑
 CameraBase          OCREngineBase          TyperBase
 (interface)          (interface)           (interface)
      └──────────────────┬──────────────────────┘
                         │
               [Pipeline Runner]
        Capture → Preprocess → OCR → Correction → Output
                         │
                  PipelineContext
               (단계 간 데이터 전달)
```

**핵심 원칙:** 인터페이스 교체 시 상위 코드 변경 없음. 양식 추가 시 코드 변경 없음.

---

## 실행 (개발 중)

```bash
python main.py                        # 기본 프로파일
python main.py --profile profiles/custom.yaml  # 특정 양식
```

---

## 개발 순서

1. ✅ `interfaces/` 추상 클래스 정의
2. ✅ `paddle_engine.py` — PaddleOCR 연동
3. `camera_usb.py` + `camera_factory.py` — 카메라 캡처
4. `pipeline/` 골격 — 카메라→텍스트 E2E 최소 동작
5. `correction/` — 신뢰도 필터 + 한글 규칙 보정
6. `output/` — 자동입력 연결
7. Fine-tuning 데이터 수집 및 학습
8. `ui/` 구성
