# AI-Powered Presentation Builder System

## 🎯 Project Purpose

**Haru Presentation Builder**는 다양한 입력 소스를 분석하여 **PDF 인쇄용 정적 HTML**을 생성합니다:
- **PDF presentations** (디자인 토큰 및 슬라이드 구조 추출)
- **Existing websites** (반응형 디자인 패턴 분석)  
- **Manual content** (사용자 제공 JSON 구조)

**Output:** 브라우저 인쇄(Ctrl+P)로 PDF 변환 가능한 정적 HTML:
- **페이지 단위 슬라이드** (인쇄 시 페이지 분리)
- **인라인 CSS 스타일링** (❌ Tailwind CDN 사용 금지)
- **인쇄 최적화 CSS** (`@media print`, `page-break-after`)
- ❌ 키보드 네비게이션 없음 (정적 문서)
- ❌ 슬라이드 인디케이터/진행바 없음
- ❌ JavaScript 애니메이션 없음

---

## 🖨️ Print-to-PDF Configuration

### 기본 설정
| 항목 | 기본값 | 비고 |
|------|--------|------|
| **슬라이드 비율** | 16:9 (와이드스크린) | 요청 시 4:3, A4 등 변경 가능 |
| **용지 크기** | 16:9 최적화 (297mm × 167mm) | 완벽한 16:9 비율 유지 |
| **PDF 변환** | 브라우저 인쇄 (Ctrl+P) | Chrome 권장 |
| **여백** | 0 (Margin: None) | 인쇄 설정에서 "여백 없음" 선택 |

### ⚠️ 필수 인쇄 CSS (검증 완료)

**중요:** `:last-child` 선택자가 제대로 작동하지 않는 문제가 있으므로, **마지막 슬라이드에 반드시 `last-slide` 클래스를 추가**해야 합니다.

```css
@media print {
  @page { 
    size: 297mm 167mm;  /* 16:9 완벽한 비율 (297 ÷ 167 ≈ 1.778) */
    margin: 0; 
  }
  
  html, body { 
    margin: 0 !important; 
    padding: 0 !important; 
    background: white !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  
  .slide {
    aspect-ratio: unset !important;
    width: 297mm !important;
    height: 167mm !important;
    max-height: 167mm !important;
    min-height: 167mm !important;
    overflow: hidden !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    box-sizing: border-box !important;
  }
  
  /* 마지막 슬라이드 제외한 모든 슬라이드에 페이지 브레이크 */
  .slide:not(.last-slide) {
    page-break-after: always !important;
    break-after: page !important;
  }
  
  /* 마지막 슬라이드는 페이지 브레이크 제거 (빈 페이지 방지) */
  .last-slide {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }
  
  /* 불필요한 요소 숨김 */
  .no-print {
    display: none !important;
  }
}

/* 화면용 기본 스타일 */
.slide {
  aspect-ratio: 16 / 9;
  max-height: 100vh;
  overflow: hidden;
}
```

### 🚫 Tailwind CDN 사용 금지

**문제:** Tailwind CDN이 동적으로 `<style>` 태그를 삽입하여 인쇄 시 빈 페이지가 추가될 수 있음

**해결책:** 모든 스타일을 인라인 CSS로 작성

```html
<!-- ❌ 사용 금지 -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- ✅ 인라인 CSS 사용 -->
<style>
  .flex { display: flex; }
  .flex-col { flex-direction: column; }
  /* ... 필요한 유틸리티 클래스 직접 정의 */
</style>
```

### HTML 구조 규칙

**슬라이드 사이 공백 제거:** 슬라이드 `<div>` 사이에 줄바꿈이나 공백이 있으면 인쇄 시 문제가 발생할 수 있음

```html
<!-- ✅ 올바른 방식 -->
</div><!-- Slide 1 --><div class="slide">

<!-- ❌ 잘못된 방식 -->
</div>
<!-- Slide 1 -->
<div class="slide">
```

**마지막 슬라이드 클래스:**

```html
<!-- 마지막 슬라이드에 반드시 last-slide 클래스 추가 -->
<div class="slide last-slide">
  ...
</div></body></html>
```

---

## 🔒 Core Principles

### 1. MCP Tool Policy (MANDATORY)

