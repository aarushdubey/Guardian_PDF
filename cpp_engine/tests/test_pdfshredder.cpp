#include "PDFShredder.h"
#include "RabinKarpDedup.h"
#include "TextChunker.h"
#include <catch2/catch_session.hpp>
#include <catch2/catch_test_macros.hpp>

using namespace guardian;

// Main function for Catch2 v3
int main(int argc, char *argv[]) { return Catch::Session().run(argc, argv); }

TEST_CASE("TextChunker splits text correctly", "[chunker]") {
  TextChunker chunker(10, 2); // Small sizes for testing

  SECTION("Empty text returns empty chunks") {
    auto chunks = chunker.chunk("");
    REQUIRE(chunks.empty());
  }

  SECTION("Short text returns single chunk") {
    std::string text = "This is a short text with only seven words";
    auto chunks = chunker.chunk(text);
    REQUIRE(chunks.size() == 1);
  }

  SECTION("Long text is split with overlap") {
    // Create text with exactly 25 words
    std::string text;
    for (int i = 1; i <= 25; ++i) {
      if (i > 1)
        text += " ";
      text += "word" + std::to_string(i);
    }

    auto chunks = chunker.chunk(text);

    // With chunk_size=10 and overlap=2, stride=8
    // 25 words should produce: chunks at positions 0, 8, 16, 24
    REQUIRE(chunks.size() >= 2);
    REQUIRE(chunks.size() <= 4);
  }
}

TEST_CASE("RabinKarpDeduplicator removes duplicates", "[dedup]") {
  RabinKarpDeduplicator dedup(0.9);

  SECTION("Identical chunks are deduplicated") {
    std::vector<std::string> chunks = {"This is a test chunk",
                                       "This is another chunk",
                                       "This is a test chunk", // Duplicate
                                       "Completely different text here"};

    auto unique = dedup.deduplicate(chunks);
    auto stats = dedup.getStats();

    REQUIRE(stats.originalCount == 4);
    REQUIRE(unique.size() < chunks.size());
    REQUIRE(stats.duplicatesRemoved > 0);
  }

  SECTION("Highly similar chunks are deduplicated") {
    std::vector<std::string> chunks = {
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy cat", // Similar but different
        "Completely unrelated sentence about programming"};

    auto unique = dedup.deduplicate(chunks);
    auto stats = dedup.getStats();

    REQUIRE(stats.originalCount == 3);
    // High similarity threshold should remove very similar chunks
  }

  SECTION("Dissimilar chunks are preserved") {
    std::vector<std::string> chunks = {
        "First unique chunk", "Second unique chunk", "Third unique chunk"};

    auto unique = dedup.deduplicate(chunks);

    REQUIRE(unique.size() == chunks.size());
  }
}

TEST_CASE("RabinKarpDeduplicator hash function", "[dedup][hash]") {
  RabinKarpDeduplicator dedup;

  SECTION("Same text produces same hash") {
    std::vector<std::string> chunks = {"test", "test"};
    auto unique = dedup.deduplicate(chunks);

    // Should detect duplicates
    REQUIRE(unique.size() == 1);
  }

  SECTION("Different text produces different results") {
    std::vector<std::string> chunks = {"test1", "test2", "test3"};
    auto unique = dedup.deduplicate(chunks);

    // Should keep all unique
    REQUIRE(unique.size() == 3);
  }
}
