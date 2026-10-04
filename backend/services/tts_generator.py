from kokoro import KPipeline
import soundfile as sf
import numpy as np
import os
import re


VOICE_MAP = {
    "HOST 1": "af_heart",
    "HOST 2": "am_adam",
}


def split_script(script: str) -> list[tuple[str, str]]:
    """Extract HOST 1 / HOST 2 dialogue from the podcast script."""

    lines = script.splitlines()
    segments = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        match = re.match(
            r"^(HOST 1|HOST 2)\s*:\s*(.+)$",
            line,
            re.IGNORECASE,
        )

        if match:
            speaker = match.group(1).upper()
            dialogue = match.group(2).strip()

            if dialogue:
                segments.append((speaker, dialogue))

    return segments


def generate_podcast_audio(script: str, output_path: str) -> str:
    """Generate a two-host podcast from a Gemini-generated script."""

    segments = split_script(script)

    if not segments:
        raise ValueError("No valid HOST 1 / HOST 2 dialogue found.")

    # Load Kokoro only when audio generation is requested.
    # This prevents the model from consuming large amounts
    # of memory when the FastAPI server starts.
    pipeline = KPipeline(lang_code="a")

    audio_segments = []

    for speaker, dialogue in segments:

        voice = VOICE_MAP.get(speaker)

        if not voice:
            continue

        generator = pipeline(
            dialogue,
            voice=voice,
            speed=1,
        )

        for _, _, audio in generator:
            audio_segments.append(audio)

    if not audio_segments:
        raise ValueError("No audio was generated.")

    combined_audio = np.concatenate(audio_segments)

    output_directory = os.path.dirname(output_path)

    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    sf.write(
        output_path,
        combined_audio,
        24000,
    )

    return output_path