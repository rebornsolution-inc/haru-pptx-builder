#!/usr/bin/env node

/**
 * Presentation Pipeline Integration Script
 * Purpose: Merge PDF style + URL content OR standalone content
 * Method: Direct JSON object merging (no AI simplification)
 */

const fs = require('fs');
const path = require('path');

console.log('\n=== Presentation Pipeline Integration Started ===\n');

// 1. Determine input mode
console.log('Step 1: Detecting input mode...');

const contentPath = 'analysis/presentation-pipeline/01_contents_slides.json';
const stylePath = 'analysis/presentation-pipeline/02_style_theme.json';
const pdfStylePath = 'analysis/pdf-analysis/bluehive_style_analysis.json';
const outputPath = 'analysis/presentation-pipeline/03_integrate_presentation.json';

const hasContent = fs.existsSync(contentPath);
const hasStyle = fs.existsSync(stylePath);
const hasPdfStyle = fs.existsSync(pdfStylePath);

let mode = 'unknown';
let slides = [];
let theme = {};

if (hasContent && hasStyle) {
  mode = 'content-and-theme';
  console.log('  Mode: Content + Theme (Standard)');
} else if (hasContent && hasPdfStyle) {
  mode = 'content-and-pdf';
  console.log('  Mode: Content + PDF Style');
} else if (hasPdfStyle) {
  mode = 'pdf-only';
  console.log('  Mode: PDF Style Only (Manual content needed)');
} else {
  console.error('  ERROR: No valid input files found');
  process.exit(1);
}

// 2. Load source files
console.log('\nStep 2: Loading source files...');

try {
  switch (mode) {
    case 'content-and-theme':
      const contentJson = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
      const styleJson = JSON.parse(fs.readFileSync(stylePath, 'utf8'));
      slides = contentJson.slides;
      theme = styleJson;
      console.log(`  ✓ 01_contents_slides.json loaded (${slides.length} slides)`);
      console.log('  ✓ 02_style_theme.json loaded');
      break;
      
    case 'content-and-pdf':
      const contentJsonPdf = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
      const pdfJson = JSON.parse(fs.readFileSync(pdfStylePath, 'utf8'));
      slides = contentJsonPdf.slides;
      
      // Convert PDF analysis to theme format
      theme = {
        metadata: {
          themeName: 'PDF-Extracted Theme',
          version: '1.0.0',
          generatedAt: new Date().toISOString(),
          sourceReference: pdfJson.metadata.sourceFile
        },
        designTokens: pdfJson.designTokens,
        slideTemplates: pdfJson.componentPatterns
      };
      
      console.log(`  ✓ 01_contents_slides.json loaded (${slides.length} slides)`);
      console.log('  ✓ PDF style analysis converted to theme');
      break;
      
    case 'pdf-only':
      console.log('  ⚠️ PDF style loaded, but no content. Manual slide creation needed.');
      const pdfJsonOnly = JSON.parse(fs.readFileSync(pdfStylePath, 'utf8'));
      theme = {
        metadata: {
          themeName: 'PDF-Extracted Theme',
          version: '1.0.0',
          generatedAt: new Date().toISOString(),
          sourceReference: pdfJsonOnly.metadata.sourceFile
        },
        designTokens: pdfJsonOnly.designTokens,
        slideTemplates: pdfJsonOnly.componentPatterns
      };
      slides = [];
      break;
  }
} catch (error) {
  console.error('  ERROR loading files:', error.message);
  process.exit(1);
}

// 3. Create integrated structure
console.log('\nStep 3: Creating integrated structure...');

const integrated = {
  metadata: {
    projectName: slides.length > 0 ? (slides[0].elements?.title?.text || 'Presentation') : 'Presentation',
    generatedAt: new Date().toISOString(),
    sourceFiles: [],
    totalSlides: slides.length,
    mode: mode
  },
  slides: [],
  theme: theme,
  navigation: {
    keyboard: {
      enabled: true,
      keys: {
        next: ['ArrowRight', 'Space'],
        previous: ['ArrowLeft'],
        first: ['Home'],
        last: ['End']
      }
    },
    dots: {
      enabled: true,
      position: 'bottom-center'
    },
    touch: {
      enabled: true,
      swipeThreshold: 50
    }
  }
};

// Add source file references
if (hasContent) integrated.metadata.sourceFiles.push('01_contents_slides.json');
if (hasStyle) integrated.metadata.sourceFiles.push('02_style_theme.json');
if (hasPdfStyle) integrated.metadata.sourceFiles.push('bluehive_style_analysis.json');

// 4. Merge slides with theme
console.log('\nStep 4: Merging slides with theme...');

slides.forEach(slide => {
  const slideType = slide.type;
  const template = theme.slideTemplates?.[slideType];
  
  // Merge slide with template styles
  const mergedSlide = {
    id: slide.id,
    type: slide.type,
    order: slide.order,
    layout: slide.layout,
    elements: slide.elements,
    background: slide.background || (template?.background?.default),
    spacing: slide.spacing || template?.spacing,
    transition: slide.transition
  };
  
  integrated.slides.push(mergedSlide);
  console.log(`  ✓ Merged slide: ${slide.id} (${slideType})`);
});

console.log(`  Total slides merged: ${integrated.slides.length}`);

// 5. Write output file
console.log('\nStep 5: Writing integrated file...');

fs.writeFileSync(outputPath, JSON.stringify(integrated, null, 2), 'utf8');
console.log(`  ✓ Written to: ${outputPath}`);

// 6. Validation
console.log('\nStep 6: Validation...');

const outputJson = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
const outputSize = fs.statSync(outputPath).size;

console.log(`  ✓ File size: ${outputSize} bytes`);
console.log(`  ✓ Slides count: ${outputJson.slides.length}`);
console.log(`  ✓ Theme templates: ${Object.keys(outputJson.theme.slideTemplates || {}).length}`);
console.log(`  ✓ Design tokens: ${Object.keys(outputJson.theme.designTokens || {}).length}`);

let validationPassed = true;

if (outputJson.slides.length === 0 && mode !== 'pdf-only') {
  console.error('  ✗ FAIL: No slides found in output');
  validationPassed = false;
}

if (!outputJson.theme.designTokens) {
  console.error('  ✗ FAIL: Design tokens missing');
  validationPassed = false;
}

if (validationPassed) {
  console.log('\n=== Integration Complete ✓ ===');
  console.log(`Output: ${outputPath}`);
  console.log(`Slides: ${outputJson.slides.length}`);
  console.log(`Mode: ${mode}`);
} else {
  console.error('\n=== Integration Failed ✗ ===');
  process.exit(1);
}
