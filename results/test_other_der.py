import os
import subprocess

output_file = "output/other_der_results.txt"
pyannote_processed_files = [
    "output/metrics_tests/pyannote/diarization_annote_1.txt",
    "output/metrics_tests/pyannote/diarization_annote_2.txt",
    "output/metrics_tests/pyannote/diarization_annote_3.txt",
    "output/metrics_tests/pyannote/diarization_annote_4.txt",
    "output/metrics_tests/pyannote/diarization_annote_5.txt",
]

with open(output_file, "w") as f:
    f.write("Other DER Results\n")
    f.write("===================\n\n")

    ground_truth_file = "output/ground_truth_zero_swapped.json"

    f.write("\n## Pyannote Diarization - Processed\n")
    f.flush()

    for index, file_path in enumerate(pyannote_processed_files):
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "der.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )
    
    f.write("\n## NEMO Diarization - Processed\n")
    f.flush()
    
    nemo_processed_files = [
        "output/metrics_tests/nemo/diarization_nemo_1.txt",
        "output/metrics_tests/nemo/diarization_nemo_2.txt",
        "output/metrics_tests/nemo/diarization_nemo_3.txt",
        "output/metrics_tests/nemo/diarization_nemo_4.txt",
        "output/metrics_tests/nemo/diarization_nemo_5.txt",
    ]
    ground_truth_file = "output/ground_truth_zero_numeric.json"

    for index, file_path in enumerate(nemo_processed_files):
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "der.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )
        
    f.write("\n## PyAnnote Diarization - NOT Processed\n")
    f.flush()
    
    pyannote_unprocessed_files = [
        "output/metrics_tests/pyannote_unprocessed/diarization_annote_nonprocessed_1.txt",
        "output/metrics_tests/pyannote_unprocessed/diarization_annote_nonprocessed_2.txt",
        "output/metrics_tests/pyannote_unprocessed/diarization_annote_nonprocessed_3.txt",
        "output/metrics_tests/pyannote_unprocessed/diarization_annote_nonprocessed_4.txt",
        "output/metrics_tests/pyannote_unprocessed/diarization_annote_nonprocessed_5.txt",
    ]
    ground_truth_file = "output/ground_truth_zero.json"

    for index, file_path in enumerate(pyannote_unprocessed_files):
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "der.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )
        
    f.write("\n## NEMO Diarization - NOT Processed\n")
    f.flush()
    
    ground_truth_file = "output/ground_truth_zero_numeric.json"
    nemo_unprocessed_files = [
        "output/metrics_tests/nemo_unprocessed/diarization_nemo_nonprocessed_1.txt",
        "output/metrics_tests/nemo_unprocessed/diarization_nemo_nonprocessed_2.txt",
        "output/metrics_tests/nemo_unprocessed/diarization_nemo_nonprocessed_3.txt",
        "output/metrics_tests/nemo_unprocessed/diarization_nemo_nonprocessed_4.txt",
        "output/metrics_tests/nemo_unprocessed/diarization_nemo_nonprocessed_5.txt",
    ]

    for index, file_path in enumerate(nemo_unprocessed_files):
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "der.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )