#!/usr/bin/env python3
"""把竖版线稿统一为标注、预览和渲染使用的 1080×1920 PNG。"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="生成的竖版线稿")
    parser.add_argument("output", type=Path, help="标注用的 PNG 路径")
    args = parser.parse_args()

    with Image.open(args.image) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    if image.width >= image.height:
        parser.error("源图需要按 9:16 竖屏构图，请重新生成竖版线稿")

    paper_color = image.getpixel((0, 0))
    canvas = ImageOps.pad(image, (1080, 1920), Image.Resampling.LANCZOS, color=paper_color)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output, format="PNG")


if __name__ == "__main__":
    main()
