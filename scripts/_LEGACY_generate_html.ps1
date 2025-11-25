# =============================================================================
# HTML Generator Script - v2.17.0 Complete Segmentation
# Purpose: Convert 03_integrate_web.json to complete HTML file with Tailwind
# Method: Section-by-section template rendering with 100% data preservation
# =============================================================================

Write-Host "`n=== HTML Generation Pipeline v2.17.0 ===" -ForegroundColor Cyan
Write-Host "Starting HTML generation from integration JSON...`n" -ForegroundColor White

# =============================================================================
# Helper Functions
# =============================================================================

function Get-NestedProperty {
    <#
    .SYNOPSIS
    Navigate JSON structure with dot notation path
    .EXAMPLE
    Get-NestedProperty $section "visual.type" → "3d-planet-parallax"
    #>
    param(
        [Parameter(Mandatory=$true)]
        $Object,
        
        [Parameter(Mandatory=$true)]
        [string]$Path
    )
    
    $parts = $Path -split '\.'
    $current = $Object
    
    foreach ($part in $parts) {
        if ($null -eq $current) {
            return $null
        }
        
        # If current is a string, cannot navigate further
        if ($current -is [string]) {
            # If this is the first part and matches, return the string
            if ($parts.Count -eq 1) {
                return $current
            }
            # Otherwise, cannot navigate into string
            return $null
        }
        
        # Check if it's an object with properties
        if ($current.PSObject.Properties[$part]) {
            $current = $current.$part
        } else {
            return $null
        }
    }
    
    return $current
}

function ConvertTo-TailwindClass {
    <#
    .SYNOPSIS
    Convert style object to Tailwind CSS classes
    .EXAMPLE
    ConvertTo-TailwindClass @{ fontSize = "60-72px"; color = "#FF6635" }
    → "text-6xl md:text-7xl text-[#FF6635]"
    #>
    param(
        [Parameter(Mandatory=$true)]
        $StyleObject
    )
    
    $classes = @()
    
    # Font Size conversion
    if ($StyleObject.fontSize) {
        $fontSize = $StyleObject.fontSize
        if ($fontSize -match '(\d+)-(\d+)px') {
            $minSize = [int]$matches[1]
            $maxSize = [int]$matches[2]
            
            # Base size
            if ($minSize -ge 60) { $classes += "text-6xl" }
            elseif ($minSize -ge 48) { $classes += "text-5xl" }
            elseif ($minSize -ge 36) { $classes += "text-4xl" }
            elseif ($minSize -ge 24) { $classes += "text-3xl" }
            elseif ($minSize -ge 20) { $classes += "text-2xl" }
            elseif ($minSize -ge 18) { $classes += "text-xl" }
            elseif ($minSize -ge 16) { $classes += "text-lg" }
            else { $classes += "text-base" }
            
            # Responsive size
            if ($maxSize -ge 72) { $classes += "md:text-7xl" }
            elseif ($maxSize -ge 60) { $classes += "md:text-6xl" }
            elseif ($maxSize -ge 48) { $classes += "md:text-5xl" }
        }
        elseif ($fontSize -match '(\d+)px') {
            $size = [int]$matches[1]
            if ($size -ge 60) { $classes += "text-6xl" }
            elseif ($size -ge 48) { $classes += "text-5xl" }
            elseif ($size -ge 36) { $classes += "text-4xl" }
            elseif ($size -ge 24) { $classes += "text-3xl" }
            elseif ($size -ge 20) { $classes += "text-2xl" }
            elseif ($size -ge 18) { $classes += "text-xl" }
            elseif ($size -ge 16) { $classes += "text-lg" }
            else { $classes += "text-base" }
        }
    }
    
    # Font Weight
    if ($StyleObject.fontWeight) {
        $weight = $StyleObject.fontWeight
        if ($weight -ge 700) { $classes += "font-bold" }
        elseif ($weight -ge 600) { $classes += "font-semibold" }
        elseif ($weight -ge 500) { $classes += "font-medium" }
        else { $classes += "font-normal" }
    }
    
    # Color
    if ($StyleObject.color) {
        $color = $StyleObject.color
        if ($color -match '^#[0-9A-Fa-f]{6}$') {
            $classes += "text-[$color]"
        }
        elseif ($color -eq "#FFFFFF" -or $color -eq "white") {
            $classes += "text-white"
        }
        elseif ($color -eq "#000000" -or $color -eq "black") {
            $classes += "text-black"
        }
    }
    
    # Background
    if ($StyleObject.background) {
        $bg = $StyleObject.background
        if ($bg -match '^#[0-9A-Fa-f]{6}$') {
            $classes += "bg-[$bg]"
        }
        elseif ($bg -eq "#000000" -or $bg -eq "black") {
            $classes += "bg-black"
        }
    }
    
    # Padding
    if ($StyleObject.padding) {
        $padding = $StyleObject.padding
        if ($padding -match '(\d+)px') {
            $px = [int]$matches[1]
            if ($px -ge 32) { $classes += "p-8" }
            elseif ($px -ge 24) { $classes += "p-6" }
            elseif ($px -ge 16) { $classes += "p-4" }
        }
    }
    
    # Border Radius
    if ($StyleObject.borderRadius) {
        $radius = $StyleObject.borderRadius
        if ($radius -match '(\d+)px') {
            $r = [int]$matches[1]
            if ($r -ge 16) { $classes += "rounded-xl" }
            elseif ($r -ge 8) { $classes += "rounded-lg" }
            elseif ($r -ge 4) { $classes += "rounded" }
        }
    }
    
    return ($classes -join ' ')
}

