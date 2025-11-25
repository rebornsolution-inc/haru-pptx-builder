# Presentation Workflow Guide

## 🎯 Overview

Haru Presentation Builder supports **3 main workflows** for generating slide-based presentations. Choose based on your input sources and requirements.

---

## 📋 Workflow 1: PDF Style + Manual Content (Fastest)

**Best for:** When you have a design reference (PDF) but need custom content

### Input Requirements
- ✅ PDF file with design elements (colors, fonts, layouts)
- ✅ Manual content creation or topic outline

### Steps

#### 1. Open PDF in Chrome
```bash
# macOS/Linux
open file:///path/to/your/presentation.pdf

# Or drag PDF into Chrome browser
```

#### 2. Analyze PDF with MCP Kapture
**AI Command:** "이 PDF의 스타일을 분석해줘"

**AI Actions:**
- Connect to Chrome tab via `mcp_kapture_list_tabs()`
- Navigate slides with `mcp_kapture_keypress({ key: "ArrowRight" })`
- Capture screenshots with `mcp_kapture_screenshot()`
- Analyze colors, fonts, layouts from visual data
- Generate `analysis/pdf-analysis/[filename]_style_analysis.json`

**Expected Output (PDF Analysis JSON):**
```json
{
  "designTokens": {
    "colors": { "primary": "#5B7BFF", "background": "#0A1428" },
    "typography": { "fontSize": { "hero": "140px", "h1": "64px" } },
    "spacing": { "page": "100px" }
  },
  "componentPatterns": {
    "hero-cover": { "layout": "centered", "elements": {...} }
  }
}
```

#### 3. Create Content JSON
**Option A: Manual Creation**
- Edit `analysis/presentation-pipeline/01_contents_slides.json`
- Define slide structure (type, layout, elements)

**Option B: AI Generation from Topic**
**User:** "주제: AI 기술 소개. 5개 슬라이드로 만들어줘"
**AI:** Generates 01_contents_slides.json with:
  - Slide 1: Hero (title + subtitle)
  - Slide 2: TOC (4 topics)
  - Slide 3: Section Divider
  - Slide 4-5: Content slides

#### 4. Integrate Style + Content
```bash
node scripts/integrate_presentation_pipeline.js
```

**Output:** `analysis/presentation-pipeline/03_integrate_presentation.json`
- Merged slides with theme styles
- Design tokens applied to all elements
- Navigation settings included

#### 5. Generate HTML Presentation
```bash
node scripts/generate_presentation.js
```

**Output:** `output/presentation/index.html`
- Full-screen slides with keyboard navigation
- Tailwind CSS styling
- Transition animations

#### 6. Preview & Iterate
- Open `output/presentation/index.html` in browser
- Use Arrow keys (←/→) or Space to navigate
- Click navigation dots to jump to slides
- Adjust content or style in JSON files and regenerate

### Pros & Cons

**✅ Pros:**
- Full design control (exact PDF style replication)
- Fast iteration (no web scraping)
- Works offline (no internet needed for generation)

**❌ Cons:**
- Manual content creation required
- PDF text extraction not automatic (OCR needed)

---

## 📋 Workflow 2: URL Content + PDF Style (Hybrid)

**Best for:** When you want website content with custom branding

### Input Requirements
- ✅ Website URL (for content structure)
- ✅ PDF file (for brand style)

### Steps

#### 1. Analyze Website for Content
**AI Command:** "/web https://example.com"

**AI Actions:**
- Progressive scroll analysis (30-80 checkpoints)
- Extract sections, headings, text, images
- Detect interactive elements
- Generate `analysis/web-pipeline/01_contents_web.json`

**Section-to-Slide Mapping:**
```javascript
// AI converts web sections → presentation slides
{
  "section-01-hero": {
    type: "hero",
    content: { heading: "...", subheading: "..." }
  }
}
↓ Transform to
{
  "slide-01": {
    type: "hero-cover",
    elements: { logo: "...", title: "...", subtitle: "..." }
  }
}
```

#### 2. Analyze PDF for Style
**AI Command:** "이 PDF의 스타일을 추출해줘"
- Same as Workflow 1, Step 2

#### 3. Merge URL Content + PDF Style
```bash
node scripts/integrate_presentation_pipeline.js --mode hybrid
```

**Merge Logic:**
- Content structure from URL (headings, text, images)
- Colors, fonts, spacing from PDF
- Layout patterns from PDF (hero, toc, divider)

**Output:** `03_integrate_presentation.json` with hybrid data

#### 4-6. Same as Workflow 1 (Generate → Preview → Iterate)

### Pros & Cons

**✅ Pros:**
- Automatic content extraction (no manual typing)
- Brand consistency (PDF colors + fonts)
- Best of both worlds

**❌ Cons:**
- Requires both URL and PDF
- Longer processing time (web scraping + PDF analysis)
- Section-to-slide mapping may need manual tweaks

