![Header](./docs/assets/github-header-banner-bord4-analysis-templates.png)

Dette repoet samler notebook- og Python-maler som brukes av
`cookiecutter-bord4-analysis` og den nye `b4-analysis-vibecoding-project`-malen.
Bruk `b4-analysis-vibecoding-project` som anbefalt prosjektmal for nye
analyseprosjekter. Dette repoet er fortsatt kilden til gjenbrukbare
analyseoppskrifter, ikke en generell prosjektmal.

## Krav

- Python 3.10 eller nyere
- `uv` for avhengigheter, virtuelle miljø og kjøring av verktøy
- `pakkenellik>=0.2.1` er minimum for malene

Installer på macOS med Homebrew:

```bash
brew install uv
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

Start Jupyter Lab:

```bash
make lab
```

Lag en ny notebook-mal fra felles header:

```bash
make new
```

Installer lokal pre-commit-hook som fjerner output fra staged notebooks:

```bash
make install-hooks
```

## Make-kommandoer

- `make sync`: installer avhengigheter med `uv`
- `make lab`: start Jupyter Lab med `uv run`
- `make new`: kopier `templates/generic-header.ipynb` til en ny mal
- `make install-hooks`: installer lokal git-hook som renser notebook-output før commit
- `make format`: formater Python-filer og notebooks med Ruff
- `make lint`: kjør Ruff og mypy

## Struktur

```text
.
├── data
│   ├── processed
│   ├── public
│   └── source
├── docs
├── git
├── src
├── templates
├── templates.toml
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

- `templates`: notebook- og scriptmaler som kan kopieres inn i prosjekter.
- `templates.toml`: maskinlesbar oversikt over maler, destination, suggested_name og dependencies per mal.
- `data/source`: rådata som ikke skal endres.
- `data/processed`: transformerte filer fra ETL eller analyse.
- `data/public`: filer som publiseres eller brukes direkte ut mot lesere.
- `docs`: dokumentasjonsfiler og grafiske ressurser for repoet.
- `src`: lokale Python-hjelpere som kan importeres fra notebooks.
- `git`: git-hooks, blant annet hook for å fjerne notebook-output før commit.

I nye analyseprosjekter er anbefalt standard én `notebooks/`-mappe:

```text
notebooks/
├── 01-etl-read-data.ipynb
├── 02-eda-quick-check.ipynb
└── 03-publish-datawrapper.ipynb
```

Template-kilden er flat i `templates/`, med fagprefix i filnavnet.
`templates.toml` forteller hvilken mappe filen skal kopieres til og hvilket
navn den bør få i et analyseprosjekt.

## Maler

ETL-maler:

- `etl-read-csv.ipynb`: les CSV fra URL eller fil og lagre behandlet CSV.
- `etl-read-excel.ipynb`: les Excel-ark, rydd kolonnenavn og lagre CSV.
- `etl-api-json.ipynb`: hent JSON fra API, normaliser og håndter enkel pagination.
- `etl-clean-join.ipynb`: slå sammen to datasett og sjekk join-dekning.
- `etl-manual-data.ipynb`: bygg et lite manuelt datasett direkte i notebook.
- `etl-gsheet.ipynb`: les fra og skriv til Google Sheets.
- `etl-screen-scraping.ipynb`: hent tabeller fra nettsider med Selenium og BeautifulSoup.
- `etl-gis.ipynb`: hent geodata fra WFS og konverter til GeoJSON.
- `etl-nvdb.ipynb`: hent data fra NVDB.
- `etl-einnsyn.ipynb`: hent journalposter fra Einnsyn.
- `etl_ssb_api.py`: hent befolkningstall fra SSB i et gjenbrukbart Python-script.

EDA-maler:

- `eda-quick-check.ipynb`: rask førstesjekk av struktur, mangler, duplikater og fordelinger.
- `eda-relationship-check.ipynb`: sjekk om to datasett henger sammen etter join.
- `eda-pairplot.ipynb`: rask pairplot og korrelasjonsmatrise for numeriske kolonner.
- `eda-compare-groups.ipynb`: sammenlign grupper med tabell, boxplot og stripplot.
- `eda-distribution.ipynb`: sjekk fordeling, percentiler og outliers i én variabel.
- `eda-ranking.ipynb`: lag rangeringer og visualiser topp/bunn.
- `eda-before-after.ipynb`: sammenlign samme enheter før og etter en hendelse.
- `eda-time-series.ipynb`: rask tidsseriesjekk med rolling average og siste verdier.
- `eda-ssb.ipynb`: analyser data hentet fra SSB API.
- `eda-nvdb.ipynb`: kartlegg behandlet NVDB-data.
- `eda-linechart-array.ipynb`: lag små multiple linecharts.

Publiseringsmaler:

- `publish-datawrapper-table.ipynb`: publiser en enkel Datawrapper-tabell.
- `publish-datawrapper-mm.ipynb`: lag og publiser Datawrapper-graf med integrasjon.
- `publish-datawrapper-update.ipynb`: oppdater eksisterende Datawrapper-chart.

Fellesmal:

- `generic-header.ipynb`: felles notebook-header med prosjektoppsett, miljøvariabler og logging.

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
