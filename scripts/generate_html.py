import json
import os
import sys

def generate_html(project_name):
    project_dir = os.path.join("projects", project_name)
    json_path = os.path.join(project_dir, "presentation.json")
    html_path = os.path.join(project_dir, "presentation.html")

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides = data.get("slides", [])
    design_tokens = data.get("designTokens", {})

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('projectName', 'Presentation')}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;700;900&family=Roboto:wght@100;300;400;500;700;900&display=swap');

        body {{
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            font-family: 'Noto Sans KR', sans-serif;
        }}

        .slide {{
            position: relative;
            width: 1280px;
            height: 720px;
            background-color: white;
            overflow: hidden;
            margin: 0 auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            page-break-after: always;
            break-after: page;
        }}

        .slide * {{
            box-sizing: border-box;
        }}

        @media print {{
            @page {{
                size: 297mm 167mm;
                margin: 0;
            }}

            html, body {{
                margin: 0 !important;
                padding: 0 !important;
                background: white !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}

            .slide {{
                width: 297mm !important;
                height: 167mm !important;
                max-height: 167mm !important;
                min-height: 167mm !important;
                box-shadow: none !important;
                margin: 0 !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                overflow: hidden !important;
            }}

            .slide:not(.last-slide) {{
                page-break-after: always !important;
                break-after: page !important;
            }}

            .last-slide {{
                page-break-after: avoid !important;
                break-after: avoid !important;
            }}
        }}
    </style>
</head>
<body>
"""

    for i, slide in enumerate(slides):
        is_last = (i == len(slides) - 1)
        slide_class = "slide last-slide" if is_last else "slide"
        
        bg_style = ""
        if "background" in slide:
            bg = slide["background"]
            if bg["type"] == "solid":
                bg_style = f"background-color: {bg['value']};"
            elif bg["type"] == "gradient":
                bg_style = f"background: {bg['value']};"
            elif bg["type"] == "image":
                bg_style = f"background-image: url('{bg['value']}'); background-size: cover; background-position: center;"

        html_content += f'<div class="{slide_class}" style="{bg_style}">\n'
        
        for element in slide.get("elements", []):
            html_content += render_element(element)
            
        html_content += '</div>'
        
        # Add comment to separate slides but NO whitespace for print safety
        if not is_last:
            html_content += '<!-- Slide -->\n'

    html_content += """
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Successfully generated {html_path}")

def render_element(element):
    el_type = element.get("type", "text")
    content = element.get("content", "")
    style = element.get("style", {})
    children = element.get("children", [])
    
    style_str = "; ".join([f"{k.replace('_', '-')}: {v}" for k, v in style.items()])
    
    # Convert camelCase keys to kebab-case for CSS
    css_style = ""
    for k, v in style.items():
        kebab_key = ''.join(['-' + i.lower() if i.isupper() else i for i in k]).lstrip('-')
        # Handle numeric values that might need px
        if isinstance(v, (int, float)) and kebab_key not in ["opacity", "z-index", "line-height", "font-weight", "flex-grow", "flex-shrink"]:
             v = f"{v}px"
        css_style += f"{kebab_key}: {v}; "

    if el_type == "text":
        # Handle newlines in text content
        content = str(content).replace("\n", "<br>")
        return f'<div style="{css_style}">{content}</div>\n'
    
    elif el_type == "heading":
        level = element.get("level", 1)
        tag = f"h{level}"
        # Reset default margins for headings as they are usually positioned absolutely or controlled via flex
        css_style += "margin: 0;" 
        return f'<{tag} style="{css_style}">{content}</{tag}>\n'
    
    elif el_type == "image":
        src = element.get("src", "") or content
        alt = element.get("alt", "image")
        return f'<img src="{src}" alt="{alt}" style="{css_style}">\n'
        
    elif el_type == "container" or el_type == "card":
        inner_html = ""
        for child in children:
            inner_html += render_element(child)
        return f'<div style="{css_style}">\n{inner_html}</div>\n'
        
    elif el_type == "badge":
        return f'<span style="{css_style}">{content}</span>\n'
        
    elif el_type == "decorative":
        return f'<div style="{css_style}"></div>\n'

    else:
        # Fallback for unknown types
        return f'<div style="{css_style}">{content}</div>\n'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_html.py [project_name]")
    else:
        generate_html(sys.argv[1])
