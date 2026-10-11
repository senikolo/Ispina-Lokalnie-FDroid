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

## Jednorazowa konfiguracja

Workflow podpisuje indeks osobnym, stałym kluczem. Jego plik i hasła są przechowywane w **Settings → Secrets and variables → Actions** jako sekrety repozytorium o nazwach:

- `FDROID_REPO_KEYSTORE_B64`
- `FDROID_REPO_KEYSTORE_PASSWORD`
- `FDROID_REPO_KEY_PASSWORD`

Nie umieszczaj pliku klucza, haseł ani wartości sekretów w publicznych plikach repozytorium, zgłoszeniach ani wiadomościach. Klucz musi pozostać taki sam przy każdej aktualizacji. Zachowaj bezpieczną kopię zapasową klucza i haseł; ich utrata może sprawić, że użytkownicy będą musieli usunąć i dodać repozytorium ponownie.

## Publikacja nowego wydania — również z telefonu

Po opublikowaniu nowego stabilnego wydania w [repozytorium aplikacji](https://github.com/senikolo/Ispina-Lokalnie-/releases):

1. Otwórz kartę **Actions** w tym repozytorium.
2. Wybierz workflow **Publikuj repozytorium F-Droid**.
3. Naciśnij **Run workflow**, pozostaw gałąź `main` i uruchom workflow.
4. Poczekaj, aż wykonanie zakończy się zielonym znacznikiem.

Nie trzeba instalować narzędzi ani używać komputera. Workflow pobiera najnowszy stabilny APK, sprawdza jego sumę SHA-256 i podpis, generuje indeks F-Droid, a następnie publikuje pliki w GitHub Pages. Dostęp do edycji głównej gałęzi i workflow powinny mieć wyłącznie zaufane osoby.
