#!/usr/bin/env python3
"""
GuardianPDF - Performance Benchmark

Measures C++ vs Python parsing performance.
"""

import sys
import time
import os

sys.path.insert(0, 'cpp_engine/build')
import pdf_shredder

print("=" * 70)
print("GuardianPDF Performance Benchmark")
print("=" * 70)
print()

def benchmark_cpp(pdf_path, iterations=3):
    """Benchmark C++ PDF processing."""
    print(f"🚀 Benchmarking C++ Module ({iterations} iterations)...")
    
    times = []
    for i in range(iterations):
        start = time.time()
        chunks = pdf_shredder.process_pdf(
            pdf_path,
            chunk_size=500,
            overlap_size=50,
            dedup=True
        )
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"   Run {i+1}: {elapsed*1000:.2f} ms ({len(chunks)} chunks)")
    
    avg_time = sum(times) / len(times)
    print(f"   Average: {avg_time*1000:.2f} ms\n")
    
    return avg_time, len(chunks)

def benchmark_python(pdf_path, iterations=3):
    """Benchmark pure Python PDF processing."""
    print(f"🐍 Benchmarking Python Baseline ({iterations} iterations)...")
    
    try:
        from pypdf import PdfReader
    except ImportError:
        print("   ⚠️  pypdf not installed, skipping Python benchmark")
        return None, 0
    
    times = []
    chunk_count = 0
    
    for i in range(iterations):
        start = time.time()
        
        # Simulate similar processing
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Simple chunking
        words = text.split()
        chunks = []
        for j in range(0, len(words), 500):
            chunk = " ".join(words[j:j+500])
            if chunk:
                chunks.append(chunk)
        
        chunk_count = len(chunks)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"   Run {i+1}: {elapsed*1000:.2f} ms ({len(chunks)} chunks)")
    
    avg_time = sum(times) / len(times)
    print(f"   Average: {avg_time*1000:.2f} ms\n")
    
    return avg_time, chunk_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python benchmark.py path/to/document.pdf")
        print("\nThis will compare C++ vs Python PDF processing performance.")
        return
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return
    
    # Get file size
    file_size = os.path.getsize(pdf_path) / 1024  # KB
    print(f"📄 File: {os.path.basename(pdf_path)}")
    print(f"📊 Size: {file_size:.2f} KB")
    print()
    
    # Benchmark C++
    cpp_time, cpp_chunks = benchmark_cpp(pdf_path)
    
    # Benchmark Python
    py_time, py_chunks = benchmark_python(pdf_path)
    
    # Compare
    if py_time:
        speedup = py_time / cpp_time
        print("=" * 70)
        print("📊 Results Summary")
        print("=" * 70)
        print(f"C++ Processing:    {cpp_time*1000:>8.2f} ms ({cpp_chunks} chunks)")
        print(f"Python Processing: {py_time*1000:>8.2f} ms ({py_chunks} chunks)")
        print(f"Speedup:           {speedup:>8.2f}x faster")
        print()
        
        # Performance tier
        if speedup > 10:
            tier = "🏆 Outstanding"
        elif speedup > 5:
            tier = "🥇 Excellent"
        elif speedup > 2:
            tier = "🥈 Good"
        else:
            tier = "🥉 Moderate"
        
        print(f"Performance Tier: {tier}")
        print("=" * 70)
    else:
        print("=" * 70)
        print("C++ processing completed successfully!")
        print(f"Time: {cpp_time*1000:.2f} ms | Chunks: {cpp_chunks}")
        print("=" * 70)

if __name__ == "__main__":
    main()
