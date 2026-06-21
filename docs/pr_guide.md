# Pull Request 가이드

main 브랜치는 직접 push가 불가합니다.
코드 수정 후 아래 순서대로 PR을 만들어 리뷰 요청을 해야 합니다.

---

## 작업 순서

### 1. 최신 코드 받기
```bash
git pull origin main
```

### 2. 작업용 브랜치 만들기
```bash
# 브랜치 이름은 작업 내용을 알 수 있게 작성
git checkout -b feature/camera-ip
```

### 3. 코드 수정 후 커밋
```bash
git add 수정한파일.py
git commit -m "작업 내용 한 줄 요약"
```

### 4. 브랜치 push
```bash
git push origin feature/camera-ip
```

### 5. GitHub에서 PR 생성
1. https://github.com/greenhelix/OCR 접속
2. 상단에 뜨는 **"Compare & pull request"** 버튼 클릭
3. 제목과 설명 작성 후 **"Create pull request"** 클릭

### 6. 리뷰 후 merge
- 리포지토리 소유자가 코드 확인 후 승인(Approve)하면 merge됩니다.
- merge 전까지 main 브랜치에 반영되지 않습니다.

---

## 브랜치 이름 규칙

| 작업 종류 | 브랜치 이름 예시 |
|---|---|
| 새 기능 추가 | `feature/camera-ip` |
| 버그 수정 | `fix/ocr-output-format` |
| 문서 수정 | `docs/update-readme` |
| 설정 변경 | `config/add-profile-custom` |

---

## 주의사항

- 브랜치 하나에 하나의 작업만 담을 것
- 커밋 전 반드시 `git pull origin main` 으로 최신 상태 확인
- main 브랜치에 직접 push 시 거절됩니다
