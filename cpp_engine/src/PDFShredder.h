#ifndef PDF_SHREDDER_H
#define PDF_SHREDDER_H

#include <string>
#include <vector>
#include <memory>

namespace guardian {

/**
 * PDFShredder - High-performance PDF text extraction
 * 
 * This class provides efficient PDF parsing with memory-optimized
 * streaming to avoid loading entire files into memory.
 */
class PDFShredder {
public:
    PDFShredder();
    ~PDFShredder();
    
    /**
     * Extract all text content from a PDF file
     * @param filepath Absolute path to PDF file
     * @return Vector of text strings (one per page)
     * @throws std::runtime_error if file cannot be opened or parsed
     */
    std::vector<std::string> extractText(const std::string& filepath);
    
    /**
     * Get the number of pages in the last processed PDF
     */
    int getPageCount() const;
    
private:
    class Impl;
    std::unique_ptr<Impl> pImpl;  // Pimpl idiom for poppler types
};

} // namespace guardian

#endif // PDF_SHREDDER_H
