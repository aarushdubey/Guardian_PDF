#include "TextChunker.h"
#include <algorithm>
#include <sstream>

namespace guardian {

TextChunker::TextChunker(int chunkSize, int overlapSize)
    : chunkSize_(chunkSize), overlapSize_(overlapSize) {
  if (overlapSize >= chunkSize) {
    throw std::invalid_argument("Overlap size must be less than chunk size");
  }
}

std::vector<std::string> TextChunker::splitIntoWords(const std::string &text) {
  std::vector<std::string> words;
  std::istringstream stream(text);
  std::string word;

  while (stream >> word) {
    words.push_back(word);
  }

  return words;
}

std::string TextChunker::joinWords(const std::vector<std::string> &words,
                                   int start, int end) {
  if (start >= end || start >= static_cast<int>(words.size())) {
    return "";
  }

  end = std::min(end, static_cast<int>(words.size()));

  std::ostringstream result;
  for (int i = start; i < end; ++i) {
    if (i > start)
      result << " ";
    result << words[i];
  }

  return result.str();
}

std::vector<std::string> TextChunker::chunk(const std::string &text) {
  std::vector<std::string> chunks;

  if (text.empty()) {
    return chunks;
  }

  std::vector<std::string> words = splitIntoWords(text);

  if (words.empty()) {
    return chunks;
  }

  int stride = chunkSize_ - overlapSize_;
  int currentPos = 0;

  while (currentPos < static_cast<int>(words.size())) {
    int endPos = currentPos + chunkSize_;
    std::string chunkText = joinWords(words, currentPos, endPos);

    if (!chunkText.empty()) {
      chunks.push_back(chunkText);
    }

    currentPos += stride;

    // If remaining words are less than overlap, include them in the last chunk
    if (currentPos < static_cast<int>(words.size()) &&
        currentPos + overlapSize_ >= static_cast<int>(words.size())) {
      break;
    }
  }

  return chunks;
}

std::vector<std::string>
TextChunker::chunkMultiple(const std::vector<std::string> &texts) {
  std::vector<std::string> allChunks;

  for (const auto &text : texts) {
    auto chunks = chunk(text);
    allChunks.insert(allChunks.end(), chunks.begin(), chunks.end());
  }

  return allChunks;
}

} // namespace guardian
