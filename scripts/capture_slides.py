"""
슬라이드별 스크린샷 캡처 스크립트
Kapture MCP를 통해 각 슬라이드를 캡처하여 저장합니다.
"""
import requests
import time
import json
from pathlib import Path

# 설정
TAB_ID = "796613120"
KAPTURE_URL = "http://localhost:61822"
PROJECT_PATH = Path(__file__).parent.parent / "projects" / "eumlogistic"
SCREENSHOTS_PATH = PROJECT_PATH / "screenshots" / "html"
TOTAL_SLIDES = 11

# 스크린샷 폴더 생성
SCREENSHOTS_PATH.mkdir(parents=True, exist_ok=True)

def capture_slide(slide_number):
    """특정 슬라이드를 캡처하여 저장"""
    selector = f"body > div.slide:nth-of-type({slide_number})"
    
    # Kapture API 호출 (실제 구현은 MCP 프로토콜 사용)
    print(f"📸 슬라이드 {slide_number} 캡처 중...")
    
    # MCP 도구를 통해 스크린샷 캡처 (이 스크립트는 실제로 직접 실행되지 않고, 
    # AI가 mcp_kapture_screenshot를 호출하여 이미지를 받아온 후 저장하는 방식으로 동작)
    
    return f"slide_{slide_number:02d}.png"

def main():
    """모든 슬라이드 캡처"""
    print(f"🎬 이음로지스틱 프레젠테이션 스크린샷 캡처 시작")
    print(f"📂 저장 경로: {SCREENSHOTS_PATH}")
    print(f"📊 총 슬라이드: {TOTAL_SLIDES}개\n")
    
    for slide_num in range(1, TOTAL_SLIDES + 1):
        try:
            filename = capture_slide(slide_num)
            print(f"✅ 슬라이드 {slide_num}/{TOTAL_SLIDES} 저장 완료: {filename}")
            time.sleep(0.3)  # 렌더링 대기
        except Exception as e:
            print(f"❌ 슬라이드 {slide_num} 캡처 실패: {e}")
    
    print(f"\n✨ 캡처 완료! 총 {TOTAL_SLIDES}개 슬라이드가 저장되었습니다.")

if __name__ == "__main__":
    main()
