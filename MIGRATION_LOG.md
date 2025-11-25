# Migration Log: Web Builder → Presentation Builder

**Date:** 2025-11-25  
**Version:** 3.0.0  
**Migration Type:** Complete Architecture Refactoring

---

## 📋 Overview

**From:** `haru-web-builder` - AI-powered website scraper and rebuilder  
**To:** `haru-presentation-builder` - AI-powered presentation generator with style reference support

---

## 🎯 Migration Goals

1. **Support Multiple Input Sources**
   - ✅ URL analysis (existing)
   - ✅ PDF style extraction (new)
   - ✅ Manual content input (enhanced)

2. **Change Output Format**
   - ❌ Long-scroll websites (sections)
   - ✅ Slide-based presentations (slides)

3. **Preserve Existing Capabilities**
   - ✅ MCP-based browser analysis
   - ✅ PowerShell/Node.js integration scripts
   - ✅ Design token extraction
   - ✅ Tailwind CSS generation

---

## 📦 Cleanup Summary (Phase 2)

### Files Deleted
1. `docs/section_structure.md` (웹 섹션 구조 가이드)
2. `docs/animation_review_tasks.md` (웹 애니메이션 분석)
3. `docs/component_structure.md` (React 컴포넌트 구조)
4. `docs/generation_report.md` (웹 생성 리포트)
5. `docs/generation_tasks.md` (웹 생성 작업)

### Files Renamed (Legacy Preservation)
1. `scripts/integrate_web_pipeline.ps1` → `scripts/_LEGACY_integrate_web_pipeline.ps1`
2. `scripts/generate_html.ps1` → `scripts/_LEGACY_generate_html.ps1`
3. `.github/copilot-instructions.md` → `.github/_LEGACY_copilot-instructions-web.md` (백업)

### New Documentation
1. `docs/slide_templates.md` - 5가지 슬라이드 템플릿 가이드 (hero-cover, table-of-contents, section-divider, content-text, bullet-list)
2. `docs/presentation_workflow.md` - 3가지 프레젠테이션 생성 워크플로우 (PDF+Manual, URL+PDF, URL-only)

### Major Refactoring
**`.github/copilot-instructions.md`:**
- **Before:** 2097 lines (웹 스크롤링 중심)
- **After:** 401 lines (프레젠테이션 중심)
- **Reduction:** 81% 축소 (1696 lines 제거)
- **Removed:**
  - 웹 스크롤링 로직 (ArrowDown-only enforcement, 30-80 checkpoints)
  - 체크포인트 강제 시스템 (progressive scroll analysis)
  - 웹 애니메이션 분석 (8-field template)
  - React/TSX 컴포넌트 생성 가이드
  - 00_analysis_note.txt 실시간 로깅 시스템
- **Added:**
  - PDF 슬라이드 분석 가이드 (ArrowRight/Left navigation)
  - 슬라이드 템플릿 참조 (5 types)
  - 3가지 입력 워크플로우 (PDF, URL, Manual)
  - 통합 파이프라인 구조 (3-stage)
  - Harufolio 링크 구성 (기본 URL 설정)

---

## 🔧 Structural Changes

### 1. Directory Structure

#### Before (Web Builder)
```
analysis/
  web-pipeline/
    01_contents_web.json      # Sections-based
    02_style_web.json          # Web-specific styles
    03_integrate_web.json      # Merged sections
    generators/
      04_generate_html.json
output/
  web/
    index.html                 # Long-scroll website
```

#### After (Presentation Builder)
```
analysis/
  presentation-pipeline/       # Renamed from web-pipeline
    01_contents_slides.json    # Slides-based (NEW schema)
    02_style_theme.json        # Theme tokens (renamed)
    03_integrate_presentation.json  # Merged slides
    generators/
      04_generate_presentation.json
  pdf-analysis/                # NEW: PDF style extraction
    bluehive_style_analysis.json
output/
  presentation/                # NEW: Slide-based output
    index.html                 # Presentation with keyboard nav
  web/                         # LEGACY: Keep for backward compatibility
    index.html
```