---

## 📋 Workflow 3: URL Only (Auto-conversion)

**Best for:** Quick prototyping or when no design reference exists

### Input Requirements
- ✅ Website URL only

### Steps

#### 1. Analyze Website
**AI Command:** "/web https://example.com"
- Same as Workflow 2, Step 1

#### 2. Auto-generate Style Theme
**AI Actions:**
- Extract colors from website
- Detect font families and sizes
- Calculate spacing patterns
- Generate `analysis/presentation-pipeline/02_style_theme.json`

**Auto-theme Logic:**
```javascript
// AI creates theme from website styles
const theme = {
  designTokens: {
    colors: extractColorsFromCSS(website),
    typography: detectFontSizes(website),
    spacing: calculateSpacing(website)
  }
}
```

#### 3. Convert Sections → Slides
**Conversion Rules:**
- **Hero section** → hero-cover slide
- **Feature grid (3-6 items)** → table-of-contents slide
- **Text + Image section** → content-text slide
- **Bullet list section** → bullet-list slide
- **Between major sections** → section-divider slide

#### 4-6. Same as Workflow 1 (Integrate → Generate → Preview)

### Pros & Cons

**✅ Pros:**
- Fastest workflow (single URL input)
- No manual design work
- Good for prototyping

**❌ Cons:**
- Less design control
- Auto-generated theme may not match brand
- Web animations/interactions lost

---

## 🔄 Workflow Comparison

| Feature | PDF + Manual | URL + PDF | URL Only |
|---------|-------------|-----------|----------|
| **Speed** | ⚡⚡⚡ Fast | ⚡⚡ Medium | ⚡ Slow |
| **Design Control** | ✅ Full | ✅ Full | ⚠️ Limited |
| **Content Automation** | ❌ Manual | ✅ Auto | ✅ Auto |
| **Brand Consistency** | ✅ High | ✅ High | ⚠️ Low |
| **Complexity** | Low | Medium | Low |
| **Best Use Case** | Branded decks | Website → Presentation | Quick prototypes |

---

## 📊 Decision Tree

```
Do you have a design reference (PDF)?
├─ Yes → Do you have content ready?
│  ├─ Yes → Workflow 1 (PDF + Manual) ⚡⚡⚡
│  └─ No → Do you have a website to scrape?
│     ├─ Yes → Workflow 2 (URL + PDF) ⚡⚡
│     └─ No → Create content manually → Workflow 1
└─ No → Do you have a website to analyze?
   ├─ Yes → Workflow 3 (URL Only) ⚡
   └─ No → Start with blank template → Workflow 1
```

---

## 🛠️ Advanced Usage

### Custom Slide Order
Edit `01_contents_slides.json` to reorder slides:
```json
{
  "slides": [
    { "id": "slide-01", "order": 1, "type": "hero-cover" },
    { "id": "slide-03", "order": 2, "type": "section-divider" },
    { "id": "slide-02", "order": 3, "type": "table-of-contents" }
  ]
}
```

### Theme Overrides
Edit `02_style_theme.json` to customize design:
```json
{
  "designTokens": {
    "colors": {
      "primary": { "main": "#FF6635" }  // Change primary color
    }
  }
}
```

### Slide Type Customization
Add new slide types in `02_style_theme.json`:
```json
{
  "slideTemplates": {
    "my-custom-type": {
      "layout": "split-vertical",
      "elements": { ... }
    }
  }
}
```

---

## 🔍 Troubleshooting

### Issue: PDF text not extracted
**Solution:** PDF embed prevents DOM access. Use OCR or manual input.

### Issue: Website sections don't map well to slides
**Solution:** Manually edit `01_contents_slides.json` to adjust structure.

### Issue: Generated theme doesn't match brand
**Solution:** Use Workflow 2 (URL + PDF) instead of Workflow 3.

### Issue: Slides look empty after generation
**Solution:** Check `03_integrate_presentation.json` for missing data. Re-run integration script.

---

## 📚 Examples

### Example 1: Corporate Presentation (PDF + Manual)
```bash
# Input: company_branding.pdf + manually written slides
# Output: 10-slide deck with exact brand colors
# Time: ~15 minutes
```

### Example 2: Website Redesign Pitch (URL + PDF)
```bash
# Input: https://client-website.com + brand_guidelines.pdf
# Output: 20-slide deck showing "before" content with new branding
# Time: ~30 minutes
```

### Example 3: Quick Demo (URL Only)
```bash
# Input: https://product-landing-page.com
# Output: 5-slide overview with auto-extracted style
# Time: ~10 minutes
```

---

## 🚀 Next Steps

1. Choose your workflow based on inputs
2. Follow step-by-step guide above
3. Preview generated presentation
4. Iterate on content/style as needed
5. Export or deploy final HTML

**Need help?** See `docs/slide_templates.md` for template details or `MIGRATION_LOG.md` for technical architecture.
