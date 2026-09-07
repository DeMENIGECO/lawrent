#!/usr/bin/env bash
set -euo pipefail

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3-gi python3-venv python3-pip gir1.2-gtk-4.0 gir1.2-webkit-6.0
else
  printf 'No apt-get found. Install Python 3, venv, pip, GTK4 and PyGObject with your distribution package manager.\n' >&2
  exit 1
fi

python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --editable .
chmod +x run.sh
printf 'Lawrent installed. Run: lawrent\n'
