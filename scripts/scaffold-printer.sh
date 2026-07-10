#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 printer-slug"
  echo "Example: $0 citizen-ct-s310a"
  exit 1
fi

SLUG="$1"

mkdir -p "drivers/workshop/$SLUG"
mkdir -p "drivers/upstream/$SLUG"
mkdir -p "profiles/printers"
mkdir -p "profiles/media"
mkdir -p "docs/printers"
mkdir -p "examples/$SLUG"
mkdir -p "scripts"

touch "drivers/workshop/$SLUG/README.md"
touch "drivers/upstream/$SLUG/README.upstream.md"
touch "profiles/printers/$SLUG.yaml"
touch "profiles/media/$SLUG-default.yaml"
touch "docs/printers/$SLUG.md"
touch "examples/$SLUG/README.md"

cat > "docs/printers/$SLUG.md" <<EOF
# $SLUG

## Overview

## Hardware

## USB / Interface

## Printer Language

## Resolution

## Media

## Known Good Settings

## Installation

## Test Commands

## Calibration

## Notes

## References
EOF

cat > "profiles/printers/$SLUG.yaml" <<EOF
name: $SLUG
queue:
technology:
protocol:
dpi:
usb:
  vendor_id:
  product_id:
  serial:
renderer:
notes:
EOF

cat > "profiles/media/$SLUG-default.yaml" <<EOF
name: $SLUG Default Media
units: inches
nominal_width:
nominal_height:
actual_width:
actual_height:
safe_margin:
orientation:
media_tracking:
notes:
EOF

cat > "drivers/workshop/$SLUG/README.md" <<EOF
# $SLUG Workshop Driver

This directory contains the current supported driver/config artifacts for $SLUG.

Upstream source or reference material belongs under:

drivers/upstream/$SLUG
EOF

cat > "drivers/upstream/$SLUG/README.upstream.md" <<EOF
# Upstream Source for $SLUG

Original project/source:

Imported:

License:

Commit/version:

Notes:
EOF

echo "Created printer scaffold for: $SLUG"