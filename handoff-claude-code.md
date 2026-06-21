# 프로젝트 인수인계서 — USB/스마트폰 카메라 기반 한글 문서 OCR 자동입력 시스템

> 이 문서는 Claude Code(CLI)에 전체 컨텍스트를 전달하기 위한 인수인계서입니다.
> 설계는 이미 확정되었으며, 아래 구조와 원칙을 그대로 따라 구현을 진행해주세요.

---

## 1. 프로젝트 목표

USB 카메라(주) 또는 스마트폰 IP카메라(보조, 같은 Wi-Fi 영상스트림)로 A4 문서를 촬영하여,
PaddleOCR로 한글 텍스트를 인식하고, 자동 보정을 거쳐 PC/스마트폰에 자동 입력하는 프로그램.

- **인쇄체 + 필기체** 모두 대상
- **특정 문서 양식**에 맞춰 PaddleOCR을 **fine-tuning** (양식별로 모델이 달라질 수 있음)
- **Mac / Windows 11** 양쪽에서 동작
- 향후 **문서 양식이 계속 추가될 예정** → 양식 추가 시 기존 코드를 최대한 건드리지 않아야 함

---

## 2. 핵심 설계 원칙 (반드시 준수)

1. **`main.py`는 조립만 담당, 로직 0줄.** 실제 동작 코드는 전부 하위 모듈에 위치. `main.py`는 프로파일을 로드하고 파이프라인을 조립해서 실행하는 것 외의 책임을 갖지 않음 (목표: 30줄 이내).

2. **문서 양식별 설정은 코드가 아닌 `profiles/*.yaml`로 분리.** 새 양식 추가 시 yaml 파일 추가 + fine-tuned 모델 저장만으로 끝나야 하며, 기존 코드 수정이 발생하면 설계 위반으로 간주.

3. **모든 외부 의존성(카메라, OCR 엔진, 자동입력)은 추상 인터페이스(`interfaces/`)를 통해 접근.** 구현체를 교체해도(예: USB↔IP카메라, PaddleOCR↔다른 엔진) 상위 코드는 변경되지 않아야 함. (Hexagonal/Ports & Adapters 패턴 차용)

4. **처리 흐름은 Pipeline 패턴.** Capture → Preprocess → OCR → Correction → Output 각 단계를 독립 클래스(`PipelineStep`)로 분리하고, 단계 추가/제거/순서변경이 리스트 조작만으로 가능해야 함.

5. **카메라는 소스 문자열 하나로 USB/IP카메라 자동 판별.** `source`가 `http://` 또는 `rtsp://`로 시작하면 IP카메라(스마트폰), 숫자면 USB로 처리. IP카메라는 연결 워밍업 및 자동 재연결 로직 포함.

---

## 3. 확정된 디렉토리 구조

```
ocr-doc-app/
├── main.py                      # 조립만 (30줄 이내)
├── app/
│   ├── interfaces/               # 추상 클래스(계약)
│   │   ├── camera_base.py
│   │   ├── ocr_engine_base.py
│   │   ├── corrector_base.py
│   │   └── typer_base.py
│   ├── core/                     # 구현체
│   │   ├── camera_usb.py
│   │   ├── camera_ip.py          # 스마트폰 Wi-Fi 스트림
│   │   ├── camera_factory.py     # source 문자열 → 적절한 카메라 구현체 생성
│   │   ├── preprocess.py         # 기울기보정, CLAHE, ROI crop
│   │   └── paddle_engine.py      # PaddleOCR 연동, fine-tuned 모델 로드
│   ├── correction/
│   │   ├── confidence_filter.py  # confidence score 기반 필터링
│   │   ├── hangul_rules.py       # 자모 조합 유효성 검사
│   │   └── dict_corrector.py     # 사전/문맥 기반 보정
│   ├── output/
│   │   ├── typer_mac.py          # macOS 자동입력
│   │   └── typer_win.py          # Windows 자동입력
│   ├── pipeline/
│   │   ├── steps.py              # CaptureStep, PreprocessStep, OCRStep, CorrectionStep
│   │   └── runner.py             # OCRPipeline, build_pipeline(profile)
│   ├── config.py                 # load_profile() — yaml 로드
│   └── ui/
│       └── main_window.py        # 카메라 미리보기 + 결과 + 수정 UI
├── profiles/                      # 문서 양식별 설정 (핵심)
│   ├── default.yaml
│   └── README.md                 # 새 프로파일 추가 가이드
├── models/
│   ├── base/                     # PaddleOCR 기본 제공 모델
│   └── finetuned/
│       └── {양식명}_v1/
├── training/
│   └── {양식명}/
│       ├── data/images/          # 라인 단위로 잘라낸 이미지
│       ├── labels.txt            # image_path\t정답텍스트
│       └── train_config.yml
└── requirements.txt
```

