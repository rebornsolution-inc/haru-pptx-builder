# Haru Presentation Builder

PDF 인쇄용 정적 HTML 프레젠테이션을 생성하는 AI 기반 빌더입니다.

## 🎯 Overview

Haru Presentation Builder는 다양한 입력 소스를 분석하여 **브라우저 인쇄(Ctrl+P)로 PDF 변환 가능한 정적 HTML**을 생성합니다.

**출력 특징:**
- 🖨️ **PDF 인쇄 최적화** - `@media print`, `page-break-after` 적용
- 📐 **16:9 기본 비율** - A4 용지, 여백 없음 설정
- ❌ **정적 문서** - 키보드 네비게이션, 슬라이드 인디케이터 없음
- 🔄 **PPTX 변환 지원** - JSON 기반 편집 가능 PPTX 생성

## 🚀 Quick Start

### Prerequisites

- Node.js 16+
- Python 3.9+ (PPTX 변환용)
- VS Code with GitHub Copilot
- Kapture MCP extension (PDF 분석용)

### Installation

```bash
# Clone the repository
git clone https://github.com/rebornsolution-inc/haru-pptx-builder.git
cd haru-pptx-builder

# Node.js dependencies
npm install

# Python dependencies (PPTX 변환용)
python -m venv .venv
.venv\Scripts\activate
pip install playwright python-pptx
playwright install chromium
```

## 📖 Usage

### Step 1: 프로젝트 폴더 생성

```bash
# 새 프로젝트 폴더 생성
mkdir projects/my-project
```

### Step 2: PDF 스타일 분석

```bash
# Chrome에서 PDF 열기
# AI에게 요청: "/pdf my-project"
# 결과: 
#   - projects/my-project/source_style.json (원본 분석)
#   - projects/my-project/presentation.json (작업용 복사본)
```

### Step 3: 콘텐츠 수정 (필요시)

```bash
# presentation.json에서 직접 수정
# source_style.json은 수정하지 않음 (롤백용 보존)
```

### Step 4: HTML 생성

```bash
# AI에게 요청: "/generate my-project"
# 결과: projects/my-project/presentation.html
```

### Step 5: PDF 또는 PPTX 변환

**PDF 변환:**
```
1. 브라우저에서 HTML 파일 열기
2. Ctrl+P (인쇄)
3. 대상: "PDF로 저장"
4. 여백: "없음"
5. 배경 그래픽: 활성화
6. 저장
```

**PPTX 변환 (편집 가능):**
```bash
# 방법 1: JSON 기반 (기본)
# AI에게 요청: "/pptx my-project"

# 방법 2: HTML 수정 후 (HTML → JSON 자동 동기화)
# HTML 파일에서 텍스트/스타일 수정 후
# AI에게 요청: "/pptx my-project.html"
# → 자동으로 JSON 업데이트 + PPTX 생성
```

## 📁 Project Structure

```
haru-pptx-builder/
├── .github/
│   └── copilot-instructions.md    # AI 동작 규칙 (상세)
├── docs/
│   ├── presentation_workflow.md   # 워크플로우 가이드
│   └── slide_templates.md         # 슬라이드 템플릿 문서
├── projects/                      # 프로젝트별 폴더
│   └── [project-name]/
│       ├── source_style.json      # PDF 분석 원본 (READ-ONLY)
│       ├── presentation.json      # 작업용 (수정 가능)
│       ├── presentation.html      # 생성된 HTML
│       └── ...
└── scripts/
    ├── json_to_pptx.py            # JSON→PPTX (편집 가능)
    └── html_to_json.py            # HTML→JSON (역변환)
```

## 🎨 Slide Templates

| 템플릿 | 용도 | 레이아웃 |
|--------|------|----------|
| `hero-cover` | 타이틀 슬라이드 | 중앙 정렬 |
| `table-of-contents` | 목차 | 2x2 또는 3x2 그리드 |
| `section-divider` | 섹션 구분 | 중앙 최소화 |
| `content-text` | 본문 내용 | 좌우 분할 |
| `bullet-list` | 요점 목록 | 중앙 리스트 |

## 🛠️ Commands

| 명령어 | 설명 |
|--------|------|
| `/pdf [project]` | PDF 스타일 분석 → `source_style.json` + `presentation.json` |
| `/web [project] [URL]` | 웹사이트 디자인 분석 |
| `/generate [project]` | HTML 생성 → `presentation.html` |
| `/pptx [project or HTML]` | PPTX 변환 (JSON 기반 또는 HTML 자동 동기화) |
| `/review [project] [URL]` | QA 검토 (JSON 명세 + 심미성 분석) → `review_report.md` |

> 📖 **상세 명령어 스펙:** `.github/copilot-instructions.md` 참조

## 📄 License

MIT License - See LICENSE file for details

---

**Version:** 3.6.0  
**Last Updated:** November 2025
