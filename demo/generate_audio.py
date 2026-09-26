#!/usr/bin/env python3
"""
Generate audio segments for PromptPulse Studio demo video using edge-tts.
"""

import os
import sys
import json
import asyncio
import subprocess

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "voiceover_script.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio_segments")

VOICE = "en-US-AndrewNeural"
RATE = "+4%"

async def generate_segment(segment_id, text, output_file):
    cmd = [
        "edge-tts",
        "--voice", VOICE,
        "--rate", RATE,
        "--text", text,
        "--write-media", output_file
    ]
    process = await asyncio.create_subprocess_exec(*cmd)
    await process.communicate()
    print(f"✅ Generated segment {segment_id}: {output_file}")

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        segments = json.load(f)

    tasks = []
    for seg in segments:
        out_file = os.path.join(OUTPUT_DIR, f"seg_{seg['id']:02d}.mp3")
        tasks.append(generate_segment(seg["id"], seg["text"], out_file))

    await asyncio.gather(*tasks)
    print("All audio segments successfully generated!")

if __name__ == "__main__":
    asyncio.run(main())
