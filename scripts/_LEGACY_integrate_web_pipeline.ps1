# ============================================================
# Web Pipeline Integration Script
# Purpose: Merge 01_contents_web.json + 02_style_web.json
# Method: Direct JSON object merging (no AI simplification)
# ============================================================

Write-Host "`n=== Web Pipeline Integration Started ===`n" -ForegroundColor Cyan

# 1. Load source files
Write-Host "Step 1: Loading source files..." -ForegroundColor Yellow
$contentsPath = "analysis\web-pipeline\01_contents_web.json"
$stylePath = "analysis\web-pipeline\02_style_web.json"
$outputPath = "analysis\web-pipeline\03_integrate_web.json"

if (-not (Test-Path $contentsPath)) {
    Write-Host "ERROR: $contentsPath not found" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $stylePath)) {
    Write-Host "ERROR: $stylePath not found" -ForegroundColor Red
    exit 1
}

$contents = Get-Content $contentsPath -Raw | ConvertFrom-Json
$style = Get-Content $stylePath -Raw | ConvertFrom-Json

Write-Host "  ✓ 01_contents_web.json loaded ($($contents.sections.Count) sections)" -ForegroundColor Green
Write-Host "  ✓ 02_style_web.json loaded" -ForegroundColor Green

# 2. Create integrated structure
Write-Host "`nStep 2: Creating integrated structure..." -ForegroundColor Yellow

$integrated = @{
    metadata = @{
        projectName = $contents.metadata.title
        generatedAt = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        sourceFiles = @("01_contents_web.json", "02_style_web.json")
        url = $contents.metadata.url
        description = $contents.metadata.description
    }
    sections = @()
    animations = @{}
    designTokens = @{}
    responsive = @{}
    accessibility = @{}
    seo = @{}
}

# 3. Merge each section with style data
Write-Host "`nStep 3: Merging sections with style data..." -ForegroundColor Yellow

foreach ($section in $contents.sections) {
    $sectionId = $section.id
    Write-Host "  Processing: $sectionId" -ForegroundColor Gray
    
    # Convert section to hashtable for manipulation
    $sectionHash = @{}
    $section.PSObject.Properties | ForEach-Object {
        $sectionHash[$_.Name] = $_.Value
    }
    
    # Add style data if exists
    if ($style.components.PSObject.Properties.Name -contains $sectionId) {
        $sectionHash["style"] = $style.components.$sectionId
    }
    
    # Add to integrated sections
    $integrated.sections += $sectionHash
}

Write-Host "  ✓ Merged $($integrated.sections.Count) sections" -ForegroundColor Green

# 4. Add global style data
Write-Host "`nStep 4: Adding global style data..." -ForegroundColor Yellow

# Animations
if ($style.PSObject.Properties.Name -contains "animations") {
    $integrated.animations = $style.animations
    Write-Host "  ✓ Added animations" -ForegroundColor Green
}

# Design Tokens
if ($style.PSObject.Properties.Name -contains "designTokens") {
    $integrated.designTokens = $style.designTokens
    Write-Host "  ✓ Added designTokens" -ForegroundColor Green
}

# Responsive
if ($style.PSObject.Properties.Name -contains "responsive") {
    $integrated.responsive = $style.responsive
    Write-Host "  ✓ Added responsive breakpoints" -ForegroundColor Green
}

# Accessibility
if ($style.PSObject.Properties.Name -contains "accessibility") {
    $integrated.accessibility = $style.accessibility
    Write-Host "  ✓ Added accessibility rules" -ForegroundColor Green
}

# SEO
$integrated.seo = @{
    title = $contents.metadata.title
    description = $contents.metadata.description
    keywords = "data infrastructure, AI data pipelines, automated testing, dbt, Airflow, data engineering"
    ogImage = "/images/og-image.jpg"
    favicon = "/favicon.ico"
}
Write-Host "  ✓ Added SEO metadata" -ForegroundColor Green

# 5. Write output file
Write-Host "`nStep 5: Writing integrated file..." -ForegroundColor Yellow

$json = $integrated | ConvertTo-Json -Depth 100 -Compress:$false
Set-Content -Path $outputPath -Value $json -Encoding UTF8

Write-Host "  ✓ File written: $outputPath" -ForegroundColor Green

# 6. Validation
Write-Host "`nStep 6: Validation..." -ForegroundColor Yellow

$contentsStr = Get-Content $contentsPath -Raw
$integratedStr = Get-Content $outputPath -Raw

$contentsRanges = ([regex]::Matches($contentsStr, '\d+-\d+px')).Count
$integratedRanges = ([regex]::Matches($integratedStr, '\d+-\d+px')).Count

$contentsCodeHints = ([regex]::Matches($contentsStr, '"codeHint"')).Count
$integratedCodeHints = ([regex]::Matches($integratedStr, '"codeHint"')).Count

$contentsColors = ([regex]::Matches($contentsStr, '#[0-9A-Fa-f]{6}')).Count
$integratedColors = ([regex]::Matches($integratedStr, '#[0-9A-Fa-f]{6}')).Count

$integratedLines = (Get-Content $outputPath).Count

Write-Host "`n=== VALIDATION RESULTS ===" -ForegroundColor Cyan
Write-Host "File size: $integratedLines lines" -ForegroundColor White
Write-Host ""

$rangePass = $integratedRanges -ge $contentsRanges
$codeHintPass = $integratedCodeHints -ge $contentsCodeHints
$colorPass = $integratedColors -ge $contentsColors

$rangeIcon = if ($rangePass) { "PASS" } else { "FAIL" }
$codeHintIcon = if ($codeHintPass) { "PASS" } else { "FAIL" }
$colorIcon = if ($colorPass) { "PASS" } else { "FAIL" }

Write-Host "Check 1 - Range values ($contentsRanges -> $integratedRanges): $rangeIcon" -ForegroundColor $(if ($rangePass) { "Green" } else { "Red" })
Write-Host "Check 2 - codeHint fields ($contentsCodeHints -> $integratedCodeHints): $codeHintIcon" -ForegroundColor $(if ($codeHintPass) { "Green" } else { "Red" })
Write-Host "Check 3 - Color hex values ($contentsColors -> $integratedColors): $colorIcon" -ForegroundColor $(if ($colorPass) { "Green" } else { "Red" })

Write-Host ""

if ($rangePass -and $codeHintPass -and $colorPass) {
    Write-Host "SUMMARY: VALIDATION PASSED" -ForegroundColor Green
    Write-Host ""
    Write-Host "Integration completed successfully!" -ForegroundColor Cyan
    Write-Host "Output: $outputPath ($integratedLines lines)" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    Write-Host "SUMMARY: VALIDATION FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Some data may have been lost during integration." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
