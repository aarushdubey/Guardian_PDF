#ifndef RABIN_KARP_DEDUP_H
#define RABIN_KARP_DEDUP_H

#include <string>
#include <unordered_set>
#include <vector>

namespace guardian {

/**
 * RabinKarpDeduplicator - Rolling hash-based text deduplication
 *
 * Uses Rabin-Karp algorithm to efficiently detect and remove
 * duplicate or highly similar text chunks (>90% similarity).
 * This is the "DAA showcase" component of GuardianPDF.
 */
class RabinKarpDeduplicator {
public:
  /**
   * Constructor
   * @param similarityThreshold Minimum similarity (0.0-1.0) to consider
   * duplicates (default: 0.9)
   */
  explicit RabinKarpDeduplicator(double similarityThreshold = 0.9);

  /**
   * Remove duplicate chunks from input
   * @param chunks Input vector of text chunks
   * @return Deduplicated vector with unique chunks only
   */
  std::vector<std::string> deduplicate(const std::vector<std::string> &chunks);

  /**
   * Get statistics from last deduplication run
   */
  struct Stats {
    int originalCount;
    int uniqueCount;
    int duplicatesRemoved;
    double deduplicationRatio;
  };

  Stats getStats() const { return stats_; }

private:
  double similarityThreshold_;
  Stats stats_;

  // Rabin-Karp parameters
  static constexpr unsigned long long BASE = 257;
  static constexpr unsigned long long MOD = 1000000007;

  /**
   * Compute rolling hash for a string
   */
  unsigned long long computeHash(const std::string &text) const;

  /**
   * Calculate Jaccard similarity between two strings
   */
  double calculateSimilarity(const std::string &a, const std::string &b) const;

  /**
   * Convert string to set of word n-grams for similarity comparison
   */
  std::unordered_set<std::string> getNGrams(const std::string &text,
                                            int n = 3) const;
};

} // namespace guardian

#endif // RABIN_KARP_DEDUP_H
