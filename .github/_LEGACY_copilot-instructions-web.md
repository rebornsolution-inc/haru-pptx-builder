# AI-Powered Content Builder System

## 🚫 ABSOLUTE PROHIBITIONS - READ FIRST (HIGHEST PRIORITY)

**NEVER, UNDER ANY CIRCUMSTANCES:**

1. ❌ **"빠르게 분석"** (Fast analysis)
2. ❌ **"주요 섹션만"** (Only main sections)
3. ❌ **"효율적인 방법"** (Efficient method)
4. ❌ **Skip viewport changes or visible content**
5. ❌ **Use `End`, `Home`, `PageDown`, or `PageUp` keys** (ONLY ArrowDown is allowed)
6. ❌ **Save screenshots to files**
7. ❌ **Generate code before analysis completion**
8. ❌ **Proactively suggest shortcuts WITHOUT user request**

**⚠️ AI MUST NOT AUTONOMOUSLY DECIDE TO "SPEED UP"**
- Do NOT say: "진행 상황이 너무 느리므로, 효율적인 방법으로..."
- Do NOT propose: "주요 섹션들을 캡처하고..."
- Do NOT use: PageDown, PageUp, End, Home keys under ANY circumstance
- **ONLY ArrowDown is permitted for scrolling** (no exceptions)
- **ALWAYS follow complete analysis process - capture ALL viewport changes**

**IF USER SAYS "너무 느리다" (too slow):**
→ Respond: "지침에 따라 정확한 분석을 위해 모든 콘텐츠를 상세히 캡처해야 합니다. 계속 진행하겠습니다."
→ Continue with systematic analysis

**THERE ARE NO SHORTCUTS. COMPLETE ANALYSIS IS MANDATORY.**

---

## 🔒 EXECUTION VALIDATION - RUNTIME ENFORCEMENT

### Auto-Detection System

**⚠️ PRE-EXECUTION CHECK - AI MUST VERIFY BEFORE EVERY `mcp_kapture_keypress()` CALL:**

**Step 1: Check intended key BEFORE calling tool**
```
IF intendedKey == "PageDown" OR "PageUp" OR "End" OR "Home":
  ❌ HALT IMMEDIATELY
  ❌ OUTPUT: "⚠️ VIOLATION DETECTED: Attempted to use {intendedKey} (FORBIDDEN)"
  ✅ CORRECTION: Change to "ArrowDown"
  ✅ THEN: Proceed with ArrowDown
```

**Step 2: Only allowed command**
```javascript
// ✅ ONLY THIS IS ALLOWED (with mandatory 500ms wait after each call)
await mcp_kapture_keypress({ tabId, key: "ArrowDown" });
await new Promise(resolve => setTimeout(resolve, 500)); // macOS CDP session cleanup

// ❌ NEVER USE THESE
await mcp_kapture_keypress({ tabId, key: "PageDown" }); // FORBIDDEN
await mcp_kapture_keypress({ tabId, key: "End" });      // FORBIDDEN
await mcp_kapture_keypress({ tabId, key: "Home" });     // FORBIDDEN
await mcp_kapture_keypress({ tabId, key: "PageUp" });   // FORBIDDEN

// ❌ FORBIDDEN: Batch calls without wait time
for (let i = 0; i < 5; i++) {
  await mcp_kapture_keypress({ tabId, key: "ArrowDown" }); // Missing 500ms wait!
}
```

**Rationale:**
- PageDown/PageUp = Jumps 800-1000px → Skips 5-10 viewports
- ArrowDown = Moves 50px → Captures EVERY viewport change
- End/Home = Jumps to page extremes → Completely skips content
- **500ms wait** = macOS CDP debugger session cleanup time (prevents "Another debugger is already attached" error)

### Behavioral Triggers - AI Self-Check

**IF AI IS ABOUT TO SAY ANY OF THESE, STOP IMMEDIATELY:**

❌ "시간 효율을 위해..."  
❌ "더 빠르게 스크롤..."  
❌ "효율적으로 분석..."
❌ "주요 섹션만..."
❌ "더 큰 간격으로..."
❌ "PageDown을 사용하여..."  
❌ "End 키로 이동..."  
❌ "이 속도로는 시간이 많이 걸릴 것 같으므로..."
❌ "진행 속도를 높이겠습니다..."
❌ "한 번에 더 많은..."
❌ "더 많은 스크롤이 필요합니다..."

**WHEN TRIGGER DETECTED, AI MUST:**
1. ❌ HALT immediately (do NOT execute the forbidden action)
2. ✅ OUTPUT violation message:
```
⚠️ BEHAVIORAL VIOLATION DETECTED
Trigger: [phrase that AI was about to say]
Reason: Attempting to deviate from systematic analysis protocol
Corrective Action: Using ArrowDown × 3-5 for fine-grained scrolling
Current checkpoint: X/30 (continuing until minimum 30 reached)
```
3. ✅ Resume with ArrowDown × 3-5 (NO changes to increment count)

**THEN:** Continue with ArrowDown × 3-5 increments, no exceptions.

---

## 🔒 CHECKPOINT COMPLETION ENFORCEMENT

### Mandatory Output Template (After EACH Checkpoint)

**AI MUST OUTPUT THIS CHECKLIST AFTER COMPLETING EACH CHECKPOINT:**

```
✅ CHECKPOINT X/30 COMPLETE
├─ 4-1: Header written to file ✅
├─ 4-2: Visual analysis (Colors: [specific], Typography: [specific], Layout: [specific]) ✅
├─ 4-3: Animation detection ([type], trigger: [specific]) ✅
├─ 4-4: Interactive elements tested (Y/10 elements) ✅
├─ 4-5: Results logged to file ✅
└─ 4-6: Tracking updated ✅

Next: Checkpoint X+1 (ArrowDown × 3-5)
```

**IF ANY ITEM SHOWS ❌ → HALT and complete before proceeding**

### Self-Check Questions (Before Moving to Next Checkpoint)

**AI MUST MENTALLY VERIFY:**
1. Did I write checkpoint header to 00_analysis_note.txt?
2. Did I analyze screenshot (colors, typography, layout, spacing)?
3. Did I check for animations (8-field template if found)?
4. Did I test 10 interactive elements (hover/click/focus)?
5. Did I log interaction results to file?
6. Did I increment checkpointIndex?

**IF ANY ANSWER IS "NO" → Go back and complete it NOW**

---

## 🤖 AGENT CONTEXT SWITCHING

**AI AUTOMATICALLY SELECTS AGENT BASED ON WORKFLOW STAGE:**

### Agent Selection Logic

**Stage 1: Web Analysis** (Default when URL provided)
→ Use **Web Analyzer Agent** context (`.github/agents/web-analyzer.agents.md`)
→ Triggers: `/web [url]`, "웹사이트 분석", URLs, "사이트 구조"
→ Output: `01_contents_web.json` + `02_style_web.json`

**Stage 2: Integration** (After analysis files exist)
→ Use **Integration Agent** context (`.github/agents/integration-agent.agents.md`)
→ Triggers: `/integrate`, "통합", "merge JSONs", "03번 파일"
→ Output: `03_integrate_web.json`

**Stage 3: Code Generation** (After integration file exists)
→ Use **Code Generator Agent** context (`.github/agents/code-generator.agents.md`)
→ Triggers: `/generate`, "코드 생성", "컴포넌트", "React"
→ Output: 17+ React/TypeScript files

### Context Switching Rules

```javascript
// AI checks current stage and loads appropriate agent context

if (userRequest.includes("URL") || userRequest.includes("/web")) {
  loadAgentContext("web-analyzer");
  // Execute: 30-80 checkpoint analysis → Generate 01/02 JSONs
}

else if (userRequest.includes("/integrate") || filesExist(["01_contents", "02_style"])) {
  loadAgentContext("integration-agent");
  // Execute: PowerShell script → Generate 03 JSON
}

else if (userRequest.includes("/generate") || fileExists("03_integrate")) {
  loadAgentContext("code-generator");
  // Execute: Component-based 3-pass → Generate React components
}
```

### User Experience

**User says: "https://example.com 분석하고 코드 생성해줘"**

```
[Stage 1: Web Analyzer Agent AUTO-LOADED]
✅ 웹 분석 시작...
→ 45 체크포인트 완료
→ 01_contents_web.json (781 lines)
→ 02_style_web.json (586 lines)
✅ 분석 완료.

[Stage 2: Integration Agent AUTO-LOADED]
✅ 통합 시작...
→ PowerShell 스크립트 실행
→ 03_integrate_web.json (1229 lines)
✅ 통합 완료.

[Stage 3: Code Generator Agent AUTO-LOADED]
✅ 코드 생성 시작...
→ Phase 1: Foundation (types, docs)
→ Phase 2: HeroSection (Pass 1/3) - 계속할까요?
   [User: yes]
→ Phase 2: HeroSection (Pass 2/3) - 계속할까요?
   [User: yes]
→ Phase 2: HeroSection (Pass 3/3) - 다음 컴포넌트로?
   [User: yes]
→ ... (13 components total)
→ Phase 3: Assembly
✅ 17개 파일 생성 완료!
```

**No manual agent selection needed - AI handles workflow automatically.**

---

## ⚠️ CRITICAL: START HERE - WEB ANALYSIS CHECKLIST

**BEFORE starting ANY web analysis, complete these steps IN ORDER:**

### ✅ Step-by-Step Execution (DO NOT SKIP ANY STEP)

1. **Get Browser Tab** ← START HERE
   ```javascript
   const tabs = await mcp_kapture_list_tabs();
   const tabId = tabs[0].id;
   ```

2. **Navigate to URL**
   ```javascript
   await mcp_kapture_navigate({ tabId, url: "https://example.com" });
   ```

3. **Initial DOM Capture**
   ```javascript
   await mcp_kapture_dom({ tabId });
   await mcp_kapture_elements({ tabId, visible: "true" });
   ```

4. **Initial Screenshot** (analyze immediately, do NOT save to file)
   ```javascript
   await mcp_kapture_screenshot({ tabId });
   // Analyze colors, layout, typography in conversation
   ```

5. **Progressive Scroll** (MANDATORY - Continue until ALL content captured)
   - Use `mcp_kapture_keypress()` with **ArrowDown ONLY** (NO OTHER KEYS)
   - ArrowDown × 3-5 per checkpoint (150-300px increments)
   - At EACH checkpoint: Screenshot → Analyze → Test interactions → Log (ALL 6 steps)
   - **Goal:** Capture EVERY visible change from top to bottom
   - **Method:** Keep scrolling until footer visible + 3 consecutive "no change" detections
   - **Expected:** 30-80 checkpoints depending on page complexity

6. **Test All Interactions**
   - Hover effects, Click navigation, Open modals/accordions, Test forms (UI only)

7. **Multi-Viewport Analysis**
   - Repeat steps 3-6 for Mobile (375x812), Tablet (768x1024), Desktop (1440x900)

