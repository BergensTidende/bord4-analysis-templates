# CLAUDE.md

Dette repoet er kilden til gjenbrukbare analyseoppskrifter for Bord4/BT.
Det er ikke en generell analyseprosjektmal.

Dokumentet er skrevet for kodeagenter som jobber enten i dette repoet eller i
prosjektmaler som bruker dette repoet, særlig `cookiecutter-bord4-analysis` og
`b4-analysis-vibecoding-project`.

## Kortversjon

- `templates/` er flat template-kilde.
- Nye analyseprosjekter bør som standard ha én `notebooks/`-mappe.
- `templates.toml` er maskinlesbar kontrakt mellom template-kilden og
  prosjektmalene.
- Filnavn i `templates/` forteller type: `etl-*`, `eda-*`, `publish-*`.
- `suggested_name` i `templates.toml` forteller anbefalt navn i analyseprosjektet:
  `01-*`, `02-*`, `03-*`.
- Dependencies skal være eksplisitte per template.
- Minimum `pakkenellik` er `pakkenellik>=0.2.1`.

## Roller

### Dette repoet

`bord4-analysis-templates` er et bibliotek av notebook- og scriptmaler. Det skal
være lett å finne, redigere og teste maler her.

Derfor er template-kilden flat:

```text
templates/
├── etl-read-csv.ipynb
├── etl-gsheet.ipynb
├── eda-quick-check.ipynb
├── eda-relationship-check.ipynb
├── publish-datawrapper-table.ipynb
└── etl_ssb_api.py
```

Ikke flytt template-kilden inn i `templates/etl`, `templates/eda` og
`templates/publish` uten en eksplisitt beslutning. Flat struktur er bevisst:
repoet er en katalog over oppskrifter, ikke et eksempelprosjekt.

### Analyseprosjekter

Nye analyseprosjekter bør være enklere for brukerne enn tidligere struktur med
separate `etl/`, `eda/` og `publish/`-mapper.

Anbefalt standard:

```text
notebooks/
├── 01-etl-read-data.ipynb
├── 02-eda-quick-check.ipynb
└── 03-publish-datawrapper.ipynb
data/
├── source/
├── processed/
├── public/
└── untracked/
src/
pyproject.toml
README.md
```

Separate mapper kan fortsatt brukes i store prosjekter, men skal ikke være
default i nye prosjektmaler.

## templates.toml

`templates.toml` er fasiten for prosjektmalene.

Hver template har denne formen:

```toml
[templates."eda-relationship-check.ipynb"]
destination = "notebooks"
suggested_name = "02-eda-relationship-check.ipynb"
dependencies = [
    "pakkenellik[viz]>=0.2.1",
    "python-dotenv",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
]
```

Feltene betyr:

- `templates."<filnavn>"`: filen slik den ligger i `templates/` i dette repoet.
- `destination`: mappe i analyseprosjektet filen bør kopieres til.
- `suggested_name`: anbefalt filnavn etter kopiering.
- `dependencies`: avhengigheter som malen trenger i prosjektet.

For notebooks skal `destination` normalt være `notebooks`.

For Python-hjelpere kan `destination` være `src`, for eksempel:

```toml
[templates."etl_ssb_api.py"]
destination = "src"
suggested_name = "ssb_population.py"
dependencies = ["pakkenellik[ssb]>=0.2.1", "pandas"]
```

Prosjektmalene bør lese `templates.toml` i stedet for å hardkode mapping mellom
template-navn, mappe og dependencies.

## Navnekonvensjon

I dette repoet:

- `etl-*`: henter, bygger eller rydder data.
- `eda-*`: utforsker, sjekker eller sammenligner data.
- `publish-*`: produserer eller oppdaterer publiseringsoutput.

I analyseprosjekter:

- `01-*`: datainnhenting og databygging.
- `02-*`: analyse og utforsking.
- `03-*`: publisering og eksport.

Eksempel:

```text
templates/eda-pairplot.ipynb
```

blir foreslått som:

