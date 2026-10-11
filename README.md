# Ispina Lokalnie — repozytorium dla F-Droid

To niezależne repozytorium udostępnia aplikację Ispina Lokalnie w kliencie F-Droid. Prowadzi je autor aplikacji; nie jest częścią głównego katalogu [f-droid.org](https://f-droid.org/).

## Adres repozytorium

`https://senikolo.github.io/Ispina-Lokalnie-FDroid/repo`

Po pierwszej publikacji dodaj ten adres w F-Droid przez **Ustawienia → Repozytoria → Dodaj repozytorium**.

## Aplikacja

- Nazwa: Ispina Lokalnie Live
- Identyfikator: `com.ispina.mldcheck`
- Minimalny Android: 6.0
- APK pochodzi z [wydań autora](https://github.com/senikolo/Ispina-Lokalnie-/releases); to repozytorium nie kompiluje aplikacji ze źródeł.

## Klucz podpisujący

Workflow używa jednego zaszyfrowanego sekretu GitHub Actions: `FDROID_REPO_KEYSTORE_B64`. Wartość sekretu to zakodowane Base64 32 losowych bajtów. Dzięki niej workflow odtwarza ten sam klucz podpisujący przy każdej publikacji; prywatny plik klucza i hasło powstają tylko na czas działania workflow.

Nie zmieniaj ani nie usuwaj tego sekretu. Zmiana oznaczałaby nowy klucz repozytorium, którego dotychczasowi użytkownicy F-Droid nie zaakceptują automatycznie. Publiczny certyfikat repozytorium jest publikowany jako `repo-signing-cert.pem`; można go udostępniać.

Sekret znajdziesz w **Settings → Secrets and variables → Actions**. Wartość może wykorzystać każda osoba z dostępem do uruchamiania workflow w tym repozytorium, więc ogranicz dostęp do zaufanych współpracowników. Nie wklejaj sekretu do publicznych plików, zgłoszeń ani wiadomości.

## Publikacja nowego wydania — również z telefonu

Po opublikowaniu nowego stabilnego wydania w [repozytorium aplikacji](https://github.com/senikolo/Ispina-Lokalnie-/releases):

1. Otwórz kartę **Actions** w tym repozytorium.
2. Wybierz workflow **Publikuj repozytorium F-Droid**.
3. Naciśnij **Run workflow**, pozostaw gałąź `main` i uruchom workflow.
4. Poczekaj, aż wykonanie zakończy się zielonym znacznikiem.

Nie trzeba instalować narzędzi ani używać komputera. Workflow pobiera najnowszy stabilny APK, sprawdza jego sumę SHA-256 i podpis, generuje indeks F-Droid, a następnie publikuje pliki w GitHub Pages.