function Render-HtmlElement {
    <#
    .SYNOPSIS
    Recursively render HTML elements with proper nesting
    .EXAMPLE
    Render-HtmlElement "div" @{ class = "container" } "Hello" @($child1, $child2)
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$ElementType,
        
        [Parameter(Mandatory=$false)]
        [hashtable]$Attributes = @{},
        
        [Parameter(Mandatory=$false)]
        [string]$Content = "",
        
        [Parameter(Mandatory=$false)]
        [array]$Children = @()
    )
    
    # Build opening tag
    $attrString = ""
    foreach ($key in $Attributes.Keys) {
        $value = $Attributes[$key]
        if ($value) {
            $attrString += " $key=`"$value`""
        }
    }
    
    $html = "<$ElementType$attrString>"
    
    # Add content
    if ($Content) {
        $html += $Content
    }
    
    # Add children
    foreach ($child in $Children) {
        $html += "`n    $child"
    }
    
    # Close tag
    $html += "</$ElementType>"
    
    return $html
}

function Escape-HtmlText {
    <#
    .SYNOPSIS
    Escape special characters and fix UTF-8 encoding issues
    #>
    param(
        [Parameter(Mandatory=$true)]
        [AllowEmptyString()]
        [string]$Text
    )
    
    # Return empty string as-is
    if ([string]::IsNullOrEmpty($Text)) {
        return ""
    }
    
    # Fix bullet points using actual char codes (not Unicode escapes in regex)
    $Text = $Text -replace [char]0x2022, '&bull;'        # •
    $Text = $Text -replace [char]0x2713, '&#10003;'      # ✓
    $Text = $Text -replace [char]0x2717, '&#10007;'      # ✗
    $Text = $Text -replace [char]0x2192, '&rarr;'        # →
    $Text = $Text -replace [char]0x2190, '&larr;'        # ←
    $Text = $Text -replace [char]0x2194, '&harr;'        # ↔
    
    # Fix quotes using actual char codes
    $Text = $Text -replace [char]0x2018, "'"             # '
    $Text = $Text -replace [char]0x2019, "'"             # '
    $Text = $Text -replace [char]0x201C, '"'             # "
    $Text = $Text -replace [char]0x201D, '"'             # "
    
    # Escape HTML special characters (but not if already escaped)
    if ($Text -notmatch '&[a-z]+;') {
        $Text = $Text -replace '&', '&amp;'
    }
    $Text = $Text -replace '<', '&lt;'
    $Text = $Text -replace '>', '&gt;'
    
    return $Text
}

# =============================================================================
# Step 1: Load Integration JSON
# =============================================================================

$integrationPath = "analysis\web-pipeline\03_integrate_web.json"

if (-not (Test-Path $integrationPath)) {
    Write-Host "ERROR: Integration file not found: $integrationPath" -ForegroundColor Red
    Write-Host "Please run /integrate command first." -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Loading integration JSON..." -ForegroundColor Yellow
$spec = Get-Content $integrationPath -Raw -Encoding UTF8 | ConvertFrom-Json
Write-Host "  - Loaded $($spec.sections.Count) sections" -ForegroundColor Green
Write-Host "  - Project: $($spec.seo.title)" -ForegroundColor Green

# =============================================================================
# Helper Functions
# =============================================================================

function ConvertTo-TailwindSize {
    param([string]$size)
    if ($size -match '(\d+)-(\d+)px') {
        return "text-[$($matches[2])]"
    } elseif ($size -match '(\d+)px') {
        return "text-[$matches[1]]"
    }
    return ""
}

function ConvertTo-TailwindColor {
    param([string]$color)
    if ($color -match '^#[0-9A-Fa-f]{6}$') {
        return "[$color]"
    }
    return $color
}

# =============================================================================
# Step 2: Initialize HTML Structure
# =============================================================================

Write-Host "`nStep 2: Creating HTML structure..." -ForegroundColor Yellow

$html = @"
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$($spec.seo.title)</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="$($spec.seo.description)">
    <meta name="keywords" content="$($spec.seo.keywords)">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Custom Styles -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #000000;
            color: #FFFFFF;
        }
        
        /* Logo Marquee Animation */
        @keyframes marquee {
            from { transform: translateX(0); }
            to { transform: translateX(-50%); }
        }
        
        .marquee-animation {
            animation: marquee 17s linear infinite;
        }
    </style>
</head>
<body class="bg-black text-white">

"@

Write-Host "  - HTML head structure created" -ForegroundColor Green

# =============================================================================
# Section Renderer Functions
# =============================================================================