**⚠️ USE KAPTURE MCP TOOLS EXCLUSIVELY:**

✅ **ALLOWED (직접 호출, 활성화 불필요):**
- `mcp_kapture_list_tabs()` - 연결된 브라우저 탭 목록
- `mcp_kapture_navigate()` - URL 이동
- `mcp_kapture_dom()` - DOM 구조 가져오기
- `mcp_kapture_elements()` - 요소 찾기
- `mcp_kapture_screenshot()` - 스크린샷 캡처 ⭐ 항상 사용 가능
- `mcp_kapture_hover()` - 마우스 호버
- `mcp_kapture_click()` - 클릭
- `mcp_kapture_keypress()` - 키 입력
- `mcp_kapture_wait()` - 대기
- `mcp_kapture_select()` - 드롭다운 선택
- `mcp_kapture_back()` / `mcp_kapture_forward()` - 브라우저 히스토리 네비게이션
- `mcp_kapture_reload()` - 페이지 새로고침
- `mcp_kapture_show()` - 탭 포커스
- `mcp_kapture_close()` - 탭 닫기

❌ **FORBIDDEN:**
- `activate_web_capture_tools()` - 호출하면 BrowserMCP 도구가 활성화됨
- `mcp_microsoft_pla_*` (Microsoft Playwright MCP)
- `mcp_browsermcp_*` (Generic Browser MCP)
- `mcp_kapture_evaluate()` (does NOT exist)

**🚨 중요:**
- Kapture MCP 도구들은 **별도 활성화 함수 호출 없이 바로 사용**
- `activate_*` 함수를 호출하면 다른 MCP 도구가 활성화되어 혼란 발생
- 스크린샷 필요 시 → 바로 `mcp_kapture_screenshot()` 호출

### 2. PDF Analysis Policy

**Navigation:**
- Use `ArrowRight` / `ArrowLeft` keys for slide navigation
- Wait 300ms after each keypress for animations to settle
- Capture screenshots immediately after navigation

**Design Token Extraction:**
- Colors: Extract ALL hex values, gradients, backgrounds
- Typography: Font families, sizes (in px), weights, line-heights
- Spacing: Margins, paddings, gaps (in px)
- Layouts: Grid systems, flexbox patterns, positioning

**Slide Pattern Detection:**
- Identify template types: hero-cover, table-of-contents, section-divider, content-text, bullet-list
- Document element positions: x, y, width, height
- Note transitions: fade, slide, zoom effects

### 3. Image Handling - Unsplash Policy

**⚠️ 모든 장식용 이미지는 주제에 맞는 Unsplash 이미지 사용**

#### 🎨 Unsplash 이미지 사용법 (2024년 11월 업데이트)

**⚠️ 중요:** `source.unsplash.com` 서비스가 2024년 11월 종료되었습니다. 반드시 **고정 이미지 ID** 방식을 사용하세요.

```
https://images.unsplash.com/photo-[PHOTO_ID]?w=[WIDTH]&h=[HEIGHT]&fit=crop
```

#### 📦 물류/운송 관련 검증된 이미지 ID
| 주제 | 이미지 ID | 설명 |
|------|----------|------|
| 항공운송 | `photo-1436491865332-7a61a109cc05` | 비행기 |
| 해상운송 | `photo-1494412574643-ff11b0a5c1c3` | 컨테이너선 |
| 해상운송2 | `photo-1605745341112-85968b19335b` | 화물선 |
| 컨테이너 | `photo-1601584115197-04ecc0da31d7` | 컨테이너 야드 |
| 국제물류 | `photo-1586528116311-ad8dd3c8310d` | 물류 센터 |
| 항만 | `photo-1578575437130-527eed3abbec` | 항구 |
| 세계지도 | `photo-1526778548025-fa2f459cd5c1` | 세계 지도 |
| 창고 | `photo-1553413077-190dd305871c` | 창고 내부 |
| 크레인 | `photo-1504307651254-35680f356dfd` | 항만 크레인 |
| 트럭운송 | `photo-1519003722824-194d4455a60c` | 화물 트럭 |

