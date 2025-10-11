import json
import sys
import argparse
from typing import List, Dict, Any, Tuple


def load_diarization_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Load diarization data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        List of diarization segments
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        sys.exit(1)


def find_ground_truth_speaker(segment: Dict[str, Any], ground_truth: List[Dict[str, Any]]) -> str | None:
    """
    Find the speaker for a given segment based on ground truth intervals.
    
    Args:
        segment: Test segment with 'start', 'end', and 'speaker' fields
        ground_truth: List of ground truth segments
        
    Returns:
        The speaker ID from ground truth, or None if no overlap found
    """
    # Convert start/end to float in case they are strings
    segment_start = float(segment['start'])
    segment_end = float(segment['end'])
    
    # Find overlapping ground truth segments
    overlapping_speakers = []
    
    for gt_segment in ground_truth:
        gt_start = float(gt_segment['start'])
        gt_end = float(gt_segment['end'])
        
        # Check if there's any overlap between the segments
        overlap_start = max(segment_start, gt_start)
        overlap_end = min(segment_end, gt_end)
        
        if overlap_start < overlap_end:  # There is overlap
            overlap_duration = overlap_end - overlap_start
            overlapping_speakers.append((str(gt_segment['speaker']), overlap_duration))
    
    if not overlapping_speakers:
        return None
    
    # Return the speaker with the maximum overlap
    overlapping_speakers.sort(key=lambda x: x[1], reverse=True)
    return overlapping_speakers[0][0]


def compute_der(ground_truth_file: str, test_file: str) -> Tuple[float, int, int]:
    """
    Compute the Diarization Error Rate (DER).
    
    Args:
        ground_truth_file: Path to ground truth JSON file
        test_file: Path to test JSON file
        
    Returns:
        Tuple of (DER, correct_count, total_count)
    """
    # Load both files
    ground_truth = load_diarization_file(ground_truth_file)
    test_data = load_diarization_file(test_file)
    
    print(f"Loaded {len(ground_truth)} ground truth segments")
    print(f"Loaded {len(test_data)} test segments")
    
    correct_count = 0
    total_count = len(test_data)
    
    # For each segment in test data, check if speaker matches ground truth
    for i, test_segment in enumerate(test_data):
        gt_speaker = find_ground_truth_speaker(test_segment, ground_truth)
        test_speaker = str(test_segment['speaker'])  # Convert to string for comparison
        
        if gt_speaker is not None and gt_speaker == test_speaker:
            correct_count += 1
            print(f"Segment {i+1}: CORRECT - {test_speaker} (time: {test_segment['start']:.2f}-{test_segment['end']:.2f})")
        else:
            if gt_speaker is None:
                print(f"Segment {i+1}: ERROR - No ground truth overlap for {test_speaker} (time: {test_segment['start']:.2f}-{test_segment['end']:.2f})")
            else:
                print(f"Segment {i+1}: ERROR - Expected {gt_speaker}, got {test_speaker} (time: {test_segment['start']:.2f}-{test_segment['end']:.2f})")
    
    # Compute DER as 1 - (correct/total)
    der = 1 - (correct_count / total_count) if total_count > 0 else 1.0
    
    return der, correct_count, total_count


def main():
    parser = argparse.ArgumentParser(
        description="Compute Diarization Error Rate (DER) between ground truth and test files"
    )
    parser.add_argument("ground_truth", help="Path to ground truth JSON file")
    parser.add_argument("test_file", help="Path to test JSON file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    original_stdout = sys.stdout
    if not args.verbose:
        # Suppress individual segment results if not verbose
        sys.stdout = open('/dev/null', 'w')
        
    der, correct, total = compute_der(args.ground_truth, args.test_file)
    
    if not args.verbose:
        sys.stdout.close()
        sys.stdout = original_stdout
    
    print("\n" + "="*50)
    print("DER COMPUTATION RESULTS")
    print("="*50)
    print(f"Ground truth file: {args.ground_truth}")
    print(f"Test file: {args.test_file}")
    print(f"Total segments: {total}")
    print(f"Correct segments: {correct}")
    print(f"Incorrect segments: {total - correct}")
    print(f"Accuracy: {correct/total*100:.2f}%" if total > 0 else "Accuracy: N/A")
    print(f"DER: {der:.4f}")
    print("="*50)


if __name__ == "__main__":
    main()