### 2. Schema Changes

#### 01_contents: Sections → Slides

**Before (Web):**
```json
{
  "sections": [
    {
      "id": "section-01-hero",
      "type": "hero",
      "content": { ... }
    }
  ]
}
```

**After (Presentation):**
```json
{
  "slides": [
    {
      "id": "slide-01",
      "type": "hero-cover",
      "layout": "centered-single-column",
      "elements": { ... },
      "background": { ... },
      "transition": "fade"
    }
  ]
}
```

**Key Changes:**
- `sections[]` → `slides[]`
- Added `layout` field (centered, grid, split, etc.)
- Added `transition` field (fade, slide, zoom)
- Added `background` object (pattern, gradient, split)

#### 02_style: Web Styles → Theme Tokens

**Before (Web):**
```json
{
  "components": {
    "section-01-hero": { ... }
  }
}
```

**After (Presentation):**
```json
{
  "slideTemplates": {
    "hero-cover": { ... },
    "table-of-contents": { ... },
    "section-divider": { ... }
  },
  "designTokens": {
    "colors": { ... },
    "typography": { ... },
    "spacing": { ... }
  }
}
```

**Key Changes:**
- `components` → `slideTemplates`
- Grouped by slide type (not by ID)
- Reusable templates for multiple slides

---

## 🚀 Pipeline Changes

### Input Processing

#### Old Workflow (Web Only)
```
1. URL → MCP Analysis → 01_contents_web.json
2. 01_contents + 02_style → 03_integrate_web.json
3. 03_integrate → HTML (long-scroll)
```

#### New Workflow (Multi-Source)
```
Option A: URL → Presentation
1. URL → MCP Analysis → 01_contents_slides.json (section-to-slide mapping)
2. 01_contents + 02_style → 03_integrate_presentation.json
3. 03_integrate → HTML (slide-based)

Option B: PDF Style + Manual Content
1. PDF → MCP Visual Analysis → theme.json (colors, fonts, layouts)
2. User Input → content.json (text, structure)
3. theme.json + content.json → 03_integrate_presentation.json
4. 03_integrate → HTML (slide-based)

Option C: URL Content + PDF Style (Hybrid)
1. URL → 01_contents_slides.json
2. PDF → theme_override.json
3. Merge → 03_integrate_presentation.json (URL content + PDF style)
4. 03_integrate → HTML (slide-based)
```

---

## 📝 Script Changes

### 1. Integration Script

**File:** `scripts/integrate_web_pipeline.ps1` → `scripts/integrate_presentation_pipeline.ps1`

**Changes:**
- Input: `01_contents_slides.json` (slides array)
- Output: `03_integrate_presentation.json`
- Added: Section-to-slide conversion logic
- Added: PDF theme merging support

### 2. Generation Script

**File:** `scripts/generate_html.ps1` → `scripts/generate_presentation.ps1`

**Changes:**
- Template system: Section templates → Slide templates
- Output: Full-screen slides with `scroll-snap`
- Added: Keyboard navigation (Arrow keys, Space)
- Added: Navigation dots
- Added: Slide transitions (fade, slide, zoom)

---

## 🎨 Component Templates

### New Slide Types (from PDF analysis)

1. **hero-cover**: Logo + Title + Subtitle (centered)
2. **table-of-contents**: Grid of numbered cards (2x2, 3x2)
3. **section-divider**: Large number + Section title (minimal)
4. **content-text**: Heading + Body text + Image (left/right)
5. **content-visual**: Large image/chart + Caption
6. **bullet-list**: Title + Bullet points (3-5 items)

### Template Files (NEW)

```
components/
  slide-templates/
    hero-cover.html
    table-of-contents.html
    section-divider.html
    content-text.html
    content-visual.html
    bullet-list.html
```

---

## 🔄 Backward Compatibility

### Legacy Support

**Keep for backward compatibility:**
- ✅ `analysis/web-pipeline/` (read-only, no new writes)
- ✅ `output/web/` (legacy output folder)
- ✅ `scripts/generate_html.ps1` (deprecated, still functional)