#### 사용 예시
```html
<!-- 항공 운송 이미지 (400x300) -->
<img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400&h=300&fit=crop" alt="항공 운송" />

<!-- 해상 운송 이미지 (800x600) -->
<img src="https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800&h=600&fit=crop" alt="해상 운송" />

<!-- 세계 지도 배경 (1200x400) -->
<img src="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=1200&h=400&fit=crop" alt="글로벌 네트워크" />
```

#### ⚠️ 주의사항
- **❌ 사용 금지:** `https://source.unsplash.com/...` (서비스 종료)
- **✅ 사용:** `https://images.unsplash.com/photo-[ID]?w=...&h=...&fit=crop`
- 새 이미지 필요 시 Unsplash 웹사이트에서 검색 후 URL에서 ID 추출

---

## 🔄 Pipeline Structure (Hybrid)

### 파일 구조
```
projects/
├── [project-name]/                   # 프로젝트별 폴더
│   ├── source_style.json             # PDF 분석 원본 (READ-ONLY, 보존용)
│   ├── presentation.json             # 작업용 (source_style 복사본, 수정 가능)
│   ├── presentation.html             # 생성된 HTML
│   ├── presentation.pptx             # 변환된 PPTX (선택)
│   ├── review_report.md              # QA 검토 결과 (선택)
│   └── screenshots/                  # QA 비교용 스크린샷 (선택)
│       ├── html/                     # HTML 원본 스크린샷
│       │   └── slide_01.png ~ N.png
│       └── pptx/                     # PPTX 결과물 스크린샷
│           └── slide_01.png ~ N.png
│
└── [another-project]/                # 다른 프로젝트
    └── ...
```

### 워크플로우
```
PDF 분석 → source_style.json (원본 보존)
                ↓ 복사
           presentation.json (작업용, 콘텐츠 수정 가능)
                ↓ 생성
           presentation.html ─────────────────┐
                ↓                             ↓
           [자동 검토] ← Live Server      review_report.md
                ↓
           presentation.pptx
                ↓
           [수동 검토] ← Google Slides URL 제공
                ↓
           review_report.md (최종)
```

### 핵심 원칙
1. **source_style.json**: 원본 분석 데이터, 수정하지 않음 (롤백용)
2. **presentation.json**: 실제 작업 파일, 콘텐츠/스타일 수정 시 여기서 편집
3. 콘텐츠 변경 → presentation.json 직접 수정
4. 스타일 초기화 필요 → source_style.json에서 다시 복사

---

## ⚙️ Execution Commands

### `/pdf [project-name]` - Analyze PDF Presentation

**Example:** `/pdf eumlogistic`

**Behavior:**
1. Connects to browser tab with PDF open
2. Navigates slides with ArrowRight (N slides)
3. Extracts design tokens from each slide
4. Identifies slide templates
5. Generates `projects/[project-name]/source_style.json` (원본 분석)
6. Copies to `projects/[project-name]/presentation.json` (작업용)
7. **AUTO-STOPS** - User must manually request `/generate [project-name]`

### `/web [project-name] [URL]` - Analyze Website Design

**Example:** `/web bluehive https://bluehive.co.kr`

**Behavior:**
1. Connects to browser tab and navigates to URL
2. Scrolls through page to capture all sections
3. Extracts design tokens (colors, typography, spacing, layouts)
4. Captures section patterns and component styles
5. Generates `projects/[project-name]/source_style.json` (원본 분석)
6. Copies to `projects/[project-name]/presentation.json` (작업용)
7. **AUTO-STOPS** - User must manually request `/generate [project-name]`

**⚠️ Website → Presentation Considerations:**
| 이슈 | 해결책 |
|------|--------|
| 반응형 레이아웃 | 16:9 고정 비율로 재배치 |
| 스크롤 콘텐츠 | 섹션별로 슬라이드 분리 |
| 인터랙티브 요소 | 정적 스냅샷으로 변환 |
| 복잡한 애니메이션 | 제거 (인쇄용) |
| 동적 콘텐츠 | 캡처 시점 기준 고정 |
| 네비게이션/푸터 | 제외 또는 별도 슬라이드로 |

---

### `/generate [project-name]` - Generate Print-Ready HTML

**Example:** `/generate eumlogistic`

**Prerequisite:** `projects/[project-name]/presentation.json` exists