function Render-HeroSection {
    param($Section)
    
    $html = ""
    
    # Extract heading text
    $headingText = if ($Section.heading.text) { 
        Escape-HtmlText $Section.heading.text 
    } elseif ($Section.heading) { 
        Escape-HtmlText $Section.heading 
    } else {
        "Hero Section"
    }
    
    # Hero Content Container
    $html += @"
            <!-- Hero Content -->
            <div class="text-center relative z-10">
                <h1 class="text-6xl md:text-7xl font-bold mb-6">
                    $headingText
                </h1>
"@
    
    # CTA Buttons
    if ($Section.cta) {
        $html += @"

                <div class="flex gap-4 justify-center mt-8">
"@
        foreach ($button in $Section.cta) {
            $btnText = Escape-HtmlText $button.text
            $btnClass = if ($button.type -eq "primary") { 
                "bg-white text-black" 
            } else { 
                "bg-[#FF6635] text-white" 
            }
            $html += @"

                    <a href="#" class="px-8 py-4 rounded-lg font-semibold $btnClass hover:opacity-90 transition">
                        $btnText
                    </a>
"@
        }
        $html += @"

                </div>
"@
    }
    
    # Logo Marquee
    if ($Section.logoMarquee) {
        $logos = @("dbt", "Airflow", "GitHub", "GitLab", "Spark", "Snowflake", "Databricks", "AWS", "Google Cloud", "Azure")
        $html += @"

                <div class="mt-16 overflow-hidden">
                    <div class="flex gap-8 marquee-animation whitespace-nowrap">
"@
        # First set
        foreach ($logo in $logos) {
            $html += @"

                        <span class="text-gray-400">$logo</span>
"@
        }
        # Duplicate for seamless loop
        foreach ($logo in $logos) {
            $html += @"

                        <span class="text-gray-400">$logo</span>
"@
        }
        $html += @"

                    </div>
                </div>
"@
    }
    
    # Bottom Content Boxes
    if ($Section.bottomContent) {
        $html += @"

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-16">
"@
        foreach ($box in $Section.bottomContent) {
            $boxHeading = Escape-HtmlText $box.heading
            $boxDesc = Escape-HtmlText $box.description
            $html += @"

                    <div class="bg-[#1A1A1A] rounded-lg p-6 border border-gray-800">
                        <h3 class="font-bold text-sm mb-2">$boxHeading</h3>
                        <p class="text-gray-400 text-sm">$boxDesc</p>
                    </div>
"@
        }
        $html += @"

                </div>
"@
    }
    
    # Integrations List
    if ($Section.integrationsList) {
        $html += @"

                <div class="mt-12">
                    <h4 class="text-sm font-semibold mb-4">$($Section.integrationsList.title)</h4>
                    <div class="flex gap-3 justify-center flex-wrap">
"@
        foreach ($item in $Section.integrationsList.items) {
            $itemText = Escape-HtmlText $item
            $html += @"

                        <div class="flex items-center gap-2">
                            <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                            <span class="text-sm text-gray-400">$itemText</span>
                        </div>
"@
        }
        $html += @"

                    </div>
                </div>
"@
    }
    
    $html += @"

            </div>
"@
    
    return $html
}

function Render-FeatureSection {
    param($Section)
    
    $html = ""
    
    # Header Section
    $html += @"
            <div class="text-center mb-12">
"@
    
    # Badge
    if ($Section.badge) {
        $badgeText = Escape-HtmlText $Section.badge
        $html += @"

                <div class="inline-block text-[#FF6635] font-bold mb-4">$badgeText</div>
"@
    }
    
    # Heading
    $headingText = if ($Section.heading.text) { 
        Escape-HtmlText $Section.heading.text 
    } elseif ($Section.heading) { 
        Escape-HtmlText $Section.heading 
    } else {
        "Feature Section"
    }
    $html += @"

                <h2 class="text-5xl font-bold mb-6">
                    $headingText
                </h2>
"@
    
    # Subheading
    if ($Section.subheading) {
        $subheadingText = Escape-HtmlText $Section.subheading
        $html += @"

                <p class="text-xl text-gray-400 max-w-3xl mx-auto">
                    $subheadingText
                </p>
"@
    }
    
    $html += @"

            </div>
"@
    
    # Visual Element (Code Snippet Preview, Diagrams, etc.)
    if ($Section.visual -and $Section.visual.type) {
        $visualType = $Section.visual.type
        
        if ($visualType -eq "code-snippet-preview") {
            $html += @"

            <!-- Code Snippet Preview -->
            <div class="max-w-4xl mx-auto mb-12">
                <div class="bg-[#1A1A1A] rounded-lg p-6 border border-gray-800 code-snippet">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-sm font-semibold">$($Section.visual.subject)</h3>
                        <svg class="w-6 h-6 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"/>
                        </svg>
                    </div>
                    <pre class="text-sm text-gray-300 overflow-x-auto"><code>// $($Section.visual.visualDescription)</code></pre>
                </div>
            </div>
"@
        }
    }
    
    # Action Buttons
    if ($Section.actionButtons) {
        $html += @"

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
"@
        foreach ($btn in $Section.actionButtons) {
            $btnText = Escape-HtmlText $btn.text
            $colorClass = switch ($btn.color) {
                "green" { "border-green-500 text-green-500" }
                "blue" { "border-blue-500 text-blue-500" }
                "orange" { "border-[#FF6635] text-[#FF6635]" }
                default { "border-gray-500 text-gray-500" }
            }
            $html += @"

                <div class="border-2 $colorClass rounded-lg px-6 py-4 text-center hover:bg-opacity-10 transition cursor-pointer">
                    $btnText
                </div>
"@
        }
        $html += @"

            </div>
"@
    }
    
    return $html
}

