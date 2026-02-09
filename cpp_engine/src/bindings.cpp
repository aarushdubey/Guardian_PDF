#include "PDFShredder.h"
#include "RabinKarpDedup.h"
#include "TextChunker.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace guardian;

/**
 * Convenience function for Python: Complete PDF processing pipeline
 *
 * @param filepath Path to PDF file
 * @param chunkSize Words per chunk (default: 500)
 * @param overlapSize Overlapping words (default: 50)
 * @param dedup Enable deduplication (default: true)
 * @return Vector of unique text chunks ready for embedding
 */
std::vector<std::string> process_pdf(const std::string &filepath,
                                     int chunkSize = 500, int overlapSize = 50,
                                     bool dedup = true) {
  // Step 1: Extract text from PDF
  PDFShredder shredder;
  auto pages = shredder.extractText(filepath);

  // Step 2: Chunk the text
  TextChunker chunker(chunkSize, overlapSize);
  auto chunks = chunker.chunkMultiple(pages);

  // Step 3: Deduplicate (optional)
  if (dedup) {
    RabinKarpDeduplicator deduplicator(0.9);
    chunks = deduplicator.deduplicate(chunks);
  }

  return chunks;
}

PYBIND11_MODULE(pdf_shredder, m) {
  m.doc() = "GuardianPDF - High-performance C++ PDF processing module";

  // Main processing function
  m.def("process_pdf", &process_pdf, py::arg("filepath"),
        py::arg("chunk_size") = 500, py::arg("overlap_size") = 50,
        py::arg("dedup") = true,
        "Complete PDF processing pipeline: extract → chunk → deduplicate");

  // PDFShredder class
  py::class_<PDFShredder>(m, "PDFShredder")
      .def(py::init<>())
      .def("extract_text", &PDFShredder::extractText,
           "Extract text from PDF file")
      .def("get_page_count", &PDFShredder::getPageCount,
           "Get number of pages in last processed PDF");

  // TextChunker class
  py::class_<TextChunker>(m, "TextChunker")
      .def(py::init<int, int>(), py::arg("chunk_size") = 500,
           py::arg("overlap_size") = 50)
      .def("chunk", &TextChunker::chunk, "Chunk a single text block")
      .def("chunk_multiple", &TextChunker::chunkMultiple,
           "chunk multiple text blocks");

  // RabinKarpDeduplicator class
  py::class_<RabinKarpDeduplicator>(m, "RabinKarpDeduplicator")
      .def(py::init<double>(), py::arg("similarity_threshold") = 0.9)
      .def("deduplicate", &RabinKarpDeduplicator::deduplicate,
           "Remove duplicate chunks")
      .def("get_stats", &RabinKarpDeduplicator::getStats,
           "Get statistics from last deduplication run");

  // Stats struct
  py::class_<RabinKarpDeduplicator::Stats>(m, "DeduplicationStats")
      .def_readonly("original_count",
                    &RabinKarpDeduplicator::Stats::originalCount)
      .def_readonly("unique_count", &RabinKarpDeduplicator::Stats::uniqueCount)
      .def_readonly("duplicates_removed",
                    &RabinKarpDeduplicator::Stats::duplicatesRemoved)
      .def_readonly("deduplication_ratio",
                    &RabinKarpDeduplicator::Stats::deduplicationRatio);
}