**Behavior:**
1. Reads `projects/[project-name]/presentation.json` (작업용 데이터)
2. Generates single HTML file with **인라인 CSS** (Tailwind CDN 사용 금지)
3. Applies print-optimized CSS (`@media print`, `page-break-after`)
4. **마지막 슬라이드에 `last-slide` 클래스 추가** (빈 페이지 방지)
5. **슬라이드 간 공백 제거** (`</div><!-- Slide --><div>` 형태)
6. ❌ NO slide navigation (static document)
7. ❌ NO JavaScript animations
8. Outputs to `projects/[project-name]/presentation.html`

**사용자 PDF 변환 방법:**
1. 브라우저에서 HTML 파일 열기
2. `Ctrl+P` (인쇄)
3. 대상: "PDF로 저장"
4. 용지 크기: A4, 가로 방향
5. 여백: "없음"
6. 배경 그래픽: 활성화
7. 저장

---

### `/pptx [project-name or HTML-file]` - PPTX 변환 (편집 가능)

**두 가지 사용 방법:**

#### 1️⃣ JSON 기반 변환 (기본)

**Example:** `/pptx eumlogistic`

presentation.json을 편집 가능한 PPTX로 변환합니다:

```powershell
.venv\Scripts\python.exe scripts/json_to_pptx.py projects/[project-name]/presentation.json
```

#### 2️⃣ HTML 기반 변환 (HTML 수정 후 자동 동기화)

**Example:** `/pptx eumlogistic.html` 또는 `/pptx presentation.html`

HTML 파일을 자동으로 JSON으로 동기화한 후 PPTX 생성:

```powershell
# 1. HTML → JSON 동기화
.venv\Scripts\python.exe scripts/html_to_json.py projects/[project-name]/presentation.html

# 2. JSON → PPTX 변환
.venv\Scripts\python.exe scripts/json_to_pptx.py projects/[project-name]/presentation.json
```

**사용 시나리오:**
1. `/generate eumlogistic` → HTML 생성
2. HTML 파일에서 텍스트/스타일 직접 수정
3. `/pptx eumlogistic.html` → **자동으로 JSON 업데이트 + PPTX 생성** ⭐

**특징:**
- ✅ 텍스트/도형 편집 가능 (실제 PowerPoint 요소)
- ✅ PowerPoint에서 직접 수정 가능
- ✅ HTML 수정사항 자동 반영 (.html 확장자 사용 시)
- ⚠️ 복잡한 CSS 레이아웃은 수동 조정 필요

**폰트 조정 설정 (`json_to_pptx.py` 상단):**

| 설정 | 기본값 | 의미 |
|------|--------|------|
| `FONT_SCALE` | 0.95 | 폰트 크기 비율 |
| `LINE_SPACING_SCALE` | 0.83 | 줄간격 비율 |
| `IMAGE_CORNER_RATIO` | 0.05 | 이미지 라운딩 비율 |

---

### `/review [project-name] [HTML_URL]` - HTML 검토 (JSON 명세 + 심미성)

**검토 목적:**
| Phase | 비교 기준 | 목적 |
|-------|----------|------|
| **Phase 1** | 스크린샷 vs `presentation.json` | JSON 명세대로 렌더링됐는지 확인 |
| **Phase 2** | LLM 이미지 분석 | 디자인 심미성 검사 및 개선 제안 |

**Example:** 
```
/review eumlogistic http://localhost:5500/projects/eumlogistic/presentation.html
```

**Behavior:**

#### Phase 1: JSON 명세 검토
- **Kapture로 HTML_URL 접속** (`mcp_kapture_list_tabs()` → `mcp_kapture_navigate()`)
- **Kapture로 슬라이드별 스크린샷 캡처**
  - 슬라이드 요소를 탐색하며 각 슬라이드 캡처 (`mcp_kapture_screenshot()`)
  - 또는 스크롤/키보드 네비게이션 후 캡처
- 저장: `projects/[project-name]/screenshots/html/slide_01.png` ~ `slide_N.png`
- **검토:** 스크린샷을 보며 `presentation.json` 명세와 일치하는지 확인
  - 슬라이드 개수, 텍스트 내용, 색상, 레이아웃, 이미지 등

