# ============================================================
# Presentation Pipeline Integration Script
# Purpose: Merge PDF style + URL content OR standalone content
# Method: Direct JSON object merging (no AI simplification)
# ============================================================

Write-Host "`n=== Presentation Pipeline Integration Started ===`n" -ForegroundColor Cyan

# 1. Determine input mode
Write-Host "Step 1: Detecting input mode..." -ForegroundColor Yellow

$contentPath = "analysis\presentation-pipeline\01_contents_slides.json"
$stylePath = "analysis\presentation-pipeline\02_style_theme.json"
$pdfStylePath = "analysis\pdf-analysis\bluehive_style_analysis.json"
$outputPath = "analysis\presentation-pipeline\03_integrate_presentation.json"

$mode = "unknown"

# Check which files exist
$hasContent = Test-Path $contentPath
$hasStyle = Test-Path $stylePath
$hasPdfStyle = Test-Path $pdfStylePath

if ($hasContent -and $hasStyle) {
    $mode = "content-and-theme"
    Write-Host "  Mode: Content + Theme (Standard)" -ForegroundColor Green
} elseif ($hasContent -and $hasPdfStyle) {
    $mode = "content-and-pdf"
    Write-Host "  Mode: Content + PDF Style" -ForegroundColor Green
} elseif ($hasPdfStyle) {
    $mode = "pdf-only"
    Write-Host "  Mode: PDF Style Only (Manual content needed)" -ForegroundColor Yellow
} else {
    Write-Host "  ERROR: No valid input files found" -ForegroundColor Red
    exit 1
}

# 2. Load source files based on mode
Write-Host "`nStep 2: Loading source files..." -ForegroundColor Yellow

$slides = $null
$theme = $null

switch ($mode) {
    "content-and-theme" {
        $contentJson = Get-Content $contentPath -Raw | ConvertFrom-Json
        $styleJson = Get-Content $stylePath -Raw | ConvertFrom-Json
        $slides = $contentJson.slides
        $theme = $styleJson
        Write-Host "  ✓ 01_contents_slides.json loaded ($($slides.Count) slides)" -ForegroundColor Green
        Write-Host "  ✓ 02_style_theme.json loaded" -ForegroundColor Green
    }
    "content-and-pdf" {
        $contentJson = Get-Content $contentPath -Raw | ConvertFrom-Json
        $pdfJson = Get-Content $pdfStylePath -Raw | ConvertFrom-Json
        $slides = $contentJson.slides
        
        # Convert PDF analysis to theme format
        $theme = @{
            metadata = @{
                themeName = "PDF-Extracted Theme"
                version = "1.0.0"
                generatedAt = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
                sourceReference = $pdfJson.metadata.sourceFile
            }
            designTokens = $pdfJson.designTokens
            slideTemplates = $pdfJson.componentPatterns
        }
        
        Write-Host "  ✓ 01_contents_slides.json loaded ($($slides.Count) slides)" -ForegroundColor Green
        Write-Host "  ✓ PDF style analysis converted to theme" -ForegroundColor Green
    }
    "pdf-only" {
        Write-Host "  ⚠️ PDF style loaded, but no content. Manual slide creation needed." -ForegroundColor Yellow
        $pdfJson = Get-Content $pdfStylePath -Raw | ConvertFrom-Json
        $theme = @{
            metadata = @{
                themeName = "PDF-Extracted Theme"
                version = "1.0.0"
                generatedAt = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
                sourceReference = $pdfJson.metadata.sourceFile
            }
            designTokens = $pdfJson.designTokens
            slideTemplates = $pdfJson.componentPatterns
        }
        $slides = @()
    }
}

# 3. Create integrated structure
Write-Host "`nStep 3: Creating integrated structure..." -ForegroundColor Yellow

