# Windows 환경 설정 가이드

---

## 1. Git 설치

https://git-scm.com/downloads/win 에서 다운로드 후 설치.
설치 시 옵션은 전부 기본값으로 진행.

설치 확인:
```bash
git --version
```

---

## 2. Python 3.11 설치

https://www.python.org/downloads/release/python-3119/ 에서
`Windows installer (64-bit)` 다운로드 후 설치.

> ⚠️ 설치 화면 첫 페이지에서 **"Add Python to PATH"** 체크박스 반드시 체크

설치 확인:
```bash
python --version   # Python 3.11.x 나와야 함
```

---

## 3. 프로젝트 받기

```bash
git clone https://github.com/greenhelix/OCR.git
cd OCR
```

---

## 4. 패키지 설치

NVIDIA GPU 없는 경우 (대부분):
```bash
pip install paddleocr paddlepaddle numpy opencv-python
```

NVIDIA GPU 있는 경우:
```bash
pip install paddleocr paddlepaddle-gpu numpy opencv-python
```

---

## 5. 작업 시작할 때마다

```bash
cd OCR          # 프로젝트 폴더로 이동
git pull        # 최신 코드 받기 (필수)
```

---

> **Python 버전 주의:** 이 프로젝트는 Python 3.11을 사용합니다. 3.12 이상이나 3.13은 PaddleOCR과 호환이 안 됩니다.