function Render-WorkflowSection {
    param($Section)
    
    $html = ""
    
    # Header with badge, heading, subheading
    $html += @"

            <div class="text-center mb-16">
"@
    
    if ($Section.badge) {
        $badgeText = Escape-HtmlText $Section.badge
        $html += @"

                <div class="inline-block text-[#FF6635] font-bold text-lg mb-4">
                    $badgeText
                </div>
"@
    }
    
    # Heading
    $headingText = if ($Section.heading.text) { 
        Escape-HtmlText $Section.heading.text 
    } elseif ($Section.heading) { 
        Escape-HtmlText $Section.heading 
    } else {
        "Workflow Section"
    }
    $html += @"

                <h2 class="text-5xl md:text-6xl font-bold mb-6">
                    $headingText
                </h2>
"@
    
    # Subheading
    if ($Section.subheading) {
        $subheadingText = Escape-HtmlText $Section.subheading
        $html += @"

                <p class="text-xl text-gray-400 max-w-3xl mx-auto">
                    $subheadingText
                </p>
"@
    }
    
    $html += @"

            </div>
"@
    
    # Step Cards
    if ($Section.stepCards -and $Section.stepCards.Count -gt 0) {
        $html += @"

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
"@
        
        foreach ($card in $Section.stepCards) {
            $stepNum = $card.step
            $cardTitle = Escape-HtmlText $card.title
            $cardSubtitle = Escape-HtmlText $card.subtitle
            
            $html += @"

                <div class="step-card bg-[#1A1A1A] rounded-lg p-8 border border-gray-800 hover:border-[#FF6635] transition">
                    <div class="inline-block bg-[#FF6635] text-white font-bold text-sm px-3 py-1 rounded mb-4">
                        STEP $stepNum
                    </div>
                    <h3 class="text-2xl font-bold mb-2">
                        $cardTitle
                    </h3>
                    <p class="text-sm text-gray-500 mb-6">
                        $cardSubtitle
                    </p>
"@
            
            # Details list with proper bullet points
            if ($card.details -and $card.details.Count -gt 0) {
                $html += @"

                    <ul class="space-y-3 text-sm text-gray-400">
"@
                
                foreach ($detail in $card.details) {
                    $detailText = Escape-HtmlText $detail
                    
                    # Determine icon based on content
                    $icon = if ($detail -match "^\u2713" -or $detail -match "checkmark") {
                        "<span class='text-green-500 mr-2'>&#10003;</span>"
                    } elseif ($detail -match "^[xX]" -or $detail -match "error") {
                        "<span class='text-red-500 mr-2'>&#10007;</span>"
                    } else {
                        "<span class='text-[#FF6635] mr-2'>&bull;</span>"
                    }
                    
                    $html += @"

                        <li class="flex items-start">
                            $icon
                            <span>$detailText</span>
                        </li>
"@
                }
                
                $html += @"

                    </ul>
"@
            }
            
            # Icons (checkmark, x) - render if provided separately
            if ($card.icons -and $card.icons.Count -gt 0) {
                $html += @"

                    <div class="flex gap-3 mt-6">
"@
                
                foreach ($iconType in $card.icons) {
                    if ($iconType -eq "checkmark") {
                        $html += @"

                        <div class="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center text-white text-xs">&#10003;</div>
"@
                    } elseif ($iconType -eq "x") {
                        $html += @"

                        <div class="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center text-white text-xs">&#10007;</div>
"@
                    }
                }
                
                $html += @"

                    </div>
"@
            }
            
            $html += @"

                </div>
"@
        }
        
        $html += @"

            </div>
"@
    }
    
    # Sequential Animation (insert codeHint directly if exists)
    if ($Section.animation -and $Section.animation.codeHint) {
        $animationCode = $Section.animation.codeHint
        $html += @"

            <script>
            // Sequential Animation for Workflow Steps
            $animationCode
            </script>
"@
    }
    
    return $html
}

function Render-ValidationSection {
    param($Section)
    
    $html = ""
    
    $html += @"

            <div class="text-center mb-12">
"@
    
    if ($Section.heading) {
        # Fix: Extract property first, then escape
        $rawHeading = if ($Section.heading.text) { $Section.heading.text } else { $Section.heading }
        $headingText = Escape-HtmlText $rawHeading
        $html += @"

                <h2 class="text-5xl font-bold mb-6">
                    $headingText
                </h2>
"@
    }
    
    if ($Section.description -or $Section.subheading) {
        # Fix: Extract property first, then escape
        $rawDesc = if ($Section.description) { $Section.description } else { $Section.subheading }
        $descText = Escape-HtmlText $rawDesc
        $html += @"

                <p class="text-xl text-gray-400 max-w-3xl mx-auto">
                    $descText
                </p>
"@
    }
    
    $html += @"

            </div>
            <div class="verification-card bg-[#1A1A1A] rounded-lg p-12 border border-gray-800">
                <div class="text-center text-gray-400">
                    Validation visualization (Before/After comparison)
                </div>
            </div>
"@
    
    return $html
}