#### Phase 2: 심미성 분석 (Design Audit)
- 캡처된 각 슬라이드 스크린샷을 **LLM 이미지 분석**으로 평가
- 아래 **Design Heuristics** 기준으로 문제점 감지
- 슬라이드별 개선 제안 생성
- `review_report.md`에 심미성 분석 결과 포함

**⚠️ PPTX 스크린샷 비교 제거됨**
- 이전에는 `/review [project-name] [HTML_URL] [PPTX_URL]` 형태로 PPTX 스크린샷과 비교했으나
- 이미지 기반 PPTX 변환 기능 제거로 인해 더 이상 PPTX 비교는 수행하지 않음

---

### 🎨 Design Heuristics (심미성 규칙)

| 항목 | 설명 | 측정 방법 | 구체적 검사 항목 |
|------|------|----------|-----------------|
| **여백 일관성** | 슬라이드 간 padding/margin 통일 | 상하좌우 여백 비교 | • 슬라이드별 상단/하단/좌측/우측 여백 픽셀 수치<br>• 콘텐츠 영역과 슬라이드 경계 간 거리<br>• 일관성 오차 범위 ±5px 이내 |
| **타이포그래피 위계** | 제목 > 부제 > 본문 크기 구분 명확 | 폰트 크기 차이 확인 | • 제목/부제/본문 간 크기 비율 (최소 1.5배 차이)<br>• 동일 레벨 텍스트의 크기 일관성<br>• 줄간격(line-height) 적정성 |
| **색상 대비** | 텍스트와 배경 간 가독성 확보 | WCAG 대비 기준 | • 텍스트와 배경 명도 차이 (최소 4.5:1)<br>• 중요 정보의 색상 강조 적절성<br>• 색약자 고려 색상 조합 |
| **정렬 일관성** | 요소들의 좌/우/중앙 정렬 통일 | 수직/수평 정렬선 | • **연결 요소 간 수직 정렬 (점, 선, 화살표 등)**<br>• **position: absolute 사용 시 top/left 값 일치**<br>• 텍스트 블록 정렬 방향 통일<br>• 그리드 시스템 일관성 |
| **텍스트 밀도** | 슬라이드당 적정 텍스트 양 | 빽빽함 vs 여유 | • 한 줄당 글자 수 (권장: 50-75자)<br>• 단락 간 간격<br>• 텍스트 영역 대비 여백 비율 (최소 30%) |
| **시각적 균형** | 좌우/상하 요소 분포 균형 | 무게중심 분석 | • 슬라이드를 4등분했을 때 각 영역 밀도<br>• 큰 요소(이미지, 제목)의 위치 균형<br>• 빈 공간의 적절한 분포 |
| **이미지 비율** | 이미지 왜곡 없이 자연스러운 비율 | aspect-ratio 확인 | • 원본 비율 유지 여부<br>• object-fit 속성 적절성<br>• 이미지 해상도와 표시 크기 적합성 |
| **요소 간격** | 카드, 리스트 등 반복 요소 간격 일정 | gap 일관성 | • 동일 유형 요소 간 gap 픽셀 값<br>• **타임라인/프로세스의 간격 등간격 유지**<br>• 중첩 요소(nested) 간격 계층 구조 |
| **시각적 위계** | 중요 정보가 먼저 눈에 들어오는지 | 크기, 색상, 위치 | • Z-패턴/F-패턴 시선 흐름<br>• 주요 정보의 크기/색상 강조<br>• CTA(행동유도) 요소의 두드러짐 |
| **좌표 정밀성** ⭐ | 관련 요소 간 픽셀 단위 정렬 | CSS position 값 검증 | • **타임라인 점(dot)과 연결선(line)의 y좌표 일치**<br>• **화살표 끝과 대상 요소의 접점 정확성**<br>• **구분선(divider)의 정렬 및 길이 일관성**<br>• **배지(badge)/라벨의 위치 일관성** |

---

### 심미성 분석 출력 형식

각 슬라이드별로 아래 형식으로 분석 결과 제공:

