#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_PRINTER_PROFILE = PROJECT_ROOT / "profiles/printers/rollo-x1038.yaml"
DEFAULT_MEDIA_PROFILE = PROJECT_ROOT / "profiles/media/rollo-2x1-inventory.yaml"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def inches(value) -> float:
    """
    Accepts:
      1.90625
      "1.90625"
      "1.90625in"
    """
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().lower().replace("in", "")
    return float(text)


def make_pdf(path: Path, media: dict, title: str, subtitle: str, note: str) -> None:
    width_in = inches(media["actual_width"])
    height_in = inches(media["actual_height"])

    margin_in = inches(media.get("safe_margin", 0.06))

    w = width_in * inch
    h = height_in * inch
    m = margin_in * inch

    c = canvas.Canvas(str(path), pagesize=(w, h))

    # Debug/safe border
    c.rect(m, m, w - 2 * m, h - 2 * m)

    # Main label content
    c.setFont("Helvetica-Bold", 13)
    c.drawString(m + 0.04 * inch, h - m - 0.16 * inch, title[:22])

    c.setFont("Helvetica", 9)
    c.drawString(m + 0.04 * inch, h - m - 0.34 * inch, subtitle[:32])

    c.setFont("Helvetica", 8)
    c.drawString(m + 0.04 * inch, h - m - 0.52 * inch, note[:38])

    c.setFont("Helvetica", 5)
    c.drawRightString(w - m - 0.02 * inch, m + 0.02 * inch, "Workshop Label")

    c.save()


def print_pdf(path: Path, printer_profile: dict, media: dict) -> None:
    queue = printer_profile.get("cups_queue", "Rollo_Test")
    quality = printer_profile.get("quality", "Draft")

    width_in = inches(media["actual_width"])
    height_in = inches(media["actual_height"])

    x_offset = str(printer_profile.get("horizontal_offset", 2))
    y_offset = str(printer_profile.get("vertical_offset", 0))

    cmd = [
        "lp",
        "-d", queue,
        "-o", f"media=Custom.{width_in}x{height_in}in",
        "-o", "print-scaling=none",
        "-o", "fit-to-page=false",
        "-o", f"cupsPrintQuality={quality}",
        "-o", f"roAdjustHorizontal={x_offset}",
        "-o", f"roAdjustVertical={y_offset}",
        str(path),
    ]

    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a simple workshop thermal label.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--printer-profile", default=str(DEFAULT_PRINTER_PROFILE))
    parser.add_argument("--media-profile", default=str(DEFAULT_MEDIA_PROFILE))
    parser.add_argument("--output", default="label-2x1.pdf")
    parser.add_argument("--no-print", action="store_true")

    args = parser.parse_args()

    printer_profile = load_yaml(Path(args.printer_profile))
    media_profile = load_yaml(Path(args.media_profile))

    output = Path(args.output).resolve()

    make_pdf(output, media_profile, args.title, args.subtitle, args.note)
    print(f"Created {output}")

    if not args.no_print:
        print_pdf(output, printer_profile, media_profile)
        print(f"Sent to {printer_profile.get('cups_queue', 'Rollo_Test')}")


if __name__ == "__main__":
    main()