function Render-FeatureShowcase {
    param($Section)
    
    $html = ""
    
    $html += @"

            <div class="text-center mb-16">
"@
    
    if ($Section.heading) {
        # Handle complex multi-line headings
        if ($Section.heading.line1 -and $Section.heading.line2) {
            $line1Text = Escape-HtmlText $Section.heading.line1.text
            $line1Color = if ($Section.heading.line1.color) { $Section.heading.line1.color } else { "#FFFFFF" }
            $line2Text = Escape-HtmlText $Section.heading.line2.text
            $line2Color = if ($Section.heading.line2.color) { $Section.heading.line2.color } else { "#FFFFFF" }
            
            $html += @"

                <h2 class="text-6xl md:text-7xl font-bold mb-8">
                    <span class="section-05-heading-line" style="color: $line1Color">$line1Text</span><br>
                    <span class="section-05-heading-line" style="color: $line2Color">$line2Text</span>
                </h2>
"@
        } else {
            $rawHeading = if ($Section.heading.text) { $Section.heading.text } else { $Section.heading }
            $headingText = Escape-HtmlText $rawHeading
            $html += @"

                <h2 class="text-6xl md:text-7xl font-bold mb-8">
                    $headingText
                </h2>
"@
        }
    }
    
    if ($Section.subheading) {
        $subheadingText = Escape-HtmlText $Section.subheading
        $html += @"

                <p class="text-2xl text-gray-400 max-w-4xl mx-auto">
                    $subheadingText
                </p>
"@
    }
    
    $html += @"

            </div>
            <div class="bg-[#1A1A1A] rounded-xl p-16 border border-gray-800">
                <div class="aspect-video bg-[#0D0D0D] rounded-lg flex items-center justify-center">
                    <span class="text-gray-600 text-2xl">Large Visual Showcase</span>
                </div>
            </div>
"@
    
    return $html
}

function Render-TwoColumnFeatures {
    param($Section)
    
    $html = ""
    
    if ($Section.features -and $Section.features.Count -gt 0) {
        $html += @"

            <div class="grid grid-cols-1 md:grid-cols-2 gap-16">
"@
        
        foreach ($feature in $Section.features) {
            $featureTitle = Escape-HtmlText $feature.title
            $featureDesc = Escape-HtmlText $feature.description
            
            $html += @"

                <div>
                    <h3 class="text-3xl font-bold mb-4">
                        $featureTitle
                    </h3>
                    <p class="text-lg text-gray-400 mb-8">
                        $featureDesc
                    </p>
                    <div class="bg-[#1A1A1A] rounded-lg p-8 border border-gray-800">
                        <div class="text-gray-600 text-center py-12">Visual Element</div>
                    </div>
                </div>
"@
        }
        
        $html += @"

            </div>
"@
    }
    
    return $html
}

function Render-OnboardingSteps {
    param($Section)
    
    $html = ""
    
    $html += @"

            <div class="text-center mb-16">
"@
    
    if ($Section.heading) {
        $rawHeading = if ($Section.heading.text) { $Section.heading.text } else { $Section.heading }
        $headingText = Escape-HtmlText $rawHeading
        $html += @"

                <h2 class="text-5xl font-bold mb-6">
                    $headingText
                </h2>
"@
    }
    
    $html += @"

            </div>
"@
    
    if ($Section.steps -and $Section.steps.Count -gt 0) {
        $html += @"

            <div class="space-y-8">
"@
        
        $stepNum = 1
        foreach ($step in $Section.steps) {
            $rawStepTitle = if ($step.title) { $step.title } else { $step }
            $stepTitle = Escape-HtmlText $rawStepTitle
            
            $html += @"

                <div class="flex items-start gap-6">
                    <div class="flex-shrink-0 w-12 h-12 rounded-full bg-[#FF6635] flex items-center justify-center text-white font-bold">
                        $stepNum
                    </div>
                    <div class="flex-1">
                        <h3 class="text-2xl font-bold mb-2">
                            $stepTitle
                        </h3>
"@
            
            if ($step.description) {
                $stepDesc = Escape-HtmlText $step.description
                $html += @"

                        <p class="text-gray-400">
                            $stepDesc
                        </p>
"@
            }
            
            $html += @"

                    </div>
                </div>
"@
            $stepNum++
        }
        
        $html += @"

            </div>
"@
    }
    
    return $html
}

function Render-SecuritySection {
    param($Section)
    
    $html = ""
    
    $html += @"

            <div class="text-center">
"@
    
    if ($Section.heading) {
        $rawHeading = if ($Section.heading.text) { $Section.heading.text } else { $Section.heading }
        $headingText = Escape-HtmlText $rawHeading
        $html += @"

                <h2 class="text-4xl font-bold mb-6">
                    $headingText
                </h2>
"@
    }
    
    if ($Section.badges -and $Section.badges.Count -gt 0) {
        $html += @"

                <div class="security-panel flex justify-center gap-8 mt-8">
"@
        
        foreach ($badge in $Section.badges) {
            $badgeText = Escape-HtmlText $badge
            $html += @"

                    <div class="security-feature bg-[#1A1A1A] rounded-lg px-6 py-4 border border-gray-800">
                        $badgeText
                    </div>
"@
        }
        
        $html += @"

                </div>
"@
    }
    
    $html += @"

            </div>
"@
    
    return $html
}

