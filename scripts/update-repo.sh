#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if ! command -v fdroid >/dev/null 2>&1; then
  echo "Nie znaleziono fdroidserver. Zainstaluj narzędzia według oficjalnej instrukcji F-Droid." >&2
  exit 1
fi

if [[ ! -f config.yml ]]; then
  echo "Najpierw uruchom 'fdroid init' i zachowaj utworzony klucz." >&2
  exit 1
fi

if [[ ! -f repo/Ispina-Lokalnie-Live-1.83.20.apk ]]; then
  bash scripts/download-current-apk.sh
fi

fdroid update --create-metadata
echo "Indeks repozytorium przygotowano w katalogu repo/."
