#!/usr/bin/env python3
"""
HTML → JSON 역변환 스크립트

HTML 파일을 파싱하여 presentation.json 형식으로 변환합니다.
HTML을 수정한 후 JSON을 업데이트하여 PPTX 생성 시 최신 상태를 반영합니다.

Usage:
    python scripts/html_to_json.py projects/[project-name]/presentation.html
    python scripts/html_to_json.py projects/eumlogistic/presentation.html
"""

import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment


def extract_css_variables(soup):
    """CSS :root 변수를 추출하여 designTokens 생성"""
    style_tag = soup.find('style')
    if not style_tag:
        return {}
    
    css_text = style_tag.string
    root_match = re.search(r':root\s*\{([^}]+)\}', css_text, re.DOTALL)
    
    if not root_match:
        return {}
    
    tokens = {}
    root_content = root_match.group(1)
    
    # CSS 변수 파싱
    for line in root_content.split(';'):
        line = line.strip()
        if not line or ':' not in line:
            continue
        
        var_name, var_value = line.split(':', 1)
        var_name = var_name.strip().lstrip('--')
        var_value = var_value.strip()
        
        # 카테고리별 분류
        if var_name.startswith('gradient-'):
            category = 'gradients'
            key = var_name.replace('gradient-', '')
        elif var_name.startswith('shadow-'):
            category = 'shadows'
            key = var_name.replace('shadow-', '')
        elif var_name.startswith('radius'):
            category = 'radius'
            key = var_name.replace('radius-', '') if '-' in var_name else 'default'
        elif 'background' in var_name:
            category = 'backgrounds'
            key = var_name
        elif 'text' in var_name or var_name in ['primary', 'secondary', 'accent', 'highlight', 'success']:
            category = 'colors'
            key = var_name
        else:
            category = 'colors'
            key = var_name
        
        if category not in tokens:
            tokens[category] = {}
        tokens[category][key] = var_value
    
    return tokens


def extract_slide_content(slide_div):
    """슬라이드 div에서 콘텐츠 추출"""
    content = {
        'texts': [],
        'images': [],
        'layout': 'unknown'
    }
    
    # 텍스트 추출 (h1, h2, h3, p, span 등)
    for tag in slide_div.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'span', 'div']):
        text = tag.get_text(strip=True)
        if not text or len(text) < 2:
            continue
        
        # 중복 제거 (부모-자식 관계)
        if any(existing['text'] == text for existing in content['texts']):
            continue
        
        # 클래스로 타입 추정
        classes = tag.get('class', [])
        text_type = 'body'
        
        if tag.name == 'h1' or 'h1' in classes:
            text_type = 'heading'
        elif tag.name == 'h2' or 'h2' in classes:
            text_type = 'subheading'
        elif tag.name == 'h3' or 'h3' in classes:
            text_type = 'title'
        elif 'label' in classes:
            text_type = 'label'
        elif 'caption' in classes:
            text_type = 'caption'
        
        # 스타일 정보 추출
        style = tag.get('style', '')
        font_size = re.search(r'font-size:\s*(\d+)px', style)
        color = re.search(r'color:\s*([^;]+)', style)
        
        content['texts'].append({
            'text': text,
            'type': text_type,
            'fontSize': font_size.group(1) + 'px' if font_size else None,
            'color': color.group(1).strip() if color else None
        })
    
    # 이미지 추출
    for img in slide_div.find_all('img'):
        src = img.get('src', '')
        alt = img.get('alt', '')
        
        if src:
            content['images'].append({
                'src': src,
                'alt': alt
            })
    
    # 레이아웃 추정
    classes = slide_div.get('class', [])
    if 'slide-dark' in classes:
        if any('hero' in str(c).lower() for c in slide_div.find_all()):
            content['layout'] = 'hero-cover'
        else:
            content['layout'] = 'content-text'
    elif 'slide-light' in classes:
        content['layout'] = 'content-text'
    elif 'slide-alt' in classes:
        content['layout'] = 'content-text'
    elif 'slide-primary' in classes:
        content['layout'] = 'section-divider'
    
    return content


def html_to_json(html_path):
    """HTML 파일을 JSON 구조로 변환"""
    
    html_path = Path(html_path)
    if not html_path.exists():
        raise FileNotFoundError(f"HTML 파일을 찾을 수 없습니다: {html_path}")
    
    # HTML 파싱
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    
    # 메타데이터
    title = soup.find('title')
    project_name = title.string if title else html_path.stem
    
    # Design Tokens 추출
    design_tokens = extract_css_variables(soup)
    
    # 슬라이드 추출
    slides = []
    slide_divs = soup.find_all('div', class_='slide')
    
    for idx, slide_div in enumerate(slide_divs, 1):
        slide_content = extract_slide_content(slide_div)
        
        # 슬라이드 제목 추출 (첫 번째 heading 또는 h2)
        title_elem = slide_div.find(['h1', 'h2'])
        slide_title = title_elem.get_text(strip=True) if title_elem else f"Slide {idx}"
        
        slides.append({
            'id': idx,
            'title': slide_title,
            'template': slide_content['layout'],
            'content': {
                'texts': slide_content['texts'],
                'images': slide_content['images']
            }
        })
    
    # JSON 구조 생성
    json_data = {
        'projectName': project_name,
        'version': '1.0',
        'lastModified': '2025-01-01',  # 현재 날짜로 업데이트 가능
        'designTokens': design_tokens,
        'slides': slides
    }
    
    return json_data


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/html_to_json.py projects/[project-name]/presentation.html")
        sys.exit(1)
    
    html_path = Path(sys.argv[1])
    
    if not html_path.exists():
        print(f"❌ 오류: HTML 파일을 찾을 수 없습니다: {html_path}")
        sys.exit(1)
    
    print(f"🔍 HTML 파일 파싱 중: {html_path}")
    
    try:
        # HTML → JSON 변환
        json_data = html_to_json(html_path)
        
        # JSON 파일 저장 (같은 디렉토리에 presentation.json)
        json_path = html_path.parent / 'presentation.json'
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 변환 완료: {json_path}")
        print(f"📊 총 {len(json_data['slides'])}개 슬라이드 추출됨")
        
        # 슬라이드별 텍스트 요약
        for slide in json_data['slides']:
            text_count = len(slide['content']['texts'])
            image_count = len(slide['content']['images'])
            print(f"   - {slide['title']}: {text_count}개 텍스트, {image_count}개 이미지")
        
        print("\n💡 다음 단계:")
        print(f"   /pptx {html_path.parent.name}")
        
    except Exception as e:
        print(f"❌ 변환 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