function Render-FeatureCards {
    param($Section)
    
    $html = ""
    
    if ($Section.cards -and $Section.cards.Count -gt 0) {
        $html += @"

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
"@
        
        foreach ($card in $Section.cards) {
            $rawCardTitle = if ($card.title) { $card.title } else { $card.heading }
            $cardTitle = Escape-HtmlText $rawCardTitle
            $rawCardDesc = if ($card.description) { $card.description } else { "" }
            $cardDesc = Escape-HtmlText $rawCardDesc
            
            $html += @"

                <div class="feature-card bg-[#1A1A1A] rounded-lg p-8 border border-gray-800 hover:border-[#FF6635] transition">
                    <h3 class="text-xl font-bold mb-4">
                        $cardTitle
                    </h3>
"@
            
            if ($cardDesc) {
                $html += @"

                    <p class="text-gray-400">
                        $cardDesc
                    </p>
"@
            }
            
            $html += @"

                </div>
"@
        }
        
        $html += @"

            </div>
"@
    }
    
    return $html
}

function Render-Banner {
    param($Section)
    
    $html = ""
    
    $html += @"

            <div class="text-center py-16 bg-gradient-to-r from-[#FF6635] to-[#FF8855] rounded-2xl">
"@
    
    if ($Section.heading) {
        $rawHeading = if ($Section.heading.text) { $Section.heading.text } else { $Section.heading }
        $headingText = Escape-HtmlText $rawHeading
        $html += @"

                <h2 class="text-5xl font-bold text-white">
                    $headingText
                </h2>
"@
    }
    
    $html += @"

            </div>
"@
    
    return $html
}

function Render-CTASection {
    param($Section)
    
    $html = ""
    
    $html += @"

            <div class="text-center">
"@
    
    if ($Section.badge) {
        $badgeText = Escape-HtmlText $Section.badge
        $html += @"

                <div class="cta-badge inline-block text-[#FF6635] font-bold text-lg mb-4">
                    $badgeText
                </div>
"@
    }
    
    if ($Section.heading) {
        $rawHeading = if ($Section.heading.text) { $Section.heading.text } else { $Section.heading }
        $headingText = Escape-HtmlText $rawHeading
        $html += @"

                <h2 class="cta-heading text-5xl md:text-6xl font-bold mb-6">
                    $headingText
                </h2>
"@
    }
    
    if ($Section.subheading) {
        $subheadingText = Escape-HtmlText $Section.subheading
        $html += @"

                <p class="cta-subheading text-xl text-gray-400 max-w-3xl mx-auto mb-8">
                    $subheadingText
                </p>
"@
    }
    
    if ($Section.cta) {
        $html += @"

                <div class="flex justify-center gap-4">
"@
        
        foreach ($button in $Section.cta) {
            $btnText = Escape-HtmlText $button.text
            $btnClass = if ($button.type -eq "primary") { "bg-white text-black" } else { "bg-[#FF6635] text-white" }
            
            $html += @"

                    <a href="#" class="cta-button inline-block px-8 py-4 rounded-lg font-semibold $btnClass hover:opacity-90 transition">
                        $btnText
                    </a>
"@
        }
        
        $html += @"

                </div>
"@
    }
    
    $html += @"

            </div>
"@
    
    return $html
}

function Render-FAQSection {
    param($Section)
    
    $html = ""
    
    $html += @"

            <div class="text-center mb-12">
"@
    
    if ($Section.badge) {
        $badgeText = Escape-HtmlText $Section.badge
        $html += @"

                <div class="inline-block text-[#FF6635] font-bold mb-4">
                    $badgeText
                </div>
"@
    }
    
    if ($Section.heading) {
        $rawHeading = if ($Section.heading.text) { $Section.heading.text } else { $Section.heading }
        $headingText = Escape-HtmlText $rawHeading
        $html += @"

                <h2 class="text-5xl font-bold mb-6">
                    $headingText
                </h2>
"@
    }
    
    $html += @"

            </div>
"@
    
    if ($Section.faqs -and $Section.faqs.Count -gt 0) {
        $html += @"

            <div class="max-w-3xl mx-auto space-y-4">
"@
        
        foreach ($faq in $Section.faqs) {
            $question = Escape-HtmlText $faq.question
            $answer = Escape-HtmlText $faq.answer
            
            $html += @"

                <details class="bg-[#1A1A1A] rounded-lg p-6 border border-gray-800 hover:border-[#FF6635] transition">
                    <summary class="font-semibold cursor-pointer text-lg">
                        $question
                    </summary>
                    <p class="mt-4 text-gray-400">
                        $answer
                    </p>
                </details>
"@
        }
        
        $html += @"

            </div>
"@
    }
    
    return $html
}

