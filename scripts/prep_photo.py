from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main():
    if len(sys.argv) != 2:
        print("Usage: python prep_photo.py source-photo.jpeg")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    print("Loading photo...")
    image = Image.open(input_path).convert("RGBA")

    print("Removing background...")
    foreground = remove(image)

    rgba = np.array(foreground)

    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb = rgba[:, :, :3].astype(np.float32)

    white = np.ones_like(rgb) * 255

    composite = rgb * alpha + white * (1 - alpha)
    composite = composite.astype(np.uint8)

    print("Converting to grayscale...")
    gray = cv2.cvtColor(
        composite,
        cv2.COLOR_RGB2GRAY
    )

    print("Improving contrast...")

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    gray = cv2.normalize(
        gray,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    output_path = Path("source-prepped.png")

    cv2.imwrite(
        str(output_path),
        gray
    )

    print()
    print("SUCCESS!")
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
