# Slide Templates Guide

## 📋 Overview

Haru Presentation Builder는 **5가지 핵심 슬라이드 템플릿**을 지원합니다. 각 템플릿은 특정 용도, 레이아웃 패턴, 스타일 가이드라인을 갖습니다.

---

## 🎨 Template Types

### 1. Hero/Cover Slide (`hero-cover`)

**용도:** 오프닝 슬라이드, 회사 소개, 타이틀 페이지

**레이아웃:** 중앙 단일 컬럼

**요소:**
- **Logo/Brand:** 대형 텍스트 (140px), Bold (900), 상단 중앙
- **Main Title:** 주요 제목 (32-48px), 중앙
- **Subtitle:** 부제목 (20px), 타이틀 하단
- **Footer:** 소형 텍스트 (16px), 하단 중앙 (회사명, 날짜 등)

**배경:**
- 단색 + 도트 패턴 옵션
- 예: Dark navy (#0A1428) + 은은한 도트 (#4A5A7A, 30% opacity)

**JSON 예시:**
```json
{
  "type": "hero-cover",
  "layout": "centered-single-column",
  "elements": {
    "logo": { "text": "COMPANY NAME", "fontSize": "140px" },
    "title": { "text": "Presentation Title", "fontSize": "32px" },
    "subtitle": { "text": "Subtitle or tagline", "fontSize": "20px" },
    "footer": { "text": "Date or Company Info", "fontSize": "16px" }
  }
}
```

---

### 2. Table of Contents (`table-of-contents`)

**용도:** 목차, 아젠다, 기능 목록

**레이아웃:** 중앙 그리드 (2x2, 3x2, 커스텀)

**요소:**
- **Heading:** "목차", "Agenda", "Contents" (64px, bold)
- **Cards:** 번호가 있는 항목들
  - 번호 배지 (예: "01", "02")
  - 아이콘 (원, 지구본, 빌딩, 사람)
  - 텍스트 라벨 (18-20px)

**카드 스타일:**
- 배경: 반투명 파란색 (rgba(59, 123, 255, 0.1))
- 테두리: 1px solid rgba(59, 123, 255, 0.3)
- 테두리 반경: 12px
- 패딩: 24px 32px
- 크기: ~400px × 120px

**JSON 예시:**
```json
{
  "type": "table-of-contents",
  "layout": "centered-grid-2x2",
  "elements": {
    "heading": { "text": "목차", "fontSize": "64px" },
    "cards": [
      { "number": "01", "icon": "circle", "text": "Introduction" },
      { "number": "02", "icon": "globe", "text": "Market Analysis" }
    ]
  }
}
```

---

### 3. Section Divider (`section-divider`)

**용도:** 챕터 구분, 섹션 전환, 시각적 구분자

**레이아웃:** 중앙 최소화 (2-3개 요소만)

**요소:**
- **Section Number:** 초대형 (180px), Bold (900), 반투명 (90% opacity)
- **Section Title:** 중형 제목 (48px), Bold (700)
- **Page Number:** 소형 텍스트 (14px), 우하단 (예: "3 / 20")

**배경:**
- 2톤 분할 효과 (50/50 수직 분할)
- 예: 좌측 #0A1428, 우측 #1A2438

**JSON 예시:**
```json
{
  "type": "section-divider",
  "layout": "centered-minimal",
  "elements": {
    "sectionNumber": { "text": "01", "fontSize": "180px", "opacity": 0.9 },
    "sectionTitle": { "text": "Market Overview", "fontSize": "48px" },
    "pageNumber": { "text": "5 / 20", "fontSize": "14px", "position": "bottom-right" }
  }
}
```

---

### 4. Content with Text (`content-text`)

**용도:** 본문 슬라이드, 단락 + 선택적 이미지

**레이아웃:** 수평 분할 (60/40 또는 50/50)

**요소:**
- **Title:** 섹션 제목 (48px), 좌측 정렬
- **Body Text:** 본문 (20px), 좌측 정렬, line-height 1.8
- **Image (선택):** 우측, 40% 너비, 둥근 모서리

**JSON 예시:**
```json
{
  "type": "content-text",
  "layout": "split-horizontal",
  "elements": {
    "title": { "text": "Our Solution", "fontSize": "48px" },
    "body": { "text": "Lorem ipsum dolor sit amet...", "fontSize": "20px" },
    "image": { "src": "/images/solution.jpg", "position": "right", "width": "40%" }
  }
}
```

---

### 5. Bullet List (`bullet-list`)

**용도:** 핵심 포인트, 기능 목록, 요약

**레이아웃:** 중앙 리스트 (3-5개 항목)

**요소:**
- **Title:** 섹션 제목 (48px), 중앙
- **Bullets:** 목록 항목 (24px), 좌측 또는 중앙 정렬
  - 커스텀 불릿 색상 (예: 프라이머리 블루)
  - 항목 간 간격: 24px

**JSON 예시:**
```json
{
  "type": "bullet-list",
  "layout": "centered-list",
  "elements": {
    "title": { "text": "Key Features", "fontSize": "48px" },
    "bullets": [
      "AI-powered automation",
      "Real-time analytics",
      "Cloud-based infrastructure"
    ]
  }
}
```

---

## 🎨 Design Tokens

> **참고:** 디자인 토큰(색상, 타이포그래피, 간격)은 **프로젝트별로 다릅니다.**  
> PDF 분석 시 `source_style.json`에 자동 추출되며, 해당 값을 기준으로 HTML을 생성합니다.

**일반적인 토큰 구조:**
- `colors`: 배경, 텍스트, 강조색
- `typography`: 폰트 패밀리, 크기, 가중치, 줄간격
- `spacing`: 페이지 패딩, 섹션 간격, 카드 gap

---

## 📐 Layout Guidelines

### 비율
- **기본:** 16:9 (1920×1080, 1440×810 등)
- **풀스크린:** `width: 100vw; height: 100vh`

### 정렬 규칙
- **Hero/Cover:** 모든 요소 중앙
- **TOC:** 제목 중앙, 카드 그리드 하단
- **Section Divider:** 번호 + 타이틀 수직 중앙
- **Content:** 텍스트 좌측, 이미지 우측
- **Bullet List:** 타이틀 중앙, 불릿 좌측

### 안전 영역
- **패딩:** 최소 80px (데스크탑)
- **태블릿:** 60px 패딩
- **모바일:** 40px 패딩

---

## 📚 Template 선택 가이드

| 콘텐츠 유형 | 템플릿 |
|------------|--------|
| 로고 + 타이틀만 | `hero-cover` |
| 4-6개 번호 카드 | `table-of-contents` |
| 큰 번호 + 짧은 타이틀 | `section-divider` |
| 단락 텍스트 + 이미지 | `content-text` |
| 3-5개 불릿 포인트 | `bullet-list` |

**Edge cases:**
- 혼합 콘텐츠 (텍스트 + 불릿 + 이미지) → `content-text` 사용
- 항목 7개 이상 → 여러 `bullet-list` 슬라이드로 분할
- 복잡한 레이아웃 → 2-3개 단순 슬라이드로 분할
