#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APK_NAME="Ispina-Lokalnie-Live-1.83.20.apk"
APK_URL="https://github.com/senikolo/Ispina-Lokalnie-/releases/download/v1.83.20/${APK_NAME}"
EXPECTED_SHA256="c9c0a0107310c3229b421a87832de1f1fc738b07db7ab1dc41eea2ead417e664"
DEST="${ROOT}/repo/${APK_NAME}"

mkdir -p "${ROOT}/repo"
curl --fail --location --retry 2 --output "${DEST}.tmp" "${APK_URL}"
printf '%s  %s\n' "${EXPECTED_SHA256}" "${DEST}.tmp" | sha256sum --check --status || {
  rm -f "${DEST}.tmp"
  echo "Błąd: suma SHA-256 APK nie zgadza się z wydaniem 1.83.20." >&2
  exit 1
}
mv "${DEST}.tmp" "${DEST}"
echo "Pobrano i sprawdzono APK: ${DEST}"
