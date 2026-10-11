#!/usr/bin/env python3
"""Build the F-Droid repository icon from the APK's adaptive launcher layers."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
import sys
from zipfile import ZipFile

from PIL import Image


BACKGROUND = "res/drawable/ic_launcher_background.png"
FOREGROUND = "res/drawable/ic_launcher_foreground.png"
OUTPUT_SIZE = (512, 512)
# Keep the foreground mark at about 82% of the canvas width.
FOREGROUND_SCALE = 1.22


def main() -> None:
    if len(sys.argv) > 1:
        apk_path = Path(sys.argv[1])
    else:
        apk_files = sorted(Path("repo").glob("*.apk"))
        if len(apk_files) != 1:
            raise SystemExit(
                f"Oczekiwano dokładnie jednego APK w repo/, znaleziono: {len(apk_files)}."
            )
        apk_path = apk_files[0]

    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("icon.png")

    try:
        with ZipFile(apk_path) as apk:
            background = Image.open(BytesIO(apk.read(BACKGROUND))).convert("RGBA")
            foreground = Image.open(BytesIO(apk.read(FOREGROUND))).convert("RGBA")
    except KeyError as error:
        raise SystemExit(f"APK nie zawiera oczekiwanej warstwy ikony: {error}") from error

    if background.size != foreground.size:
        raise SystemExit(
            f"Warstwy ikony mają różne rozmiary: {background.size} i {foreground.size}."
        )

    scaled_size = tuple(round(dimension * FOREGROUND_SCALE) for dimension in foreground.size)
    foreground = foreground.resize(scaled_size, Image.Resampling.LANCZOS)
    crop_left = (foreground.width - background.width) // 2
    crop_top = (foreground.height - background.height) // 2
    foreground = foreground.crop(
        (crop_left, crop_top, crop_left + background.width, crop_top + background.height)
    )

    icon = Image.alpha_composite(background, foreground)
    icon = icon.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS).convert("RGB")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    icon.save(output_path, format="PNG", optimize=True)
    print(f"Utworzono ikonę {output_path} z APK {apk_path}.")


if __name__ == "__main__":
    main()
