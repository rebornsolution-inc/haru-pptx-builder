import json
import os
import sys

# Icon mapping - Unicode/Emoji icons for common logistics icons
ICON_MAP = {
    'ship': '🚢',
    'plane': '✈️',
    'truck': '🚚',
    'warehouse': '🏭',
    'globe': '🌍',
    'handshake': '🤝',
    'snowflake': '❄️',
    'boxes': '📦',
    'tag': '🏷️',
    'door': '🚪',
    'barcode': '📊',
    'calendar': '📅',
    'chart': '📈',
    'check': '✅',
    'users': '👥',
    'clipboard': '📋',
    'building': '🏢',
    'label': '🏷️',
    'search': '🔍',
    'box': '📦',
    'ruler': '📏',
    'weight': '⚖️',
    'route': '🛤️',
    'clock': '⏰',
    'phone': '📞',
    'fax': '📠',
    'email': '📧',
    'asia': '🌏',
    'europe': '🌍',
    'americas': '🌎',
    # Shapes for business model
    'circle': '●',
    'square': '■',
    'triangle': '▲',
    'diamond': '◆',
}

def get_icon(icon_name):
    """Convert icon name to actual icon (emoji or SVG)"""
    return ICON_MAP.get(icon_name, '●')

def extract_color_value(color_obj):
    """Extract actual color value from color object or string"""
    if isinstance(color_obj, dict):
        # Try to get 'main' first, then 'dark', then first available value
        return color_obj.get('main') or color_obj.get('dark') or next(iter(color_obj.values()), '#333333')
    return color_obj if color_obj else '#333333'

