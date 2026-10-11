# Własne repozytorium F-Droid — Ispina Lokalnie

To repozytorium przygotowuje własne źródło aplikacji Ispina Lokalnie dla aplikacji F-Droid. Jest prowadzone przez autora aplikacji i **nie należy do głównego katalogu f-droid.org**.

## Aktualny stan

Repozytorium GitHub już istnieje i zawiera instrukcje oraz pliki przygotowawcze. Nie jest jeszcze gotowe do dodania w aplikacji F-Droid: trzeba najpierw wygenerować podpisany indeks i opublikować pliki w katalogu GitHub Pages `docs/`.

Planowany adres repozytorium F-Droid:

`https://senikolo.github.io/Ispina-Lokalnie-FDroid/`

## Przygotowana wersja aplikacji

- Nazwa: Ispina Lokalnie Live 1.83.20
- Identyfikator aplikacji: `com.ispina.mldcheck`
- Minimalny Android: 6.0
- APK pochodzi z [wydania 1.83.20](https://github.com/senikolo/Ispina-Lokalnie-/releases/tag/v1.83.20)
- SHA-256: `c9c0a0107310c3229b421a87832de1f1fc738b07db7ab1dc41eea2ead417e664`

Skrypt pobierania sprawdza sumę SHA-256 przed użyciem pliku. To repozytorium przekazuje APK opublikowany przez autora; nie kompiluje go ze źródeł.

## Przygotowanie repozytorium na Windowsie

Do wygenerowania indeksu potrzebny jest komputer z Windows i środowisko Ubuntu w WSL. Oficjalna instrukcja F-Droid opisuje instalację narzędzi dla WSL: [instalacja fdroidserver](https://f-droid.org/pl/docs/Installing_the_Server_and_Repo_Tools/).

1. Zainstaluj Ubuntu w WSL, jeśli jeszcze go nie masz.
2. Otwórz terminal Ubuntu i zainstaluj narzędzia:
   ```bash
   sudo add-apt-repository ppa:fdroid/fdroidserver
   sudo apt update
   sudo apt install fdroidserver git
   ```
3. Pobierz to repozytorium i przejdź do jego folderu:
   ```bash
   git clone https://github.com/senikolo/Ispina-Lokalnie-FDroid.git
   cd Ispina-Lokalnie-FDroid
   ```
4. Pobierz i sprawdź APK:
   ```bash
   bash scripts/download-current-apk.sh
   ```
5. Utwórz klucz repozytorium (wykonuje się tylko raz):
   ```bash
   fdroid init
   ```
6. W lokalnym pliku `config.yml` ustaw wartości z pliku `repo-public-settings.yml`. Zachowaj `config.yml` i klucz na swoim komputerze. **Nie wysyłaj ich do GitHuba.**
7. Wygeneruj indeks:
   ```bash
   bash scripts/update-repo.sh
   ```
8. Skopiuj wygenerowane pliki do folderu strony:
   ```bash
   cp -a repo/. docs/
   ```
9. W GitHubie otwórz **Settings → Pages**. W sekcji publikowania wybierz **Deploy from a branch**, gałąź `main` i folder `/docs`, a następnie zapisz.
10. Dodaj zmienione pliki z folderu `docs/` do repozytorium i opublikuj je na GitHubie.

Po opublikowaniu indeksu użytkownicy będą mogli dodać w F-Droid adres podany wyżej: **Ustawienia → Repozytoria → Dodaj repozytorium**.

## Klucz repozytorium

`fdroid init` tworzy prywatny klucz, którym podpisywany jest indeks repozytorium. Zachowaj go i zrób bezpieczną kopię zapasową. Jeśli go utracisz, aktualizacje z tego źródła mogą wymagać ponownego dodania repozytorium przez użytkowników.

Plik `config.yml`, klucz i hasła nie mogą trafić do publicznego GitHuba. Plik `.gitignore` zawiera reguły pomagające uniknąć ich przypadkowego dodania.

## Aktualizacja aplikacji

Przy następnym wydaniu trzeba zaktualizować nazwę pliku, adres wydania i sumę SHA-256 w skryptach pobierania, a następnie wygenerować nowy indeks i opublikować jego pliki w `docs/`.
