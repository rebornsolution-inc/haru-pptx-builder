# Slide Templates Guide

## 📋 Overview

Haru Presentation Builder supports **5 core slide types** extracted from PDF analysis. Each template has specific use cases, layout patterns, and styling guidelines.

---

## 🎨 Template Types

### 1. Hero/Cover Slide (`hero-cover`)

**Purpose:** Opening slide, company introduction, title page

**Layout:** Centered single-column

**Elements:**
- **Logo/Brand:** Large text (140px), bold (900), centered top
- **Main Title:** Primary heading (32-48px), centered
- **Subtitle:** Secondary text (20px), centered below title
- **Footer:** Small text (16px), centered bottom (company name, date, etc.)

**Background:**
- Solid color with optional dotted grid pattern
- Example: Dark navy (#0A1428) + subtle dots (#4A5A7A, 30% opacity)

**Example JSON:**
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

**Use Cases:**
- Presentation cover page
- Section opener with company branding
- Title slides for webinars

---

### 2. Table of Contents (`table-of-contents`)

**Purpose:** Agenda overview, navigation menu, feature list

**Layout:** Centered grid (2x2, 3x2, or custom)

**Elements:**
- **Heading:** "목차", "Agenda", "Contents" (64px, bold)
- **Cards:** Numbered items with optional icons
  - Number badge (e.g., "01", "02")
  - Icon (circle, globe, building, people)
  - Text label (18-20px)
  - Click target (link to specific slide)

**Card Styling:**
- Background: Semi-transparent blue (rgba(59, 123, 255, 0.1))
- Border: 1px solid rgba(59, 123, 255, 0.3)
- Border radius: 12px
- Padding: 24px 32px
- Size: ~400px × 120px

**Hover Effects:**
- Background brightens (0.1 → 0.2 opacity)
- Lift animation (translateY -4px)
- Box shadow (0 8px 24px)

**Example JSON:**
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

**Use Cases:**
- Presentation agenda
- Service/feature list (4-6 items)
- Navigation hub for sections

---

### 3. Section Divider (`section-divider`)

**Purpose:** Chapter breaks, section transitions, visual separator

**Layout:** Centered minimal (2-3 elements only)

**Elements:**
- **Section Number:** Very large (180px), bold (900), semi-transparent (90% opacity)
- **Section Title:** Medium heading (48px), bold (700)
- **Page Number:** Small text (14px), bottom-right corner (e.g., "3 / 20")

**Background:**
- Split two-tone effect (50/50 vertical split)
- Example: Left #0A1428, Right #1A2438

**Example JSON:**
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

**Use Cases:**
- Section start markers (Chapter 1, Chapter 2)
- Visual breaks between topics
- Breathing space in long presentations

---

### 4. Content with Text (`content-text`)

**Purpose:** Main content slides with paragraphs and optional images

**Layout:** Split horizontal (60/40 or 50/50)

**Elements:**
- **Title:** Section heading (48px), left-aligned
- **Body Text:** Paragraph (20px), left-aligned, line-height 1.8
- **Image (optional):** Right side, 40% width, rounded corners

**Background:**
- Solid color (dark or light depending on theme)

**Example JSON:**
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

**Use Cases:**
- Detailed explanations
- Case studies
- Product descriptions

---

### 5. Bullet List (`bullet-list`)

**Purpose:** Key points, features, takeaways

**Layout:** Centered list (3-5 items)

**Elements:**
- **Title:** Section heading (48px), centered
- **Bullets:** List items (24px), left-aligned or centered
  - Custom bullet color (e.g., primary blue)
  - Gap between items: 24px

**Background:**
- Solid color (usually dark for emphasis)

**Example JSON:**
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

**Use Cases:**
- Feature lists (3-5 items)
- Summary slides
- Key takeaways

---

## 🎨 Design Token Reference

### Colors (from PDF analysis)
```css
--primary-blue: #5B7BFF;
--bg-dark: #0A1428;
--bg-darker: #1A2438;
--text-primary: #FFFFFF;
--text-secondary: #E0E6F0;
--text-muted: #8899BB;
```

### Typography
```css
--font-hero: 140px / 900;
--font-h1: 64px / 700;
--font-h2: 48px / 700;
--font-body: 20px / 400;
--font-small: 16px / 500;
```

### Spacing
```css
--page-padding: 100px;
--section-gap: 60px;
--card-gap: 24px;
```

---

## 📐 Layout Guidelines

### Aspect Ratio
- **Default:** 16:9 (1920×1080, 1440×810, etc.)
- **Full-screen:** `width: 100vw; height: 100vh`

### Alignment Rules
- **Hero/Cover:** Center everything
- **TOC:** Center heading, grid cards below
- **Section Divider:** Center number + title vertically
- **Content:** Left-align text, right-align image
- **Bullet List:** Center title, left-align bullets

### Safe Zones
- **Padding:** Minimum 80px on all sides (desktop)
- **Tablet:** 60px padding
- **Mobile:** 40px padding

---

## 🔄 Template Selection Logic

**When analyzing a slide, choose template based on:**

| Content Type | Template |
|--------------|----------|
| Logo + Title only | `hero-cover` |
| 4-6 numbered cards | `table-of-contents` |
| Large number + short title | `section-divider` |
| Paragraph text + image | `content-text` |
| 3-5 bullet points | `bullet-list` |

**Edge cases:**
- Mixed content (text + bullets + image) → Use `content-text` with bullets
- Many items (7+) → Split into multiple `bullet-list` slides
- Complex layouts → Break into 2-3 simpler slides

---

## 💡 Template Customization

### Adding New Templates
1. Analyze PDF for new patterns
2. Add to `02_style_theme.json` under `slideTemplates`
3. Define layout, elements, background, spacing
4. Document in this file
5. Create HTML template in `components/slide-templates/`

### Modifying Existing Templates
1. Update `02_style_theme.json`
2. Regenerate `03_integrate_presentation.json`
3. Test with `node scripts/generate_presentation.js`

---

## 📚 Examples

See `output/presentation/bluehive_sample.html` for working examples of:
- Hero/Cover slide (Slide 1)
- Table of Contents (Slide 2)
- Section Divider (Slide 3)
