# Haru Presentation Builder

AI-powered presentation generator that creates slide-based web presentations from multiple input sources.

## 🎯 Overview

Haru Presentation Builder is an intelligent system that combines AI analysis with the Model Context Protocol (MCP) to generate professional slide-based presentations. It supports multiple input sources: URL analysis for content, PDF for style extraction, and manual JSON input.

**Key Features:**
- 🔍 **Multi-Source Input** - URL content analysis + PDF style extraction
- 🎨 **Design System Extraction** - Automatic design token generation from PDFs
- 💻 **Slide Generation** - Production-ready HTML presentations with keyboard navigation
- 🤖 **MCP Integration** - Kapture MCP for real browser interaction
- 📱 **Responsive Slides** - Full-screen slides with 16:9 aspect ratio
- ⌨️ **Keyboard Navigation** - Arrow keys, Space, Home/End for slide control

## 🚀 Quick Start

### Prerequisites

- Node.js 16+
- VS Code with GitHub Copilot
- Kapture MCP extension (for web/PDF exploration)

### Installation

```bash
# Clone the repository
git clone https://github.com/rebornsolution-inc/haru-presentation-builder.git
cd haru-presentation-builder

# Install dependencies (if needed)
npm install
```

### Usage

#### Option 1: PDF Style + Manual Content (Fastest)

```bash
# 1. Open PDF in Chrome
open file:///path/to/your/presentation.pdf

# 2. Analyze PDF style (AI will capture design tokens)
# AI generates: analysis/pdf-analysis/[filename]_style_analysis.json

# 3. Create content JSON manually or let AI generate from topic
# File: analysis/presentation-pipeline/01_contents_slides.json

# 4. Integrate style + content
node scripts/integrate_presentation_pipeline.js

# 5. Generate HTML presentation
node scripts/generate_presentation.js

# Output: output/presentation/index.html
```

#### Option 2: URL Content + PDF Style (Hybrid)

```bash
# 1. Analyze website for content structure
# AI converts sections → slides

# 2. Analyze PDF for brand style
# AI extracts colors, fonts, layouts

# 3. Merge URL content with PDF style
node scripts/integrate_presentation_pipeline.js

# 4. Generate HTML presentation
node scripts/generate_presentation.js
```

#### Option 3: URL Only (Auto-conversion)

```bash
# 1. Analyze website
# AI converts long-scroll website → slide-based presentation

# 2. Generate presentation
node scripts/integrate_presentation_pipeline.js
node scripts/generate_presentation.js
```

# Install dependencies
npm install
```

### Configuration

The project uses MCP (Model Context Protocol) for web exploration. Configuration is in `.vscode/mcp.json`.

## 📖 Usage

### Basic Web Analysis

```bash
# In VS Code with Copilot Chat
/web https://example.com
```

This will:
1. Explore the website (MCP-based browser interaction)
2. Analyze the website structure (content) → `01_contents_web.json`
3. Extract design system (style) → `02_style_web.json`
4. ⚠️ **Auto-stop here** (integration and code generation require manual commands)

### Complete Workflow

```bash
# Step 1: Analysis (Auto-stop after this)
/web https://example.com
# → Outputs: 01_contents_web.json + 02_style_web.json

# Step 2: Integration (Manual request)
/integrate
# → Outputs: 03_integrate_web.json

