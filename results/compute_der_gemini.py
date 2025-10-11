"""
Compute the DER for the Gemini models
"""

import argparse
import re
import sys
from typing import List, Tuple, Optional
from difflib import SequenceMatcher
from dataclasses import dataclass


@dataclass
class TranscriptSegment:
    """Represents a segment of transcription with speaker and text."""

    speaker: str
    text: str
    timestamp: Optional[str] = None

    def __str__(self):
        if self.timestamp:
            return f"[{self.timestamp}] {self.speaker}: {self.text}"
        return f"{self.speaker}: {self.text}"


def normalize_speaker_name(speaker: str) -> str:
    """
    Maps name variations to standard speaker names.
    """
    speaker = speaker.strip()
    speaker_mappings = {
        "professore": "Professore",
        "professor": "Professore",
        "prof": "Professore",
        "studente 1": "Studente 1",
        "student 1": "Studente 1",
        "studente1": "Studente 1",
        "martin": "Studente 1",
        "studente 2": "Studente 2",
        "student 2": "Studente 2",
        "studente2": "Studente 2",
        "cecilia": "Studente 2",
    }
    return speaker_mappings.get(speaker.lower(), speaker)


def parse_ground_truth_file(file_path: str) -> List[TranscriptSegment]:
    """
    Parse ground truth transcription file (format: "Speaker: text").
    """
    segments = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Ground truth file '{file_path}' not found.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Could not decode '{file_path}'. Please check file encoding.")
        sys.exit(1)

    lines = content.split("\n")
    current_segment = None

    # Adds segments, joining lines that don't start with a speaker label
    for line in lines:
        line = line.strip()
        if not line:
            continue

        speaker_match = re.match(r"^([^:]+):\s*(.*)$", line)
        if speaker_match:
            if current_segment:
                segments.append(current_segment)

            speaker = normalize_speaker_name(speaker_match.group(1))
            text = speaker_match.group(2).strip()
            current_segment = TranscriptSegment(speaker=speaker, text=text)
        else:
            if current_segment:
                current_segment.text += " " + line

    # Add final segment
    if current_segment:
        segments.append(current_segment)
    return segments


def parse_test_file(file_path: str) -> List[TranscriptSegment]:
    """
    Parse test transcription file (format: "[timestamp] Speaker: text").
    """
    segments = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Test file '{file_path}' not found.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Could not decode '{file_path}'. Please check file encoding.")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match pattern: [timestamp] Speaker: text
        match = re.match(r"^\[([^\]]+)\]\s*([^:]+):\s*(.*)$", line)
        if match:
            timestamp = match.group(1)
            speaker = normalize_speaker_name(match.group(2))
            text = match.group(3).strip()

            segment = TranscriptSegment(speaker=speaker, text=text, timestamp=timestamp)
            segments.append(segment)
    return segments


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison by removing punctuation and standardizing spacing.
    """
    text = text.lower()  # lowercase
    text = re.sub(r'[.,;!?()"\[\]{}]', "", text)  # Remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Standardize whitespace
    return text


def text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two text segments.
    Prioritizes exact matches and penalizes excessive length differences.

    Returns:
        Similarity score between 0 and 1
    """
    # Normalize both texts
    norm_text1 = normalize_text(text1)
    norm_text2 = normalize_text(text2)

    # If either text is empty, no similarity
    if not norm_text1 or not norm_text2:
        return 0.0

    # Use SequenceMatcher for basic similarity
    matcher = SequenceMatcher(None, norm_text1, norm_text2)
    basic_similarity = matcher.ratio()

    # Determine shorter and longer texts
    shorter_text = norm_text1 if len(norm_text1) <= len(norm_text2) else norm_text2
    longer_text = norm_text2 if len(norm_text1) <= len(norm_text2) else norm_text1

    # Calculate length ratio (shorter/longer)
    length_ratio = len(shorter_text) / len(longer_text) if len(longer_text) > 0 else 0

    # If texts are very similar in length, prioritize basic similarity
    if length_ratio >= 0.8:
        return basic_similarity

    # Check for exact substring containment
    if shorter_text in longer_text:
        if length_ratio >= 0.9:
            containment_score = 0.95 + (0.05 * length_ratio)
        elif length_ratio >= 0.7:
            containment_score = 0.85 + (0.1 * length_ratio)
        else:
            # Penalize cases where shorter text is much smaller than longer text
            containment_score = 0.6 + (0.25 * length_ratio)

        return max(basic_similarity, containment_score)

    # Check for fuzzy word-based matching
    words1 = shorter_text.split()
    words2 = longer_text.split()

    if len(words1) > 0:
        # Count consecutive matching words from the beginning
        consecutive_matches = 0
        for i, word in enumerate(words1):
            if i < len(words2) and word == words2[i]:
                consecutive_matches += 1
            else:
                break

        # Count how many words from shorter text appear in longer text
        matching_words = sum(1 for word in words1 if word in words2)
        word_match_ratio = matching_words / len(words1)

        # Prioritize consecutive matches from the beginning
        consecutive_ratio = consecutive_matches / len(words1)

        # If most words match and there's good consecutive matching
        if word_match_ratio >= 0.8 and consecutive_ratio >= 0.6:
            # Apply length penalty for very different lengths
            length_penalty = max(0, (1 - length_ratio) * 0.3)
            fuzzy_score = (
                0.7 + (0.2 * word_match_ratio) + (0.1 * consecutive_ratio)
            ) - length_penalty
            return max(basic_similarity, min(fuzzy_score, 0.95))
        elif word_match_ratio >= 0.7:
            # Standard fuzzy matching with length penalty
            length_penalty = max(0, (1 - length_ratio) * 0.2)
            fuzzy_score = (0.6 + (0.3 * word_match_ratio)) - length_penalty
            return max(basic_similarity, min(fuzzy_score, 0.85))

    return basic_similarity