def generate_html(project_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_dir = os.path.join(base_dir, 'projects', project_name)
    json_path = os.path.join(project_dir, 'presentation.json')
    html_path = os.path.join(project_dir, 'presentation.html')

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    slides = data.get('slides', [])
    design_tokens = data.get('designTokens', {})
    colors = design_tokens.get('colors', {})
    typography = design_tokens.get('typography', {})
    fonts = design_tokens.get('fonts', {})
    shadows = design_tokens.get('shadows', {})
    radius = design_tokens.get('radius', {})
    
    # Extract actual color values
    primary_color = extract_color_value(colors.get('primary', '#FF6B35'))
    secondary_color = extract_color_value(colors.get('secondary', '#FFB800'))
    bg_dark = extract_color_value(colors.get('background', {}).get('dark', '#1A1A1A')) if isinstance(colors.get('background'), dict) else '#1A1A1A'
    bg_card = extract_color_value(colors.get('background', {}).get('card', '#2A2A2A')) if isinstance(colors.get('background'), dict) else '#2A2A2A'
    text_primary = extract_color_value(colors.get('text', {}).get('primary', '#FFFFFF')) if isinstance(colors.get('text'), dict) else '#FFFFFF'
    text_secondary = extract_color_value(colors.get('text', {}).get('secondary', '#CCCCCC')) if isinstance(colors.get('text'), dict) else '#CCCCCC'
    text_muted = extract_color_value(colors.get('text', {}).get('muted', '#888888')) if isinstance(colors.get('text'), dict) else '#888888'
    
    # CSS Variables - properly formatted with full design token system
    css_vars = f""":root {{
  /* Colors */
  --primary: {primary_color};
  --primary-light: {colors.get('primary', {}).get('light', '#FF8A5B') if isinstance(colors.get('primary'), dict) else '#FF8A5B'};
  --primary-dark: {colors.get('primary', {}).get('dark', '#E55A25') if isinstance(colors.get('primary'), dict) else '#E55A25'};
  --secondary: {secondary_color};
  --bg-dark: {bg_dark};
  --bg-darker: {colors.get('background', {}).get('darker', '#0D0D0D') if isinstance(colors.get('background'), dict) else '#0D0D0D'};
  --bg-card: {bg_card};
  --bg-overlay: rgba(0, 0, 0, 0.7);
  --text-primary: {text_primary};
  --text-secondary: {text_secondary};
  --text-muted: {text_muted};
  --chart-orange: {primary_color};
  --chart-yellow: {secondary_color};
  --chart-gray: #4A4A4A;
  
  /* Typography */
  --font-main: 'Pretendard', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-heading: 'Pretendard', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  
  /* Font Sizes - from design tokens */
  --size-hero: 72px;
  --size-h1: 48px;
  --size-h2: 36px;
  --size-h3: 24px;
  --size-body: 16px;
  --size-caption: 12px;
  --size-stat: 64px;
  
  /* Font Weights */
  --weight-extra-bold: 800;
  --weight-bold: 700;
  --weight-semi-bold: 600;
  --weight-regular: 400;
  
  /* Spacing - 8px grid system */
  --space-page-h: 60px;
  --space-page-v: 48px;
  --space-section: 40px;
  --space-element: 24px;
  --space-tight: 12px;
  --space-xs: 8px;
  
  /* Effects */
  --radius-card: 8px;
  --radius-image: 4px;
  --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.3);
}}
"""

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('metadata', {}).get('companyName', data.get('projectName', 'Presentation'))}</title>
    <style>
        {css_vars}
        
        /* Import Fonts */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--font-main);
            background-color: #202020;
            color: var(--text-primary);
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .slide {{
            width: 297mm;
            height: 167mm;
            background: var(--bg-dark);
            color: var(--text-primary);
            position: relative;
            overflow: hidden;
            page-break-after: always;
            break-after: page;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
        }}

        .slide.last-slide {{
            page-break-after: avoid;
            break-after: avoid;
        }}

        /* Layout Containers */
        .content-overlay {{
            position: relative;
            z-index: 2;
            width: 100%;
            height: 100%;
            padding: var(--space-page-v) var(--space-page-h);
            display: flex;
            flex-direction: column;
        }}

        /* Split Layout (Left Text / Right Image) */
        .layout-split {{
            display: flex;
        }}
        
        .layout-split .content-overlay {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
            align-items: stretch;
            padding: 0;
            width: 100%;
            height: 100%;
        }}
        
        /* Image Left Layout */
        .layout-split.image-left .content-overlay {{
            grid-template-columns: 1fr 1fr;
        }}
        
        .layout-split .col-left {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
            padding: var(--space-page-v) var(--space-section) var(--space-page-v) var(--space-page-h);
            overflow: hidden;
        }}
        
        .layout-split.image-left .col-left {{
            padding: 0;
            overflow: hidden;
        }}
        
        .layout-split.image-left .col-left .element-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 0;
        }}
        
        .layout-split .col-right {{
            position: relative;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
        }}
        
        .layout-split:not(.image-left) .col-right {{
            padding: 0;
        }}
        
        .layout-split.image-left .col-right {{
            padding: var(--space-page-v) var(--space-page-h) var(--space-page-v) var(--space-section);
        }}
        
        .layout-split:not(.image-left) .col-right .element-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 0;
        }}

        /* Center Layout */
        .layout-center .content-overlay {{
            align-items: center;
            text-align: center;
            justify-content: center;
        }}

        /* Typography - Professional Template Style */
        .element-heading {{
            font-family: var(--font-heading);
            font-size: var(--size-h1);
            font-weight: var(--weight-extra-bold);
            line-height: 1.1;
            letter-spacing: -0.02em;
            margin-bottom: var(--space-element);
            color: var(--text-primary);
            text-transform: uppercase;
            white-space: pre-line;
        }}
        
        .element-subheading {{
            font-size: 20px;
            font-weight: var(--weight-regular);
            line-height: 1.5;
            margin-bottom: var(--space-element);
            color: var(--text-secondary);
            white-space: pre-line;
        }}
        
        .element-badge {{
            font-size: var(--size-caption);
            font-weight: var(--weight-regular);
            color: var(--text-muted);
            letter-spacing: 0.05em;
            margin-bottom: var(--space-tight);
            display: inline-block;
            text-transform: none;
        }}
        
        .element-body {{
            font-size: var(--size-body);
            font-weight: var(--weight-regular);
            line-height: 1.7;
            color: var(--text-secondary);
            margin-bottom: var(--space-tight);
        }}
        
        .element-quote {{
            font-size: 18px;
            font-style: italic;
            color: var(--text-secondary);
            margin-top: var(--space-element);
            padding: 20px;
            border-left: 3px solid var(--primary);
            background: rgba(255,255,255,0.03);
        }}
        
        .element-logo {{
            font-size: var(--size-h3);
            font-weight: var(--weight-bold);
            color: var(--primary);
            margin-bottom: var(--space-xs);
        }}

        /* Image Handling */
        .element-image {{
            max-width: 100%;
            height: auto;
            border-radius: var(--radius-image);
            box-shadow: var(--shadow-card);
        }}

        /* Background Image */
        .bg-image {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: 0;
        }}
        
        .bg-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }}
        
        /* Section Divider - Professional Style */
        .template-section-divider .content-overlay {{
            justify-content: center;
            align-items: flex-start;
            padding: var(--space-page-v) var(--space-page-h);
            padding-left: 80px;
        }}
        
        .template-section-divider.align-center .content-overlay {{
            align-items: center;
            text-align: center;
            padding-left: var(--space-page-h);
            padding-right: var(--space-page-h);
        }}
        
        .template-section-divider.align-right .content-overlay {{
            align-items: flex-end;
            text-align: right;
            padding-left: var(--space-page-h);
            padding-right: 80px;
        }}
        
        .template-section-divider .element-heading {{
            font-size: 96px;
            opacity: 0.3;
            margin-bottom: -16px;
            letter-spacing: -0.03em;
            white-space: nowrap;
        }}
        
        .template-section-divider .element-subheading {{
            font-size: 72px;
            font-weight: var(--weight-extra-bold);
            margin: 0;
            color: var(--primary);
            letter-spacing: -0.02em;
            white-space: nowrap;
        }}
        
        .section-divider-text {{
            display: flex;
            flex-direction: column;
            gap: 0;
        }}
        
        .section-divider-text .element-heading {{
            font-size: 96px;
            opacity: 0.3;
            margin-bottom: -16px;
            letter-spacing: -0.03em;
        }}
        
        .section-divider-text .element-subheading {{
            font-size: 72px;
            font-weight: var(--weight-extra-bold);
            margin: 0;
            color: var(--primary);
            letter-spacing: -0.02em;
        }}
        
        /* Timeline Styles - Greyco Roadmap Style */
        .timeline-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 0;
            margin-top: var(--space-section);
            width: 100%;
        }}
        
        .timeline-item {{
            padding: var(--space-tight) var(--space-tight) 0 0;
            position: relative;
            border-top: 4px solid var(--primary);
        }}
        
        .timeline-year {{
            font-size: 18px;
            font-weight: var(--weight-extra-bold);
            margin-bottom: var(--space-xs);
            letter-spacing: -0.01em;
        }}
        
        .timeline-milestone {{
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.4;
        }}
        
        /* TOC - Table of Contents (Greyco Style) */
        .toc-container {{
            display: flex;
            flex-direction: column;
            gap: var(--space-element);
            margin-top: var(--space-section);
        }}
        
        .toc-item {{
            display: flex;
            align-items: baseline;
            gap: var(--space-tight);
        }}
        
        .toc-number {{
            font-size: var(--size-h3);
            font-weight: var(--weight-bold);
            min-width: 50px;
            letter-spacing: -0.01em;
        }}
        
        .toc-title {{
            font-size: 20px;
            font-weight: var(--weight-semi-bold);
        }}
        
        /* Stats Block - Greyco Style */
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: var(--space-section);
            margin-top: var(--space-section);
        }}
        
        .stat-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .stat-value {{
            font-size: var(--size-stat);
            font-weight: var(--weight-bold);
            line-height: 1;
            margin-bottom: var(--space-xs);
            letter-spacing: -0.02em;
        }}
        
        .stat-unit {{
            font-size: var(--size-h3);
            font-weight: var(--weight-regular);
            margin-left: 4px;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}
        
        /* Chart - Horizontal Bar */
        .chart-container {{
            margin-top: var(--space-section);
            width: 100%;
        }}
        
        .chart-title {{
            font-size: var(--size-body);
            font-weight: var(--weight-semi-bold);
            margin-bottom: var(--space-tight);
            color: var(--text-primary);
        }}
        
        .chart-bar-item {{
            margin-bottom: var(--space-tight);
        }}
        
        .chart-bar-label {{
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }}
        
        .chart-bar-wrapper {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            height: 8px;
            overflow: hidden;
        }}
        
        .chart-bar {{
            height: 100%;
            border-radius: 4px;
        }}
        
        /* Business Model Cards - Greyco Style */
        .model-cards-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-element);
            margin-top: var(--space-section);
        }}
        
        .model-card {{
            background: var(--bg-card);
            border-radius: var(--radius-card);
            padding: var(--space-section) var(--space-element);
            text-align: center;
        }}
        
        .model-card-icon {{
            font-size: 48px;
            margin-bottom: 20px;
        }}
        
        .model-card-title {{
            font-size: 20px;
            font-weight: var(--weight-bold);
            color: var(--text-primary);
            margin-bottom: var(--space-tight);
        }}
        
        .model-card-desc {{
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}
        
        /* Comparison Table - Greyco Style */
        .comparison-table {{
            width: 100%;
            margin-top: var(--space-section);
            border-collapse: collapse;
        }}
        
        .comparison-table th,
        .comparison-table td {{
            padding: var(--space-tight);
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .comparison-table th {{
            font-size: 14px;
            font-weight: var(--weight-semi-bold);
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.05);
        }}
        
        .comparison-table td:first-child {{
            text-align: left;
            font-weight: var(--weight-semi-bold);
        }}
        
        .comparison-table tr.highlight {{
            background: rgba(255, 107, 53, 0.1);
        }}
        
        .comparison-table tr.highlight td {{
            color: var(--primary);
            font-weight: var(--weight-bold);
        }}
        
        .comparison-table .check {{
            color: var(--text-muted);
            font-size: 18px;
        }}
        
        .comparison-table .highlight-check {{
            color: var(--primary);
            font-weight: var(--weight-bold);
            font-size: 18px;
        }}
        
        /* Icon Grid (6 out of 10 style) - Greyco Style */
        .icon-grid-container {{
            display: flex;
            gap: var(--space-tight);
            margin: var(--space-section) 0;
            justify-content: center;
        }}
        
        .icon-grid-item {{
            width: 40px;
            height: 40px;
            border-radius: var(--radius-card);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}
        
        /* Client Logos - Greyco Style */
        .client-logos-container {{
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-tight);
            margin-top: var(--space-element);
            justify-content: center;
        }}
        
        .client-logo-item {{
            background: rgba(255, 255, 255, 0.1);
            padding: var(--space-tight) var(--space-element);
            border-radius: var(--radius-card);
            font-size: 14px;
            font-weight: var(--weight-semi-bold);
            color: var(--text-secondary);
        }}
        
        .client-logo-item.highlighted {{
            background: var(--primary);
            color: #FFFFFF;
        }}
        
        /* Center Statement - Greyco Style */
        .template-content-statement .content-overlay {{
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        
        .center-statement-text {{
            max-width: 900px;
            text-align: center;
        }}
        
        .center-statement-text .element-heading {{
            font-size: var(--size-h1);
            font-weight: var(--weight-bold);
            line-height: 1.2;
            text-transform: none;
            letter-spacing: -0.01em;
        }}
        
        /* Contact Info - Greyco Style */
        .template-contact .content-overlay,
        .template-contact-info .content-overlay {{
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: var(--space-element) var(--space-page-h);
            gap: 4px;
        }}
        
        .template-contact .element-heading,
        .template-contact-info .element-heading {{
            margin-bottom: 0;
            font-size: 36px !important;
            line-height: 1.1;
        }}
        
        .template-contact .element-badge,
        .template-contact-info .element-badge {{
            margin-bottom: 0;
            font-size: 11px !important;
        }}
        
        .template-contact .element-logo,
        .template-contact-info .element-logo {{
            margin: 8px 0;
            font-size: 16px !important;
        }}
        
        .contact-info-list {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin: 8px 0;
            align-items: center;
        }}
        
        .contact-info-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: var(--text-secondary);
        }}
        
        .contact-info-icon {{
            font-size: 14px;
            width: 20px;
            text-align: center;
        }}
        
        .template-contact .element-body,
        .template-contact-info .element-body {{
            font-size: 12px !important;
            margin-top: 8px;
        }}
        
        /* Value Cards (Why E-UM) - Greyco Style */
        .value-cards-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: var(--space-element);
            width: 100%;
        }}
        
        .value-card {{
            background: var(--bg-card);
            border-radius: var(--radius-card);
            padding: 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 0;
        }}
        
        .value-card-icon {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        
        .value-card-title {{
            font-size: 14px;
            font-weight: var(--weight-bold);
            margin-bottom: 4px;
            color: var(--text-primary);
        }}
        
        .value-card-desc {{
            font-size: 11px;
            color: var(--text-secondary);
            line-height: 1.4;
        }}
        
        /* Image Overlay Layout - Greyco Style */
        .template-content-image .content-overlay {{
            justify-content: center;
            padding-left: 80px;
        }}

        /* Feature List - Greyco Style */
        .list-container {{
            margin-top: var(--space-element);
            display: flex;
            flex-direction: column;
            gap: var(--space-tight);
        }}
        
        .list-item {{
            display: flex;
            align-items: flex-start;
            background: rgba(255,255,255,0.05);
            padding: var(--space-tight) 20px;
            border-radius: 10px;
        }}
        
        .list-icon {{
            font-size: 20px;
            margin-right: var(--space-tight);
            flex-shrink: 0;
        }}
        
        .list-content {{
            flex: 1;
        }}
        
        .list-title {{
            font-weight: var(--weight-bold);
            font-size: 17px;
            margin-bottom: 4px;
            color: var(--text-primary);
        }}
        
        .list-desc {{
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.4;
        }}
        
        /* Content Features Template - Split Layout with Image */
        .template-content-features .content-overlay,
        .template-image-features .content-overlay {{
            display: grid;
            grid-template-columns: 2fr 3fr;
            gap: var(--space-section);
            align-items: center;
            padding: var(--space-page-v) var(--space-page-h);
            height: 100%;
        }}
        
        .template-content-features.image-right .content-overlay,
        .template-image-features.image-right .content-overlay {{
            grid-template-columns: 3fr 2fr;
        }}
        
        .template-content-features .content-left,
        .template-image-features .content-left {{
            display: flex;
            flex-direction: column;
            gap: var(--space-element);
            height: 100%;
            justify-content: center;
        }}
        
        .template-content-features .content-right,
        .template-image-features .content-right {{
            display: flex;
            flex-direction: column;
            gap: var(--space-element);
            height: 100%;
            justify-content: center;
        }}
        
        .template-content-features .element-image,
        .template-image-features .element-image {{
            width: 100%;
            height: auto;
            max-height: 400px;
            object-fit: cover;
            border-radius: var(--radius-card);
        }}

        /* Cards Container */
        .cards-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            width: 100%;
            margin-top: var(--space-section);
        }}
        
        .cards-container.service-cards {{
            grid-template-columns: repeat(5, 1fr);
        }}
        
        .cards-container.value-cards {{
            grid-template-columns: repeat(3, 1fr);
        }}

        /* Card Styles */
        .card {{
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: var(--radius-card);
            padding: var(--space-element);
            display: flex;
            flex-direction: column;
        }}
        
        .card-icon {{
            font-size: 32px;
            margin-bottom: var(--space-tight);
        }}
        
        .card-title {{
            font-size: 18px;
            font-weight: var(--weight-bold);
            margin-bottom: var(--space-xs);
            color: var(--primary);
        }}
        
        .card-subtitle {{
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: var(--space-xs);
        }}
        
        .card-value {{
            font-size: 15px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}
        
        /* Client Grid */
        .clients-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: var(--space-tight);
        }}
        
        .client-item {{
            background: white;
            color: #333;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: var(--weight-bold);
            font-size: 14px;
        }}
        
        .client-item.highlight {{
            background: var(--primary);
            color: white;
        }}

        /* Print Optimization */
        @media print {{
            @page {{
                size: 297mm 167mm;
                margin: 0;
            }}
            html, body {{
                margin: 0 !important;
                padding: 0 !important;
                background: white !important;
            }}
            .slide {{
                margin: 0 !important;
                box-shadow: none !important;
                page-break-inside: avoid !important;
            }}
        }}
    </style>
