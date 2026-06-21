# AI 어시스턴트를 위한 프로젝트 규칙

이 파일은 Claude Code 및 모든 AI 어시스턴트가 반드시 먼저 읽어야 합니다.
코드 작성 전에 이 규칙과 `docs/dev_rules.md`를 숙지하세요.

---

## 프로젝트 한 줄 요약

USB/스마트폰 카메라로 한글 문서를 촬영 → PaddleOCR로 텍스트 인식 → PC 자동 입력.
Mac / Windows 양쪽 지원. Python 3.11.

---

## 코드 수정 전 필수 확인 사항

1. **반드시 `git pull` 먼저** — 코드 한 줄이라도 수정하기 전에 실행
2. **`docs/dev_rules.md` 확인** — 설계 원칙 위반 여부 체크
3. **`README.md` 구조 확인** — 파일을 어느 위치에 만들어야 하는지 파악

```bash
git pull origin main
```

---

## 절대 하지 말 것

- `main.py`에 로직 코드 추가 (조립만 허용, 30줄 이내 유지)
- 새 문서 양식 지원을 위해 기존 Python 코드 수정 (yaml 파일 추가로만 해결)
- `app/interfaces/` 밖에서 카메라/OCR/자동입력 구현체 직접 호출
- `if sys.platform` 분기를 `app/output/` 밖에서 사용

---

## 디렉토리별 역할 요약

| 경로 | 역할 |
|---|---|
| `app/interfaces/` | 추상 클래스만 — 구현 코드 없음 |
| `app/core/` | 카메라·OCR 구현체 |
| `app/correction/` | 텍스트 보정 로직 |
| `app/output/` | OS별 자동입력 (Mac/Windows 분기 여기서만) |
| `app/pipeline/` | 단계 조립 및 실행 |
| `profiles/` | 문서 양식별 yaml 설정 |
| `models/` | OCR 모델 파일 (git 추적 안 함) |
| `docs/` | 개발 문서 |

---

## 커밋 전 체크리스트

- [ ] `git pull` 했는가
- [ ] 설계 원칙(`docs/dev_rules.md`) 위반 없는가
- [ ] 새 파일 위치가 디렉토리 역할에 맞는가
- [ ] `README.md`의 개발 순서 진행 상황을 업데이트했는가