# Step 3: Code Generation (Manual request)
/generate
# → Outputs: output/web/index.html
```

## 📁 Project Structure

```
haru-web-builder/
├── .github/
│   └── copilot-instructions.md    # AI behavior rules
├── .vscode/
│   └── mcp.json                   # MCP configuration
├── analysis/
│   └── web-pipeline/
│       ├── 01_contents_web.json   # Content analysis output
│       ├── 02_style_web.json      # Style analysis output
│       ├── 03_integrate_web.json  # Integrated specification
│       └── generators/
│           └── 04_generate_tailwind.json
├── output/
│   ├── web_contents.json          # Public content spec
│   ├── web_style.json             # Public style spec
│   ├── WebDevSpec.json            # Public integration spec
│   └── web/
│       └── index.html             # Generated code
├── docs/
└── scripts/
```

## 🎨 Features

### Progressive 5% Scroll Analysis

The system uses a **21-checkpoint scrolling protocol** (0%, 5%, 10%...100%) to ensure complete coverage:

- Captures every visual change
- Detects all scroll animations (fade-in, parallax, etc.)
- Tests interactive elements at each checkpoint
- Documents state changes systematically

### Design Token Extraction

Automatically extracts:
- Color system (primary, secondary, accent, neutrals)
- Typography (font families, sizes, weights, line heights)
- Spacing system (margins, padding, gaps)
- Component patterns (buttons, cards, forms)
- Animation timings and easings

### Code Generation Options

**Tailwind Single-Page (Default)**
- Single HTML file with Tailwind v4 CDN
- Utility-first approach
- Fast prototyping
- Easy maintenance

## 🛠️ Commands

| Command | Execution | Output | Description |
|---------|-----------|--------|-------------|
| `/web [url]` | **AUTO** | `01_contents_web.json`<br>`02_style_web.json` | Web exploration + analysis (auto-stop) |
| `/integrate` | **MANUAL** | `03_integrate_web.json` | Merge content + style specs |
| `/generate` | **MANUAL** | `output/web/index.html` | Generate production code |

## 📋 Analysis Quality Checklist

**Content Analysis (01_contents_web.json)**
- [ ] Complete page structure
- [ ] Navigation hierarchy
- [ ] SEO metadata
- [ ] Interactive elements documented
- [ ] Accessibility requirements
- [ ] **Complex features with full implementation details**

**Style Analysis (02_style_web.json)**
- [ ] Color system with states
- [ ] Responsive typography
- [ ] Spacing system
- [ ] Component patterns
- [ ] Animation specifications (with code hints)
- [ ] 21-checkpoint scroll coverage
- [ ] **All animations include: type, trigger, properties, library, codeHint**

**Integration (03_integrate_web.json)**
- [ ] Content + style merged
- [ ] No hard-coded values
- [ ] All states documented
- [ ] Responsive behavior defined
- [ ] Accessibility mapped
- [ ] **Implementation details preserved from analysis**

**Code Generation**
- [ ] Production-ready code
- [ ] WCAG 2.1 AA compliance
- [ ] SEO optimized
- [ ] All animations implemented
- [ ] No placeholder content (except images)
- [ ] **✅ JSON-to-HTML Fidelity Check (MANDATORY)**
  - [ ] Every visual element from JSON is rendered
  - [ ] All animations from JSON are implemented
  - [ ] All images use exact paths from JSON (no placeholders unless specified)
  - [ ] All complex features (3D, video, SVG) are fully implemented
  - [ ] All specified libraries are included via CDN
  - [ ] No simplification or placeholder replacements
  - [ ] Interactive behaviors match JSON specifications

## 🔒 Core Principles

### 1. MCP Tool Policy
- ✅ Use Kapture MCP exclusively (`mcp_kapture_*`)
- ❌ No Microsoft Playwright MCP
- ❌ No generic browser MCP

### 2. Screenshot Policy
- Take via MCP → Analyze immediately
- No file saving (memory-based analysis)
- Compare with conversation history

### 3. No Shortcuts
- Complete 21-checkpoint process mandatory
- No "End" key jumps
- No "fast analysis"
- Systematic approach required

## 🤖 AI Integration

This project is designed to work with **GitHub Copilot** using detailed instructions in `.github/copilot-instructions.md`.

The AI follows strict protocols:
- 21-checkpoint progressive scrolling
- Mandatory interaction testing
- Complete feature implementation
- No simplification of complex features
- **Detailed JSON schemas to prevent information loss**

### Key Feature: Information Preservation

**Problem Solved:** AI analyzes in detail but JSON simplification causes implementation detail loss

**Solution:**
- Content JSON includes full `implementation` objects
- Style JSON includes `codeHint` for animations
- Integration JSON preserves all technical specifications
- Code generation has complete implementation instructions

**Example:**
```
Analysis: "Ship moves in 3D with scroll, ocean has parallax"
     ↓
JSON: { type: "3d-canvas-animation", implementation: { technology: "Three.js", 
       trigger: "scroll", details: "Ship translateX 0→100vw, ocean -20% parallax",
       codeHint: "gsap.to('.ship', {x:'100vw', scrollTrigger:{scrub:true}})" }}
     ↓
Code: Full Three.js implementation with GSAP ScrollTrigger
```

## 🎯 Use Cases

- **Website Replication** - Recreate existing sites
- **Design System Documentation** - Extract design tokens
- **Prototype Generation** - Quick mockups from reference
- **Accessibility Audit** - Analyze WCAG compliance
- **Responsive Analysis** - Multi-viewport testing

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

## 📞 Support

- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/haru-web-builder/issues)
- Discussions: [GitHub Discussions](https://github.com/YOUR_USERNAME/haru-web-builder/discussions)

## 🙏 Acknowledgments

- Built with [GitHub Copilot](https://github.com/features/copilot)
- Uses [Kapture MCP](https://github.com/microsoft/mcp) for web exploration
- Powered by [Tailwind CSS v4](https://tailwindcss.com/)

---

**Version:** 2.2.0  
**Last Updated:** November 11, 2025