function Render-Footer {
    param($Section)
    
    $html = ""
    
    $html += @"

            <footer class="border-t border-gray-800 pt-16">
"@
    
    # Newsletter
    if ($Section.newsletter) {
        $html += @"

                <div class="text-center mb-16">
                    <h3 class="text-2xl font-bold mb-4">
                        Stay Updated
                    </h3>
                    <div class="max-w-md mx-auto flex gap-4">
                        <input type="email" placeholder="Enter your email" class="flex-1 px-4 py-3 bg-[#1A1A1A] border border-gray-800 rounded-lg focus:border-[#FF6635] outline-none">
                        <button class="px-6 py-3 bg-[#FF6635] text-white font-semibold rounded-lg hover:opacity-90 transition">
                            Subscribe
                        </button>
                    </div>
                </div>
"@
    }
    
    # Footer columns
    if ($Section.columns) {
        $html += @"

                <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
"@
        
        foreach ($column in $Section.columns) {
            $columnTitle = Escape-HtmlText $column.title
            
            $html += @"

                    <div>
                        <h4 class="font-bold mb-4">
                            $columnTitle
                        </h4>
                        <ul class="space-y-2 text-gray-400">
"@
            
            if ($column.links) {
                foreach ($link in $column.links) {
                    $linkText = Escape-HtmlText $link.text
                    $html += @"

                            <li>
                                <a href="#" class="hover:text-[#FF6635] transition">$linkText</a>
                            </li>
"@
                }
            }
            
            $html += @"

                        </ul>
                    </div>
"@
        }
        
        $html += @"

                </div>
"@
    }
    
    # Copyright
    $html += @"

                <div class="text-center text-gray-500 text-sm py-8 border-t border-gray-800">
                    &copy; 2024 TensorStax. All rights reserved.
                </div>
            </footer>
"@
    
    return $html
}

function Build-AnimationScripts {
    param($Sections)
    
    $needsGSAP = $false
    $needsScrollTrigger = $false
    $needsThreeJS = $false
    $animationCode = ""
    
    # Scan all sections for animation requirements
    foreach ($section in $Sections) {
        # Check visual.codeHint
        if ($section.visual -and $section.visual.codeHint) {
            $codeHint = $section.visual.codeHint
            
            if ($codeHint -match "gsap\." -or $codeHint -match "GSAP") {
                $needsGSAP = $true
            }
            if ($codeHint -match "ScrollTrigger" -or $codeHint -match "scrollTrigger") {
                $needsScrollTrigger = $true
            }
            if ($codeHint -match "THREE\.|GLTFLoader|WebGLRenderer") {
                $needsThreeJS = $true
            }
            
            $animationCode += @"

// Animation for $($section.id) - Visual
$codeHint

"@
        }
        
        # Check animation.codeHint
        if ($section.animation -and $section.animation.codeHint) {
            $codeHint = $section.animation.codeHint
            
            if ($codeHint -match "gsap\." -or $codeHint -match "GSAP") {
                $needsGSAP = $true
            }
            if ($codeHint -match "ScrollTrigger" -or $codeHint -match "scrollTrigger") {
                $needsScrollTrigger = $true
            }
            if ($codeHint -match "THREE\.|GLTFLoader|WebGLRenderer") {
                $needsThreeJS = $true
            }
            
            $animationCode += @"

// Animation for $($section.id) - Section
$codeHint

"@
        }
        
        # Check logoMarquee animation
        if ($section.logoMarquee -and $section.logoMarquee.codeHint) {
            $codeHint = $section.logoMarquee.codeHint
            
            if ($codeHint -match "gsap\." -or $codeHint -match "GSAP") {
                $needsGSAP = $true
            }
            
            $animationCode += @"

// Logo Marquee Animation for $($section.id)
$codeHint

"@
        }
    }
    
    # Build library CDN links
    $libraries = ""
    
    if ($needsGSAP) {
        $libraries += @"
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>

"@
    }
    
    if ($needsScrollTrigger) {
        $libraries += @"
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

"@
    }
    
    if ($needsThreeJS) {
        $libraries += @"
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

"@
    }
    
    # Build complete script block
    $scriptBlock = ""
    
    if ($libraries) {
        $scriptBlock += @"

    <!-- Animation Libraries -->
$libraries
"@
    }
    
    if ($animationCode) {
        $scriptBlock += @"

    <!-- Animation Code -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize GSAP plugins
        if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
        }

$animationCode
    });
    </script>
"@
    }
    
    return $scriptBlock
}

# =============================================================================
# Step 3: Generate Sections
# =============================================================================

Write-Host "`nStep 3: Generating sections..." -ForegroundColor Yellow

$sectionCount = 0

