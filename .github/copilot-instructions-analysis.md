# Web & PDF Analysis Guide

## 🎯 Purpose

이 문서는 PDF 및 웹사이트 분석을 위한 MCP Kapture 사용 지침입니다.
분석 결과는 **PDF 인쇄용 정적 HTML** 생성에 사용됩니다.

---

## 🔒 MCP Tool Policy (MANDATORY)

**⚠️ USE KAPTURE MCP TOOLS EXCLUSIVELY:**

✅ **ALLOWED:**
- `mcp_kapture_list_tabs()`, `mcp_kapture_navigate()`, `mcp_kapture_dom()`
- `mcp_kapture_elements()`, `mcp_kapture_screenshot()`, `mcp_kapture_hover()`
- `mcp_kapture_click()`, `mcp_kapture_keypress()`, `mcp_kapture_resize()`

❌ **FORBIDDEN:**
- `mcp_microsoft_pla_*` (Microsoft Playwright MCP)
- `mcp_browsermcp_*` (Generic Browser MCP)
- `mcp_kapture_evaluate()` (does NOT exist)

---

## 📋 PDF Analysis Workflow

### When to Use
- PDF 프레젠테이션의 디자인 토큰 추출 (색상, 타이포그래피, 레이아웃)
- 기존 PDF 스타일을 새 프레젠테이션에 적용

### Steps

#### 1. 브라우저 탭 연결
```javascript
const tabs = await mcp_kapture_list_tabs();
const tabId = tabs[0].id; // PDF가 열린 탭
```

#### 2. 슬라이드 탐색
```javascript
// ArrowRight/ArrowLeft로 슬라이드 이동
await mcp_kapture_keypress({ tabId, key: "ArrowRight" });
await new Promise(resolve => setTimeout(resolve, 300)); // 애니메이션 대기
```

#### 3. 스크린샷 캡처 및 분석
```javascript
await mcp_kapture_screenshot({ tabId });
// 즉시 분석: 색상, 폰트, 레이아웃 추출
```

#### 4. 디자인 토큰 추출

각 슬라이드에서 추출:
- **Colors:** 배경색, 텍스트색, 강조색 (hex 값)
- **Typography:** 폰트 크기 (px), 굵기, 줄 높이
- **Spacing:** 여백, 패딩, 간격 (px)
- **Layout:** 그리드 패턴, 정렬 방식

#### 5. 결과 저장
```
analysis/pdf-analysis/[filename]_style_analysis.json
```

### Output Schema
```json
{
  "slides": [
    {
      "slideNumber": 1,
      "template": "hero-cover",
      "designTokens": {
        "colors": { "primary": "#5B7BFF", "background": "#0A1428" },
        "typography": { "heading": "140px/1.2/800", "body": "18px/1.8/400" },
        "spacing": { "padding": "100px" }
      }
    }
  ],
  "totalSlides": 5
}
```

---

## 🌐 URL Analysis Workflow

### When to Use
- 웹사이트 콘텐츠를 슬라이드로 변환
- 웹사이트 디자인 시스템 추출

### Steps

#### 1. 웹사이트 탐색
```javascript
await mcp_kapture_navigate({ tabId, url: "https://example.com" });
```

#### 2. Progressive Scroll 분석
```javascript
// ArrowDown으로 스크롤 (150-300px 단위)
for (let i = 0; i < 5; i++) {
  await mcp_kapture_keypress({ tabId, key: "ArrowDown" });
  await new Promise(resolve => setTimeout(resolve, 300));
}

// 현재 뷰포트 캡처
await mcp_kapture_elements({ tabId, visible: "true" });
await mcp_kapture_screenshot({ tabId });
```

#### 3. 섹션 → 슬라이드 매핑

| 웹 섹션 | 슬라이드 템플릿 |
|---------|----------------|
| Hero section | `hero-cover` |
| Feature grid | `table-of-contents` |
| Text + Image | `content-text` |
| Bullet list | `bullet-list` |
| Section header | `section-divider` |

#### 4. 결과 저장
```
analysis/presentation-pipeline/01_contents_slides.json
analysis/presentation-pipeline/02_style_theme.json
```

---

## 📐 Scrolling Rules

### ✅ ALLOWED
```javascript
await mcp_kapture_keypress({ tabId, key: "ArrowDown" });  // 웹 스크롤
await mcp_kapture_keypress({ tabId, key: "ArrowRight" }); // PDF 다음 슬라이드
await mcp_kapture_keypress({ tabId, key: "ArrowLeft" });  // PDF 이전 슬라이드
```

### ❌ FORBIDDEN (내용 건너뛰기 위험)
```javascript
await mcp_kapture_keypress({ tabId, key: "PageDown" });   // 800px 점프
await mcp_kapture_keypress({ tabId, key: "End" });        // 페이지 끝으로
await mcp_kapture_keypress({ tabId, key: "Home" });       // 페이지 처음으로
```

---

## 🎨 Design Token Extraction Template

### 8-Field Animation Template
복잡한 애니메이션 발견 시:

```json
{
  "subject": "무엇이 움직이는지",
  "visualDescription": "시각적 외관 설명",
  "observedBehavior": "어떻게 움직이는지 (px 단위)",
  "type": "애니메이션 유형",
  "trigger": "트리거 조건",
  "technicalImplementation": "구현 방법",
  "propertyChanges": "CSS/JS 속성 변화",
  "codeHint": "구현 예시 코드"
}
```

---

## ✅ Completion Criteria

### PDF 분석 완료 조건
- [ ] 모든 슬라이드 캡처됨 (N/N)
- [ ] 디자인 토큰 추출됨 (색상, 타이포그래피, 간격)
- [ ] 슬라이드 템플릿 식별됨
- [ ] JSON 파일 생성됨

### URL 분석 완료 조건
- [ ] 주요 섹션 캡처됨 (5-10개)
- [ ] 디자인 시스템 추출됨
- [ ] 섹션 → 슬라이드 매핑됨
- [ ] JSON 파일 생성됨

---

## 📁 Output Files

| 분석 유형 | 출력 파일 |
|-----------|-----------|
| PDF 스타일 | `analysis/pdf-analysis/[name]_style_analysis.json` |
| 슬라이드 콘텐츠 | `analysis/presentation-pipeline/01_contents_slides.json` |
| 테마 스타일 | `analysis/presentation-pipeline/02_style_theme.json` |
| 통합 결과 | `analysis/presentation-pipeline/03_integrate_presentation.json` |

---

## ⚠️ Important Notes

1. **분석 결과는 정적 HTML 생성용**
   - 키보드 네비게이션 없음
   - 슬라이드 인디케이터 없음
   - 애니메이션 없음 (정적 문서)

2. **출력 형식**
   - HTML: 브라우저 인쇄(Ctrl+P) → PDF
   - PPTX: HTML 스크린샷 기반 변환

3. **슬라이드 비율**
   - 기본: 16:9
   - 요청 시: 4:3, A4 등 변경 가능