**Mark as deprecated in README:**
```markdown
## ⚠️ Deprecated Features

- `analysis/web-pipeline/` → Use `analysis/presentation-pipeline/`
- `scripts/generate_html.ps1` → Use `scripts/generate_presentation.ps1`
- Long-scroll website output → Use slide-based presentation output
```

---

## 📊 Testing Plan

### Test Cases

1. **URL → Presentation**
   - Input: Website URL
   - Expected: Sections mapped to slides, navigation works
   - Status: ⏳ Pending

2. **PDF → Theme Extraction**
   - Input: PDF file (via `file://`)
   - Expected: Colors, fonts, layouts extracted
   - Status: ✅ Completed (bluehive_sample.html)

3. **Hybrid: URL Content + PDF Style**
   - Input: URL + PDF
   - Expected: Website content with PDF design
   - Status: ⏳ Pending

4. **Manual Content Input**
   - Input: JSON with slide definitions
   - Expected: Presentation generated from scratch
   - Status: ⏳ Pending

---

## 📦 Files to Create

### New Files
- [x] `analysis/pdf-analysis/bluehive_style_analysis.json`
- [x] `output/presentation/bluehive_sample.html`
- [x] `analysis/presentation-pipeline/01_contents_slides.json`
- [x] `analysis/presentation-pipeline/02_style_theme.json`
- [x] `analysis/presentation-pipeline/03_integrate_presentation.json`
- [x] `scripts/integrate_presentation_pipeline.js`
- [x] `scripts/integrate_presentation_pipeline.ps1`
- [ ] `scripts/generate_presentation.js`
- [ ] `components/slide-templates/hero-cover.html`
- [ ] `components/slide-templates/table-of-contents.html`
- [ ] `components/slide-templates/section-divider.html`

### Modified Files
- [x] `README.md` (updated for presentation mode)
- [x] `package.json` (renamed project, added scripts)
- [ ] `.github/copilot-instructions.md` (update for presentation mode)

### Deprecated Files (Keep but mark)
- `scripts/integrate_web_pipeline.ps1` (legacy)
- `scripts/generate_html.ps1` (legacy)

---

## 🎯 Success Criteria

### Phase 1: Core Pipeline ✅
- [x] PDF style extraction working
- [x] Sample presentation generated
- [x] 3 slide types validated

### Phase 2: Automation ✅
- [x] Node.js integration script created
- [x] JSON schema finalized
- [x] Content + Theme merge working (15917 bytes output)
- [ ] Template system implemented (pending)

### Phase 3: Full Integration (Pending)
- [ ] URL → Presentation working
- [ ] PDF + URL hybrid working
- [ ] Documentation complete

---

## 📌 Next Steps

1. **Immediate (Task 2-3)**
   - Rename `analysis/web-pipeline/` → `analysis/presentation-pipeline/`
   - Update JSON schemas to slides-based structure
   - Implement PDF + URL merge logic

2. **Short-term (Task 4-5)**
   - Create slide template system
   - Rewrite PowerShell generation script
   - Add keyboard navigation to all outputs

3. **Long-term (Task 6-8)**
   - Update integration script
   - Complete documentation
   - Full workflow testing

---

## 🔗 Related Files

- **Analysis Results:** `analysis/pdf-analysis/bluehive_style_analysis.json`
- **Sample Output:** `output/presentation/bluehive_sample.html`
- **Original Instructions:** `.github/copilot-instructions.md` (to be updated)

---

## 📝 Notes

- **Design Decision:** Keep web-pipeline as legacy to avoid breaking existing workflows
- **Performance:** Presentation mode is lighter (3-20 slides vs 100+ sections)
- **User Experience:** Keyboard navigation (Arrow keys) > Scroll for presentations
- **Flexibility:** Support both automatic (URL) and manual (JSON) content input

---

**Migration Status:** 🟡 In Progress (Phase 1 Complete, Phase 2 Starting)  
**Estimated Completion:** 2025-11-25 (8 tasks remaining)