$integrated = @{
    metadata = @{
        projectName = if ($slides.Count -gt 0) { $slides[0].elements.title.text } else { "Presentation" }
        generatedAt = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        sourceFiles = @()
        totalSlides = $slides.Count
        mode = $mode
    }
    slides = @()
    theme = $theme
    navigation = @{
        keyboard = @{
            enabled = $true
            keys = @{
                next = @("ArrowRight", "Space")
                previous = @("ArrowLeft")
                first = @("Home")
                last = @("End")
            }
        }
        dots = @{
            enabled = $true
            position = "bottom-center"
        }
        touch = @{
            enabled = $true
            swipeThreshold = 50
        }
    }
}

# Add source file references
if ($hasContent) { $integrated.metadata.sourceFiles += "01_contents_slides.json" }
if ($hasStyle) { $integrated.metadata.sourceFiles += "02_style_theme.json" }
if ($hasPdfStyle) { $integrated.metadata.sourceFiles += "bluehive_style_analysis.json" }

# 4. Merge slides with theme
Write-Host "`nStep 4: Merging slides with theme..." -ForegroundColor Yellow

foreach ($slide in $slides) {
    $slideType = $slide.type
    $template = $null
    
    # Find matching template
    if ($theme.slideTemplates.PSObject.Properties.Name -contains $slideType) {
        $template = $theme.slideTemplates.$slideType
    }
    
    # Merge slide with template styles
    $mergedSlide = @{
        id = $slide.id
        type = $slide.type
        order = $slide.order
        layout = $slide.layout
        elements = $slide.elements
        background = $slide.background
        spacing = $slide.spacing
        transition = $slide.transition
    }
    
    # Apply template defaults if available
    if ($template) {
        if (-not $mergedSlide.background) {
            $mergedSlide.background = $template.background.default
        }
        if (-not $mergedSlide.spacing) {
            $mergedSlide.spacing = $template.spacing
        }
    }
    
    $integrated.slides += $mergedSlide
    Write-Host "  ✓ Merged slide: $($slide.id) ($slideType)" -ForegroundColor Green
}

Write-Host "  Total slides merged: $($integrated.slides.Count)" -ForegroundColor Cyan

# 5. Write output file
Write-Host "`nStep 5: Writing integrated file..." -ForegroundColor Yellow

$integrated | ConvertTo-Json -Depth 100 | Set-Content $outputPath -Encoding UTF8
Write-Host "  ✓ Written to: $outputPath" -ForegroundColor Green

# 6. Validation
Write-Host "`nStep 6: Validation..." -ForegroundColor Yellow

$outputJson = Get-Content $outputPath -Raw | ConvertFrom-Json
$outputSize = (Get-Item $outputPath).Length

Write-Host "  ✓ File size: $outputSize bytes" -ForegroundColor Green
Write-Host "  ✓ Slides count: $($outputJson.slides.Count)" -ForegroundColor Green
Write-Host "  ✓ Theme templates: $($outputJson.theme.slideTemplates.PSObject.Properties.Name.Count)" -ForegroundColor Green
Write-Host "  ✓ Design tokens: $($outputJson.theme.designTokens.PSObject.Properties.Name.Count)" -ForegroundColor Green

# Validation checks
$validationPassed = $true

if ($outputJson.slides.Count -eq 0 -and $mode -ne "pdf-only") {
    Write-Host "  ✗ FAIL: No slides found in output" -ForegroundColor Red
    $validationPassed = $false
}

if (-not $outputJson.theme.designTokens) {
    Write-Host "  ✗ FAIL: Design tokens missing" -ForegroundColor Red
    $validationPassed = $false
}

if ($validationPassed) {
    Write-Host "`n=== Integration Complete ✓ ===" -ForegroundColor Green
    Write-Host "Output: $outputPath" -ForegroundColor Cyan
    Write-Host "Slides: $($outputJson.slides.Count)" -ForegroundColor Cyan
    Write-Host "Mode: $mode" -ForegroundColor Cyan
} else {
    Write-Host "`n=== Integration Failed ✗ ===" -ForegroundColor Red
    exit 1
}
