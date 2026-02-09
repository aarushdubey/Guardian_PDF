#include "PDFShredder.h"
#include <poppler/cpp/poppler-document.h>
#include <poppler/cpp/poppler-page.h>
#include <sstream>
#include <stdexcept>

namespace guardian {

// Pimpl implementation
class PDFShredder::Impl {
public:
  int pageCount = 0;

  std::vector<std::string> extract(const std::string &filepath) {
    // Load PDF document
    std::unique_ptr<poppler::document> doc(
        poppler::document::load_from_file(filepath));

    if (!doc) {
      throw std::runtime_error("Failed to open PDF: " + filepath);
    }

    if (doc->is_locked()) {
      throw std::runtime_error("PDF is password protected: " + filepath);
    }

    pageCount = doc->pages();
    std::vector<std::string> pages;
    pages.reserve(pageCount);

    // Extract text from each page
    for (int i = 0; i < pageCount; ++i) {
      std::unique_ptr<poppler::page> page(doc->create_page(i));
      if (!page) {
        pages.push_back(""); // Empty page
        continue;
      }

      poppler::byte_array text = page->text().to_utf8();
      pages.push_back(std::string(text.data(), text.size()));
    }

    return pages;
  }
};

PDFShredder::PDFShredder() : pImpl(std::make_unique<Impl>()) {}

PDFShredder::~PDFShredder() = default;

std::vector<std::string> PDFShredder::extractText(const std::string &filepath) {
  return pImpl->extract(filepath);
}

int PDFShredder::getPageCount() const { return pImpl->pageCount; }

} // namespace guardian