```markdown
### 슬라이드 N: [슬라이드 제목]

**심미성 점수:** X/10

| 항목 | 상태 | 현상 | 개선 제안 |
|------|------|------|----------|
| 여백 일관성 | ⚠️ | 하단 여백 부족 | padding-bottom: 48px 추가 |
| 타이포그래피 | ✅ | 위계 명확 | - |
| 색상 대비 | ✅ | 가독성 양호 | - |
| 텍스트 밀도 | ⚠️ | 설명 텍스트 빽빽함 | 폰트 14px → 16px, 줄간격 1.6 |
| 시각적 균형 | ✅ | 좌우 대칭 | - |
```

---

## 🚨 Review 단계에서 자주 놓치는 검토 항목

### 1. 픽셀 단위 정렬 문제
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **타임라인 요소 불일치** | 점(dot)과 연결선(line)의 y좌표 차이 | CSS `top` 값 비교, 육안으로 수직 정렬 확인 |
| **화살표 접점 오차** | 화살표가 대상을 정확히 가리키지 않음 | 화살표 끝점과 대상 요소의 좌표 일치 확인 |
| **구분선 정렬** | 수평선이 기울어지거나 길이가 다름 | 여러 슬라이드의 동일 요소 비교 |
| **배지/라벨 위치** | 같은 역할의 배지가 다른 위치에 표시됨 | 슬라이드 간 동일 요소의 position 값 비교 |

### 2. CSS 스타일 불일치
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **border-radius 차이** | 일부 카드만 모서리가 둥글거나 각짐 | 동일 컴포넌트의 스타일 일관성 확인 |
| **box-shadow 누락** | 일부 요소만 그림자 효과 없음 | 카드/버튼 등 반복 요소의 그림자 통일 |
| **hover/active 상태** | 인터랙티브 요소의 시각적 피드백 부재 | (정적 HTML이므로 제거 필요) |
| **opacity 불일치** | 배경 투명도가 슬라이드마다 다름 | 동일 배경 스타일의 opacity 값 비교 |

### 3. 타이포그래피 오류
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **line-height 불일치** | 동일 레벨 텍스트의 줄간격 차이 | 제목/본문의 줄간격 일관성 확인 |
| **letter-spacing 누락** | 일부 제목만 자간이 넓음 | 동일 스타일 텍스트의 letter-spacing 비교 |
| **말줄임(...) 부적절** | text-overflow: ellipsis가 필요 없는 곳에 적용 | 텍스트 길이와 박스 크기 비율 확인 |
| **폰트 weight 혼용** | 제목이 일부는 bold, 일부는 semibold | 위계별 font-weight 통일 |

### 4. 레이아웃 구조 문제
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **z-index 충돌** | 요소가 의도와 다르게 겹침 | 중첩 요소의 z-index 계층 확인 |
| **overflow 처리 누락** | 콘텐츠가 박스 밖으로 삐져나옴 | 긴 텍스트/이미지가 있는 슬라이드 중점 검사 |
| **flexbox gap 불일치** | 카드 간격이 슬라이드마다 다름 | gap 또는 margin 값 비교 |
| **aspect-ratio 미적용** | 브라우저 크기 변경 시 비율 깨짐 | 반응형 테스트 (하지만 인쇄용이므로 고정) |

### 5. 색상 관련 오류
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **그라디언트 방향 불일치** | 배경 그라디언트가 슬라이드마다 다른 방향 | linear-gradient 각도 확인 |
| **투명도 불일치** | rgba() 또는 opacity 값이 다름 | 동일 요소의 알파 값 비교 |
| **색상 코드 오타** | #3B82F6 vs #3B82F5 같은 미세한 차이 | designTokens의 색상 팔레트와 실제 사용 비교 |
| **인쇄 시 색상 손실** | 배경색이 인쇄되지 않음 | `print-color-adjust: exact` 적용 확인 |

### 6. 이미지 관련 문제
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **Unsplash URL 오류** | 이미지 로드 실패 (404) | `source.unsplash.com` 사용 금지, `images.unsplash.com` 확인 |
| **이미지 비율 왜곡** | 이미지가 늘어나거나 찌그러짐 | object-fit: cover/contain 적용 확인 |
| **해상도 부족** | 인쇄 시 이미지가 흐릿함 | w, h 파라미터 크기 확인 (최소 800px) |
| **배경 이미지 반복** | background-repeat: no-repeat 누락 | 배경 이미지가 타일처럼 반복됨 |