8. **Generate Analysis Files (STOP HERE)**
   - Write to `analysis/web-pipeline/01_contents_web.json`
   - Write to `analysis/web-pipeline/02_style_web.json`
   - ⚠️ **STOP HERE - Do NOT proceed to integration or code generation**
   - ⚠️ **DO NOT automatically create 03_integrate_web.json**
   - ⚠️ **User must manually request `/integrate` or `/generate` commands**

---

## ⚠️ CRITICAL: Core Analysis Policies

### 1. MCP Tool Policy (Mandatory)

**⚠️ YOU MUST USE KAPTURE MCP TOOLS EXCLUSIVELY:**

✅ **ALLOWED:**
- `mcp_kapture_list_tabs()`, `mcp_kapture_navigate()`, `mcp_kapture_dom()`
- `mcp_kapture_elements()`, `mcp_kapture_screenshot()`, `mcp_kapture_hover()`
- `mcp_kapture_click()`, `mcp_kapture_keypress()`, `mcp_kapture_resize()`

❌ **FORBIDDEN:**
- `mcp_microsoft_pla_*` (Microsoft Playwright MCP)
- `mcp_browsermcp_*` (Generic Browser MCP)
- `mcp_kapture_evaluate()` (does NOT exist)

### 2. Screenshot Policy (Memory-Based Analysis)

**⚠️ DO NOT SAVE SCREENSHOTS TO FILES**

- Take via `mcp_kapture_screenshot()` → Analyze base64 immediately → Move to next
- Screenshots exist in conversation history for comparison
- Reference: "Compare this screenshot with the one from Step 3"

### 3. Analysis File Structure

```
analysis/
├── web-pipeline/
│   ├── 00_analysis_note.txt       ← Real-time checkpoint logging (NEW)
│   ├── 01_contents_web.json       ← AI writes analysis results here
│   ├── 02_style_web.json          ← AI writes design tokens here
│   ├── 03_integrate_web.json      ← AI writes integrated spec here
│   └── generators/
│       └── 04_generate_tailwind.json
```

**Workflow:** User provides URL → AI explores (writes to 00_analysis_note.txt) → Reads notes → Generates JSON files → Generates code

### 4. Output File Locations

```
output/
├── web_contents.json
├── web_style.json
├── WebDevSpec.json
└── web/
    └── index.html             ← Final generated code
```

---

## ⚠️ CRITICAL: Core Analysis Policies

```javascript
// 1. Initialize tracking
let checkpointIndex = 0;
let previousVisibleElements = new Set();
let previousScreenshotHash = null;
let consecutiveNoChangeCount = 0;
const MIN_CHECKPOINTS = 30; // Minimum required checkpoints for valid analysis
const MAX_NO_CHANGE_THRESHOLD = 3;
const MAX_CHECKPOINTS = 100; // Safety limit (increased for detailed analysis)

// NEW: Quantitative comparison tracking
const checkpointData = []; // Store {index, positions, screenshot, timestamp}
let previousElementPositions = new Map(); // Map<selector, {x, y, width, height}>

// 2. Simple hash function for screenshot comparison
function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < Math.min(str.length, 1000); i++) { // First 1000 chars only
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return hash.toString(36);
}

// 3. Capture initial state
const initialElements = await mcp_kapture_elements({ tabId, visible: "true" });
const initialScreenshot = await mcp_kapture_screenshot({ tabId });
previousVisibleElements = new Set(initialElements.map(el => el.selector || el.xpath));
previousScreenshotHash = simpleHash(initialScreenshot);

// NEW: Extract initial element positions for quantitative tracking
initialElements.forEach(el => {
  const selector = el.selector || el.xpath;
  if (el.boundingBox) {
    previousElementPositions.set(selector, {
      x: el.boundingBox.x || 0,
      y: el.boundingBox.y || 0,
      width: el.boundingBox.width || 0,
      height: el.boundingBox.height || 0
    });
  }
});

// NEW: Store checkpoint data for future comparison
checkpointData.push({
  index: 0,
  screenshot: initialScreenshot,
  positions: new Map(previousElementPositions),
  timestamp: new Date().toISOString()
});

console.log(`✅ 체크포인트 ${checkpointIndex++} 완료 (초기 상태)`);
```

### Main Loop: Continue Until Page End

**YOU MUST COMPLETE ALL 7 STEPS AT EACH VIEWPORT CHANGE:**

**1. 📐 Scroll Down (Small increments with ArrowDown)**
```javascript
// Small scroll increment (ArrowDown × 3-5 for fine-grained capture)
const SCROLL_INCREMENT = 3; // ~150-300px per checkpoint

// ⚠️ CRITICAL: macOS CDP session cleanup requires 500ms between keypress calls
// DO NOT use batch loops - each keypress must wait for previous session to close
for (let i = 0; i < SCROLL_INCREMENT; i++) {
  await mcp_kapture_keypress({ tabId, key: "ArrowDown" });
  await new Promise(resolve => setTimeout(resolve, 500)); // macOS CDP session cleanup
}

// Wait for animations to settle
await new Promise(resolve => setTimeout(resolve, 300));
```

**2. 📸 Viewport State Capture**
```javascript
// Capture current state
const currentElements = await mcp_kapture_elements({ tabId, visible: "true" });
const currentScreenshot = await mcp_kapture_screenshot({ tabId });

// NEW: Extract current element positions for quantitative comparison
const currentElementPositions = new Map();
currentElements.forEach(el => {
  const selector = el.selector || el.xpath;
  if (el.boundingBox) {
    currentElementPositions.set(selector, {
      x: el.boundingBox.x || 0,
      y: el.boundingBox.y || 0,
      width: el.boundingBox.width || 0,
      height: el.boundingBox.height || 0
    });
  }
});
```

**3. 🔍 Change Detection (Structural + Visual)**
```javascript
// 3-1. Structural change detection
const currentElementSet = new Set(currentElements.map(el => el.selector || el.xpath));

const newElements = [...currentElementSet].filter(
  sel => !previousVisibleElements.has(sel)
);
const removedElements = [...previousVisibleElements].filter(
  sel => !currentElementSet.has(sel)
);

const structuralChange = newElements.length >= 2 || removedElements.length >= 2;

// 3-2. Visual change detection (if no structural change)
let visualChange = false;
if (!structuralChange) {
  const currentHash = simpleHash(currentScreenshot);
  visualChange = currentHash !== previousScreenshotHash;
  previousScreenshotHash = currentHash;
}

// 3-3. Determine if checkpoint is needed
const significantChange = structuralChange || visualChange;
```

**4. 🔄 Checkpoint Creation (if change detected) - CANNOT BE SKIPPED**

⚠️ **ALL 6 SUB-STEPS ARE MANDATORY - NO EXCEPTIONS:**

```javascript
if (significantChange) {
  console.log(`✅ 체크포인트 ${checkpointIndex} 완료 - ${structuralChange ? '구조 변화' : '시각적 변화'} 감지`);
  
  // 4-1. ✅ MANDATORY: Write checkpoint header (CANNOT SKIP)
  // ⚠️ CRITICAL: Use replace_string_in_file tool, NOT PowerShell echo command
  // PowerShell echo causes UTF-16 encoding issues that corrupt the file
  
  // NEW: Calculate quantitative movements from previous checkpoint
  const movementAnalysis = [];
  for (const [selector, currentPos] of currentElementPositions.entries()) {
    if (previousElementPositions.has(selector)) {
      const prevPos = previousElementPositions.get(selector);
      const deltaX = currentPos.x - prevPos.x;
      const deltaY = currentPos.y - prevPos.y;
      const deltaWidth = currentPos.width - prevPos.width;
      const deltaHeight = currentPos.height - prevPos.height;
      
      // Only log significant movements (>5px change)
      if (Math.abs(deltaX) > 5 || Math.abs(deltaY) > 5 || Math.abs(deltaWidth) > 5 || Math.abs(deltaHeight) > 5) {
        movementAnalysis.push({
          selector: selector.substring(0, 50), // Truncate long selectors
          deltaX: Math.round(deltaX),
          deltaY: Math.round(deltaY),
          deltaWidth: Math.round(deltaWidth),
          deltaHeight: Math.round(deltaHeight)
        });
      }
    }
  }
  
  const checkpointHeader = `
=== CHECKPOINT ${checkpointIndex} ===
Timestamp: ${new Date().toISOString()}
Viewport: Desktop 1440x900
Scroll Position: ~${checkpointIndex * 200}px
Change Type: ${structuralChange ? 'Structural' : 'Visual'}

📋 STRUCTURAL CHANGES:
- New Elements (${newElements.length}): ${newElements.slice(0, 5).join(', ')}
- Removed Elements (${removedElements.length}): ${removedElements.slice(0, 5).join(', ')}

📊 QUANTITATIVE COMPARISON (vs Checkpoint ${checkpointIndex - 1}):
${movementAnalysis.length > 0 ? movementAnalysis.slice(0, 5).map(m => 
  `- ${m.selector}: ΔX=${m.deltaX > 0 ? '+' : ''}${m.deltaX}px, ΔY=${m.deltaY > 0 ? '+' : ''}${m.deltaY}px${m.deltaWidth !== 0 ? `, ΔWidth=${m.deltaWidth > 0 ? '+' : ''}${m.deltaWidth}px` : ''}${m.deltaHeight !== 0 ? `, ΔHeight=${m.deltaHeight > 0 ? '+' : ''}${m.deltaHeight}px` : ''}`
).join('\n') : '- No significant position changes detected (< 5px threshold)'}
- Total tracked elements: ${currentElementPositions.size}
- Elements moved: ${movementAnalysis.length}
`;

  // ✅ CORRECT: Use replace_string_in_file tool
  await replace_string_in_file({
    filePath: 'analysis/web-pipeline/00_analysis_note.txt',
    oldString: '---\n\n',  // Find last checkpoint separator
    newString: `---\n\n${checkpointHeader}`
  });
  
  // ❌ FORBIDDEN: Do NOT use these methods
  // await run_in_terminal(`echo "${content}" >> file.txt`);  // Causes encoding issues
  // await run_in_terminal(`Out-File ...`);  // Slower, unnecessary
  
  // 4-2. ✅ MANDATORY: Visual analysis (CANNOT SKIP)
  const visualAnalysis = `
🎨 VISUAL ANALYSIS:
- Colors: [AI analyzes screenshot: e.g., "Blue gradient #1E3A8A → #3B82F6"]
- Typography: [AI analyzes: e.g., "Heading 48px, weight 700, 'Noto Sans KR'"]
- Layout: [AI analyzes: e.g., "3-column grid with 24px gap"]
- Spacing: [AI analyzes: e.g., "Section padding 80px vertical, 0 horizontal"]
`;

  await replace_string_in_file({
    filePath: 'analysis/web-pipeline/00_analysis_note.txt',
    oldString: '---\n\n',
    newString: `${visualAnalysis}\n---\n\n`
  });
  
  // 4-3. ✅ MANDATORY: Animation detection (CANNOT SKIP)
  const isSectionTransition = newElements.length >= 5 || 
                              removedElements.length >= 5 ||
                              newElements.some(sel => sel.includes('section'));
  
  if (isSectionTransition) {
    console.log("🎬 섹션 전환 감지 - 애니메이션 프레임 추가 캡처");
    
    const animationHeader = `
