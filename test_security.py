#!/usr/bin/env python3
"""
GuardianPDF - Security Demo

Demonstrates AI detection and integrity verification.
"""

import sys
sys.path.insert(0, 'security_auditor')

from perplexity_analyzer import PerplexityAnalyzer
from signature_verifier import SignatureVerifier

print("=" * 70)
print("GuardianPDF Security Auditor - Demo")
print("=" * 70)
print()

# Test 1: AI Detection
print("1. Testing AI Detection (Perplexity Analysis)")
print("-" * 70)

analyzer = PerplexityAnalyzer()

# Human-written text (creative, unpredictable)
human_text = """
The weathered lighthouse stood defiantly against the tempestuous sea,
its beam cutting through fog like a sword through silk. Nobody knew
exactly when it was built, though local legends spoke of shipwrecked
sailors and midnight rituals performed during the equinox.
"""

# AI-generated text (structured, predictable)
ai_text = """
Artificial intelligence is transforming modern society in many ways.
First, it improves efficiency in business operations. Second, it enables
better decision-making through data analysis. Third, it automates
repetitive tasks, freeing humans for creative work.
"""

print("\n📝 Analyzing Human-Written Text:")
human_result = analyzer.analyze_chunk(human_text)
print(f"   Perplexity: {human_result['perplexity']}")
print(f"   Classification: {human_result['label']}")
print(f"   AI Probability: {human_result['confidence'] if human_result['is_ai'] else 1 - human_result['confidence']}")

print("\n🤖 Analyzing AI-Like Text:")
ai_result = analyzer.analyze_chunk(ai_text)
print(f"   Perplexity: {ai_result['perplexity']}")
print(f"   Classification: {ai_result['label']}")
print(f"   AI Probability: {ai_result['confidence'] if ai_result['is_ai'] else 1 - ai_result['confidence']}")

# Test 2: Document Summary
print("\n\n2. Testing Document-Level Analysis")
print("-" * 70)

test_chunks = [human_text, ai_text, human_text, ai_text, ai_text]
results = analyzer.analyze_multiple(test_chunks)
summary = analyzer.get_document_summary(results)

print(f"\n📊 Document Summary:")
print(f"   Total Chunks: {summary['total_chunks']}")
print(f"   AI Chunks: {summary['ai_chunks']}")
print(f"   Human Chunks: {summary['human_chunks']}")
print(f"   Uncertain: {summary['uncertain_chunks']}")
print(f"   AI Percentage: {summary['ai_percentage']}%")
print(f"   Warning Level: {summary['warning_level']}")
print(f"   Assessment: {summary['overall_label']}")

# Test 3: Signature Verification (if PDF provided)
print("\n\n3. PDF Integrity Verification")
print("-" * 70)

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
    print(f"\n🔒 Verifying: {pdf_path}")
    
    verifier = SignatureVerifier()
    result = verifier.verify_pdf(pdf_path)
    
    print(f"\n✓ Verification Results:")
    print(f"   File Size: {result.get('file_size', 0)} bytes")
    print(f"   Pages: {result.get('page_count', 0)}")
    print(f"   Encrypted: {result.get('is_encrypted', False)}")
    print(f"   Has Signature: {result.get('has_signature', False)}")
    print(f"   Verified: {'✅ Yes' if result.get('verified', False) else '❌ No'}")
    
    if result.get('warnings'):
        print(f"\n⚠️  Warnings:")
        for warning in result['warnings']:
            print(f"   • {warning}")
    
    if 'metadata' in result:
        print(f"\n📋 Metadata:")
        for key, value in result['metadata'].items():
            print(f"   {key}: {value}")
else:
    print("\n💡 To test PDF verification, run:")
    print("   python test_security.py path/to/document.pdf")

print("\n" + "=" * 70)
print("✅ Security Demo Complete!")
print("=" * 70)
