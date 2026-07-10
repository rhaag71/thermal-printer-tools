#!/usr/bin/env python3

import argparse
from pathlib import Path
from PIL import Image, ImageOps

PRINTABLE_WIDTH_DOTS = 384
DEFAULT_DEVICE = "/dev/usb/lp0"


def image_to_escpos_raster(img: Image.Image) -> bytes:
    img = img.convert("1")
    width, height = img.size
    width_bytes = (width + 7) // 8

    data = bytearray()
    data += b"\x1b\x40"  # ESC @ initialize

    # GS v 0 raster image
    data += b"\x1d\x76\x30\x00"
    data += bytes([width_bytes & 0xFF, (width_bytes >> 8) & 0xFF])
    data += bytes([height & 0xFF, (height >> 8) & 0xFF])

    pixels = img.load()
    for y in range(height):
        for xb in range(width_bytes):
            byte = 0
            for bit in range(8):
                x = xb * 8 + bit
                if x < width and pixels[x, y] == 0:
                    byte |= 0x80 >> bit
            data.append(byte)

    data += b"\n\n\n"
    return bytes(data)


def prepare_image(path: Path, actual_size: bool, invert: bool) -> Image.Image:
    img = Image.open(path).convert("L")

    if invert:
        img = ImageOps.invert(img)

    if not actual_size and img.width > PRINTABLE_WIDTH_DOTS:
        ratio = PRINTABLE_WIDTH_DOTS / img.width
        new_height = max(1, int(img.height * ratio))
        img = img.resize((PRINTABLE_WIDTH_DOTS, new_height), Image.Resampling.LANCZOS)

    # Center image on receipt width
    canvas = Image.new("L", (PRINTABLE_WIDTH_DOTS, img.height), 255)
    x = max(0, (PRINTABLE_WIDTH_DOTS - img.width) // 2)
    canvas.paste(img, (x, 0))

    # Simple threshold for now
    return canvas.point(lambda p: 0 if p < 128 else 255, "1")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print PNG/JPEG images to Citizen CT-S310A using ESC/POS raster mode.")
    parser.add_argument("image", help="Image file to print")
    parser.add_argument("--device", default=DEFAULT_DEVICE, help="Raw printer device, default /dev/usb/lp0")
    parser.add_argument("--actual-size", action="store_true", help="Do not best-fit image wider than printable width")
    parser.add_argument("--invert", action="store_true", help="Invert black/white before printing")
    parser.add_argument("--preview", default=None, help="Write processed 1-bit preview image instead of printing")

    args = parser.parse_args()

    img = prepare_image(Path(args.image), args.actual_size, args.invert)

    if args.preview:
        img.save(args.preview)
        print(f"Wrote preview: {args.preview}")
        return

    payload = image_to_escpos_raster(img)

    with open(args.device, "wb") as f:
        f.write(payload)

    print(f"Printed {args.image} to {args.device}")


if __name__ == "__main__":
    main()