### 7. 인쇄 관련 문제
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **마지막 슬라이드 빈 페이지** | `last-slide` 클래스 누락 | 마지막 슬라이드에 클래스 있는지 확인 |
| **슬라이드 사이 공백** | 불필요한 빈 페이지 추가됨 | `</div><div>` 사이 공백 제거 확인 |
| **Tailwind CDN 사용** | 동적 스타일로 인쇄 깨짐 | `<script src="...tailwindcss...">` 존재 여부 |
| **@media print 누락** | 브라우저 화면과 인쇄 결과 다름 | print 미디어 쿼리 존재 및 내용 확인 |

### 8. 접근성/사용성 문제
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **alt 속성 누락** | 이미지에 대체 텍스트 없음 | `<img>` 태그의 alt 속성 확인 |
| **색상만으로 정보 전달** | 색약자가 구분 불가능한 색상 조합 | 중요 정보에 아이콘/텍스트 병기 확인 |
| **대비 부족** | 회색 텍스트가 읽기 어려움 | WCAG 대비 비율 4.5:1 이상 확인 |

### 9. 콘텐츠 정합성 문제
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **텍스트 내용 불일치** | JSON과 HTML의 텍스트 다름 | presentation.json의 텍스트와 렌더링 결과 대조 |
| **슬라이드 개수 차이** | JSON에 10개인데 HTML에 9개 | slides 배열 개수와 실제 슬라이드 개수 비교 |
| **빠진 요소** | JSON에 명시된 이미지/버튼이 없음 | 각 슬라이드의 elements 배열과 실제 렌더링 비교 |

### 10. 성능/최적화 문제
| 문제 유형 | 증상 | 검사 방법 |
|----------|------|----------|
| **중복 스타일 정의** | 같은 스타일이 여러 곳에 반복됨 | CSS 클래스 재사용 확인 |
| **불필요한 !important** | 과도한 !important 사용 | CSS 특정성 문제 확인 |
| **인라인 스타일 남용** | style="..." 속성이 과다함 | 클래스 기반 스타일링으로 통합 |

---

### 🎯 Review 우선순위

검토 시 다음 순서로 집중:

1. **🔴 치명적:** 인쇄 깨짐, 슬라이드 빠짐, 텍스트 누락
2. **🟠 중요:** 정렬 불일치, 색상 오류, 이미지 로드 실패
3. **🟡 보통:** 간격 차이, 폰트 불일치, 그림자 누락
4. **🟢 경미:** 최적화, 접근성, 중복 코드

---

## 🔍 QA 검토 체크리스트

### HTML 검토용 (스크린샷 vs JSON 명세)

HTML 스크린샷을 보면서 `presentation.json`의 명세와 일치하는지 확인:

| 항목 | 검증 내용 |
|------|----------|
| 슬라이드 개수 | JSON의 slides 배열 개수와 일치 |
| 텍스트 내용 | 각 슬라이드의 제목, 본문, 라벨 등 정확히 표시 |
| 색상 | designTokens의 색상 팔레트 정확히 적용 |
| 타이포그래피 | 폰트 크기, weight, lineHeight 명세 준수 |
| 레이아웃 | 슬라이드 템플릿(hero-cover, content-text 등) 정확히 적용 |
| 이미지 | 지정된 이미지 URL 정상 로드, 위치/크기 정확 |
| 간격 | spacing 명세(padding, gap 등) 준수 |
| 배경 | 각 슬라이드별 배경색/그라디언트/이미지 정확 |

---

### Review Report 형식

QA 검토 결과는 다음 형식으로 `review_report.md`에 저장:

