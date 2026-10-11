#!/usr/bin/env python3
"""Download the latest stable Ispina Lokalnie APK and pin its signer."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

RELEASE_API = "https://api.github.com/repos/senikolo/Ispina-Lokalnie-/releases/latest"
METADATA = Path("metadata/com.ispina.mldcheck.yml")


def request(url: str, accept: str) -> bytes:
    headers = {
        "Accept": accept,
        "User-Agent": "Ispina-Lokalnie-FDroid-Repo",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as response:
        return response.read()


def fail(message: str) -> None:
    print(f"BŁĄD: {message}", file=sys.stderr)
    raise SystemExit(1)


release = json.loads(request(RELEASE_API, "application/vnd.github+json"))
if release.get("draft") or release.get("prerelease"):
    fail("Najnowsze wydanie nie jest stabilnym wydaniem publicznym.")

match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", release.get("tag_name", ""))
if not match:
    fail(f"Nieobsługiwany format tagu wydania: {release.get('tag_name')!r}")
version = ".".join(match.groups())
major, minor, patch = (int(part) for part in match.groups())
version_code = major * 10000 + minor * 100 + patch
expected_name = f"Ispina-Lokalnie-Live-{version}.apk"
assets = [item for item in release.get("assets", []) if item.get("name") == expected_name]
if len(assets) != 1:
    fail(f"W wydaniu {version} nie znaleziono dokładnie jednego pliku {expected_name}.")
asset = assets[0]
digest = asset.get("digest", "")
if not digest.startswith("sha256:"):
    fail("GitHub nie podał SHA-256 pliku APK; publikację przerwano.")
expected_sha256 = digest.split(":", 1)[1].lower()
if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
    fail("GitHub zwrócił nieprawidłową sumę SHA-256.")

apk_dir = Path("repo")
apk_dir.mkdir(exist_ok=True)
apk_path = apk_dir / expected_name
apk_bytes = request(asset["browser_download_url"], "application/octet-stream")
actual_sha256 = hashlib.sha256(apk_bytes).hexdigest()
if actual_sha256 != expected_sha256:
    fail("Pobrany APK nie zgadza się z SHA-256 podanym przez GitHub.")
apk_path.write_bytes(apk_bytes)

verify = subprocess.run(
    ["apksigner", "verify", "--print-certs", str(apk_path)],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
if verify.returncode:
    fail("Podpis APK nie przeszedł weryfikacji narzędziem apksigner.")
signer_match = re.search(
    r"certificate SHA-256 digest:\s*([0-9a-fA-F:]+)", verify.stdout
)
if not signer_match:
    fail("Nie udało się odczytać odcisku certyfikatu podpisującego APK.")
signer = signer_match.group(1).replace(":", "").lower()

text = METADATA.read_text(encoding="utf-8")
if not re.search(r"(?m)^CurrentVersion:\s*", text):
    fail("Brak pola CurrentVersion w metadanych aplikacji.")
if not re.search(r"(?m)^CurrentVersionCode:\s*", text):
    fail("Brak pola CurrentVersionCode w metadanych aplikacji.")
text = re.sub(r"(?m)^CurrentVersion:.*$", f"CurrentVersion: {version}", text, count=1)
text = re.sub(
    r"(?m)^CurrentVersionCode:.*$",
    f"CurrentVersionCode: {version_code}",
    text,
    count=1,
)

allowed = re.search(
    r"(?ms)^AllowedAPKSigningKeys:\s*\n((?:[ \t]*-[^\n]*\n)+)", text
)
if allowed:
    known_signers = {
        line.strip().lstrip("-").strip().lower()
        for line in allowed.group(1).splitlines()
        if line.strip()
    }
    if signer not in known_signers:
        fail(
            "APK jest podpisany innym kluczem niż wcześniej zatwierdzony. "
            "Publikację przerwano; trzeba sprawdzić zmianę podpisu ręcznie."
        )
else:
    text = re.sub(
        r"(?m)^(CurrentVersionCode:.*\n)",
        f"\\1AllowedAPKSigningKeys:\n  - {signer}\n",
        text,
        count=1,
    )

METADATA.write_text(text, encoding="utf-8")
print(f"Pobrano {expected_name}; SHA-256 został sprawdzony.")
print(f"Wydanie {version}, kod {version_code}; klucz podpisujący APK został zweryfikowany.")
