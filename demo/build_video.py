"""Build the captioned ScriptProof demo from reviewed browser captures."""

from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"
FPS = 30

TIMELINE = (
    ("01-home.png", 9.20),
    ("02-input.png", 11.48),
    ("09-architecture.png", 15.56),
    ("03-research.png", 15.40),
    ("04-report-overview.png", 3.70),
    ("05-evidence.png", 15.06),
    ("06-continuity.png", 19.80),
    ("07-handoff.png", 14.42),
    ("09-architecture.png", 15.24),
    ("08-runtime-proof.png", 16.80),
)


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def srt_timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    whole_seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{whole_seconds:02},{milliseconds:03}"


def load_segments() -> list[dict]:
    transcript = json.loads((OUTPUT / "narration_asr.json").read_text())
    segments = transcript["segments"]
    for segment in segments:
        segment["text"] = segment["text"].strip().replace("parallel", "Parallel")
    return segments


def build_subtitles(segments: list[dict]) -> Path:
    blocks = []
    for index, segment in enumerate(segments, start=1):
        wrapped = "\n".join(textwrap.wrap(segment["text"], width=54))
        blocks.append(
            f"{index}\n{srt_timestamp(segment['start'])} --> "
            f"{srt_timestamp(segment['end'])}\n{wrapped}\n"
        )
    target = OUTPUT / "scriptproof-demo.srt"
    target.write_text("\n".join(blocks), encoding="utf-8")
    return target


def build_caption_images(segments: list[dict]) -> list[Path]:
    font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 39)
    targets = []
    for index, segment in enumerate(segments, start=1):
        lines = textwrap.wrap(segment["text"], width=58)
        canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        spacing = 8
        bounds = [draw.textbbox((0, 0), line, font=font) for line in lines]
        text_width = max(bound[2] - bound[0] for bound in bounds)
        line_height = max(bound[3] - bound[1] for bound in bounds)
        text_height = (line_height * len(lines)) + (spacing * (len(lines) - 1))
        box_width = text_width + 60
        box_height = text_height + 36
        left = (1920 - box_width) // 2
        top = 780 if index >= 25 else 1080 - box_height - 46
        draw.rounded_rectangle(
            (left, top, left + box_width, top + box_height),
            radius=12,
            fill=(23, 23, 20, 220),
        )
        y = top + 18
        for line, bound in zip(lines, bounds, strict=True):
            width = bound[2] - bound[0]
            draw.text(
                ((1920 - width) // 2, y),
                line,
                font=font,
                fill=(248, 248, 244, 255),
            )
            y += line_height + spacing
        target = OUTPUT / f"caption-{index:02}.png"
        canvas.save(target)
        targets.append(target)
    return targets


def build_visual_track() -> Path:
    clips = []
    for index, (filename, duration) in enumerate(TIMELINE, start=1):
        source = ASSETS / filename
        clip = OUTPUT / f"clip-{index:02}.mp4"
        frames = round(duration * FPS)
        filter_graph = (
            "zoompan="
            "z='min(max(zoom,pzoom)+0.00012,1.035)':"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s=1920x1080:fps={FPS},"
            f"trim=duration={duration:.2f},setpts=PTS-STARTPTS,format=yuv420p"
        )
        run(
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-i",
            str(source),
            "-vf",
            filter_graph,
            "-frames:v",
            str(frames),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            str(clip),
        )
        clips.append(clip)

    concat_file = OUTPUT / "visuals.txt"
    concat_file.write_text(
        "".join(f"file '{clip}'\n" for clip in clips), encoding="utf-8"
    )
    visual = OUTPUT / "scriptproof-demo-visual.mp4"
    run(
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(visual),
    )
    return visual


def build_demo() -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    segments = load_segments()
    build_subtitles(segments)
    captions = build_caption_images(segments)
    visual = build_visual_track()
    narration = OUTPUT / "narration.wav"
    target = OUTPUT / "scriptproof-demo-final.mp4"
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(visual),
        "-i",
        str(narration),
    ]
    for caption in captions:
        command.extend(("-loop", "1", "-framerate", "1", "-i", str(caption)))

    filters = ["[0:v]fade=t=in:st=0:d=0.5[base]"]
    previous = "base"
    for index, segment in enumerate(segments, start=1):
        output_label = f"captioned{index}"
        filters.append(
            f"[{previous}][{index + 1}:v]overlay=0:0:"
            f"enable='between(t,{segment['start']:.3f},{segment['end']:.3f})'"
            f"[{output_label}]"
        )
        previous = output_label
    command.extend(
        (
            "-filter_complex",
            ";".join(filters),
            "-map",
            f"[{previous}]",
            "-map",
            "1:a:0",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-t",
            "136.625",
            "-r",
            str(FPS),
            "-movflags",
            "+faststart",
            str(target),
        )
    )
    run(*command)
    return target


if __name__ == "__main__":
    print(build_demo())
