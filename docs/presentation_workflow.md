# Presentation Workflow Guide

## 🎯 Overview

Haru Presentation Builder는 **PDF 인쇄용 정적 HTML**을 생성합니다.

### 출력 형식

| 형식 | 용도 | 특징 |
|------|------|------|
| **HTML** | PDF 인쇄용 | 브라우저 Ctrl+P로 PDF 변환 |
| **PPTX** | 편집/발표용 | JSON 기반 (편집 가능) |

---

## 📁 프로젝트 구조 (Hybrid Pipeline)

```
projects/
├── eumlogistic/                   # 프로젝트 1
│   ├── source_style.json          # PDF 분석 원본 (READ-ONLY)
│   ├── presentation.json          # 작업용 (수정 가능)
│   ├── presentation.html          # 생성된 HTML
│   ├── presentation.pptx          # 변환된 PPTX (선택)
│   ├── review_report.md           # QA 검토 결과 (선택)
│   └── screenshots/               # QA 비교용 스크린샷 (선택)
│       ├── html/                  # HTML 원본
│       └── pptx/                  # PPTX 결과물
│
└── bluehive/                      # 프로젝트 2
    └── ...
```

### 핵심 원칙

| 파일 | 역할 | 수정 가능 |
|------|------|----------|
| `source_style.json` | 원본 분석 데이터 (롤백용) | ❌ READ-ONLY |
| `presentation.json` | 작업용 (콘텐츠/스타일 수정) | ✅ 수정 가능 |
| `review_report.md` | QA 검토 결과 | - 자동 생성 |

---

## 📋 워크플로우

### Step 1: 프로젝트 폴더 생성

```bash
mkdir projects/my-project
```

### Step 2: PDF 스타일 분석

1. Chrome에서 PDF 열기
2. AI에게 요청: `/pdf my-project`
3. 결과:
   - `projects/my-project/source_style.json` (원본 분석)
   - `projects/my-project/presentation.json` (작업용 복사본)

**AI 동작:**
- `mcp_kapture_keypress({ key: "ArrowRight" })`로 슬라이드 탐색
- 스크린샷 캡처 및 디자인 토큰 분석

### Step 3: 콘텐츠 수정 (필요시)

**presentation.json에서 직접 수정:**
- 슬라이드 텍스트 변경
- 디자인 토큰 조정
- 슬라이드 추가/삭제

**롤백이 필요한 경우:**
```bash
# source_style.json에서 다시 복사
cp projects/my-project/source_style.json projects/my-project/presentation.json
```

### Step 4: HTML 생성

AI 요청: `/generate my-project`

결과: `projects/my-project/presentation.html`

### Step 5: HTML 검토 (JSON 명세 + 심미성 분석)

HTML 생성 후 Live Server로 검토:

1. `/generate` 완료 후 Live Server로 HTML 열기
2. AI가 슬라이드별 스크린샷 캐처
3. **`presentation.json` 명세와 비교하여 검증**

**AI 검토 요청:**
```
/review my-project http://localhost:5500/projects/my-project/presentation.html
```

#### Phase 1: JSON 명세 검토
- 슬라이드 개수 일치
- 텍스트 내용 정확성
- 색상 팔레트 적용
- 레이아웃/템플릿 정확성
- 이미지 로드 및 배치

#### Phase 2: 심미성 분석 (Design Audit)
LLM 이미지 분석으로 디자인 품질 검사:

| 항목 | 설명 |
|------|------|
| 여백 일관성 | 슬라이드 간 padding/margin 통일 |
| 타이포그래피 위계 | 제목 > 부제 > 본문 크기 구분 |
| 색상 대비 | 텍스트와 배경 간 가독성 |
| 정렬 일관성 | 좌/우/중앙 정렬 통일 |
| 텍스트 밀도 | 슬라이드당 적정 텍스트 양 |
| 시각적 균형 | 좌우/상하 요소 분포 |
| 이미지 비율 | 왜곡 없이 자연스러운 비율 |
| 요소 간격 | 카드, 리스트 등 반복 요소 간격 |

**결과:**
- `projects/my-project/review_report.md` (JSON 명세 + 심미성 분석)
- `projects/my-project/screenshots/html/` (슬라이드별 스크린샷)

### Step 6: PDF 또는 PPTX 변환

**PDF 변환:**
1. 브라우저에서 HTML 열기
2. `Ctrl+P` → "PDF로 저장"
3. 여백: 없음, 배경 그래픽: 활성화

**PPTX 변환 (편집 가능):**

**방법 1: JSON 기반 (기본)**
```bash
# AI에게 요청: "/pptx my-project"
```

**방법 2: HTML 수정 후 (자동 동기화)**
```bash
# 1. HTML 파일에서 텍스트/스타일 수정
# 2. AI에게 요청: "/pptx my-project.html" 
# → 자동으로 HTML → JSON 동기화 + PPTX 생성
```

**직접 실행 (터미널):**
```powershell
# JSON 기반
.venv\Scripts\python.exe scripts/json_to_pptx.py projects/my-project/presentation.json

# HTML 기반 (자동 동기화)
.venv\Scripts\python.exe scripts/html_to_json.py projects/my-project/presentation.html
.venv\Scripts\python.exe scripts/json_to_pptx.py projects/my-project/presentation.json
```

---

### PPTX 변환 설정

`json_to_pptx.py` 상단에서 제작마다 조정 가능:

| 설정 | 기본값 | 의미 | 조정 예시 |
|------|--------|------|----------|
| `FONT_SCALE` | 0.95 | 폰트 크기 비율 | 0.9 (-10%), 1.0 (원본) |
| `LINE_SPACING_SCALE` | 0.83 | 줄간격 비율 (기준 1.2 대비) | 1.0 (1.2 유지), 0.75 (더 좁게) |
| `PARAGRAPH_SPACING_SCALE` | 0.0 | 문단 간격 비율 (폰트 대비) | 0.5 (폰트의 50%) |
| `IMAGE_CORNER_RATIO` | 0.05 | 이미지 라운딩 비율 | 0.0 (없음), 0.1 (10%) |

---

## 🖨️ PDF 변환 설정

| 항목 | 설정값 |
|------|--------|
| 대상 | PDF로 저장 |
| 레이아웃 | 가로 (Landscape) |
| 용지 크기 | A4 |
| 여백 | 없음 |
| 배경 그래픽 | ✅ 활성화 |

---

## 🛠️ 파일 설명

| 파일 | 용도 | 수정 |
|------|------|------|
| `source_style.json` | PDF 분석 원본 (롤백용) | ❌ |
| `presentation.json` | 작업용 (수정 시 여기서) | ✅ |
| `presentation.html` | PDF 인쇄용 정적 HTML | - |
| `presentation.pptx` | PowerPoint 파일 (선택) | - |
| `review_report.md` | QA 검토 결과 (선택) | - |
| `screenshots/` | HTML/PPTX 비교 스크린샷 (선택) | - |

---

## 🔍 Troubleshooting

### Issue: PDF 텍스트 추출 안 됨
**Solution:** PDF embed는 DOM 접근 불가. 수동 입력 사용.

### Issue: PPTX 변환 시 빈 슬라이드
**Solution:** Python 패키지 설치 확인: `pip install python-pptx pillow`

### Issue: 스타일 수정 후 원본 복원 필요
**Solution:** `source_style.json`에서 `presentation.json`으로 다시 복사

---

**Version:** 3.6.0  
**Last Updated:** November 2025
