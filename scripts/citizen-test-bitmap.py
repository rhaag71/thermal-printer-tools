#!/usr/bin/env python3

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


DEVICE = sys.argv[1] if len(sys.argv) > 1 else "/dev/usb/lp0"
WIDTH_DOTS = 384  # likely 58mm-class printable width; we'll verify


def escpos_raster(img: Image.Image) -> bytes:
    img = img.convert("1")
    width, height = img.size
    width_bytes = (width + 7) // 8

    data = bytearray()
    data += b"\x1b\x40"  # ESC @ initialize

    # GS v 0 raster bit image
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


def make_test_image() -> Image.Image:
    w = WIDTH_DOTS
    h = 220
    img = Image.new("1", (w, h), 1)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, w - 1, h - 1], outline=0)
    d.rectangle([16, 16, 16 + 64, 16 + 64], outline=0)
    d.line([0, 110, w - 1, 110], fill=0)
    d.line([w // 2, 0, w // 2, h - 1], fill=0)

    for i, thickness in enumerate([1, 2, 3, 4, 6, 8]):
        y = 135 + i * 12
        d.line([16, y, 200, y], fill=0, width=thickness)

    d.text((100, 20), "Citizen CT-S310A", fill=0)
    d.text((100, 42), "ESC/POS bitmap test", fill=0)
    d.text((100, 64), "384 dot width", fill=0)

    return img


def main() -> None:
    img = make_test_image()
    payload = escpos_raster(img)

    with open(DEVICE, "wb") as f:
        f.write(payload)

    print(f"Sent bitmap test to {DEVICE}")


if __name__ == "__main__":
    main()