```markdown
# QA Review Report: [project-name]

## 📋 검토 정보
- **검토 일시:** YYYY-MM-DD HH:MM
- **검토 유형:** HTML
- **URL:** [검토 대상 URL]
- **총 슬라이드:** N개

---

## 🔍 Phase 1: JSON 명세 검토

### ✅ 통과 항목
- [x] 슬라이드 개수 일치 (N/N)
- [x] 색상 팔레트 정확
- ...

### ⚠️ 주의 필요
| 슬라이드 | 항목 | 현상 | 수정 제안 |
|----------|------|------|----------|
| #3 | 텍스트 오버플로우 | 본문이 박스 밖으로 넘침 | 폰트 크기 14px → 12px |

---

## 🎨 Phase 2: 심미성 분석 (Design Audit)

### 전체 심미성 점수: X/10

| 항목 | 점수 | 상태 |
|------|------|------|
| 여백 일관성 | 8/10 | ⚠️ 일부 슬라이드 하단 여백 부족 |
| 타이포그래피 위계 | 9/10 | ✅ 명확 |
| 색상 대비 | 9/10 | ✅ 가독성 양호 |
| 정렬 일관성 | 8/10 | ✅ 양호 |
| 텍스트 밀도 | 7/10 | ⚠️ 일부 빽빽함 |
| 시각적 균형 | 7/10 | ⚠️ 일부 슬라이드 하단 무거움 |
| 이미지 비율 | 9/10 | ✅ 양호 |
| 요소 간격 | 8/10 | ✅ 양호 |

### 슬라이드별 상세 분석

#### 슬라이드 1: 표지
**심미성 점수:** 7/10

| 항목 | 상태 | 현상 | 개선 제안 | 자동 적용 |
|------|------|------|----------|----------|
| 여백 | ⚠️ | 이미지 하단 여백 부족 | padding-bottom: 48px | ✅ 가능 |
| 배지 크기 | ⚠️ | 12px로 작음 | font-size: 14px | ✅ 가능 |
| 텍스트 밀도 | ⚠️ | 설명 텍스트 빽빽함 | 폰트 16px, 줄간격 1.6 | ✅ 가능 |

#### 슬라이드 2: 회사개요
**심미성 점수:** 8/10

| 항목 | 상태 | 현상 | 개선 제안 | 자동 적용 |
|------|------|------|----------|----------|
| 카드 간격 | ✅ | 일관성 있음 | - | - |
| 통계 배치 | ✅ | 적절함 | - | - |

...

---

## 📊 최종 요약

### JSON 명세 검토
- **통과:** X개
- **주의:** X개  
- **수정 필요:** X개

### 심미성 분석
- **전체 점수:** X/10
- **자동 수정 가능:** X개 항목
- **수동 검토 필요:** X개 항목

### 권장 조치
1. ⚡ [자동 적용 가능] 슬라이드 1 하단 여백 추가
2. ⚡ [자동 적용 가능] 설명 텍스트 폰트 크기/줄간격 조정
3. 👀 [수동 검토] 전체 슬라이드 시각적 균형 재확인
```

---

## 📋 Slide Templates Reference

### 1. hero-cover
- **Layout:** Center-aligned, full viewport height
- **Elements:** heading, subheading, cta
- **Background:** Gradient or image
- **Use Case:** Title slide, opening statement

### 2. table-of-contents
- **Layout:** 2-3 column grid
- **Elements:** section cards with numbers/icons
- **Background:** Solid color or subtle gradient
- **Use Case:** Agenda, navigation slide

### 3. section-divider
- **Layout:** Center-aligned, minimal elements
- **Elements:** section title, subtitle (optional)
- **Background:** Bold color or pattern
- **Use Case:** Topic transitions

### 4. content-text
- **Layout:** Left/right split or centered column
- **Elements:** heading, paragraph, bullet points, image
- **Background:** Clean, high contrast
- **Use Case:** Detailed explanations, feature descriptions

### 5. bullet-list
- **Layout:** Grid or stacked list
- **Elements:** title, list items with icons/numbers
- **Background:** Subtle texture or gradient
- **Use Case:** Key points, feature lists, process steps

---

## ✅ HTML 생성 체크리스트

HTML 생성 시 반드시 확인:

- [ ] **Tailwind CDN 미사용** - 모든 스타일 인라인 CSS로 정의
- [ ] **마지막 슬라이드에 `last-slide` 클래스** 추가
- [ ] **슬라이드 사이 공백 없음** - `</div><!-- Slide --><div>` 형태
- [ ] **Unsplash 이미지 ID 형식** - `images.unsplash.com/photo-[ID]?w=...`
- [ ] **@media print CSS 포함** - A4 landscape (297mm x 210mm)
- [ ] **page-break 설정** - `.slide:not(.last-slide)` 에만 적용
