"""
Runs all the tests to compute the DER for Gemini models, saving to output/gemini_der_results.txt
"""

import os
import subprocess

output_file = "output/gemini_der_results.txt"

with open(output_file, "w") as f:
    f.write("Gemini DER Results\n")
    f.write("===================\n\n")

    base_path = "output/metrics_tests"
    pro_processed_files = [
        "pro_2.5-temp0/zero_transcription_temp0_1.txt",
        "pro_2.5-temp0/zero_transcription_temp0_2.txt",
        "pro_2.5-temp0/zero_transcription_temp0_3.txt",
        "pro_2.5-temp0/zero_transcription_temp0_4.txt",
        "pro_2.5-temp0/zero_transcription_temp0_5.txt",
    ]
    ground_truth_file = "output/gemini_der_ground_truth.txt"

    f.write("\n## Gemini 2.5 - Temp 0.0 - Processed\n")
    f.flush()

    for index, file in enumerate(pro_processed_files):
        file_path = os.path.join(base_path, file)
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "compute_der_gemini.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )

    flash_processed_files = [
        "flash-.2.5/flash_1.txt",
        "flash-.2.5/flash_2.txt",
        "flash-.2.5/flash_3.txt",
        "flash-.2.5/flash_4.txt",
        "flash-.2.5/flash_5.txt",
    ]

    f.write("\n## Gemini 2.5-Flash - Processed\n")
    f.flush()

    for index, file in enumerate(flash_processed_files):
        file_path = os.path.join(base_path, file)
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "compute_der_gemini.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )

    f.write("\n## Gemini 2.5 - Temp 0.0 - Raw\n")
    f.flush()

    pro_unprocessed_files = [
        "pro_temp0_unprocessed/pro_nonprocessed_1.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_2.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_3.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_4.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_5.txt",
    ]

    for index, file in enumerate(pro_unprocessed_files):
        file_path = os.path.join(base_path, file)
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "compute_der_gemini.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )

    flash_unprocessed_files = [
        "flash_unprocessed/flash_nonprocessed_1.txt",
        "flash_unprocessed/flash_nonprocessed_2.txt",
        "flash_unprocessed/flash_nonprocessed_3.txt",
        "flash_unprocessed/flash_nonprocessed_4.txt",
        "flash_unprocessed/flash_nonprocessed_5.txt",
    ]

    f.write("\n## Gemini 2.5-Flash - Raw\n")
    f.flush()
    for index, file in enumerate(flash_unprocessed_files):
        file_path = os.path.join(base_path, file)
        f.write("\n### {}\n".format(index + 1))
        f.flush()
        subprocess.run(
            [
                "python3",
                "compute_der_gemini.py",
                ground_truth_file,
                file_path,
            ],
            stdout=f,
        )