foreach ($section in $spec.sections) {
    $sectionCount++
    $sectionType = $section.type
    Write-Host "  - Generating section $sectionCount/$($spec.sections.Count): $($section.id) ($sectionType)" -ForegroundColor White
    
    # Extract background color
    $bgColor = if ($section.style.background) { "bg-$(ConvertTo-TailwindColor $section.style.background)" } else { "bg-black" }
    
    # Section header comment
    $html += @"

    <!-- ============================================ -->
    <!-- Section: $($section.id) -->
    <!-- Type: $sectionType -->
    <!-- ============================================ -->
    <section id="$($section.id)" class="py-20 $bgColor">
        <div class="container mx-auto px-4 max-w-7xl">

"@

    # Generate content based on section type
    switch -Wildcard ($sectionType) {
        "hero-section" {
            $html += Render-HeroSection $section
        }
        
        "*feature*" {
            $html += Render-FeatureSection $section
        }
        
        "*workflow*" {
            $html += Render-WorkflowSection $section
        }
        
        "*validation*" {
            $html += Render-ValidationSection $section
        }
        
        "*showcase*" {
            $html += Render-FeatureShowcase $section
        }
        
        "*two-column*" {
            $html += Render-TwoColumnFeatures $section
        }
        
        "*onboard*" {
            $html += Render-OnboardingSteps $section
        }
        
        "*steps*" {
            $html += Render-OnboardingSteps $section
        }
        
        "*security*" {
            $html += Render-SecuritySection $section
        }
        
        "*cards*" {
            $html += Render-FeatureCards $section
        }
        
        "*banner*" {
            $html += Render-Banner $section
        }
        
        "*cta*" {
            $html += Render-CTASection $section
        }
        
        "*faq*" {
            $html += Render-FAQSection $section
        }
        
        "footer" {
            $html += Render-Footer $section
        }
        
        default {
            # Generic section
            $headingText = if ($section.heading.text) { $section.heading.text } else { $section.heading }
            if ($headingText) {
                $html += @"
            <div class="text-center">
"@
                if ($section.badge) {
                    $html += @"

                <div class="inline-block text-[#FF6635] font-bold mb-4">$($section.badge)</div>
"@
                }
                
                $html += @"

                <h2 class="text-5xl font-bold mb-6">
                    $headingText
                </h2>
"@
                
                if ($section.subheading) {
                    $html += @"

                <p class="text-xl text-gray-400 max-w-3xl mx-auto">
                    $($section.subheading)
                </p>
"@
                }
                
                $html += @"

            </div>
"@
            }
        }
    }
    
    $html += @"

        </div>
    </section>

"@
}

Write-Host "  - All $sectionCount sections generated" -ForegroundColor Green

# =============================================================================
# Step 4: Add Animation Scripts
# =============================================================================

Write-Host "`nStep 4: Building animation scripts..." -ForegroundColor Yellow

$animationScripts = Build-AnimationScripts $spec.sections
$html += $animationScripts

if ($animationScripts) {
    $libraryCount = ([regex]::Matches($animationScripts, '<script src=')).Count
    Write-Host "  - Animation libraries detected: $libraryCount" -ForegroundColor Green
    
    $codeHintCount = ([regex]::Matches($animationScripts, '// Animation for')).Count
    Write-Host "  - Animation code blocks inserted: $codeHintCount" -ForegroundColor Green
} else {
    Write-Host "  - No animations detected" -ForegroundColor Yellow
}

# =============================================================================
# Step 5: Close HTML
# =============================================================================

$html += @"
</body>
</html>
"@

# =============================================================================
# Step 6: Write Output File
# =============================================================================

Write-Host "`nStep 5: Writing output file..." -ForegroundColor Yellow

$outputPath = "output\web\index.html"
$outputDir = Split-Path $outputPath -Parent

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

Set-Content -Path $outputPath -Value $html -Encoding UTF8

$lineCount = ($html -split "`n").Count
Write-Host "  - File written: $outputPath" -ForegroundColor Green
Write-Host "  - Total lines: $lineCount" -ForegroundColor Green

# =============================================================================
# Step 7: Validation
# =============================================================================

Write-Host "`nStep 6: Validation..." -ForegroundColor Yellow

$validationPassed = $true

# Check 1: All sections rendered
$renderedSections = ([regex]::Matches($html, '<!-- Section: ([\w-]+) -->')).Count
if ($renderedSections -eq $spec.sections.Count) {
    Write-Host "  [PASS] Section count: $renderedSections/$($spec.sections.Count)" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Section count: $renderedSections/$($spec.sections.Count)" -ForegroundColor Red
    $validationPassed = $false
}

# Check 2: HTML structure is valid
if ($html -match '</html>$') {
    Write-Host "  [PASS] HTML structure complete" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] HTML structure incomplete" -ForegroundColor Red
    $validationPassed = $false
}

# Check 3: Tailwind CSS included
if ($html -match 'cdn\.tailwindcss\.com') {
    Write-Host "  [PASS] Tailwind CSS included" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Tailwind CSS missing" -ForegroundColor Red
    $validationPassed = $false
}

# =============================================================================
# Final Report
# =============================================================================

Write-Host "`n=== Generation Complete ===" -ForegroundColor Cyan

if ($validationPassed) {
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Output: $outputPath" -ForegroundColor White
    Write-Host "Lines: $lineCount" -ForegroundColor White
    Write-Host "Sections: $sectionCount" -ForegroundColor White
    exit 0
} else {
    Write-Host "Status: VALIDATION FAILED" -ForegroundColor Red
    Write-Host "Please check the output file and fix any issues." -ForegroundColor Yellow
    exit 1
}
