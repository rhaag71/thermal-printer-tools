#!/usr/bin/env bash
set -euo pipefail

QUEUE_NAME="${1:-Rollo_X1038}"
DEVICE_URI="${2:-}"

PPD_SOURCE="drivers/workshop/rollo/rollo-x1038.ppd"
FILTER_SOURCE="drivers/workshop/rollo/rastertorollo"

CUPS_FILTER_DIR="/usr/lib/cups/filter"
CUPS_MODEL_DIR="/usr/share/cups/model"

if [[ ! -f "$PPD_SOURCE" ]]; then
  echo "Missing $PPD_SOURCE"
  exit 1
fi

if [[ ! -f "$FILTER_SOURCE" ]]; then
  echo "Missing $FILTER_SOURCE"
  exit 1
fi

if [[ -z "$DEVICE_URI" ]]; then
  DEVICE_URI="$(lpinfo -v | grep -i 'usb://Printer/ThermalPrinter' | head -n1 | awk '{print $2}')"
fi

if [[ -z "$DEVICE_URI" ]]; then
  echo "Could not auto-detect Rollo USB printer."
  echo "Run: lpinfo -v"
  echo "Then pass the device URI manually:"
  echo "  sudo $0 Rollo_X1038 'usb://Printer/ThermalPrinter?serial=...'"
  exit 1
fi

echo "Installing Rollo CUPS filter..."
sudo install -m 755 "$FILTER_SOURCE" "$CUPS_FILTER_DIR/rastertorollo"

echo "Installing Rollo PPD..."
sudo install -m 644 "$PPD_SOURCE" "$CUPS_MODEL_DIR/rollo-x1038.ppd"

echo "Restarting CUPS..."
sudo systemctl restart cups

echo "Removing existing queue if present..."
sudo lpadmin -x "$QUEUE_NAME" 2>/dev/null || true

echo "Creating queue: $QUEUE_NAME"
sudo lpadmin \
  -p "$QUEUE_NAME" \
  -E \
  -v "$DEVICE_URI" \
  -P "$CUPS_MODEL_DIR/rollo-x1038.ppd"

echo "Applying known-good defaults..."
sudo lpadmin -p "$QUEUE_NAME" \
  -o cupsPrintQuality-default=Draft \
  -o roAdjustHorizontal-default=2 \
  -o roAdjustVertical-default=0 \
  -o roMediaTracking-default=Gap

echo "Done."
echo
lpstat -p "$QUEUE_NAME"
lpoptions -p "$QUEUE_NAME" -l | grep -E 'cupsPrintQuality|roAdjust|roMediaTracking|roDarkness|roPrintRate'