🎬 ANIMATION DETECTION:
`;
    await replace_string_in_file({
      filePath: 'analysis/web-pipeline/00_analysis_note.txt',
      oldString: '---\n\n',
      newString: `${animationHeader}\n---\n\n`
    });
    
    // Capture animation frames (3-5 additional screenshots)
    for (let frame = 0; frame < 3; frame++) {
      await new Promise(resolve => setTimeout(resolve, 400));
      await mcp_kapture_screenshot({ tabId });
      console.log(`   프레임 ${frame+1}/3 캡처`);
    }
    
    // Analyze and document animation details (8-field template)
    const animationDetails = `
- Subject: [AI observes: e.g., "Container ship with red cargo"]
- Visual Description: [AI describes: e.g., "Blue ship body, 3 red containers on deck"]
- Observed Behavior: [AI documents: e.g., "Moves left to right during scroll, ~1600px travel"]
- Trigger: [AI identifies: e.g., "scroll position 0-100%"]
- Technical Details: [AI infers: e.g., "GSAP ScrollTrigger with scrub:true, parallax effect"]
- Property Changes: [AI calculates: e.g., "translateX: -100px → 1500px, duration matches scroll"]
- Implementation Hint: [AI suggests: e.g., "gsap.to(ship, { x: 15, scrollTrigger: { scrub: true } })"]
`;
    
    await replace_string_in_file({
      filePath: 'analysis/web-pipeline/00_analysis_note.txt',
      oldString: '---\n\n',
      newString: `${animationDetails}\n---\n\n`
    });
  } else {
    // No animation detected
    const noAnimation = `
🎬 ANIMATION DETECTION: None detected in this viewport
`;
    await replace_string_in_file({
      filePath: 'analysis/web-pipeline/00_analysis_note.txt',
      oldString: '---\n\n',
      newString: `${noAnimation}\n---\n\n`
    });
  }
  
  // 4-4. ✅ MANDATORY: Test 10 interactive elements (CANNOT SKIP)
  // ⚠️ THIS STEP IS INTEGRATED - AI CANNOT PROCEED WITHOUT COMPLETING THIS
  console.log("🖱️ 인터랙티브 요소 테스트 시작... (필수 단계)");
  
  const interactiveElements = await mcp_kapture_elements({ 
    tabId, 
    selector: "button, a, input, textarea, select, [role='button'], [onclick]",
    visible: "true"
  });
  
  const elementsToTest = interactiveElements.slice(0, 10);
  let testedCount = 0;
  const interactionResults = [];
  
  for (const element of elementsToTest) {
    const selector = element.selector || element.xpath;
    
    try {
      // Test hover effect
      await mcp_kapture_hover({ tabId, selector });
      await mcp_kapture_screenshot({ tabId });
      
      // Test click (for buttons, links)
      if (element.tagName === 'BUTTON' || element.tagName === 'A' || element.role === 'button') {
        await mcp_kapture_click({ tabId, selector });
        await mcp_kapture_screenshot({ tabId });
        interactionResults.push(`${element.tagName}:hover+click`);
      }
      
      // Test focus (for form inputs)
      if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
        await mcp_kapture_click({ tabId, selector });
        await mcp_kapture_screenshot({ tabId });
        interactionResults.push(`${element.tagName}:focus`);
      }
      
      testedCount++;
      console.log(`   [${testedCount}/${elementsToTest.length}] Tested: ${element.tagName} - ${selector}`);
    } catch (error) {
      console.log(`   ⚠️ Failed to test: ${selector} - ${error.message}`);
    }
  }
  
  console.log(`✅ 인터랙션 테스트 완료: ${testedCount}개`);
  
  // 4-5. ✅ MANDATORY: Log interaction results (CANNOT SKIP)
  const interactionLog = `
🖱️ INTERACTIVE ELEMENTS TESTED (${testedCount} total):
${interactionResults.length > 0 ? interactionResults.map(r => `- ${r}`).join('\n') : '- No interactive elements found in this viewport'}

---

`;

  await replace_string_in_file({
    filePath: 'analysis/web-pipeline/00_analysis_note.txt',
    oldString: '---\n\n',
    newString: `${interactionLog}`
  });
  
  // 4-6. ✅ MANDATORY: Update tracking (CANNOT SKIP)
  checkpointIndex++;
  previousVisibleElements = currentElementSet;
  consecutiveNoChangeCount = 0;
  
  // NEW: Update position tracking for next comparison
  previousElementPositions = new Map(currentElementPositions);
  
  // NEW: Store checkpoint data for future reference
  checkpointData.push({
    index: checkpointIndex - 1,
    screenshot: currentScreenshot,
    positions: new Map(currentElementPositions),
    timestamp: new Date().toISOString(),
    movements: movementAnalysis.length
  });
  
} else {
  consecutiveNoChangeCount++;
  console.log(`⚠️ 변화 없음 ${consecutiveNoChangeCount}/${MAX_NO_CHANGE_THRESHOLD}`);
}
```

**5. ➡️ Next Checkpoint**
- ONLY proceed after steps 1-4 complete
- Report to user: "✅ 체크포인트 X 완료. 다음 체크포인트로 진행합니다."

### Completion Criteria
- ✅ **MINIMUM 30 checkpoints required** (if less than 30, analysis is INVALID - continue scrolling)
- ✅ All viewport changes captured (30-80 checkpoints depending on page complexity)
- ✅ Every animation detected and logged
- ✅ All interactive elements tested (minimum 50+ total interactions)
- ✅ Footer visible + 3 consecutive "no change" detections
- ✅ **Only ArrowDown key used** (PageDown, PageUp, End, Home are ALL FORBIDDEN)

### ❌ FORBIDDEN METHODS
```javascript
// ❌ NEVER USE
await mcp_kapture_keypress({ tabId, key: "End" }); // Jumps to bottom
await mcp_kapture_keypress({ tabId, key: "Home" }); // Jumps to top
await mcp_kapture_keypress({ tabId, key: "PageDown" }); // Jumps 800px, skips content
await mcp_kapture_keypress({ tabId, key: "PageUp" }); // Jumps backward
await mcp_kapture_click({ tabId }); // No selector = error

// ✅ ONLY USE
await mcp_kapture_keypress({ tabId, key: "ArrowDown" }); // Primary scroll (small increment)
await new Promise(resolve => setTimeout(resolve, 500)); // MANDATORY: Wait for macOS CDP session cleanup
```

### 🚨 ENFORCEMENT RULES

**IF AI SUGGESTS SHORTCUTS:**
1. User must reject and reference this section
2. AI must acknowledge: "모든 뷰포트 변화를 캡처할 때까지 계속하겠습니다"
3. Resume from last completed checkpoint

**PROGRESS REPORTING:**
- After every 3 checkpoints, report: "체크포인트 X/30 완료 (최소 30개 필요, 현재 진행 중)"
- When reaching 30: "✅ 최소 체크포인트 30개 달성. 계속 진행합니다."
- Do NOT say: "빠르게", "효율적으로", "주요 섹션", "더 큰 간격으로"
- Only say: "다음 체크포인트로 진행" or "진행 중"

**NO EXCEPTIONS. SYSTEMATIC ANALYSIS IS MANDATORY.**

---

## Pipeline Details

### Web Pipeline

#### 00. Real-Time Analysis Logging (NEW)
- **File:** `analysis/web-pipeline/00_analysis_note.txt`
- **Purpose:** Capture detailed observations during web exploration
- **Content:** Checkpoint-by-checkpoint documentation of visual elements, animations, interactions
- **Usage:** Primary reference for generating 01_contents and 02_style JSON files
- **Format:**
  ```
  === CHECKPOINT X ===
  - Structural Changes: New/removed elements
  - Visual Analysis: Colors, typography, layout, spacing
  - Animation Detection: Subject, behavior, trigger, implementation hints
  - Interactive Elements: Hover/click/focus test results
  ```

#### 01. Web Content Analysis
- **Input:** `00_analysis_note.txt` (accumulated observations)
- Site structure, SEO, navigation, interactive elements
- Output: Page structure, navigation hierarchy, metadata
- **Critical:** Preserve ALL observed details (animations, interactions, complex features)
- **Method:** Read 00_analysis_note.txt → Extract structural/content data → Generate JSON

#### 02. Web Style Analysis
- **Input:** `00_analysis_note.txt` (accumulated observations)
- Responsive design tokens, component states, CSS specifications
- Output: Color system, typography, spacing, component patterns
- **Critical:** Document animation types, scroll behaviors, 3D effects with full context
- **Method:** Read 00_analysis_note.txt → Extract visual/style data → Generate JSON

#### 03. Web Integration
- Merge content + style into complete developer spec
- Output: Page-by-page specifications, component library
- **Critical:** Maintain detailed implementation instructions from analysis phase
- **Method:** PowerShell merge script (see below)
- **Validation:** Auto-verify no information loss (see validation section below)

#### 03-0. Integration Generation Method (MANDATORY)

**⚠️ CRITICAL: Use PowerShell Script - NOT AI Direct Generation**

**Problem:** 
- AI token limit (~4K-8K tokens) causes automatic content simplification
- AI writing JSON directly results in 70% data loss (e.g., 1367 lines → 392 lines)
- Section-by-Section approach still simplifies internal details (stepCards details omitted, visual fields truncated)

**Root Cause:**
```javascript
// ❌ AI tries to write from memory → automatic summarization
const section = {
  stepCards: [
    { title: "..." }  // Details omitted due to token pressure
  ]
}

// ✅ Script copies entire objects → zero data loss
const section = contents.sections.find(s => s.id === "section-02");
integrated.sections.push({ ...section, style: style.components[section.id] });
```

**Solution: PowerShell Merge Script**

**AI must execute this command instead of generating JSON:**
```powershell
powershell -ExecutionPolicy Bypass -File "scripts\integrate_web_pipeline.ps1"
```

**Script performs:**
1. Load 01_contents_web.json + 02_style_web.json as objects
2. For each section: `merged = { ...contentSection, style: styleComponent }`
3. Add global style data (animations, designTokens, responsive, accessibility, seo)
4. Write 03_integrate_web.json with full data preservation
5. Auto-validate (ranges, codeHints, colors)

