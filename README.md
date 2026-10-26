![Header](./docs/assets/github-header-banner-bord4-analysis-templates.png)

Dette repoet samler cellebaserte Python-maler som brukes av
`cookiecutter-bord4-analysis` og den nye `b4-analysis-vibecoding-project`-malen.
Bruk `b4-analysis-vibecoding-project` som anbefalt prosjektmal for nye
analyseprosjekter. Dette repoet er fortsatt kilden til gjenbrukbare
analyseoppskrifter, ikke en generell prosjektmal.

## Krav

- Python 3.11 eller nyere. Bruk en sikkerhetsoppdatert patchversjon (minst
  3.11.18, 3.12.16, 3.13.18, 3.14.10 eller 3.15.2).
- `uv>=0.13.5` for avhengigheter, virtuelle miljø og kjøring av verktøy
- `pakkenellik>=0.2.1` er minimum for malene

Installer på macOS med Homebrew:

```bash
brew install uv
brew upgrade uv
```

## Kom i gang

Installer avhengigheter:

```bash
uv sync
```

Base-avhengighetene er holdt relativt lette. Tunge eller spesialiserte
avhengigheter installeres etter behov, styrt av malen du bruker:

```bash
uv sync --group gis
uv sync --group nvdb
uv sync --group gsheet
uv sync --group scraping
uv sync --group publish
uv sync --group ssb
uv sync --group viz
```

Åpne en mal i en editor som støtter `# %%`-celler, for eksempel VS Code med
Jupyter-utvidelsen. Velg prosjektets `.venv` som kernel og kjør én celle om
gangen. Kode og markdown ligger i vanlige `.py`-filer; celleoutput lagres ikke i
repoet.

Lag en ny cellebasert Python-mal fra felles header:

```bash
make new
```

## Make-kommandoer

- `make sync`: installer avhengigheter med `uv`
- `make new`: kopier `templates/generic-header.py` til en ny mal
- `make format`: formater Python-filene med Ruff
- `make lint`: kjør Ruff og mypy

## Struktur

```text
.
├── data
│   ├── processed
│   ├── public
│   └── source
├── docs
├── src
├── templates
├── templates.toml
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

- `templates`: cellebaserte Python-maler som kan kopieres inn i prosjekter.
- `templates.toml`: maskinlesbar oversikt over maler, destination, suggested_name og dependencies per mal.
- `data/source`: rådata som ikke skal endres.
- `data/processed`: transformerte filer fra ETL eller analyse.
- `data/public`: filer som publiseres eller brukes direkte ut mot lesere.
- `docs`: dokumentasjonsfiler og grafiske ressurser for repoet.
- `src`: lokale Python-hjelpere som kan importeres fra analysemalene.

I nye analyseprosjekter er anbefalt standard én `notebooks/`-mappe:

```text
notebooks/
├── 01-etl-read-data.py
├── 02-eda-quick-check.py
└── 03-publish-datawrapper.py
```

Template-kilden er flat i `templates/`, med fagprefix i filnavnet.
`templates.toml` forteller hvilken mappe filen skal kopieres til og hvilket
navn den bør få i et analyseprosjekt.

## Maler

ETL-maler:

- `etl-read-csv.py`: les CSV fra URL eller fil og lagre behandlet CSV.
- `etl-read-excel.py`: les Excel-ark, rydd kolonnenavn og lagre CSV.
- `etl-api-json.py`: hent JSON fra API, normaliser og håndter enkel pagination.
- `etl-clean-join.py`: slå sammen to datasett og sjekk join-dekning.
- `etl-manual-data.py`: bygg et lite manuelt datasett direkte i en cellebasert Python-fil.
- `etl-gsheet.py`: les fra og skriv til Google Sheets.
- `etl-screen-scraping.py`: hent tabeller fra nettsider med Selenium og BeautifulSoup.
- `etl-gis.py`: hent geodata fra WFS og konverter til GeoJSON.
- `etl-nvdb.py`: hent data fra NVDB.
- `etl-einnsyn.py`: hent journalposter fra Einnsyn.
- `etl_ssb_api.py`: hent befolkningstall fra SSB i et gjenbrukbart Python-script.

EDA-maler:

- `eda-quick-check.py`: rask førstesjekk av struktur, mangler, duplikater og fordelinger.
- `eda-relationship-check.py`: sjekk om to datasett henger sammen etter join.
- `eda-pairplot.py`: rask pairplot og korrelasjonsmatrise for numeriske kolonner.
- `eda-compare-groups.py`: sammenlign grupper med tabell, boxplot og stripplot.
- `eda-distribution.py`: sjekk fordeling, percentiler og outliers i én variabel.
- `eda-ranking.py`: lag rangeringer og visualiser topp/bunn.
- `eda-before-after.py`: sammenlign samme enheter før og etter en hendelse.
- `eda-time-series.py`: rask tidsseriesjekk med rolling average og siste verdier.
- `eda-ssb.py`: analyser data hentet fra SSB API.
- `eda-nvdb.py`: kartlegg behandlet NVDB-data.
- `eda-linechart-array.py`: lag små multiple linecharts.

Publiseringsmaler:

- `publish-datawrapper-table.py`: publiser en enkel Datawrapper-tabell.
- `publish-datawrapper-mm.py`: lag og publiser Datawrapper-graf med integrasjon.
- `publish-datawrapper-update.py`: oppdater eksisterende Datawrapper-chart.

Fellesmal:

- `generic-header.py`: felles header med prosjektoppsett, miljøvariabler og logging.

`templates.toml` er fasiten for hvor en mal skal kopieres i et prosjekt, hva den
bør hete der og hvilke dependencies den trenger. Oppdater den når en mal får nye
imports eller slutter å trenge en avhengighet.

## Bidra

Opprett en branch, gjør endringen, kjør formattering og lint, og åpne PR:

```bash
git checkout -b name-of-branch
make format
make lint
```

Skriv commit-meldinger i presens og beskriv hva commit-en gjør når den blir
brukt.

## Kontakt

Bord4 - bord4@bt.no
