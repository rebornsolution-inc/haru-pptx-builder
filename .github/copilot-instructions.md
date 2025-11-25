# AI-Powered Presentation Builder System

## 🎯 Project Purpose

**Haru Presentation Builder** generates presentation-style static websites from multiple input sources:
- **PDF presentations** (extract design tokens and slide structure)
- **Existing websites** (analyze responsive design patterns)  
- **Manual content** (user-provided JSON structure)

**Output:** Single-page HTML presentations with:
- Slide-based navigation (keyboard: Arrow keys, Space)
- Tailwind CSS styling
- Responsive design (mobile, tablet, desktop)
- Animation support (GSAP, CSS transforms)

---

## 🔒 Core Principles

### 1. MCP Tool Policy (MANDATORY)

**⚠️ USE KAPTURE MCP TOOLS EXCLUSIVELY:**

✅ **ALLOWED:**
- `mcp_kapture_list_tabs()`, `mcp_kapture_navigate()`, `mcp_kapture_dom()`
- `mcp_kapture_elements()`, `mcp_kapture_screenshot()`, `mcp_kapture_hover()`
- `mcp_kapture_click()`, `mcp_kapture_keypress()`, `mcp_kapture_resize()`

❌ **FORBIDDEN:**
- `mcp_microsoft_pla_*` (Microsoft Playwright MCP)
- `mcp_browsermcp_*` (Generic Browser MCP)
- `mcp_kapture_evaluate()` (does NOT exist)

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

### 3. Image Handling - Smart Policy

**⚠️ Distinguish functional vs decorative images**

#### 🔧 Functional Images (Use Exact JSON Path)
- Canvas textures, materials, assets
- Video thumbnails and posters
- Interactive diagrams with animations
- Document viewers (charts, graphs)
- SVG graphics with specific animations

**Example:**
```json
{ "visual": { "type": "canvas", "texture": "/images/chart.png" }}
→ HTML: <img src="/images/chart.png" />
```

#### 🎨 Decorative Images (Use Picsum Placeholder)
- Company/partner logos
- Product photos in cards
- Team member portraits
- Testimonial avatars
- General illustrations
- Background images (without animation requirements)

**Example:**
```json
{ "illustration": "/images/product.svg" }
→ HTML: <img src="https://picsum.photos/seed/product/400/300" />
```

---

## 📐 Input Analysis Workflows

### Workflow 1: PDF Analysis (Primary Method)

**Use Case:** PDF presentation already exists, need to extract design and structure

**Steps:**
1. Open PDF in browser (Chrome/Safari)
2. Navigate slides with `ArrowRight` / `ArrowLeft`
3. Capture screenshots of each slide (wait 300ms after navigation)
4. Extract design tokens: colors, typography, spacing
5. Identify slide templates: hero-cover, toc, divider, content, bullet-list
6. Generate `analysis/pdf-analysis/[filename]_style_analysis.json`

**Expected Output:**
```json
{
  "slides": [
    {
      "slideNumber": 1,
      "template": "hero-cover",
      "elements": [...],
      "designTokens": {
        "colors": { "primary": "#5B7BFF", "background": "#0A1428" },
        "typography": { "heading": "140px/1.2/800", "body": "18px/1.8/400" },
        "spacing": { "sectionPadding": "100px 0" }
      }
    }
  ],
  "totalSlides": 3
}
```

### Workflow 2: URL Analysis (Website Conversion)

**Use Case:** Convert existing long-scroll website into slide-based presentation

**Steps:**
1. Navigate to URL with `mcp_kapture_navigate()`
2. Capture initial DOM and elements
3. Scroll with `ArrowDown` to capture major sections (5-10 sections typical)
4. Test interactive elements (hover, click)
5. Extract design system (colors, fonts, spacing)
6. Map sections to slide templates
7. Generate `analysis/web-pipeline/01_contents_web.json` + `02_style_web.json`

**Section → Slide Mapping:**
- Hero section → `hero-cover` slide
- Feature grid → `bullet-list` slide
- Process steps → `content-text` slide with numbered list
- Team/Partners → `content-text` slide with grid layout

### Workflow 3: Manual Content (JSON Input)

**Use Case:** User provides content directly as JSON

**Steps:**
1. User provides `01_contents_slides.json` (slide content)
2. User provides `02_style_theme.json` (design tokens) OR references PDF
3. AI validates JSON structure
4. Proceed to integration step

---

## 🔄 Pipeline Structure

```
analysis/
├── pdf-analysis/                     # PDF style extraction results
│   └── [filename]_style_analysis.json
│
└── presentation-pipeline/            # Core pipeline data
    ├── 01_contents_slides.json       # Slide content (manual or extracted)
    ├── 02_style_theme.json           # Theme tokens (manual or from PDF)
    └── 03_integrate_presentation.json # Merged output (ready for generation)
```

### 01_contents_slides.json Schema

```json
{
  "slides": [
    {
      "id": "slide-01",
      "template": "hero-cover",
      "elements": {
        "heading": { "text": "...", "style": "heading1" },
        "subheading": { "text": "...", "style": "body" },
        "cta": { "text": "...", "link": "#next" }
      },
      "background": {
        "type": "gradient",
        "colors": ["primary", "secondary"]
      },
      "transition": "fade"
    }
  ]
}
```

### 02_style_theme.json Schema

```json
{
  "slideTemplates": {
    "hero-cover": {
      "layout": "center-aligned",
      "heading": { "fontSize": "140px", "fontWeight": 800 },
      "background": "gradient"
    }
  },
  "designTokens": {
    "colors": {
      "primary": "#5B7BFF",
      "secondary": "#FF6B6B",
      "background": "#0A1428"
    },
    "typography": {
      "heading1": { "size": "140px", "weight": 800, "lineHeight": 1.2 },
      "body": { "size": "18px", "weight": 400, "lineHeight": 1.8 }
    },
    "spacing": {
      "sectionPadding": "100px",
      "elementGap": "40px"
    }
  }
}
```

