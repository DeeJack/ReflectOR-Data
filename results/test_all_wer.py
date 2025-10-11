import os
import subprocess

output_file = "output/all_wer_results.txt"
ground_truth_file = "output/manual_transcript_zero.txt"

with open(output_file, "w") as f:
    f.write("All WER Results\n")
    f.write("===================\n\n")

    base_path = "output/metrics_tests"
    pro_processed_files = [
        "pro_2.5-temp0/zero_transcription_temp0_1.txt",
        "pro_2.5-temp0/zero_transcription_temp0_2.txt",
        "pro_2.5-temp0/zero_transcription_temp0_3.txt",
        "pro_2.5-temp0/zero_transcription_temp0_4.txt",
        "pro_2.5-temp0/zero_transcription_temp0_5.txt",
    ]

    f.write("\n## Gemini 2.5 - Temp 0.0 - Processed\n")
    f.flush()

    for index, file in enumerate(pro_processed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
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

    for index, file in enumerate(flash_processed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
            stdout=f,
        )

    f.write("\n## Whisper API - Processed\n")
    f.flush()

    whisper_processed_files = [
        "whisper-api/whisper_1.txt",
        "whisper-api/whisper_2.txt",
        "whisper-api/whisper_3.txt",
        "whisper-api/whisper_4.txt",
        "whisper-api/whisper_5.txt",
    ]

    for index, file in enumerate(whisper_processed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
            stdout=f,
        )

    f.write("\n## Whisperx-large-v3 - Processed\n")
    f.flush()

    whisperx_processed_files = [
        "whisperx_largev3/first_audio_processed_1.txt",
        "whisperx_largev3/first_audio_processed_2.txt",
        "whisperx_largev3/first_audio_processed_3.txt",
        "whisperx_largev3/first_audio_processed_4.txt",
        "whisperx_largev3/first_audio_processed_5.txt",
    ]

    for index, file in enumerate(whisperx_processed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
            stdout=f,
        )

    f.write("\n## Gemini-2.5-pro - NOT Processed\n")
    f.flush()

    pro_unprocessed_files = [
        "pro_temp0_unprocessed/pro_nonprocessed_1.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_2.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_3.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_4.txt",
        "pro_temp0_unprocessed/pro_nonprocessed_5.txt",
    ]
    for index, file in enumerate(pro_unprocessed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
            stdout=f,
        )

    f.write("\n## Gemini-2.5-Flash - NOT Processed\n")
    f.flush()

    flash_unprocessed_files = [
        "flash_unprocessed/flash_nonprocessed_1.txt",
        "flash_unprocessed/flash_nonprocessed_2.txt",
        "flash_unprocessed/flash_nonprocessed_3.txt",
        "flash_unprocessed/flash_nonprocessed_4.txt",
        "flash_unprocessed/flash_nonprocessed_5.txt",
    ]

    for index, file in enumerate(flash_unprocessed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
            stdout=f,
        )

    f.write("\n## Whisper-API - NOT Processed\n")
    f.flush()

    whisper_unprocessed_files = [
        "whisper_unprocessed/whisper_nonprocessed_1.txt",
        "whisper_unprocessed/whisper_nonprocessed_2.txt",
        "whisper_unprocessed/whisper_nonprocessed_3.txt",
        "whisper_unprocessed/whisper_nonprocessed_4.txt",
        "whisper_unprocessed/whisper_nonprocessed_5.txt",
    ]

    for index, file in enumerate(whisper_unprocessed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
            stdout=f,
        )

    f.write("\n## Whisperx-large-v3 - NOT Processed\n")
    f.flush()

    whisperx_unprocessed_files = [
        "whisperx_largev3_unprocessed/first_audio_nonprocessed_1.txt",
        "whisperx_largev3_unprocessed/first_audio_nonprocessed_2.txt",
        "whisperx_largev3_unprocessed/first_audio_nonprocessed_3.txt",
        "whisperx_largev3_unprocessed/first_audio_nonprocessed_4.txt",
        "whisperx_largev3_unprocessed/first_audio_nonprocessed_5.txt",
    ]
    for index, file in enumerate(whisperx_unprocessed_files, start=1):
        file_path = os.path.join(base_path, file)
        f.write(f"### {file}\n")
        f.flush()
        result = subprocess.run(
            ["python3", "compute_wer.py", ground_truth_file, file_path],
            stdout=f,
        )