def find_best_match_in_test(
    gt_segment: TranscriptSegment,
    test_candidates: List[TranscriptSegment],
    similarity_threshold: float = 0.5,
) -> Tuple[Optional[int], float]:
    """
    Find the best matching test segment for the given ground truth segment.
    First checks for exact matches, then falls back to similarity matching.

    Args:
        gt_segment: Ground truth segment to find a match for
        test_candidates: List of test segments to search in
        similarity_threshold: Minimum similarity threshold

    Returns:
        Tuple of (best_match_index, similarity_score) or (None, 0.0)
    """
    # Normalize GT text for exact matching
    gt_normalized = normalize_text(gt_segment.text)

    # First pass: Look for exact matches
    for i, test_candidate in enumerate(test_candidates):
        test_normalized = normalize_text(test_candidate.text)
        if gt_normalized in test_normalized:
            return i, 1.0  # Perfect match

    # Second pass: Use similarity matching if no exact match found
    best_match_idx = None
    best_similarity = 0.0

    for i, test_candidate in enumerate(test_candidates):
        similarity = text_similarity(gt_segment.text, test_candidate.text)

        if similarity > best_similarity and similarity >= similarity_threshold:
            best_similarity = similarity
            best_match_idx = i

    return best_match_idx, best_similarity


def compute_der_gt_based(
    ground_truth_segments: List[TranscriptSegment],
    test_segments: List[TranscriptSegment],
    verbose: bool = False,
) -> Tuple[float, int, int, List[dict]]:
    """
    Compute Diarization Error Rate (DER) by matching GT segments to test segments.
    DER is calculated based on how many ground truth segments are correctly matched.

    Args:
        ground_truth_segments: List of ground truth segments
        test_segments: List of test segments
        verbose: Whether to print detailed matching information

    Returns:
        Tuple of (DER, correct_count, total_gt_count, match_details)
    """
    if not ground_truth_segments:
        print("Warning: No ground truth segments found")
        return 1.0, 0, 0, []

    if not test_segments:
        print("Warning: No test segments found")
        return 1.0, 0, len(ground_truth_segments), []

    correct_count = 0
    match_details = []

    if verbose:
        print(
            f"\nMatching {len(ground_truth_segments)} ground truth segments against {len(test_segments)} test segments..."
        )

    for i, gt_segment in enumerate(ground_truth_segments):
        # Find the best match from ALL test segments
        best_match_idx, similarity = find_best_match_in_test(gt_segment, test_segments)

        match_info = {
            "gt_index": i,
            "gt_segment": gt_segment,
            "test_index": best_match_idx,
            "test_segment": (
                test_segments[best_match_idx] if best_match_idx is not None else None
            ),
            "similarity": similarity,
            "correct": False,
        }

        if best_match_idx is not None:
            test_segment = test_segments[best_match_idx]

            # Check if speakers match
            if gt_segment.speaker == test_segment.speaker:
                correct_count += 1
                match_info["correct"] = True

                if verbose:
                    print(
                        f"✓ GT {i+1}: CORRECT - {gt_segment.speaker} "
                        f"(similarity: {similarity:.3f})"
                    )
                    print(f"  GT text:   {gt_segment.text[:80]}...")
                    print(f"  Test text: {test_segment.text[:80]}...")
            else:
                if verbose:
                    print(
                        f"✗ GT {i+1}: WRONG SPEAKER - Expected '{gt_segment.speaker}', "
                        f"got '{test_segment.speaker}' (similarity: {similarity:.3f})"
                    )
                    print(f"  GT text:   {gt_segment.text[:80]}...")
                    print(f"  Test text: {test_segment.text[:80]}...")
        else:
            if verbose:
                print(f"✗ GT {i+1}: NO MATCH - {gt_segment.speaker}")
                print(f"  GT text: {gt_segment.text[:80]}...")

        match_details.append(match_info)

        if verbose:
            print()

    total_count = len(ground_truth_segments)
    der = 1 - (correct_count / total_count) if total_count > 0 else 1.0

    return der, correct_count, total_count, match_details


