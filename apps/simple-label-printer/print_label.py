#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

LABEL_W_IN = 1 + 29 / 32      # 1.90625"
LABEL_H_IN = 31 / 32          # 0.96875"

DEFAULT_PRINTER = "Rollo_Test"
DEFAULT_X_OFFSET = "2"
DEFAULT_Y_OFFSET = "0"


def make_pdf(path: Path, title: str, subtitle: str, note: str) -> None:
    w = LABEL_W_IN * inch
    h = LABEL_H_IN * inch

    c = canvas.Canvas(str(path), pagesize=(w, h))

    # Safe border / debug frame
    c.rect(0.06 * inch, 0.06 * inch, w - 0.12 * inch, h - 0.12 * inch)

    # Main text
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.10 * inch, h - 0.24 * inch, title[:22])

    c.setFont("Helvetica", 9)
    c.drawString(0.10 * inch, h - 0.42 * inch, subtitle[:32])

    c.setFont("Helvetica", 8)
    c.drawString(0.10 * inch, h - 0.60 * inch, note[:38])

    # Footer
    c.setFont("Helvetica", 5)
    c.drawRightString(w - 0.10 * inch, 0.10 * inch, "Workshop Label")

    c.save()


def print_pdf(path: Path, printer: str, x_offset: str, y_offset: str) -> None:
    cmd = [
        "lp",
        "-d", printer,
        "-o", f"media=Custom.{LABEL_W_IN}x{LABEL_H_IN}in",
        "-o", "print-scaling=none",
        "-o", "fit-to-page=false",
        "-o", "cupsPrintQuality=Draft",
        "-o", f"roAdjustHorizontal={x_offset}",
        "-o", f"roAdjustVertical={y_offset}",
        str(path),
    ]

    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a simple 2x1 Rollo workshop label.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--printer", default=DEFAULT_PRINTER)
    parser.add_argument("--x-offset", default=DEFAULT_X_OFFSET)
    parser.add_argument("--y-offset", default=DEFAULT_Y_OFFSET)
    parser.add_argument("--output", default="label-2x1.pdf")
    parser.add_argument("--no-print", action="store_true")

    args = parser.parse_args()

    output = Path(args.output).resolve()
    make_pdf(output, args.title, args.subtitle, args.note)

    print(f"Created {output}")

    if not args.no_print:
        print_pdf(output, args.printer, args.x_offset, args.y_offset)
        print(f"Sent to {args.printer}")


if __name__ == "__main__":
    main()