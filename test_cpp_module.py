#!/usr/bin/env python3
"""
Demo script to test the C++ pdf_shredder module
"""

import sys
sys.path.insert(0, 'cpp_engine/build')

import pdf_shredder

print("=" * 60)
print("GuardianPDF C++ Module - Quick Demo")
print("=" * 60)

# Test chunking
print("\n1. Testing TextChunker:")
chunker = pdf_shredder.TextChunker(chunk_size=10, overlap_size=2)
test_text = " ".join([f"word{i}" for i in range(1, 26)])
chunks = chunker.chunk(test_text)
print(f"   Input: 25 words")
print(f"   Output: {len(chunks)} chunks")
print(f"   First chunk: {chunks[0][:50]}...")

# Test deduplication
print("\n2. Testing RabinKarpDeduplicator:")
dedup = pdf_shredder.RabinKarpDeduplicator(similarity_threshold=0.9)
test_chunks = [
    "This is a test chunk",
    "This is another chunk",
    "This is a test chunk",  # Duplicate
    "Completely different text"
]
unique = dedup.deduplicate(test_chunks)
stats = dedup.get_stats()
print(f"   Original: {stats.original_count} chunks")
print(f"   Unique: {stats.unique_count} chunks")
print(f"   Removed: {stats.duplicates_removed} duplicates")
print(f"   Dedup ratio: {stats.deduplication_ratio:.2%}")

print("\n" + "=" * 60)
print("✅ C++ Module Working!")
print("=" * 60)

# Note: PDF extraction would require an actual PDF file
print("\n📝 Note: To test PDF extraction, run:")
print("   pdf_shredder.process_pdf('path/to/your.pdf')")
