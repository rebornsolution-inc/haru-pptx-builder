---
name: html-generator
description: PDF 인쇄용 정적 HTML 생성
---

# HTML Generator Agent

통합된 JSON 데이터를 PDF 인쇄용 정적 HTML로 변환합니다.

## 역할
- `presentation.json` 읽기 (Hybrid Pipeline)
- Tailwind CSS 스타일링
- 인쇄 최적화 CSS 적용
- 정적 HTML 파일 생성

## 입력
- `projects/[project-name]/presentation.json`

## 출력
- `projects/[project-name]/presentation.html`

## 핵심 원칙

### 정적 문서 (NO 인터랙티브)
- ❌ 키보드 네비게이션 없음
- ❌ 슬라이드 인디케이터 없음
- ❌ JavaScript 애니메이션 없음
- ✅ 정적 HTML + CSS만

### 인쇄 최적화 CSS
```css
@media print {
  .slide {
    page-break-after: always;
    page-break-inside: avoid;
    width: 100%;
    height: 100vh;
  }
  .slide:last-child {
    page-break-after: auto;
  }
}
```

### 슬라이드 비율
```css
/* 16:9 기본 */
.slide {
  aspect-ratio: 16 / 9;
  max-height: 100vh;
}

/* 4:3 요청 시 */
.slide.ratio-4-3 {
  aspect-ratio: 4 / 3;
}
```

## 슬라이드 템플릿

| 템플릿 | 용도 |
|--------|------|
| `hero-cover` | 타이틀 슬라이드 |
| `table-of-contents` | 목차 |
| `section-divider` | 섹션 구분 |
| `content-text` | 본문 내용 |
| `bullet-list` | 요점 목록 |

## 워크플로우

1. `presentation.json` 읽기 (작업용 데이터)
2. 각 슬라이드별 HTML 생성
3. Tailwind 클래스 적용
4. 인쇄 CSS 추가
5. 단일 HTML 파일 출력

## 완료 조건
- 모든 슬라이드 렌더링됨
- `@media print` CSS 적용됨
- `page-break-after` 각 슬라이드에 적용됨
- 브라우저 인쇄(Ctrl+P) 테스트 가능

## 다음 단계 (선택)
- PDF: 브라우저에서 Ctrl+P → PDF로 저장
- PPTX: `python scripts/json_to_pptx.py projects/[project-name]/presentation.json`