---

## ⚙️ Execution Commands

### `/pdf [filepath]` - Analyze PDF Presentation

**Example:** `/pdf /Users/jadon/Downloads/presentation.pdf`

**Behavior:**
1. Connects to browser tab with PDF open
2. Navigates slides with ArrowRight (N slides)
3. Extracts design tokens from each slide
4. Identifies slide templates
5. **AUTO-STOPS** after generating `[filename]_style_analysis.json`
6. User must manually request `/integrate` or `/generate`

### `/url [website]` - Analyze Website for Conversion

**Example:** `/url https://example.com`

**Behavior:**
1. Navigates to URL
2. Captures major sections (5-10 typical)
3. Extracts design system
4. Maps sections to slide templates
5. **AUTO-STOPS** after generating `01_contents_web.json` + `02_style_web.json`
6. User must manually request `/integrate`

### `/integrate` - Merge Content + Style

**Prerequisite:** Either (`01_contents` + `02_style`) OR (`01_contents` + `PDF analysis`)

**Behavior:**
```bash
node scripts/integrate_presentation_pipeline.js
```

**Output:** `03_integrate_presentation.json` (merged slides with applied styles)

**Modes:**
- **Mode 1:** content + theme (both JSON files exist)
- **Mode 2:** content + pdf (01_contents + pdf_analysis exist)
- **Mode 3:** pdf-only (only pdf_analysis exists, generates sample content)

### `/generate` - Generate HTML Presentation

**Prerequisite:** `03_integrate_presentation.json` exists

**Behavior:**
1. Reads integrated JSON
2. Generates single HTML file with Tailwind CSS
3. Includes slide navigation logic (Arrow keys, Space)
4. Adds GSAP animations if specified
5. Outputs to `output/presentation/[filename].html`

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

## ✅ Quality Checklist

### PDF Analysis
- [ ] All slides captured (N/N complete)
- [ ] Design tokens extracted (colors, typography, spacing)
- [ ] Slide templates identified
- [ ] Transitions noted (if animated)
- [ ] JSON file generated in `analysis/pdf-analysis/`

### URL Analysis  
- [ ] Major sections captured (5-10 typical)
- [ ] Design system extracted
- [ ] Sections mapped to slide templates
- [ ] Interactive elements tested
- [ ] JSON files generated in `analysis/web-pipeline/`

### Integration
- [ ] Content + style merged successfully
- [ ] All slides have applied styles
- [ ] Design tokens validated (no missing references)
- [ ] Output file size reasonable (10-50KB typical)

### Code Generation
- [ ] HTML file generated with correct structure
- [ ] Tailwind classes applied correctly
- [ ] Keyboard navigation working (Arrow keys, Space)
- [ ] Responsive design implemented (mobile, tablet, desktop)
- [ ] Animations added if specified (GSAP)

---

## 🔗 Default Link Configuration (Harufolio Project)

**⚠️ CRITICAL: All generated code MUST use these default URLs**

| Link Type | Display Text | Actual URL | Notes |
|-----------|-------------|------------|-------|
| **Social Links** | Instagram, SNS, Social | `https://instagram.com/haru_folio` | All social media references |
| **Gallery/Portfolio** | Gallery, Works, Projects | `https://port.gallery` | All portfolio/gallery pages |
| **Company Info** | Contact, About, Company | `https://rebornsolution.com` | Contact forms, company info |
| **Footer Credit** | "built by harufolio" | `https://port.gallery` | Always in footer, hyperlinked |

**Footer Template (MANDATORY):**
```html
<footer class="py-8 text-center text-sm text-gray-500">
  <p>built by <a href="https://port.gallery" class="hover:text-gray-700 transition">harufolio</a></p>
</footer>
```

---

## 📦 Configuration

- **Viewports:** Mobile (375px), Tablet (768px), Desktop (1440px)
- **Animation Wait:** 300ms after slide navigation
- **Slide Transition Duration:** 0.5s (default)
- **Keyboard Shortcuts:** 
  - Arrow Left/Right: Navigate slides
  - Space: Next slide
  - Home: First slide
  - End: Last slide

---

## 🚨 Common Issues & Solutions

### Issue: PDF slides not advancing
- **Solution:** Ensure PDF is in "presentation mode" (full-screen)
- **Solution:** Increase wait time to 500ms between keypresses

### Issue: Design tokens incomplete
- **Solution:** Review screenshots for missing colors/fonts
- **Solution:** Manually add tokens to `02_style_theme.json`

### Issue: Website sections don't map to slides well
- **Solution:** Use manual content mode (`01_contents_slides.json`)
- **Solution:** Combine/split sections to match slide templates

### Issue: Generated HTML has layout issues
- **Solution:** Verify `03_integrate_presentation.json` structure
- **Solution:** Check Tailwind classes for typos
- **Solution:** Test responsive breakpoints (md:, lg:)

---

## 📝 Version History

- **v3.0.0** (2025-01-17): Presentation Builder Launch
  - **CRITICAL:** Complete refactor from Web Builder to Presentation Builder
  - **New Pipeline:** PDF analysis → slide templates → HTML generation
  - **Workflows:** PDF-first, URL conversion, manual content
  - **Removed:** Web scraping logic (progressive scroll, 30-80 checkpoints)
  - **Removed:** React/TSX component generation
  - **Added:** Slide template system (5 types)
  - **Added:** Node.js integration script (3 input modes)
  - **Documentation:** Created slide_templates.md, presentation_workflow.md
  - **Impact:** Project fully optimized for presentation generation