```text
notebooks/02-eda-pairplot.ipynb
```

## Dependencies

Base dependencies i dette repoet skal holdes relativt lette. Tunge eller
spesialiserte dependencies skal ligge i grupper og i `templates.toml`.

Viktige grupper i `pyproject.toml`:

- `gis`: geodata og kart.
- `nvdb`: NVDB og tilhørende GIS-avhengigheter.
- `gsheet`: Google Sheets.
- `scraping`: Selenium, BeautifulSoup og HTML-parsing.
- `publish`: Datawrapper/MM-publisering.
- `ssb`: SSB-helperne i `pakkenellik`.
- `viz`: plotting, inkludert `matplotlib`, `plotly` og `seaborn`.

Når en template får en ny import, oppdater `templates.toml` samtidig.

## pakkenellik

Bruk `pakkenellik>=0.2.1`.

Viktige API-mønstre:

- Bruk `pakkenellik.regions`, ikke `pakkenellik.dataframe.regions`.
- Bruk `pakkenellik.ssb` for folketall, rater og rangeringer.
- Bruk `pakkenellik.datawrapper.client.Datawrapper` for Datawrapper.
- Bruk `pakkenellik.integration.client` for MM/Datawrapper-integrasjoner.
- Bruk ny Google Sheets-auth:
  1. eksplisitt `credentials_path`
  2. `GOOGLE_APPLICATION_CREDENTIALS`
  3. legacy `GOOGLE_APPLICATION_CREDENTIALS_PATH`
  4. Application Default Credentials

Ikke introduser nye templates som lærer bort gamle imports.

## Notebook-header

Notebookene skal kunne kjøres både fra template-repoet og etter kopiering til et
analyseprosjekt.

Standardmønsteret er:

```python
PROJECT_DIR = Path.cwd().resolve()
if PROJECT_DIR.name in {"templates", "notebooks"}:
    PROJECT_DIR = PROJECT_DIR.parent
```

Ikke legg tilbake `etl`, `eda` eller `publish` i denne listen som default. Den
nye prosjektstrukturen bruker `notebooks/`.

## Ikke gjeninnfør etl-symlink

Det har tidligere eksistert en symlink:

```text
etl -> templates
```

Den gjorde det mulig å simulere gamle analyseprosjekter med `etl/`, `eda/` og
`publish/`, men den gjorde template-repoet forvirrende fordi alle maler også
så ut til å ligge i `etl`.

Ikke gjeninnfør den symlinken uten eksplisitt beslutning.

## Når du legger til en ny template

1. Legg filen i `templates/`.
2. Bruk prefix: `etl-*`, `eda-*` eller `publish-*`.
3. Bruk notebook-headeren med `{"templates", "notebooks"}`.
4. Legg inn entry i `templates.toml`.
5. Sett `destination`, normalt `notebooks` for notebooks.
6. Sett `suggested_name` med `01-`, `02-` eller `03-`.
7. Legg inn alle nødvendige dependencies.
8. Oppdater README-listen hvis malen er relevant for brukere.
9. Kjør:

```bash
uv lock
make format
make lint
```

Søk også etter gamle mønstre:

```bash
rg "pakkenellik.dataframe.regions|from datawrapper import Datawrapper|GOOGLE_APPLICATION_CREDENTIALS_PATH|pyjstat|from etl\\.|etl -> templates"
```

Hvis et treff beholdes, dokumenter hvorfor.

## For prosjektmalene

Prosjektmaler som bruker dette repoet bør:

- Opprette `notebooks/` som standard arbeidsmappe.
- Ikke opprette `etl/`, `eda/` og `publish/` som default.
- Kopiere valgte notebook-maler til `destination/suggested_name`.
- Installere eller skrive dependencies fra `templates.toml`.
- Beholde `src/` for delte Python-hjelpere.
- Bruke `data/source`, `data/processed`, `data/public` og `data/untracked`.

Prosjektmalene kan fortsatt la avanserte brukere lage egne undermapper senere,
men standardopplevelsen skal være enkel.