</head>
<body>
"""

    for i, slide in enumerate(slides):
        is_last = (i == len(slides) - 1)
        slide_class = "slide last-slide" if is_last else "slide"
        
        # Determine Layout Type
        layout_config = slide.get('layout', {})
        template = slide.get('type', 'content-text')
        if isinstance(layout_config, dict):
            template = layout_config.get('template', template)
        
        # Check imagePosition for split layouts
        image_position = ""
        if isinstance(layout_config, dict):
            image_position = layout_config.get('imagePosition', 'right')
        
        # Map templates to layout classes
        layout_class = ""
        split_templates = ['hero-cover', 'content-split', 'service-detail', 'content-profile']
        center_templates = ['center-statement', 'contact-info', 'vision-mission', 'content-statement', 'contact']
        features_templates = ['content-features', 'image-features']
        
        if template in split_templates:
            layout_class = "layout-split"
            if image_position == 'left':
                layout_class += " image-left"
        elif template in center_templates:
            layout_class = "layout-center"
        elif template in features_templates:
            if image_position == 'right':
                layout_class = "image-right"
        
        # Add alignment class for section-divider
        alignment = ""
        if template == 'section-divider':
            alignment_config = layout_config.get('alignment', 'center-left') if isinstance(layout_config, dict) else 'center-left'
            if 'right' in alignment_config:
                alignment = "align-right"
            elif 'center' in alignment_config and 'left' not in alignment_config:
                alignment = "align-center"
            else:
                alignment = "align-left"
        
        # Handle slide background
        bg_style = ""
        bg_html = ""
        background = slide.get('background', {})
        if background.get('type') == 'solid':
            bg_style = f"background-color: {background.get('color', bg_dark)};"
        elif background.get('type') == 'gradient':
            grad_colors = background.get('colors', [bg_dark, bg_card])
            if grad_colors:
                bg_style = f"background: linear-gradient(135deg, {', '.join(grad_colors)});"
        elif background.get('type') == 'image-overlay':
            bg_image = background.get('image', '')
            bg_opacity = background.get('imageOpacity', 0.4)
            overlay_color = background.get('overlayColor', 'rgba(0, 0, 0, 0.7)')
            bg_html = f'<img src="{bg_image}" class="bg-image" style="opacity: {bg_opacity};" alt="">'
            bg_html += f'<div class="bg-overlay" style="background: {overlay_color};"></div>'
            bg_style = f"background-color: {bg_dark};"
        else:
            bg_style = f"background-color: {bg_dark};"
        
        html_content += f'<div class="{slide_class} {layout_class} {alignment} template-{template}" id="slide-{slide.get("slideNumber", i+1)}" style="{bg_style}">'
        
        # Add background image overlay if present
        if bg_html:
            html_content += bg_html
        
        elements = slide.get('elements', [])
        
        # Handle content-features template specially
        if template in features_templates:
            html_content += '<div class="content-overlay">'
            
            # Separate image elements from text elements
            image_elements = [el for el in elements if el.get('type') == 'image']
            text_elements = [el for el in elements if el.get('type') != 'image']
            
            if image_position == 'left':
                # Image on left, text on right
                html_content += '<div class="content-left">'
                for el in image_elements:
                    html_content += render_element(el, primary_color, secondary_color)
                html_content += '</div>'
                html_content += '<div class="content-right">'
                for el in text_elements:
                    html_content += render_element(el, primary_color, secondary_color)
                html_content += '</div>'
            else:
                # Text on left, image on right
                html_content += '<div class="content-left">'
                for el in text_elements:
                    html_content += render_element(el, primary_color, secondary_color)
                html_content += '</div>'
                html_content += '<div class="content-right">'
                for el in image_elements:
                    html_content += render_element(el, primary_color, secondary_color)
                html_content += '</div>'
            
            html_content += '</div>'
        
        # Handle split layouts
        elif "layout-split" in layout_class:
            # Separate elements for split layout
            left_elements = []
            right_elements = []
            
            if "image-left" in layout_class:
                # Image goes to left, everything else to right
                for el in elements:
                    if el.get('type') == 'image' and el.get('position') != 'right':
                        left_elements.append(el)
                    else:
                        right_elements.append(el)
            else:
                # Text goes to left, image to right
                for el in elements:
                    if el.get('position') == 'right' or (el.get('type') == 'image' and el.get('position') != 'left'):
                        right_elements.append(el)
                    else:
                        left_elements.append(el)
            
            html_content += '<div class="content-overlay">'
            
            # Left Column
            html_content += '<div class="col-left">'
            for el in left_elements:
                html_content += render_element(el, primary_color, secondary_color)
            html_content += '</div>'
            
            # Right Column
            html_content += '<div class="col-right">'
            for el in right_elements:
                html_content += render_element(el, primary_color, secondary_color)
            html_content += '</div>'
            
            html_content += '</div>'
            
        else:
            # Standard Layout
            html_content += '<div class="content-overlay">'
            for el in elements:
                # For contact-info template, limit font sizes to avoid overflow
                if template == 'contact-info':
                    el_copy = el.copy()
                    if 'style' in el_copy:
                        style_copy = el_copy['style'].copy()
                        el_type = el_copy.get('type', '')
                        if el_type == 'heading':
                            style_copy['fontSize'] = '36px'
                        elif el_type == 'badge':
                            style_copy['fontSize'] = '12px'
                        elif el_type in ['company-name', 'logo']:
                            style_copy['fontSize'] = '16px'
                        elif el_type in ['body', 'tagline']:
                            style_copy['fontSize'] = '12px'
                        el_copy['style'] = style_copy
                    html_content += render_element(el_copy, primary_color, secondary_color)
                else:
                    html_content += render_element(el, primary_color, secondary_color)
            html_content += '</div>'

        html_content += '</div>'
        
        if not is_last:
            html_content += '<!-- Slide -->'

    html_content += """</body></html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {html_path}")


