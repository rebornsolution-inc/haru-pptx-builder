# MCP 도구 사용 가이드

**날짜:** 2025-11-10  
**업데이트:** 통합 정리 완료  
**목적:** Kapture MCP 사용법 가이드

---

## ⚠️ CRITICAL: 올바른 MCP 도구 사용

### 이 프로젝트에서 사용할 MCP

✅ **Kapture MCP** - 유일한 공식 도구

**사용하지 않는 도구:**
- ❌ Microsoft Playwright MCP
- ❌ Generic Browser MCP

**이유:**
- 일관성 유지
- AI 혼란 방지
- 단일 도구 마스터
- 직관적인 DOM 접근

---

## Kapture MCP 주요 도구

### 탐색 기본
```javascript
// 1. 탭 목록 가져오기
const tabs = await mcp_kapture_list_tabs();
const tabId = tabs[0].id;

// 2. 탭 상세 정보
await mcp_kapture_tab_detail({ tabId });

// 3. 탭 활성화 (포커스)
await mcp_kapture_show({ tabId });
```

### DOM 분석
```javascript
// 1. 전체 DOM 가져오기
await mcp_kapture_dom({ tabId });

// 2. 특정 요소의 DOM
await mcp_kapture_dom({ tabId, selector: ".hero-section" });

// 3. XPath로 DOM 가져오기
await mcp_kapture_dom({ tabId, xpath: "//div[@class='hero']" });
```

### 요소 탐색
```javascript
// 1. 보이는 모든 요소
await mcp_kapture_elements({ tabId, visible: "true" });

// 2. 특정 셀렉터의 요소들
await mcp_kapture_elements({ tabId, selector: "button" });

// 3. 숨겨진 요소만
await mcp_kapture_elements({ tabId, visible: "false" });

// 4. 모든 요소 (보이는 것 + 숨겨진 것)
await mcp_kapture_elements({ tabId, visible: "all" });
```

### 인터랙션
```javascript
// 1. 호버
await mcp_kapture_hover({ tabId, selector: ".card" });

// 2. 클릭
await mcp_kapture_click({ tabId, selector: "button.submit" });

// 3. 포커스
await mcp_kapture_focus({ tabId, selector: "input[name='email']" });

// 4. 블러 (포커스 해제)
await mcp_kapture_blur({ tabId, selector: "input" });

// 5. 입력
await mcp_kapture_fill({ tabId, selector: "input", value: "test@example.com" });

// 6. 선택 (select 요소)
await mcp_kapture_select({ tabId, selector: "select", value: "option1" });

// 7. 키 입력
await mcp_kapture_keypress({ tabId, key: "Enter" });
await mcp_kapture_keypress({ tabId, key: "Control+a" }); // 조합키
```

### 네비게이션
```javascript
// 1. URL로 이동
await mcp_kapture_navigate({ tabId, url: "https://example.com" });

// 2. 뒤로 가기
await mcp_kapture_back({ tabId });

// 3. 앞으로 가기
await mcp_kapture_forward({ tabId });

// 4. 새로고침
await mcp_kapture_reload({ tabId });
```

### 좌표 기반
```javascript
// 특정 좌표의 모든 요소
await mcp_kapture_elementsFromPoint({ tabId, x: 500, y: 300 });
```

### 스크린샷
```javascript
// 1. 전체 페이지
await mcp_kapture_screenshot({ tabId });

// 2. 특정 요소만
await mcp_kapture_screenshot({ tabId, selector: ".hero" });

// 3. 옵션 지정
await mcp_kapture_screenshot({
  tabId,
  format: "webp",
  quality: 0.7,
  scale: 0.3
});
```

### 브라우저 제어
```javascript
// 1. 윈도우 크기 조절
await mcp_kapture_resize({ tabId, width: 375, height: 812 });

// 2. 새 탭 열기
await mcp_kapture_new_tab({ browser: "chrome" });

// 3. 탭 닫기
await mcp_kapture_close({ tabId });
```

