#!/usr/bin/env bash
# Exporta notas/parcial-2026-resolucion.md a PDF usando pandoc + xelatex.
# Instala dependencias automáticamente si faltan.
#
# Uso:
#   ./notas/build-pdf.sh
#   ./notas/build-pdf.sh notas/otro-archivo.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

INPUT="${1:-$ROOT_DIR/notas/parcial-2026-resolucion.md}"
OUTPUT="${INPUT%.md}.pdf"

# Asegurar que /Library/TeX/texbin está en PATH (BasicTeX se instala ahí)
export PATH="/Library/TeX/texbin:$PATH"

# 1) Homebrew
if ! command -v brew >/dev/null 2>&1; then
    echo ">> Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if [ -x /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [ -x /usr/local/bin/brew ]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
fi

# 2) pandoc
if ! command -v pandoc >/dev/null 2>&1; then
    echo ">> Instalando pandoc..."
    brew install pandoc
fi

# 3) BasicTeX (provee xelatex)
if ! command -v xelatex >/dev/null 2>&1; then
    echo ">> Instalando BasicTeX (requiere sudo)..."
    brew install --cask basictex
    export PATH="/Library/TeX/texbin:$PATH"
fi

# 4) Preprocesar: si la imagen referenciada en 1.4 no existe, comentar la línea
TMP_INPUT="$(mktemp -t parcial.XXXXXX.md)"
trap 'rm -f "$TMP_INPUT"' EXIT

# Comenta cualquier ![alt](path) cuyo path no exista relativo al .md
python3 - "$INPUT" "$TMP_INPUT" <<'PY'
import os
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(src))
pat = re.compile(r'^(!\[[^\]]*\]\(([^)]+)\))\s*$')

with open(src, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for line in lines:
    m = pat.match(line.rstrip('\n'))
    if m:
        path = m.group(2)
        full = path if os.path.isabs(path) else os.path.join(base, path)
        if not os.path.exists(full):
            out.append(f'<!-- imagen no encontrada: {path} -->\n')
            continue
    out.append(line)

with open(dst, 'w', encoding='utf-8') as f:
    f.writelines(out)
PY

# 5) Generar PDF (usa fuentes del sistema macOS)
echo ">> Generando $OUTPUT ..."

pandoc "$TMP_INPUT" \
    -o "$OUTPUT" \
    --pdf-engine=xelatex \
    -V mainfont="Helvetica" \
    -V monofont="Menlo" \
    -V geometry:margin=2cm \
    -V colorlinks=true \
    -V linkcolor=blue \
    --toc \
    --toc-depth=3 \
    --resource-path="$ROOT_DIR:$ROOT_DIR/notas"

echo "OK: $OUTPUT"