def render_element(el, primary_color='#FF6B35', secondary_color='#FFB800'):
    el_type = el.get('type', 'body')
    style_obj = el.get('style', {})
    
    # Convert style dict to string
    style_str = ""
    for k, v in style_obj.items():
        kebab = ''.join(['-' + c.lower() if c.isupper() else c for c in k]).lstrip('-')
        # Skip positioning styles that might conflict with grid
        if kebab in ['position', 'top', 'left', 'right', 'bottom', 'transform']:
            continue
        style_str += f"{kebab}: {v}; "
    
    content = ""
    
    # Text elements
    if el_type == 'heading':
        text = el.get('text', '')
        content = f'<div class="element-heading" style="{style_str}">{text}</div>'
    
    elif el_type == 'subheading':
        text = el.get('text', '')
        content = f'<div class="element-subheading" style="{style_str}">{text}</div>'
    
    elif el_type == 'badge':
        text = el.get('text', '')
        content = f'<div class="element-badge" style="{style_str}">{text}</div>'
    
    elif el_type == 'logo':
        text = el.get('text', '')
        content = f'<div class="element-logo" style="{style_str}">{text}</div>'
    
    elif el_type in ['body', 'tagline']:
        text = el.get('text', '')
        content = f'<div class="element-body" style="{style_str}">{text}</div>'
    
    elif el_type == 'quote':
        text = el.get('text', '')
        content = f'<div class="element-quote" style="{style_str}">{text}</div>'
    
    elif el_type == 'company-name':
        text = el.get('text', '')
        content = f'<div class="element-logo" style="font-size: 28px; {style_str}">{text}</div>'
    
    elif el_type == 'image':
        src = el.get('src', '')
        alt = el.get('alt', '')
        content = f'<img src="{src}" alt="{alt}" class="element-image" style="{style_str}">'
    
    # Card-based elements
    elif el_type in ['info-cards', 'philosophy-cards', 'service-cards', 'value-cards']:
        items = el.get('items', [])
        content += f'<div class="cards-container {el_type}">'
        for item in items:
            title = item.get('title', '') or item.get('label', '')
            value = item.get('value', '') or item.get('description', '')
            subtitle = item.get('subtitle', '')
            icon = item.get('icon', '')
            color = item.get('color', primary_color)
            
            content += f'<div class="card">'
            if icon:
                icon_char = get_icon(icon)
                content += f'<div class="card-icon">{icon_char}</div>'
            if title:
                content += f'<div class="card-title" style="color: {color};">{title}</div>'
            if subtitle:
                content += f'<div class="card-subtitle">{subtitle}</div>'
            if value:
                content += f'<div class="card-value">{value}</div>'
            content += '</div>'
        content += '</div>'

    # Timeline
    elif el_type == 'timeline':
        periods = el.get('periods', [])
        content += '<div class="timeline-container">'
        for p in periods:
            # Support both 'year' and 'label' keys
            year = p.get('label', '') or p.get('year', '')
            milestone = p.get('milestone', '')
            color = p.get('barColor', primary_color)
            highlight = p.get('highlight', False)
            highlight_style = f"background: {color}; color: white; padding: 4px 8px; border-radius: 4px;" if highlight else ""
            content += f'<div class="timeline-item" style="border-top: 4px solid {color};">'
            content += f'<div class="timeline-year" style="color: {color}; {highlight_style}">{year}</div>'
            content += f'<div class="timeline-milestone">{milestone}</div>'
            content += '</div>'
        content += '</div>'
    
    # Feature/Service/Capability lists
    elif el_type in ['feature-list', 'service-list', 'capability-list']:
        items = el.get('items', [])
        content += '<div class="list-container">'
        for item in items:
            title = item.get('title', '')
            desc = item.get('description', '')
            icon = item.get('icon', '')
            icon_char = get_icon(icon) if icon else '●'
            content += f'<div class="list-item">'
            content += f'<span class="list-icon">{icon_char}</span>'
            content += f'<div class="list-content">'
            content += f'<div class="list-title">{title}</div>'
            content += f'<div class="list-desc">{desc}</div>'
            content += '</div></div>'
        content += '</div>'
    
    # Client sections
    elif el_type in ['client-section', 'client-highlight']:
        title = el.get('title', '')
        clients = el.get('clients', [])
        if title:
            content += f'<div class="section-title">{title}</div>'
        
        content += '<div class="clients-grid">'
        for client in clients:
            if isinstance(client, dict):
                name = client.get('name', '')
                highlight = client.get('highlight', False)
                cls = 'client-item highlight' if highlight else 'client-item'
            else:
                name = client
                cls = 'client-item'
            content += f'<div class="{cls}">{name}</div>'
        content += '</div>'

    # Contact section
    elif el_type == 'contact-section':
        title = el.get('title', '')
        items = el.get('items', [])
        content += f'<div class="contact-section">'
        if title:
            content += f'<div class="contact-title">{title}</div>'
        for item in items:
            val = item.get('value', '')
            itype = item.get('type', '')
            icon = item.get('icon', itype)
            icon_char = get_icon(icon) if icon else ''
            content += f'<div class="contact-item">'
            content += f'<span class="contact-label">{itype.upper()}</span>'
            if icon_char:
                content += f'<span style="margin-right: 8px;">{icon_char}</span>'
            content += f'{val}</div>'
        content += '</div>'
    
    # Highlight box
    elif el_type == 'highlight-box':
        title = el.get('title', '')
        content_text = el.get('content', '')
        content += f'<div class="highlight-box">'
        if title:
            content += f'<div class="box-title">{title}</div>'
        content += f'<div class="box-content">{content_text}</div>'
        content += '</div>'

    # Image grid
    elif el_type == 'image-grid':
        images = el.get('images', [])
        content += '<div class="image-grid">'
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt', '')
            content += f'<div class="grid-image-wrapper">'
            content += f'<img src="{src}" alt="{alt}">'
            content += '</div>'
        content += '</div>'
    
    # Process flow
    elif el_type == 'process-flow':
        title = el.get('title', '')
        steps = el.get('steps', [])
        if title:
            content += f'<div class="section-title">{title}</div>'
        content += '<div class="process-flow">'
        for step in steps:
            num = step.get('step', '')
            step_title = step.get('title', '')
            desc = step.get('description', '')
            content += f'<div class="process-step">'
            content += f'<div class="process-number">{num}</div>'
            content += f'<div class="process-title">{step_title}</div>'
            content += f'<div class="process-desc">{desc}</div>'
            content += '</div>'
        content += '</div>'
    
    # Facility info
    elif el_type == 'facility-info':
        items = el.get('items', [])
        content += '<div class="facility-info">'
        for item in items:
            label = item.get('label', '')
            value = item.get('value', '')
            content += f'<div class="facility-item">'
            content += f'<div class="facility-label">{label}</div>'
            content += f'<div class="facility-value">{value}</div>'
            content += '</div>'
        content += '</div>'
    
    # Feature grid
    elif el_type == 'feature-grid':
        items = el.get('items', [])
        content += '<div class="feature-grid">'
        for item in items:
            icon = item.get('icon', '')
            title = item.get('title', '')
            desc = item.get('description', '')
            icon_char = get_icon(icon) if icon else '●'
            content += f'<div class="feature-item">'
            content += f'<div class="feature-icon">{icon_char}</div>'
            content += f'<div class="feature-title">{title}</div>'
            content += f'<div class="feature-desc">{desc}</div>'
            content += '</div>'
        content += '</div>'
    
    # Network regions
    elif el_type == 'network-regions':
        items = el.get('items', [])
        content += '<div class="network-regions">'
        for item in items:
            region = item.get('region', '')
            countries = item.get('countries', [])
            icon = item.get('icon', '')
            icon_char = get_icon(icon) if icon else '🌐'
            content += f'<div class="region-card">'
            content += f'<div class="region-icon">{icon_char}</div>'
            content += f'<div class="region-name">{region}</div>'
            content += f'<div class="region-countries">{", ".join(countries)}</div>'
            content += '</div>'
        content += '</div>'
    
    # Image gallery
    elif el_type == 'image-gallery':
        images = el.get('images', [])
        content += '<div class="image-grid">'
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt', '')
            caption = img.get('caption', '')
            content += f'<div class="grid-image-wrapper">'
            content += f'<img src="{src}" alt="{alt}">'
            if caption:
                content += f'<div style="text-align: center; margin-top: 8px; font-size: 12px; color: #888;">{caption}</div>'
            content += '</div>'
        content += '</div>'
    
    # TOC Item (Table of Contents)
    elif el_type == 'toc-item':
        items = el.get('items', [])
        content += '<div class="toc-container">'
        for item in items:
            num = item.get('number', '')
            title = item.get('title', '')
            num_color = item.get('numberColor', primary_color)
            title_color = item.get('titleColor', '#FFFFFF')
            content += f'<div class="toc-item">'
            content += f'<span class="toc-number" style="color: {num_color};">{num}</span>'
            content += f'<span class="toc-title" style="color: {title_color};">{title}</span>'
            content += '</div>'
        content += '</div>'
    
    # Stat Block
    elif el_type == 'stat-block':
        items = el.get('items', [])
        content += '<div class="stats-container">'
        for item in items:
            value = item.get('value', '')
            unit = item.get('unit', '')
            label = item.get('label', '')
            value_color = item.get('valueColor', '#FFFFFF')
            value_size = item.get('valueSize', '64px')
            content += f'<div class="stat-item">'
            content += f'<div class="stat-value" style="color: {value_color}; font-size: {value_size};">{value}<span class="stat-unit">{unit}</span></div>'
            content += f'<div class="stat-label">{label}</div>'
            content += '</div>'
        content += '</div>'
    
    # Chart (Horizontal Bar)
    elif el_type == 'chart':
        chart_type = el.get('chartType', 'horizontal-bar')
        title = el.get('title', '')
        data = el.get('data', [])
        content += '<div class="chart-container">'
        if title:
            content += f'<div class="chart-title">{title}</div>'
        for item in data:
            label = item.get('label', '')
            value = item.get('value', 0)
            color = item.get('color', primary_color)
            content += f'<div class="chart-bar-item">'
            content += f'<div class="chart-bar-label">{label} ({value}%)</div>'
            content += f'<div class="chart-bar-wrapper">'
            content += f'<div class="chart-bar" style="width: {value}%; background: {color};"></div>'
            content += '</div></div>'
        content += '</div>'
    
    # Model Cards (Business Model)
    elif el_type == 'model-cards':
        items = el.get('items', [])
        content += '<div class="model-cards-container">'
        for item in items:
            icon = item.get('icon', 'circle')
            icon_color = item.get('iconColor', primary_color)
            title = item.get('title', '')
            desc = item.get('description', '')
            icon_char = get_icon(icon)
            content += f'<div class="model-card">'
            content += f'<div class="model-card-icon" style="color: {icon_color};">{icon_char}</div>'
            content += f'<div class="model-card-title">{title}</div>'
            content += f'<div class="model-card-desc">{desc}</div>'
            content += '</div>'
        content += '</div>'
    
    # Comparison Table
    elif el_type == 'comparison-table':
        headers = el.get('headers', [])
        rows = el.get('rows', [])
        highlight_color = el.get('highlightColor', primary_color)
        content += '<table class="comparison-table">'
        # Header row
        content += '<thead><tr>'
        for h in headers:
            content += f'<th>{h}</th>'
        content += '</tr></thead>'
        # Body rows
        content += '<tbody>'
        for row in rows:
            company = row.get('company', '')
            values = row.get('values', [])
            is_highlight = row.get('isHighlight', False)
            row_class = 'highlight' if is_highlight else ''
            content += f'<tr class="{row_class}">'
            content += f'<td>{company}</td>'
            for v in values:
                if v == 'check':
                    content += '<td class="check">✓</td>'
                elif v == 'highlight':
                    content += f'<td class="highlight-check">✓</td>'
                else:
                    content += f'<td>{v}</td>'
            content += '</tr>'
        content += '</tbody></table>'
    
    # Icon Grid (6 out of 10)
    elif el_type == 'icon-grid':
        total = el.get('total', 10)
        highlighted = el.get('highlighted', 6)
        highlight_color = el.get('highlightColor', primary_color)
        default_color = el.get('defaultColor', '#4A4A4A')
        content += '<div class="icon-grid-container">'
        for i in range(total):
            color = highlight_color if i < highlighted else default_color
            content += f'<div class="icon-grid-item" style="background: {color};">●</div>'
        content += '</div>'
    
    # Client Logos
    elif el_type == 'client-logos':
        clients = el.get('clients', [])
        content += '<div class="client-logos-container">'
        for client in clients:
            name = client.get('name', '')
            is_highlight = client.get('highlight', False)
            cls = 'client-logo-item highlighted' if is_highlight else 'client-logo-item'
            content += f'<div class="{cls}">{name}</div>'
        content += '</div>'
    
    # Contact Info (list style)
    elif el_type == 'contact-info':
        items = el.get('items', [])
        content += '<div class="contact-info-list">'
        for item in items:
            itype = item.get('type', '')
            value = item.get('value', '')
            icon = get_icon(itype) if itype else ''
            content += f'<div class="contact-info-item">'
            content += f'<span class="contact-info-icon">{icon}</span>'
            content += f'<span>{value}</span>'
            content += '</div>'
        content += '</div>'
    
    # Label
    elif el_type == 'label':
        text = el.get('text', '')
        content = f'<div class="element-body" style="font-style: italic; {style_str}">{text}</div>'
    
    # Logo placeholder
    elif el_type == 'logo-placeholder':
        text = el.get('text', '')
        content = f'<div style="margin-top: 32px; font-size: 14px; color: {primary_color}; {style_str}">{text}</div>'

    return content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_html.py [project_name]")
    else:
        generate_html(sys.argv[1])