### 고급
```javascript
// 1. Accessibility Snapshot
await mcp_kapture_snapshot({ tabId });

// 2. Console 로그 가져오기
await mcp_kapture_console_logs({ tabId, level: "error", limit: 50 });

// 3. 키보드 입력 (스크롤용)
await mcp_kapture_keypress({ tabId, key: "ArrowDown" }); // 작은 스크롤
await mcp_kapture_keypress({ tabId, key: "PageDown" });  // 큰 스크롤
```

**⚠️ 참고:** `mcp_kapture_evaluate()` (JavaScript 실행)는 Kapture MCP에서 지원하지 않습니다.

---

## 실전 예제

### 예제 1: 페이지 로드 후 분석
```javascript
const tabs = await mcp_kapture_list_tabs();
const tabId = tabs[0].id;

// 페이지 정보
const pageInfo = await mcp_kapture_tab_detail({ tabId });
console.log(`URL: ${pageInfo.url}`);
console.log(`Title: ${pageInfo.title}`);

// DOM 구조
const dom = await mcp_kapture_dom({ tabId });

// 인터랙티브 요소
const elements = await mcp_kapture_elements({
  tabId,
  selector: "button, a, input"
});
```

### 예제 2: 호버 효과 테스트
```javascript
const tabId = tabs[0].id;

// Before state
const beforeElements = await mcp_kapture_elements({
  tabId,
  selector: ".card"
});

// Hover
await mcp_kapture_hover({ tabId, selector: ".card" });

// After state
const afterElements = await mcp_kapture_elements({
  tabId,
  selector: ".card"
});

// Compare
console.log("Before:", beforeElements);
console.log("After:", afterElements);
```

### 예제 3: 폼 검증 테스트
```javascript
const tabId = tabs[0].id;

// 빈 값으로 제출 시도
await mcp_kapture_click({ tabId, selector: "button[type='submit']" });

// 에러 메시지 확인
const errors = await mcp_kapture_elements({
  tabId,
  selector: ".error, [role='alert']"
});

console.log("Validation errors:", errors);
```

### 예제 4: 반응형 테스트
```javascript
const tabId = tabs[0].id;
const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1440, height: 900 }
];

for (const viewport of viewports) {
  // Resize
  await mcp_kapture_resize({
    tabId,
    width: viewport.width,
    height: viewport.height
  });
  
  // Get navigation elements
  const nav = await mcp_kapture_elements({
    tabId,
    selector: "nav, .header"
  });
  
  console.log(`${viewport.name} navigation:`, nav);
}
```

### 예제 5: Progressive Scroll 분석 (⭐ 중요)
```javascript
const tabId = tabs[0].id;

// ✅ 올바른 방법: keypress로 스크롤하며 전체 페이지 분석
async function progressiveScroll(tabId) {
  const previousStates = [];
  let checkpointCount = 0;
  
  console.log("\n=== Progressive Scroll Analysis Started ===");
  
  while (checkpointCount < 25) { // 최소 20+ 체크포인트
    console.log(`\n=== Checkpoint ${checkpointCount + 1} ===`);
    
    // 1. 스크린샷 촬영
    const screenshot = await mcp_kapture_screenshot({ tabId });
    console.log(`Screenshot captured at ${i}%`);
    
    // 2. 즉시 분석
    const dom = await mcp_kapture_dom({ tabId });
    const visibleElements = await mcp_kapture_elements({
      tabId,
      visible: "true"
    });
    
    console.log(`Visible elements: ${visibleElements.length}`);
    
    // 3. 이전 상태와 비교
    if (previousStates.length > 0) {
      const previous = previousStates[previousStates.length - 1];
      console.log(`Comparing with ${i-5}% position...`);
      // 비교 로직: 새로운 요소, 애니메이션 감지 등
    }
    
    // 4. 인터랙션 테스트 (보이는 요소만)
    const buttons = await mcp_kapture_elements({
      tabId,
      selector: "button:visible, a:visible"
    });
    console.log(`Testable interactions: ${buttons.length}`);
    
    // 5. 로깅
    previousStates.push({
      position: i,
      dom,
      visibleElements,
      screenshot
    });
    
    // 6. 다음 위치로 스크롤 (100%가 아닐 때만)
    if (i < 100) {
      // PageDown 또는 ArrowDown 사용
      await mcp_kapture_keypress({ tabId, key: "PageDown" });
      
      // 애니메이션 대기
      await new Promise(resolve => setTimeout(resolve, 300));
    }
  }
  
  console.log("\n✅ Progressive scroll complete: 20+ checkpoints analyzed");
  return previousStates;
}

// 실행
const scrollAnalysis = await progressiveScroll(tabId);
```
```

**⚠️ 잘못된 방법 (사용 금지):**
```javascript
// ❌ PageDown 키 사용 - 제어 불가능, 분석 생략
await mcp_kapture_keypress({ tabId, key: "PageDown" });

