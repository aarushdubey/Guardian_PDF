#ifndef TEXT_CHUNKER_H
#define TEXT_CHUNKER_H

#include <string>
#include <vector>

namespace guardian {

/**
 * TextChunker - Intelligent text segmentation
 *
 * Splits text into fixed-size chunks with overlap, preserving
 * sentence boundaries to maintain semantic coherence.
 */
class TextChunker {
public:
  /**
   * Constructor
   * @param chunkSize Target number of words per chunk (default: 500)
   * @param overlapSize Number of overlapping words between chunks (default: 50)
   */
  explicit TextChunker(int chunkSize = 500, int overlapSize = 50);

  /**
   * Chunk a single text block
   * @param text Input text to be chunked
   * @return Vector of text chunks
   */
  std::vector<std::string> chunk(const std::string &text);

  /**
   * Chunk multiple text blocks (e.g., PDF pages)
   * @param texts Vector of input texts
   * @return Vector of all chunks from all texts
   */
  std::vector<std::string> chunkMultiple(const std::vector<std::string> &texts);

private:
  int chunkSize_;
  int overlapSize_;

  std::vector<std::string> splitIntoWords(const std::string &text);
  std::string joinWords(const std::vector<std::string> &words, int start,
                        int end);
};

} // namespace guardian

#endif // TEXT_CHUNKER_H
