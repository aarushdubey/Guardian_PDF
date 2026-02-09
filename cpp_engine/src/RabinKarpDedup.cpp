#include "RabinKarpDedup.h"
#include <algorithm>
#include <sstream>
#include <unordered_map>

namespace guardian {

RabinKarpDeduplicator::RabinKarpDeduplicator(double similarityThreshold)
    : similarityThreshold_(similarityThreshold) {
  stats_ = {0, 0, 0, 0.0};
}

unsigned long long
RabinKarpDeduplicator::computeHash(const std::string &text) const {
  unsigned long long hash = 0;
  unsigned long long pow = 1;

  for (char c : text) {
    hash = (hash + (static_cast<unsigned long long>(c) * pow)) % MOD;
    pow = (pow * BASE) % MOD;
  }

  return hash;
}

std::unordered_set<std::string>
RabinKarpDeduplicator::getNGrams(const std::string &text, int n) const {
  std::unordered_set<std::string> ngrams;
  std::istringstream stream(text);
  std::vector<std::string> words;
  std::string word;

  // Split into words
  while (stream >> word) {
    // Convert to lowercase for comparison
    std::transform(word.begin(), word.end(), word.begin(), ::tolower);
    words.push_back(word);
  }

  // Generate n-grams
  for (size_t i = 0; i + n <= words.size(); ++i) {
    std::string ngram;
    for (int j = 0; j < n; ++j) {
      if (j > 0)
        ngram += " ";
      ngram += words[i + j];
    }
    ngrams.insert(ngram);
  }

  return ngrams;
}

double RabinKarpDeduplicator::calculateSimilarity(const std::string &a,
                                                  const std::string &b) const {
  auto ngramsA = getNGrams(a);
  auto ngramsB = getNGrams(b);

  if (ngramsA.empty() && ngramsB.empty()) {
    return 1.0; // Both empty = identical
  }

  if (ngramsA.empty() || ngramsB.empty()) {
    return 0.0; // One empty = completely different
  }

  // Jaccard similarity: |A ∩ B| / |A ∪ B|
  int intersection = 0;
  for (const auto &ngram : ngramsA) {
    if (ngramsB.count(ngram)) {
      intersection++;
    }
  }

  int unionSize = ngramsA.size() + ngramsB.size() - intersection;
  return static_cast<double>(intersection) / unionSize;
}

std::vector<std::string>
RabinKarpDeduplicator::deduplicate(const std::vector<std::string> &chunks) {
  std::vector<std::string> uniqueChunks;
  std::unordered_map<unsigned long long, std::vector<int>> hashToIndices;

  stats_.originalCount = chunks.size();
  stats_.uniqueCount = 0;
  stats_.duplicatesRemoved = 0;

  // Group chunks by hash
  for (size_t i = 0; i < chunks.size(); ++i) {
    unsigned long long hash = computeHash(chunks[i]);
    hashToIndices[hash].push_back(i);
  }

  std::vector<bool> isDuplicate(chunks.size(), false);

  // For each hash bucket, check actual similarity
  for (const auto &[hash, indices] : hashToIndices) {
    for (size_t i = 0; i < indices.size(); ++i) {
      if (isDuplicate[indices[i]])
        continue;

      for (size_t j = i + 1; j < indices.size(); ++j) {
        if (isDuplicate[indices[j]])
          continue;

        double similarity =
            calculateSimilarity(chunks[indices[i]], chunks[indices[j]]);

        if (similarity >= similarityThreshold_) {
          isDuplicate[indices[j]] = true;
          stats_.duplicatesRemoved++;
        }
      }
    }
  }

  // Collect unique chunks
  for (size_t i = 0; i < chunks.size(); ++i) {
    if (!isDuplicate[i]) {
      uniqueChunks.push_back(chunks[i]);
    }
  }

  stats_.uniqueCount = uniqueChunks.size();
  stats_.deduplicationRatio =
      stats_.originalCount > 0
          ? 1.0 -
                (static_cast<double>(stats_.uniqueCount) / stats_.originalCount)
          : 0.0;

  return uniqueChunks;
}

} // namespace guardian