---

## 4. 이미 합의된 코드 스니펫 (참고용 — 그대로 또는 개선해서 사용)

### main.py (목표 형태)
```python
from app.config import load_profile
from app.pipeline.runner import build_pipeline
from app.ui.main_window import MainWindow

def main():
    profile = load_profile("profiles/default.yaml")
    pipeline = build_pipeline(profile)
    app = MainWindow(pipeline=pipeline, profile=profile)
    app.run()

if __name__ == "__main__":
    main()
```

### profiles/default.yaml (형태 예시)
```yaml
name: default
camera:
  source: "0"   # 테스트: USB(정수) / 운영 전환 시: "http://192.168.x.x:8080/video"
ocr:
  model_path: "models/base/"
  lang: korean
  use_gpu: false
roi: []          # 양식 확정 후 칸 좌표 채울 예정
correction:
  dict_path: "correction/dicts/default.txt"
  min_confidence: 0.75
```

### 카메라 소스 자동 판별 로직 (camera_factory.py에 구현)
```python
def is_network_source(source: str) -> bool:
    return isinstance(source, str) and (
        source.startswith("http://") or
        source.startswith("https://") or
        source.startswith("rtsp://")
    )
# True면 camera_ip.py 구현체, False면 camera_usb.py 구현체 생성
```

### PipelineContext (단계 간 데이터 전달용, 함수 인자 누적 방지)
```python
@dataclass
class PipelineContext:
    raw_frame: Any = None
    processed_frame: Any = None
    ocr_results: list = field(default_factory=list)
    corrected_results: list = field(default_factory=list)
    final_text: str = ""
```

---

## 5. 기술 스택 / 라이브러리

- **언어**: Python 3.10+ (Mac/Windows 공용 검증 필요)
- **카메라 캡처**: OpenCV (`cv2.VideoCapture` — USB 인덱스/HTTP/RTSP URL 동일 인터페이스)
- **OCR**: PaddleOCR (PP-OCRv4, `lang="korean"`), 추후 fine-tuning 진행 예정
  - mobile 모델(가벼움, CPU 가능) vs server 모델(정확도↑, GPU 권장) 중 초기엔 mobile로 시작
- **필기체 후보(추후)**: TrOCR (HuggingFace) — 별도 OCREngineBase 구현체로 추가 예정
- **자동입력**: `pyautogui` 기반, Mac은 접근성 권한 필요 / Windows는 `pywin32` 보조 가능
- **UI**: 미정 (PySide6 또는 Tkinter 중 추천 받고 싶음 — Claude Code에서 제안 가능)
- **패키징**: PyInstaller (Mac `.app` / Windows `.exe`)
- **GPU**: 로컬엔 없을 수 있음. Fine-tuning은 Google Colab 무료 GPU 활용 가능성 고려

---

## 6. 아직 미정 / Claude Code가 판단해도 되는 부분

- UI 프레임워크 최종 선택 (PySide6 vs Tkinter vs 기타)
- `preprocess.py`의 구체적 알고리즘 파라미터(임계값 등) — 실제 캡처 테스트하며 튜닝 필요
- `dict_corrector.py`의 사전 소스 (자체 단어집 vs 외부 맞춤법 API 연동 여부)
- 테스트 프레임워크 (pytest 권장하나 미확정)
- requirements.txt 구체 버전 핀

---

## 7. 개발 순서 제안 (참고)

1. `interfaces/` 추상 클래스 정의
2. `camera_usb.py` + `camera_factory.py` → USB 카메라로 프레임 캡처 확인
3. `camera_ip.py` → 스마트폰 IP카메라 연동 테스트 (보조)
4. `paddle_engine.py` → 기본 모델로 1차 인식 확인 (fine-tuning 이전)
5. `pipeline/` 골격 연결 → 카메라→텍스트 출력까지 최소 동작 버전(E2E) 완성
6. 특정 문서 양식 데이터 수집/라벨링 → fine-tuning
7. `correction/` 모듈 추가
8. `output/` 자동입력 연결
9. `ui/` 구성 및 다듬기

---

## 8. 비용/환경 참고사항

- PaddleOCR은 Apache 2.0, 완전 무료 (상업적 이용 포함)
- 로컬 추론은 비용 없음. Fine-tuning도 로컬/Colab 무료 GPU로 가능 (클라우드 GPU는 선택사항)
- Mac은 Apple Silicon에서도 PaddleOCR 정상 동작하나 GPU 가속은 제한적 → CPU 또는 mobile 모델 권장
- Windows는 NVIDIA GPU 보유 시 PaddleOCR-GPU로 학습 속도 확보 가능