def print_summary(
    ground_truth_file: str,
    test_file: str,
    der: float,
    correct: int,
    total: int,
    match_details: List[dict],
):
    """Print summary of DER computation results."""
    print("\n" + "=" * 70)
    print("DIARIZATION ERROR RATE (DER) COMPUTATION RESULTS")
    print("=" * 70)
    print(f"Ground truth file: {ground_truth_file}")
    print(f"Test file: {test_file}")
    print(f"Total ground truth segments: {total}")
    print(f"Correctly matched GT segments: {correct}")
    print(f"Incorrectly matched GT segments: {total - correct}")

    # Count unique test segments used
    used_test_segments = set()
    for match in match_details:
        if match["test_index"] is not None:
            used_test_segments.add(match["test_index"])

    print(f"Test segments used in matching: {len(used_test_segments)}")
    print(f"GT Accuracy: {correct/total*100:.2f}%" if total > 0 else "GT Accuracy: N/A")
    print(f"DER: {der:.4f} ({der*100:.2f}%)")

    # Speaker-wise breakdown (based on ground truth speakers)
    speaker_stats = {}
    for match in match_details:
        gt_speaker = match["gt_segment"].speaker
        if gt_speaker not in speaker_stats:
            speaker_stats[gt_speaker] = {"total": 0, "correct": 0}
        speaker_stats[gt_speaker]["total"] += 1
        if match["correct"]:
            speaker_stats[gt_speaker]["correct"] += 1

    print("\nSpeaker-wise GT accuracy:")
    for speaker, stats in speaker_stats.items():
        accuracy = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
        print(f"  {speaker}: {stats['correct']}/{stats['total']} ({accuracy:.1f}%)")

    print("=" * 70)


def main():
    """Main function to run DER computation."""
    parser = argparse.ArgumentParser(
        description="Compute Diarization Error Rate (DER) by matching ground truth segments to test segments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compute_der_gemini_gt_based.py output/manual_transcript_zero.txt output/metrics_tests/pro_temp0_unprocessed/pro_nonprocessed_1.txt
  python compute_der_gemini_gt_based.py ground_truth.txt test.txt -v
        """,
    )

    parser.add_argument(
        "ground_truth",
        help="Path to ground truth transcription file (format: 'Speaker: text')",
    )
    parser.add_argument(
        "test_file",
        help="Path to test transcription file (format: '[timestamp] Speaker: text')",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output showing segment matching details",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.3,
        help="Minimum text similarity threshold for matching (default: 0.3)",
    )

    args = parser.parse_args()

    # Parse input files
    if args.verbose:
        print("Parsing ground truth file...")
    ground_truth_segments = parse_ground_truth_file(args.ground_truth)

    if args.verbose:
        print("Parsing test file...")
    test_segments = parse_test_file(args.test_file)

    if not ground_truth_segments:
        print("Error: No segments found in ground truth file")
        sys.exit(1)

    if not test_segments:
        print("Error: No segments found in test file")
        sys.exit(1)

    # Compute DER
    der, correct, total, match_details = compute_der_gt_based(
        ground_truth_segments, test_segments, args.verbose
    )

    # Print summary
    print_summary(args.ground_truth, args.test_file, der, correct, total, match_details)


if __name__ == "__main__":
    main()