**Expected Results:**
- File size: 1200-1500 lines (vs AI's 392 lines)
- codeHint preservation: 16/16 (100%, vs AI's 8/16)
- Range preservation: All fontSize ranges maintained
- Color preservation: All hex values maintained

**Mandatory Workflow:**
```
Step 1: AI detects /integrate command
Step 2: AI calls run_in_terminal with PowerShell script
Step 3: Script outputs validation results
Step 4: AI reports success/failure to user
Step 5: STOP (do NOT attempt to generate JSON manually)
```

**Old Method (DEPRECATED - DO NOT USE):**
~~Section-by-Section generation with replace_string_in_file~~
- ❌ Caused 70% data loss
- ❌ AI simplified stepCards, visual fields, animation details
- ❌ Token limit hit during each section generation

#### 04. Code Generation
- **Method:** Section-by-Section 3-Pass Generation (see below)
- **Output:** Single HTML file with Tailwind CSS
- **Format:** HTML5 + Tailwind CDN

#### 04-0. HTML Generation Method (MANDATORY) - UPDATED v2.20.0

**⚠️ CRITICAL: Section-by-Section 3-Pass Generation (HTML + Tailwind)**

### **Problem Analysis:**
- **Previous method:** React/TSX components (wrong output format)
- **Correct output:** Single HTML file with Tailwind CSS classes
- **Root cause:** Misunderstood project requirements

### **NEW Solution: Section-by-Section HTML Generation (Incremental Approach)**

**Core Principle:** Generate ONE section at a time with THREE quality passes per section

**AI MUST follow this workflow WITH user confirmation after each section:**

```
Phase 1: HTML Skeleton → Phase 2: Section Generation (per section) → Phase 3: Final Assembly
```

**User confirms completion of EACH section before proceeding to next.**

---

### **Phase 1: HTML Skeleton (One-Time Setup)**

**Task 1-1: Generate Base HTML Structure**
```html
<!-- output/web/index.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><!-- From 03_integrate_web.json seo.title --></title>
  <meta name="description" content="<!-- From seo.description -->">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Animation Libraries (if needed) -->
  <!-- GSAP will be added in Phase 2 if animations detected -->
  <!-- Three.js will be added in Phase 2 if 3D content detected -->
  
  <style>
    /* Custom styles from designTokens */
  </style>
</head>
<body>
  <!-- Sections will be inserted here in Phase 2 -->
</body>
</html>
```

**Task 1-2: Generate Section Structure Document**
```markdown
// docs/section_structure.md

# Section Mapping (from 03_integrate_web.json)

## Sections → HTML Sections

1. section-01-hero → <section id="hero">
2. section-02-transition → <section id="transition">
3. section-03-description → <section id="description">
... (list all 14 sections)

Total: 14 sections in single HTML file
```

**Completion Check:**
```
✅ Phase 1 완료
- output/web/index.html (기본 구조)
- docs/section_structure.md (14 섹션 매핑)

다음: section-01-hero 생성을 시작합니다.
```

---

### **Phase 2: Section Generation (Per Section)**

**For EACH section in 03_integrate_web.json.sections, execute 3 passes:**

#### **Pass 1: HTML Structure + Data Mapping**

**AI creates HTML section with basic structure:**

```html
<!-- Section 01: Hero -->
<section id="section-01-hero" class="hero-section">
  <!-- 1. Main heading -->
  <h1>The AI-Native Operating System For Global Supply Chains</h1>
  
  <!-- 2. CTA buttons -->
  <div class="buttons">
    <a href="#demo">Book a demo</a>
  </div>
  
  <!-- 3. 3D visual canvas (placeholder) -->
  <canvas id="hero-img"></canvas>
  
  <!-- All JSON fields mapped to HTML elements -->
</section>
```

**Output:** "✅ Pass 1/3 완료 (HTML 구조) - 모든 JSON 필드 매핑됨. 계속할까요?"

#### **Pass 2: Tailwind Styling**

**AI adds Tailwind classes based on section.style:**

```html
<section 
  id="section-01-hero" 
  class="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-[#1E3A8A] to-[#3B82F6]"
>
  <!-- 1. Main heading with responsive typography -->
  <h1 class="text-6xl md:text-7xl font-bold leading-tight text-white text-center">
    The AI-Native Operating System For Global Supply Chains
  </h1>
  
  <!-- 2. CTA buttons with hover effects -->
  <div class="flex gap-4 mt-8">
    <a 
      href="#demo"
      class="px-8 py-4 bg-white text-black rounded-lg font-semibold hover:scale-105 transition"
    >
      Book a demo
    </a>
  </div>
  
  <!-- 3. 3D visual canvas -->
  <canvas 
    id="hero-img" 
    class="absolute left-0 w-full h-full pointer-events-none"
  ></canvas>
  
  <!-- All elements styled with Tailwind -->
</section>
```

**Output:** "✅ Pass 2/3 완료 (스타일링) - Tailwind 적용됨. 계속할까요?"

#### **Pass 3: Validation + codeHint Insertion**

**AI verifies JSON compliance and inserts animation code:**

```tsx
export function HeroSection({ data }: { data: HeroSectionType }) {
  const { style } = data;
  
  React.useEffect(() => {
    // Insert codeHint directly (NO interpretation)
    if (data.visual?.codeHint) {
      // EXAMPLE: data.visual.codeHint contains GSAP/Three.js code
      eval(data.visual.codeHint); // Or better: parse and execute safely
    }
  }, [data.visual]);
  
  return (
    <section className="...">
      {/* All elements with complete styling */}
      
      {/* 3D visual with actual implementation */}
      {data.visual?.type === '3d-planet-parallax' && (
        <div id="planet-canvas" className="absolute left-0 w-1/2 h-full">
          {/* Canvas will be created by codeHint script */}
        </div>
      )}
      
      {/* ... */}
    </section>
  );
}
```

**Output:** "✅ Pass 2/3 완료 (스타일링) - Tailwind 적용됨. 계속할까요?"

#### **Pass 3: Validation + codeHint Insertion**

**AI verifies JSON compliance and inserts animation code:**

```html
<!-- Section 01: Hero (Final with animations) -->
<section 
  id="section-01-hero" 
  class="relative min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-[#1E3A8A] to-[#3B82F6] px-6"
>
  <h1 class="text-6xl md:text-7xl font-bold leading-tight text-white text-center mb-8">
    The AI-Native Operating System For Global Supply Chains
  </h1>
  
  <div class="flex gap-4 mt-8 z-10">
    <a 
      href="#demo"
      class="px-8 py-4 bg-white text-black rounded-lg font-semibold hover:scale-105 transition"
    >
      Book a demo
    </a>
  </div>
  
  <!-- 3D Canvas with animation script -->
  <canvas 
    id="hero-img" 
    class="absolute left-0 top-0 w-full h-full pointer-events-none"
  ></canvas>
  
  <script>
    // Insert codeHint directly (NO interpretation)
    const canvas = document.querySelector('#hero-img');
    const scene = new THREE.Scene();
    const loader = new THREE.GLTFLoader();
    
    const ships = [];
    const parallaxSpeeds = [0.3, 0.5, 0.7];
    
    parallaxSpeeds.forEach((speed, i) => {
      loader.load(`ship-${i}.gltf`, (gltf) => {
        const ship = gltf.scene;
        scene.add(ship);
        ships.push({ model: ship, speed });
      });
    });
    
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      ships.forEach(ship => {
        ship.model.position.x = -scrollY * ship.speed * 0.05;
        ship.model.position.y = scrollY * ship.speed * 0.08;
      });
    });
  </script>
</section>
```

**Validation Checklist (AI outputs):**
```
✅ Pass 3/3 완료 (검증)

JSON 일치 확인:
- ✅ All fields mapped: heading, buttons, visual, bottomContent, integrations
- ✅ Style applied: background (gradient), heading (fontSize, color), buttons (padding, rounded)
- ✅ codeHint preserved: visual.codeHint inserted in <script> tag without modification
- ✅ No missing properties
- ✅ No unused properties

Section 01 (Hero) 완료! 다음 섹션으로 진행할까요?
```

**User responds:** "yes" → AI proceeds to next section

---

### **Phase 3: Final Assembly**

**Task 3-1: Combine All Sections into Single HTML File**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nauta - The AI-Native Operating System For Global Supply Chains</title>
  <meta name="description" content="AI-powered logistics intelligence for a world that never stops">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Animation Libraries (auto-detected) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  
  <style>
    /* Custom design tokens */
    :root {
      --color-primary: #4E73D6;
      --color-accent: #FF6635;
      --font-heading: 'Inter', sans-serif;
    }
  </style>
</head>
<body class="font-sans antialiased">
  <!-- Section 01: Hero -->
  <section id="section-01-hero" class="...">...</section>
  
  <!-- Section 02: Transition -->
  <section id="section-02-transition" class="...">...</section>
  
  <!-- ... (all 14 sections) -->
  
  <!-- Section 14: CTA -->
  <section id="section-14-cta" class="...">...</section>
</body>
</html>
```

**Task 3-2: Final Validation**
```
✅ Phase 3 완료

생성된 파일:
- output/web/index.html (단일 HTML 파일, 1500-3000 lines)


검증:
- ✅ 모든 섹션 렌더링됨 (13/13)
- ✅ 모든 codeHint 삽입됨 (16/16)
- ✅ 필요한 라이브러리 자동 로드 (GSAP, Three.js)
- ✅ TypeScript 타입 안전성 확보
```

---

### **Execution Rules**

**AI MUST:**
1. ✅ Complete Phase 1 first (Foundation)
2. ✅ For EACH component: Execute Pass 1 → Pass 2 → Pass 3
3. ✅ WAIT for user confirmation after EACH component completion
4. ✅ Report progress: "✅ Pass X/3 완료 (HeroSection). 계속할까요?"
5. ✅ Only proceed to next component when user says "yes"

**AI MUST NOT:**
1. ❌ Generate multiple components without user confirmation
2. ❌ Skip any pass (1, 2, or 3)
3. ❌ Combine components into single file
4. ❌ Simplify JSON data or omit fields

---

### **Expected Results**

- File count: 17+ files (1 page + 13 components + 3 config/docs)
- Section rendering: 100% (all sections mapped to components)
- Feature preservation: 100% (no simplification, 3-pass quality check)
- Animation preservation: 100% (all codeHints inserted verbatim)
- Type safety: 100% (TypeScript interfaces from JSON)

---

### **DEPRECATED Methods:**

**❌ v2.17.0 - PowerShell 18-Task Method:**
- Problem: AI stops midway, requires manual intervention
- Reason: Monolithic generation, no checkpoints
- Status: DEPRECATED as of v2.18.0

**❌ v2.16.0 - Single PowerShell Script:**
- Problem: 70% data loss (generic templates)
- Status: DEPRECATED as of v2.17.0

검증:
- ✅ 모든 섹션 렌더링됨 (13/13)
- ✅ 모든 codeHint 삽입됨 (16/16)
- ✅ 필요한 라이브러리 자동 로드 (GSAP, Three.js)
- ✅ TypeScript 타입 안전성 확보
```

---

### **Execution Rules**

**AI MUST:**
1. ✅ Complete Phase 1 first (Foundation)
2. ✅ For EACH component: Execute Pass 1 → Pass 2 → Pass 3
3. ✅ WAIT for user confirmation after EACH component completion
4. ✅ Report progress: "✅ Pass X/3 완료 (HeroSection). 계속할까요?"
5. ✅ Only proceed to next component when user says "yes"

**AI MUST NOT:**
1. ❌ Generate multiple components without user confirmation
2. ❌ Skip any pass (1, 2, or 3)
3. ❌ Combine components into single file
4. ❌ Simplify JSON data or omit fields

---

### **Expected Results**

- File count: 17+ files (1 page + 13 components + 3 config/docs)
- Section rendering: 100% (all sections mapped to components)
- Feature preservation: 100% (no simplification, 3-pass quality check)
- Animation preservation: 100% (all codeHints inserted verbatim)
- Type safety: 100% (TypeScript interfaces from JSON)

---

### **🔗 MANDATORY: Default Link Configuration (Harufolio Project)**

**⚠️ CRITICAL: All generated code MUST use these default URLs**

**Link Mapping (ALWAYS apply during code generation):**

| Link Type | Display Text | Actual URL | Notes |
|-----------|-------------|------------|-------|
| **Social Links** | Instagram, SNS, Social | `https://instagram.com/haru_folio` | All social media references |
| **Gallery/Portfolio** | Gallery, Works, Projects | `https://port.gallery` | All portfolio/gallery pages |
| **Company Info** | Contact, About, Company | `https://rebornsolution.com` | Contact forms, company info |
| **Footer Credit** | "built by harufolio" | `https://port.gallery` | Always in footer, hyperlinked |

**Implementation Rules:**

1. **Social Links:**
   ```html
   <!-- ✅ CORRECT -->
   <a href="https://instagram.com/haru_folio" target="_blank" rel="noopener">Instagram</a>
   
   <!-- ❌ WRONG -->
   <a href="#instagram">Instagram</a>
   <a href="https://example.com/social">Follow us</a>
   ```

2. **Gallery/Portfolio:**
   ```html
   <!-- ✅ CORRECT -->
   <a href="https://port.gallery">View Gallery</a>
   <a href="https://port.gallery">Our Works</a>
   
   <!-- ❌ WRONG -->
   <a href="/gallery">Gallery</a>
   <a href="#portfolio">Portfolio</a>
   ```

3. **Contact/Company:**
   ```html
   <!-- ✅ CORRECT -->
   <a href="https://rebornsolution.com">Contact Us</a>
   <a href="https://rebornsolution.com">About Company</a>
   
   <!-- ❌ WRONG -->
   <a href="/contact">Contact</a>
   <a href="mailto:info@example.com">Email</a>
   ```

4. **Footer Credit (MANDATORY):**
   ```html
   <!-- ✅ CORRECT - Always include in footer -->
   <footer>
     <!-- ... other footer content ... -->
     <p class="text-sm text-gray-500">
       built by <a href="https://port.gallery" class="hover:text-gray-700 transition">harufolio</a>
     </p>
   </footer>
   
   <!-- ❌ WRONG - Missing credit or wrong link -->
   <footer>
     <p>© 2025 Company Name</p>
   </footer>
   ```

**Auto-Detection & Replacement:**

During code generation, AI MUST:
1. Scan all `<a>` tags for link types
2. Replace placeholder URLs with correct URLs
3. Add footer credit if missing
4. Verify all links before file completion

**Example Auto-Replacement:**
```javascript
// AI detects these patterns in JSON or generated code:
"instagram" → https://instagram.com/haru_folio
"gallery", "portfolio", "works" → https://port.gallery
"contact", "about", "company" → https://rebornsolution.com

// Footer check:
if (!footer.includes("built by harufolio")) {
  footer += '<p>built by <a href="https://port.gallery">harufolio</a></p>';
}
```

**Validation Checklist (before completing code generation):**
- [ ] All social links point to `instagram.com/haru_folio`
- [ ] All gallery/portfolio links point to `port.gallery`
- [ ] All contact/company links point to `rebornsolution.com`
- [ ] Footer includes "built by harufolio" with `port.gallery` link
- [ ] No placeholder URLs (`#`, `/gallery`, `mailto:`) remain

---

### **DEPRECATED Methods:**

**❌ v2.17.0 - PowerShell 18-Task Method:**
- Problem: AI stops midway, requires manual intervention
- Reason: Monolithic generation, no checkpoints
- Status: DEPRECATED as of v2.18.0

**❌ v2.16.0 - Single PowerShell Script:**
- Problem: 70% data loss (generic templates)
- Status: DEPRECATED as of v2.17.0

---

## ⚠️ CRITICAL: JSON Analysis Schema - PREVENT INFORMATION LOSS

### Problem: Analysis Detail Loss
**Issue:** AI analyzes in detail ("ship moves in 3D scroll animation") but simplifies in JSON ("3D animation")  
**Impact:** Integration JSON lacks implementation details → Generated code is incomplete

### Solution: Implementation-Ready Descriptions

**❌ FORBIDDEN: Abstract Classification**
```json
{
  "animation": {
    "type": "3d-canvas-animation",
    "description": "3D animation effect"
  }
}
```
→ Developer cannot implement this

**✅ REQUIRED: Concrete Implementation Details**
```json
{
  "animation": {
    "subject": "파란색 화물선과 빨간색 컨테이너 3개",
    "visualDescription": "Blue cargo ship body with 3 red containers on deck, white cabin",
    "observedBehavior": "스크롤 0-100% 구간에서 화면 왼쪽(-100px)에서 오른쪽(1500px)으로 수평 이동. 배 위 컨테이너가 2초 주기로 상하 미세 흔들림 (translateY: -5px ~ +5px)",
    "type": "3d-canvas-animation",
    "trigger": "scroll position 0-100%",
    "technicalImplementation": "Three.js GLTFLoader + GSAP ScrollTrigger { scrub: true }",
    "propertyChanges": "translateX: -100px → 1500px, translateY: -5px ↔ +5px (sine wave)",
    "codeHint": "gsap.to(shipMesh.position, { x: 15, scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1.5 } }); // + sine wave animation for containers"
  }
}
```
→ Developer can implement immediately

### 8-Field Documentation Template (MANDATORY)

For EVERY animation, interaction, or complex feature, include ALL 8 fields:

1. **subject** - "Container ship with cargo" (what is animating)
2. **visualDescription** - "Blue cargo ship with red containers" (visual appearance)
3. **observedBehavior** - "Ship travels left to right as user scrolls" (what happens)
4. **type** - "3d-canvas-animation" | "video-player" | "svg-path-animation" (technical category)
5. **trigger** - "scroll position 0-100%" | "hover" | "click" (what causes it)
6. **technicalImplementation** - "Three.js with ScrollTrigger" | "CSS 3D transforms" (how to build)
7. **propertyChanges** - "translateX: -100px → 1500px" | "opacity: 0 → 1" (CSS/JS changes)
8. **codeHint** - Pseudo-code or actual snippet (implementation example)

### Real-World Example Comparison

**❌ BAD (Abstract):**
```
Checkpoint 5 - Animation detected: 3D effect
```

**✅ GOOD (Concrete):**
```
=== CHECKPOINT 5 ===
🎬 ANIMATION DETECTION:
- Subject: 컨테이너 화물선 (파란색 선체 + 빨간색 컨테이너 3개 + 흰색 선실)
- Visual Description: Blue cargo ship body, 3 red containers stacked on deck, white cabin on top
- Observed Behavior: 스크롤 다운 시 왼쪽에서 오른쪽으로 수평 이동 (~1600px travel). 동시에 배 위 컨테이너가 2초 주기로 미세 상하 흔들림 (파도 효과)
- Trigger: scroll position 0% → 100% (hero section)
- Technical Details: Three.js scene with GLTF model + GSAP ScrollTrigger { scrub: true }
- Property Changes: 
  - translateX: -100px (left offscreen) → 1500px (right offscreen)
  - translateY: -5px ↔ +5px (sine wave, 2s period)
- Implementation Hint:
  ```javascript
  // Load ship model
  const loader = new GLTFLoader();
  loader.load('ship.gltf', (gltf) => {
    const ship = gltf.scene;
    
    // Scroll animation
    gsap.to(ship.position, {
      x: 15,
      scrollTrigger: {
        trigger: '.hero-section',
        start: 'top top',
        end: 'bottom top',
        scrub: 1.5
      }
    });
    
    // Container wave effect
    gsap.to(ship.children[0].position, {
      y: 0.5,
      duration: 2,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });
  });
  ```
```

### Checkpoint Logging Format (Updated)

```json
{
  "checkpoint": "5",
  "changeType": "structural|visual|animation",
  "detectedFeatures": [
    {
      "subject": "container ship with cargo",
      "visualDescription": "Blue cargo ship body, 3 red containers, white cabin",
      "observedBehavior": "Horizontal scroll-linked movement + vertical wave motion",
      "type": "3d-canvas-animation",
      "trigger": "scroll position 0-100%",
      "technicalImplementation": "Three.js GLTFLoader + GSAP ScrollTrigger",
      "propertyChanges": "translateX(-100px → 1500px), translateY(-5px ↔ +5px)",
      "codeHint": "gsap.to(shipMesh.position, { x: 15, scrollTrigger: { scrub: true } }) + sine wave"
    }
  ]
}
```

---

## Common Principles

### 1. Input Validation
- **Required:** `sitePurpose`, `targetAudience`, `brandGuide`
- **Optional:** If missing, insert `"AI-Default"`

### 2. MCP Integration (Site Exploration)
- Navigate → Explore interactions → Screenshot → Log evidence

### 3. Image Handling - Smart Policy

**⚠️ Distinguish between functional images and decorative images**

#### 🔧 Functional Images (Use Exact JSON Path)
**When to use exact path:**
- 3D canvas textures, materials, or assets
- Video thumbnails and poster images
- Interactive diagrams with animations
- Document viewers (Bill of Lading, etc.)
- SVG graphics with specific animations
- UI mockups showing specific screens

**Examples:**
```json
// JSON: 3D animation texture
{ "visual": { "type": "3d-canvas-animation", "texture": "/images/container.png" }}
→ HTML: <img src="/images/container.png" />

// JSON: Video thumbnail
{ "video": true, "videoThumbnail": "/images/video-thumb.jpg" }
→ HTML: <video poster="/images/video-thumb.jpg">
```

#### 🎨 Decorative Images (Use Picsum Placeholder)
**When to use picsum.photos:**
- Company/partner logos
- Product photos in cards
- Team member portraits
- Testimonial avatars
- General illustrations
- Background images (without specific animation requirements)

**Examples:**
```json
// JSON: Product card image
{ "illustration": "/images/truck-warehouse.svg" }
→ HTML: <img src="https://picsum.photos/seed/truck-warehouse/400/300" />

// JSON: Logo
{ "logo": { "src": "/logos/company.svg" }}
→ HTML: <img src="https://picsum.photos/seed/company-logo/200/100" />

// JSON: Portrait
{ "photo": "/images/testimonials/person.jpg" }
→ HTML: <img src="https://picsum.photos/seed/person-name/300/300" />
```

#### Decision Flow:
```
1. Check parent component type:
   - If type includes: "3d-*", "video", "interactive-*", "document-*" 
     → Use exact JSON path
   
2. Check for animation properties:
   - If image has: animation, transform, parallax properties
     → Use exact JSON path
   
3. Otherwise (simple cards, logos, portraits, illustrations):
   → Use picsum placeholder
```

#### Rationale:
- Functional images are critical to features → must match specification
- Decorative images are for visual layout → placeholders are acceptable
- This balances specification accuracy with practical implementation

### 3.1. Complex Feature Implementation - MANDATORY FULL IMPLEMENTATION

**⚠️ ABSOLUTE RULE: All features in integration JSON must be fully implemented**

#### No Simplification Allowed:
- ❌ **FORBIDDEN:** Replacing 3D animations with static placeholders
- ❌ **FORBIDDEN:** Replacing videos with images
- ❌ **FORBIDDEN:** Replacing SVG diagrams with plain divs
- ❌ **FORBIDDEN:** Omitting interactive behaviors
- ✅ **REQUIRED:** Implement exactly as specified in JSON

#### Feature Implementation Requirements:

| JSON Specification | Required Implementation |
|-------------------|------------------------|
| `"type": "3d-canvas-animation"` | **Three.js MANDATORY** (NO CSS 3D transforms) |
| `"type": "video"` | HTML5 `<video>` element with controls |
| `"type": "interactive-diagram"` | SVG with actual paths and animations |
| `"animation": "parallax-scroll"` | GSAP ScrollTrigger + CSS initial state |
| `"connectionStyle": "dotted-svg-paths"` | Generate actual SVG `<path>` elements |
| `"video": true` | Full video player implementation |

#### Library Integration Policy:
```html
<!-- If JSON specifies GSAP animations -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

<!-- If JSON specifies 3D graphics - MANDATORY Three.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/GLTFLoader.js"></script>

<!-- Always include libraries mentioned in JSON's "animations" or "framework" fields -->
```

#### ⚠️ CRITICAL: Animation Implementation Rules

**1. 3D Animations → MANDATORY Three.js**

❌ **FORBIDDEN:**
- CSS 3D transforms for complex 3D scenes
- Canvas 2D API for 3D objects
- SVG for 3D models

✅ **REQUIRED:**
- Use Three.js for ALL 3D animations
- Use GLTFLoader for 3D models
- Proper scene, camera, renderer setup

**2. GSAP Animations → MANDATORY CSS Initial State**

❌ **FORBIDDEN:**
- Setting initial state in GSAP `.from()` only
- Relying on JavaScript for initial positioning
- No CSS fallback for non-JS users

✅ **REQUIRED:**
- Set initial state in CSS classes (opacity: 0, transform: translateY(50px))
- Use GSAP only for transitions/animations
- Ensure graceful degradation without JavaScript

**Example CSS for GSAP:**
```css
.gsap-fade-in { opacity: 0; transform: translateY(50px); }
.gsap-slide-left { opacity: 0; transform: translateX(-100px); }
.gsap-scale-in { opacity: 0; transform: scale(0.8); }
```

**3. 3D Asset Sources → MANDATORY Free Downloads**

When 3D models are required, download from these sources (in priority order):

1. **Sketchfab** (https://sketchfab.com/) - Filter: "Downloadable", Format: GLTF/GLB
2. **Poly Haven** (https://polyhaven.com/) - 100% CC0, Format: GLTF/FBX/OBJ
3. **Free3D** (https://free3d.com/) - Filter: Free models, Format: GLTF/OBJ/FBX
4. **CGTrader Free** (https://www.cgtrader.com/free-3d-models) - Filter: Free, Royalty Free

**Asset Organization:**
```
output/web/assets/3d/
├── ship.gltf
├── container.gltf
├── planet.gltf
└── README.md  (attribution list)
```

**Example Code with Asset:**
```html
<script>
// Model: "Cargo Ship" by [Author] on Sketchfab
// License: CC BY 4.0
const loader = new THREE.GLTFLoader();
loader.load('/assets/3d/ship.gltf', (gltf) => {
  const model = gltf.scene;
  scene.add(model);
});
</script>
```

#### Verification Checklist:
- [ ] Every visual element from JSON is rendered
- [ ] All animations from JSON are implemented
- [ ] All interactive behaviors function correctly
- [ ] No "placeholder" divs replacing complex features
- [ ] All specified libraries are included via CDN

### 4. Accessibility
- **Web:** WCAG 2.1 AA (4.5:1 contrast, keyboard nav, alt text)

---

## Execution Workflow

### Web Pipeline (Updated: Auto-Stop After Analysis)

**Command: `/web [input]`**
```
Step 1: Browser exploration (MCP Kapture)
  ↓
Step 2: Analyze content → OVERWRITE 01_contents_web.json
  ↓
Step 3: Extract style → OVERWRITE 02_style_web.json
  ↓
⚠️ AUTO-STOP HERE ⚠️
Output: "✅ 분석 완료. 통합이 필요하면 /integrate를 입력하세요."
```

**Command: `/integrate` (Manual Request Only)**
```
Step 4: Execute PowerShell merge script
  ↓
  Command: powershell -ExecutionPolicy Bypass -File "scripts\integrate_web_pipeline.ps1"
  ↓
  Script performs:
    - Load 01_contents_web.json + 02_style_web.json
    - Merge all sections (full data preservation)
    - Add animations, designTokens, responsive, accessibility, seo
    - Write 03_integrate_web.json
    - Auto-validate (ranges, codeHints, colors)
  ↓
  Expected output:
    - File size: 1200-1500 lines
    - Validation: PASSED (all checks green)
  ↓
⚠️ AUTO-STOP HERE ⚠️
Output: "✅ 통합 완료 (1229 lines, validation PASSED). 코드 생성이 필요하면 /generate를 입력하세요."
```

**⚠️ CRITICAL: DO NOT use Section-by-Section manual generation**

**Why PowerShell script is mandatory:**
- AI token limit causes 70% data loss when writing JSON directly
- Script preserves 100% of original data (1229 lines vs AI's 392 lines)
- Script handles all validation automatically

**If script fails:**
1. Check script exists: `scripts\integrate_web_pipeline.ps1`
2. Check source files exist: `01_contents_web.json`, `02_style_web.json`
3. Report error to user with full error message
4. Do NOT attempt manual JSON generation as fallback


**⚠️ CRITICAL: `/integrate` No Simplification Policy**

When merging `01_contents_web.json` + `02_style_web.json` into `03_integrate_web.json`:

❌ **FORBIDDEN Operations:**
1. **Range Simplification**: `"60-72px"` → `"72px"` (단일값 변환)
2. **Detail Removal**: Deleting `codeHint`, `propertyChanges`, `technicalImplementation` fields
3. **Color Generalization**: `"#FF6635"` → `"orange"` (구체적 → 추상적)
4. **Animation Loss**: Removing GSAP/Three.js code snippets
5. **Property Omission**: Skipping any field present in source JSONs

✅ **REQUIRED Operations:**
1. **Preserve Ranges**: Keep `"60-72px"`, `"48-56px"` as-is (ranges stay ranges)
2. **Merge 8-Field Templates**: All animation fields must be included
   - `subject`, `visualDescription`, `observedBehavior`
   - `type`, `trigger`, `technicalImplementation`
   - `propertyChanges`, `codeHint`
3. **Exact Color Values**: Use hex codes from source (`#FF6635`, not "primary-orange")
4. **Code Preservation**: Include all implementation hints from 01/02
5. **Context Addition**: Add page-level organization, but don't remove details

**Validation Rule:**
- After generating `03_integrate_web.json`, AI must verify:
  - Field count in 03 ≥ Field count in (01 + 02)
  - All `codeHint` fields present
  - All color hex values preserved
  - All font size ranges maintained

**Command: `/generate` (Manual Request Only)**
```
Step 5: Component-Based 3-Pass Generation
  ↓
Phase 1: Foundation Setup
  - Generate TypeScript interfaces from 03_integrate_web.json
  - Create component structure document (sections → components mapping)
  - Create docs/ui_rules.md (implementation rules)
  ↓
Phase 2: Component Generation (Per Section)
  For EACH section in 03_integrate_web.json.sections:
    Pass 1: JSX Structure + Data Mapping
      → Create component file with basic structure
      → Map all JSON fields to JSX elements
      → Output: "✅ Pass 1/3 완료 (뼈대). 계속할까요?"
      → WAIT for user confirmation
    
    Pass 2: Tailwind Styling
      → Add Tailwind classes based on section.style
      → Apply responsive breakpoints (mobile → desktop)
      → Convert ranges (60-72px → text-6xl md:text-7xl)
      → Output: "✅ Pass 2/3 완료 (스타일링). 계속할까요?"
      → WAIT for user confirmation
    
    Pass 3: Validation + codeHint Insertion
      → Verify all JSON fields are mapped
      → Insert codeHints verbatim (NO interpretation)
      → Output validation checklist
      → Output: "✅ Pass 3/3 완료 (검증). HeroSection 완료! 다음 컴포넌트로 진행할까요?"
      → WAIT for user confirmation
  ↓
Phase 3: Assembly
  - Generate pages/index.tsx (import and render all components)
  - Generate components/AnimationLoader.tsx (collect all codeHints, load libraries)
  - Final validation (17+ files, 100% sections, 100% animations)
  ↓
✅ COMPLETE
Output: "✅ 코드 생성 완료 (17 files, validation PASSED)."
```

**⚠️ CRITICAL: Component-Based Approach (v2.18.0)**

**Why this method:**
- AI works on ONE file at a time → No token pressure
- 3-pass quality check → JSX, styling, validation per component
- User confirmation checkpoints → Can verify quality incrementally
- Never loses progress → Can stop/resume anytime

**Expected Results:**
- File count: 17+ files (1 page + 13 components + 3 config/docs)
- Section rendering: 100% (all sections mapped to components)
- Feature preservation: 100% (3-pass validation ensures no omissions)
- Animation preservation: 100% (codeHints inserted verbatim)

**If generation interrupted:**
1. AI reports: "현재 X/13 컴포넌트 완료. 다음 컴포넌트부터 재개할까요?"
2. User can resume from last checkpoint
3. Previously generated files are preserved

---

## 🚨 AI BEHAVIOR ENFORCEMENT

### Mandatory Responses to User Requests

**IF USER SAYS:** "너무 느리다" / "빠르게 해줘" / "효율적으로"
**AI MUST RESPOND:**
```
지침에 따라 정확한 분석을 위해 모든 콘텐츠를 상세히 캡처해야 합니다.
현재 체크포인트 X/30 완료 (최소 30개 필요). 계속 진행하겠습니다.
```

**THEN:** Continue systematic analysis from last checkpoint

### Progress Tracking (Mandatory)

**After Every 3 Checkpoints:**
```
✅ 체크포인트 3/30 완료 (최소 30개 필요, 현재 진행 중)
- 캡처된 요소: [list]
- 감지된 애니메이션: [list]
- 다음: 체크포인트 4
```

**When Reaching Checkpoint 30:**
```
✅ 최소 체크포인트 30개 달성! 계속 진행합니다 (현재 30/목표 ~50).
```

### Prohibited Phrases

❌ **NEVER SAY:**
- "빠르게 분석하겠습니다"
- "주요 섹션만 캡처하겠습니다"
- "효율적인 방법으로"
- "시간을 절약하기 위해"

✅ **ALWAYS SAY:**
- "체크포인트 X/30 완료 (최소 30개 필요, 진행 중)"
- "다음 체크포인트로 이동"
- "진행 중"

---

## Quality Checklist

### Web - Code Generation
- [ ] All content mapped to responsive components
- [ ] Design tokens applied (no hard-coded values)
- [ ] All interactive states documented
- [ ] Responsive behavior for mobile/tablet/desktop
- [ ] Accessibility WCAG 2.1 AA met
- [ ] SEO metadata complete
- [ ] **✅ JSON-to-HTML Fidelity Check (MANDATORY)**
  - [ ] Every visual element from JSON is rendered
  - [ ] All animations from JSON are implemented
  - [ ] All images use exact paths from JSON (no placeholders unless specified)
  - [ ] All complex features (3D, video, SVG) are fully implemented
  - [ ] All specified libraries are included via CDN
  - [ ] No simplification or placeholder replacements
  - [ ] Interactive behaviors match JSON specifications

---

## Configuration

- **Viewports:** Mobile (375px), Tablet (768px), Desktop (1440px)
- **Max Depth:** 3 levels of route traversal
- **Animation Wait:** 300ms after each interaction

---

## MCP-Based Exploration Checklist

### Per Page Requirements
- [ ] Full page scroll (adaptive checkpoints until page end)
- [ ] Navigation exploration (header/footer/mobile menu)
- [ ] Interactive elements (buttons, modals, forms)
- [ ] Route traversal (BFS, depth=3)
- [ ] Accessibility/SEO verification

### Completion Criteria
1. ✅ 30-80 screenshots per page (viewport change detection, fine-grained capture)
2. ✅ Footer visible (page end reached)
3. ✅ All interactive elements tested (minimum 50+ total interactions)
4. ✅ All animation frames captured
5. ✅ Route map complete
6. ✅ Evidence logged in analysis files

---

## Version History

- **v2.20.0** (2025-01-17): Default Link Configuration for Harufolio Project
  - **CRITICAL:** Added mandatory default URL configuration for all generated code
  - **Problem:** Generated code used placeholder URLs (#, /gallery, /contact) instead of actual project URLs
    - Social links pointed to generic placeholders
    - Gallery/portfolio links were relative paths
    - Contact links used mailto: instead of company website
    - Footer credits missing or incomplete
  - **Solution:** Mandatory link mapping table with auto-detection rules
    - Social → `https://instagram.com/haru_folio`
    - Gallery/Portfolio → `https://port.gallery`
    - Contact/Company → `https://rebornsolution.com`
    - Footer credit → "built by harufolio" with `port.gallery` link
  - **Implementation:**
    - Added link mapping table with 4 categories
    - Created implementation rules with correct/wrong examples
    - Auto-detection logic for link type identification
    - Validation checklist before code completion
    - Footer credit mandatory insertion
  - **Expected Results:**
    - 100% working links (no placeholders remain)
    - Footer credit on every generated page
    - Consistent branding across all projects
  - **Impact:** Eliminates manual link correction, ensures all generated sites have working navigation from day 1
- **v2.19.0** (2025-01-17): Quantitative Checkpoint Comparison System
  - **CRITICAL:** Added element position tracking and quantitative movement analysis
  - **Problem:** Previous checkpoints used qualitative descriptions ("moved slightly", "shifted positions")
    - No pixel-level measurements for movement detection
    - No stored position data for frame-by-frame comparison
    - Impossible to generate accurate animation specifications
  - **Solution:** Position tracking system with Map-based storage
    - Extract boundingBox (x, y, width, height) for all visible elements
    - Store positions in `previousElementPositions` Map
    - Calculate deltas (ΔX, ΔY, ΔWidth, ΔHeight) between checkpoints
    - Log significant movements (>5px threshold) in checkpoint header
    - Store complete checkpoint data (screenshot + positions + timestamp) for future reference
  - **New Fields in Checkpoint Header:**
    - `📊 QUANTITATIVE COMPARISON (vs Checkpoint X):`
    - Per-element movements: `selector: ΔX=+20px, ΔY=-10px`
    - Total tracked elements count
    - Elements moved count
  - **Implementation Details:**
    - Step 0: Initialize `checkpointData[]` and `previousElementPositions` Map
    - Step 0: Extract initial positions from `el.boundingBox`
    - Step 2: Extract current positions for all visible elements
    - Step 4-1: Calculate movement deltas and generate comparison log
    - Step 4-6: Update `previousElementPositions` and store checkpoint data
  - **Expected Results:**
    - Accurate pixel measurements: "ship-left: ΔX=-20px, ΔY=+10px"
    - Animation speed calculations: "Element moved 150px over 3 checkpoints = 50px/checkpoint"
    - Parallax layer detection: "Layer 1: ΔY=10px, Layer 2: ΔY=25px → 2.5x speed ratio"
    - Viewport change coverage: "120/150 elements tracked consistently across checkpoints"
  - **Impact:** Enables precise animation specifications, eliminates guesswork in movement descriptions, provides data-driven insights for code generation
- **v2.18.0** (2025-01-16): Component-Based 3-Pass Generation (RECOMMENDED)
  - **CRITICAL:** Replaced PowerShell monolithic generation with incremental component approach
  - **Problem:** v2.17.0 PowerShell 18-Task method caused AI to stop midway
    - Root cause: Single long-running process, AI requests user confirmation between tasks
    - Result: 50% completion rate, requires manual intervention to continue
  - **Solution:** Component-Based 3-Pass Generation (inspired by best practices)
    - Phase 1: Foundation (TypeScript types + component structure + UI rules)
    - Phase 2: Per-Component Generation (3 passes per section: JSX → Tailwind → Validation)
    - Phase 3: Assembly (main page + animation loader + final validation)
  - **Key Improvements:**
    - ✅ File-level context focus → Improved code quality per component
    - ✅ 3-pass quality check → JSX structure, styling, JSON validation per component
    - ✅ User confirmation checkpoints → After each component completion
    - ✅ Incremental progress → Never lose work, can stop/resume anytime
    - ✅ Type safety → TypeScript interfaces from JSON schema
  - **Expected Results:**
    - File count: 17+ files (1 page + 13 components + 3 config/docs)
    - Section rendering: 100% (all sections mapped to components)
    - Feature preservation: 100% (3-pass validation ensures no field omitted)
    - Animation preservation: 100% (codeHints inserted verbatim in Pass 3)
    - Type safety: 100% (TypeScript interfaces prevent runtime errors)
  - **Workflow Changes:**
    - Updated "04-0. HTML Generation Method" with Component-Based approach
    - Created `docs/ui_rules.md` (JSON-to-Component implementation rules)
    - Added Phase 1-3 execution model with user confirmation
    - Marked v2.17.0 PowerShell 18-Task as "DEPRECATED"
  - **Impact:** Eliminates AI stopping issues, ensures 100% completion rate, improves maintainability
- **v2.17.0** (2025-01-16): Incremental Template Building - A-1 Complete Segmentation Method (DEPRECATED)
  - **CRITICAL:** Replaced single PowerShell script with 18-task sequential execution
  - **Problem:** v2.16.0 PowerShell script still caused 70% data loss (1229 → 367 lines)
    - Root cause: Generic templates couldn't handle complex JSON structures
    - Example: 3D Planet Parallax completely omitted, Step Cards content missing
  - **Solution:** Complete section-by-section template builder approach
    - Phase 1: Helper functions (Get-NestedProperty, ConvertTo-TailwindClass, Render-HtmlElement)
    - Phase 2: 13 dedicated section renderers (Hero, Feature, Workflow, etc.)
    - Phase 3: Animation script builder + UTF-8 encoding fix + final integration
  - **Task Execution Model:**
    - AI executes all 18 tasks sequentially WITHOUT user intervention
    - manage_todo_list tracks progress automatically
    - NO pausing between tasks (continuous execution)
    - Report "✅ Task X/18 complete" after each task
  - **Expected Results:**
    - File size: 2000-4000 lines (full complexity preserved)
    - Section rendering: 100% (all 14 sections with complete content)
    - Feature preservation: 95%+ (3D visuals, code previews, step cards all included)
    - Animation preservation: 100% (all codeHints inserted verbatim)
    - Text accuracy: 100% (UTF-8 encoding fixed)
  - **Workflow Changes:**
    - Updated "04-0. HTML Generation Method" with A-1 methodology
    - Added mandatory task sequence (Tasks 1-18)
    - Added execution rules (auto-proceed, no user confirmation)
    - Marked v2.16.0 single-script approach as "DEPRECATED"
  - **Impact:** Eliminates all remaining data loss, achieves 95%+ original site fidelity
- **v2.16.0** (2025-01-16): PowerShell HTML Generator (DEPRECATED - See v2.17.0)
  - **CRITICAL:** Replaced AI-based HTML generation with PowerShell template script
  - **Root Cause:** AI token limit causes animation/interaction loss during HTML generation
    - Example: Complex animations, GSAP/Three.js snippets omitted
    - Section-by-Section approach still simplified codeHints and complex features
  - **Solution:** `scripts/generate_html.ps1` performs template-based HTML generation
    - Loads 03_integrate_web.json as PowerShell object
    - Applies type-specific templates (hero, features, steps, cta, footer)
    - Inserts codeHints directly without AI interpretation
    - Auto-detects and includes required libraries (GSAP, Three.js)
    - Auto-validates section count, animation count, library includes
  - **Results:** 1500-3000 lines HTML (depends on complexity)
    - Section preservation: 100% (all sections rendered with full styles)
    - Animation preservation: 100% (all codeHints inserted verbatim)
    - Library inclusion: Auto-detected based on animation types
  - **Workflow Changes:**
    - Updated "04. Code Generation" method: Section-by-Section → PowerShell script
    - Updated Execution Workflow: `/generate` now executes PowerShell command
    - Deleted "📐 HTML Generation Workflow" section (150+ lines, now obsolete)
    - Marked old method as "DEPRECATED - DO NOT USE"
  - **Impact:** Eliminates all HTML generation data loss, ensures full feature implementation
- **v2.15.0** (2025-01-16): PowerShell Integration Pipeline (CRITICAL FIX)
  - **CRITICAL:** Replaced AI-based JSON generation with PowerShell merge script
  - **Root Cause:** AI token limit (4K-8K) caused 70% data loss during integration
    - Example: 01_contents (781 lines) + 02_style (586 lines) → AI output (392 lines)
    - Lost data: stepCards details, codeHint fields, fontSize ranges, color hex values
  - **Solution:** `scripts/integrate_web_pipeline.ps1` performs object-level merging
    - Loads JSON as PowerShell objects (ConvertFrom-Json)
    - Merges without AI involvement: `$section + $style[$section.id]`
    - Writes with full preservation (ConvertTo-Json -Depth 100)
    - Auto-validates: ranges, codeHints, colors
  - **Results:** 1229 lines (vs AI's 392 lines, 213% increase)
    - codeHint preservation: 16/16 (100%, vs AI's 8/16)
    - Range preservation: 34 ranges (vs AI's 1)
    - Color preservation: 74 hex values (vs AI's 37)
  - **Workflow Changes:**
    - Updated "03. Web Integration" method: Section-by-Section → PowerShell script
    - Updated Execution Workflow: `/integrate` now executes PowerShell command
    - Marked old method as "DEPRECATED - DO NOT USE"
  - **Impact:** Eliminates all integration data loss, ensures developer-implementable specifications
- **v2.14.0** (2025-01-16): Section-by-Section Integration - Token Limit Workaround (DEPRECATED)
  - **NOTE:** This version is now DEPRECATED - see v2.15.0 for PowerShell solution
  - ~~Restructured `/integrate` command to use incremental file generation~~
  - ~~Problem: AI token limit caused truncation/syntax errors in 2000+ line JSON files~~
  - ~~Solution: Section-by-Section generation with progress tracking~~ (Failed - 70% data loss)
  - **Root Issue:** AI still simplified internal fields despite incremental approach
- **v2.13.0** (2025-01-16): Integration Validation System + No Simplification Policy (SUPERSEDED by v2.15.0)
  - **NOTE:** This version is now SUPERSEDED - v2.15.0 PowerShell script handles validation automatically
  - ~~Added mandatory validation after `/integrate` command execution~~ (Now done by script)
  - **No Simplification Policy (Still Valid):**
    - Added 5 FORBIDDEN operations (range simplification, detail removal, color generalization, animation loss, property omission)
    - Added 5 REQUIRED operations (preserve ranges, merge 8-field templates, exact colors, code preservation, context addition)
  - ~~Auto-Validation Logic~~ (Now in PowerShell script)
  - ~~AI Output Format~~ (Script outputs validation results)
  - ~~Enforcement: If validation fails, AI must regenerate~~ (Script handles retry logic)
  - **Impact:** Principles remain valid, but implementation moved to PowerShell script
- **v2.12.0** (2025-01-16): File Writing Method Standardization - Encoding Fix
  - **CRITICAL:** Replaced all `appendToAnalysisNote()` calls with `replace_string_in_file` tool
  - **Reason:** PowerShell's `echo` command causes UTF-16 encoding issues (fullwidth space corruption)
  - **Changes:**
    - Step 4-1: Added explicit warning about PowerShell echo
    - Step 4-2: Changed to replace_string_in_file
    - Step 4-3: Changed to replace_string_in_file (both animation paths)
    - Step 4-5: Changed to replace_string_in_file
  - **Result:** All checkpoint logs now written with correct UTF-8 encoding
  - **Impact:** Fixes "= = =   C H E C K P O I N T" corruption issue permanently
- **v2.11.0** (2025-01-16): Checkpoint Completion Enforcement + Extended Behavioral Triggers
  - **CHECKPOINT COMPLETION ENFORCEMENT:** Added mandatory output template after each checkpoint
  - **Self-Check Questions:** Added 6-item verification list before moving to next checkpoint
  - **Behavioral Triggers:** Added 4 new forbidden phrases from actual violation logs
    - "이 속도로는 시간이 많이 걸릴 것 같으므로..."
    - "진행 속도를 높이겠습니다..."
    - "한 번에 더 많은..."
    - "더 많은 스크롤이 필요합니다..."
  - **Progressive Scroll:** Clarified "ArrowDown ONLY" and "ALL 6 steps per checkpoint"
  - **Reason:** v2.10.0 test showed AI still skipped Step 4 sub-steps despite guidelines
  - **Result:** Forces AI to output completion checklist, self-verify before proceeding
- **v2.10.0** (2025-01-16): Critical Enforcement Update - PageDown Prevention
  - **ABSOLUTE PROHIBITIONS:** Updated item #5 to explicitly list all forbidden keys
  - **EXECUTION VALIDATION:** Rewrote validateScrollCommand with Step 1-2 pre-execution check
  - **Behavioral Triggers:** Added 5 new forbidden phrases ("효율적으로 분석", "더 큰 간격으로")
  - **Step 4:** Added "CANNOT BE SKIPPED" header with ⚠️ ALL 6 SUB-STEPS ARE MANDATORY
  - **Step 4-4:** Added "(필수 단계)" to console log, "⚠️ THIS STEP IS INTEGRATED" warning
  - **Completion Criteria:** Changed from text to code block with ❌ NEVER USE examples
  - **ENFORCEMENT RULES:** Updated progress reporting format to "X/30"
  - **Reason:** v2.9.0 test showed AI still used PageDown despite guidelines (15+ violations)
  - **Result:** Forces AI to validate BEFORE every keypress, blocks PageDown at decision point
- **v2.9.0** (2025-01-16): Real-Time File Append Architecture
  - **Critical:** Restructured Step 4 to prioritize file writes over memory operations
  - Changed from single large write to progressive append operations (4-1 → 4-2 → 4-3 → 4-4 → 4-5)
  - File write sequence: Header → Visual Analysis → Animation → Interaction Test → Results
  - Each analysis component writes immediately after completion (no batching)
  - Removed Steps 5-6 (consolidated into Step 4's append operations)
  - **Result:** Ensures checkpoint data persists incrementally, prevents memory overflow, enables real-time progress monitoring
  - **Reason:** Large pages (100+ checkpoints) caused memory issues with batch writes
- **v2.8.0** (2025-01-15): Real-Time Analysis Logging & Concrete Documentation
  - **Critical:** Added 00_analysis_note.txt real-time logging system
  - Integrated checkpoint-by-checkpoint documentation into Progressive Scroll Analysis
  - Added mandatory 8-field template for animations/interactions (subject, visualDescription, observedBehavior, type, trigger, technicalImplementation, propertyChanges, codeHint)
  - Updated Pipeline Details: 01_contents and 02_style now read from 00_analysis_note.txt
  - Added concrete vs abstract examples to prevent information loss
  - Enhanced JSON schema with implementation-ready descriptions
  - **Result:** Prevents detail loss from analysis to JSON generation, ensures developer-implementable specifications
  - **Reason:** Previous system lost critical implementation details during JSON generation phase
- **v2.7.0** (2025-01-14): Documentation Optimization & Deduplication
  - **Critical:** Reduced file size from 1057 lines to 773 lines (27% reduction)
  - Removed 150+ lines of verbose JSON examples while preserving core templates
  - Consolidated redundant workflow descriptions (Phase 1-3 simplified)
  - Streamlined Tailwind conversion table (removed verbose mappings)
  - Removed duplicate "User Input Format" examples
  - **Result:** Maintains complete functionality with improved readability
  - **Reason:** 1000+ line file was difficult to navigate, contained excessive examples
- **v2.6.0** (2025-01-14): Interaction Testing Enforcement - Pipeline Fix
  - **Critical:** Moved interaction testing from Step 5 to Step 4 (integrated, cannot skip)
  - Added testedCount counter and console logging for transparency
  - Updated logging format: `interactionsTested.count` + `interactionsTested.elements`
  - Renumbered steps: 1-4 (integrated), 5 (logging), 6 (next checkpoint)
  - **Result:** Forces AI to test 10 interactions per checkpoint = 300-800 total tests
  - **Reason:** v2.5.0 test showed AI skipped all interactions (5/50 = 10%)
- **v2.5.0** (2025-01-14): Runtime Enforcement & Minimum Checkpoint Validation
  - Added validateScrollCommand() auto-detection system (EXECUTION VALIDATION)
  - Added MIN_CHECKPOINTS = 30 constant with validation logic
  - Enhanced PROGRESS REPORTING with "X/30" format and milestone messages
  - Added Behavioral Triggers detection (AI self-check before deviation)
  - Updated Completion Criteria to explicitly reject analysis with < 30 checkpoints
  - Strengthened ENFORCEMENT RULES to prevent PageDown/End key usage
  - **Result:** Forces AI to complete minimum 30 checkpoints, prevents premature shortcuts
- **v2.4.0** (2025-01-14): High-Fidelity Scroll Analysis System
  - Changed from fixed 21 checkpoints to adaptive 30-80 checkpoints
  - Implemented ArrowDown-based fine-grained scrolling (150-300px increments)
  - Added structural + visual change detection (dual-mode)
  - Implemented animation frame capture (3-5 frames per section transition)
  - Added screenshot hash comparison for visual changes
  - Updated all related sections (ABSOLUTE PROHIBITIONS, ENFORCEMENT RULES, MCP Checklist)
  - Expected result: 3-4x more detailed analysis with complete animation coverage
- **v2.3.0** (2025-11-11): Added HTML Generation Workflow (DEPRECATED in v2.16.0)
  - **NOTE:** This version is now DEPRECATED - see v2.16.0 for PowerShell solution
  - ~~Step-by-step section-based generation strategy~~ (Replaced by PowerShell script)
  - ~~Todo list planning and progress tracking~~ (No longer needed)
  - ~~JSON-to-HTML mapping guidelines~~ (Automated by template engine)
  - ~~Tailwind conversion reference table~~ (Automated by script)
  - **Root Issue:** AI token limit caused feature simplification during HTML generation
- **v2.2.0** (2025-11-11): Updated auto-stop behavior
  - `/web` command now auto-stops after analysis (01_contents + 02_style)
  - `/integrate` command requires manual request
  - `/generate` command requires manual request
  - Improved user control over pipeline execution
- **v2.1.0** (2025-11-11): Fixed JSON-to-HTML fidelity issues
  - Added CRITICAL_POLICY for image handling (use exact paths)
  - Added FULL_IMPLEMENTATION mode for complex features
  - Updated generator configs (04_generate_html.json, 04_generate_tailwind.json)
  - Added mandatory verification checklist
  - Removed "minimal dependencies" constraint for complex features
- **v2.0.0** (2025-11-07): Separate pipelines, no shared analysis
- **v1.0.0** (2025-11-07): Initial modular architecture