// ❌ End 키로 끝까지 점프 - 중간 과정 모두 생략
await mcp_kapture_keypress({ tabId, key: "End" });

// ❌ 큰 간격 스크롤 - 애니메이션 놓침
window.scrollTo(0, document.body.scrollHeight);

// ❌ 분석 없이 스크린샷만 찍기
for (let i = 0; i <= 100; i += 10) {
  await mcp_kapture_screenshot({ tabId }); // 분석이 없음!
}
```

---

## 자주 하는 실수

### ❌ 잘못된 사용
```javascript
// tabId 누락
await mcp_kapture_dom(); // Error!

// 잘못된 파라미터
await mcp_kapture_click({ selector: ".button" }); // tabId 누락!

// selector 오타
await mcp_kapture_hover({ tabId, selector: "buton" }); // 'button' 오타
```

### ✅ 올바른 사용
```javascript
// 항상 tabId 먼저 획득
const tabs = await mcp_kapture_list_tabs();
const tabId = tabs[0].id;

// 모든 필수 파라미터 포함
await mcp_kapture_snapshot({ tabId });
await mcp_kapture_click({ tabId, selector: ".button" });
await mcp_kapture_hover({ tabId, selector: ".card" });
```

---

## 문제 해결

### Q: "Tool not found" 에러가 나요
**A:** `mcp_kapture_*` 도구 이름이 정확한지 확인하세요. 오타가 없는지 체크!

### Q: tabId를 어떻게 얻나요?
**A:** 항상 `mcp_kapture_list_tabs()`로 시작하세요.

### Q: selector가 작동하지 않아요
**A:** 
1. CSS selector 문법이 올바른지 확인
2. `mcp_kapture_elements`로 요소가 존재하는지 먼저 확인
3. XPath 사용 가능: `xpath: "//div[@class='hero']"`

### Q: 스크린샷을 저장해야 하나요?
**A:** 아니요! 메모리 기반 분석을 사용합니다. 스크린샷은 conversation history에 남아 있으므로 "이전 스크린샷과 비교해줘"로 참조할 수 있습니다.

---

## 체크리스트

탐색 시작 전에 확인하세요:

- [ ] `mcp_kapture_list_tabs()`로 tabId 획득
- [ ] 모든 명령어에 `mcp_kapture_*` 접두어 사용
- [ ] 모든 명령어에 `tabId` 파라미터 포함
- [ ] 상태 비교 시 before/after 메모리에 저장
- [ ] 스크린샷은 conversation history로 참조

---

**참고 문서:**
- `.github/copilot-instructions.md` - 전체 워크플로우 및 정책
- `PIPELINE_GUIDE.md` - 파이프라인 사용 가이드
- `analysis/` - 분석 결과 출력 폴더
