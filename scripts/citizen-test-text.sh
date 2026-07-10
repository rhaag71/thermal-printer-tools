#!/usr/bin/env bash
set -euo pipefail

DEVICE="${1:-/dev/usb/lp0}"

{
  printf '\x1b\x40'
  printf 'Citizen CT-S310A\n'
  printf 'ESC/POS text test\n'
  printf '----------------\n'
  printf 'ABCDEFGHIJKLMNOPQRSTUVWXYZ\n'
  printf '0123456789\n'
  printf '\n\n\n'
} | sudo tee "$DEVICE" > /dev/null