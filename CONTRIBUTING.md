# Contributing — Timmerhus

## Innehåll
- [Arbetsflöde](#arbetsflöde)
- [Namnkonvention](#namnkonvention)
- [Tester](#tester)
- [Generera PDF](#generera-pdf)
- [Taggning och releases](#taggning-och-releases)
- [Direktiv för Claude](#direktiv-för-claude)

---

## Arbetsflöde

1. Skapa feature-branch från `main`
2. Gör ändringar, kör tester lokalt
3. Pusha och skapa PR mot `main`
4. GitHub Actions kör tester automatiskt
5. Merga när tester är gröna
6. Ta bort feature-branch efter merge
7. Sätt tag på `main` när versionen är godkänd

---

## Namnkonvention

### Filer (zip/leverans)
```
Timmerhus-[Beskrivning]-YYYYMMDD-HHMM-v[VERSION].[ext]
```

### Docs i git
Enkla namn utan datum:
```
docs/Timmerhus-Konstruktionsdokument.pdf
docs/Timmerhus-Projektbeskrivning.md
```

### Branches
```
feature/[kort-beskrivning]
fix/[vad-som-fixas]
```

### Commits
```
feat:  ny funktion eller layout
fix:   buggfix eller korrigering
chore: städning, namnbyten
ci:    CI/CD-ändringar
test:  teständringar
docs:  dokumentationsändringar
```

### Zip-filer (ändringar)
```
timmerhus-changes-YYYYMMDD-HHMM-[beskrivning].zip
```
Innehåller **endast ändrade filer** — inte hela repot.

---

## Tester

### Kör lokalt
```bash
python tests/test_consistency.py
```

### Vad testas
| Testklass | Innehåll |
|---|---|
| `TestMåttkedjor` | Längd- och breddkedjor summerar korrekt |
| `TestRumsAreaer` | Alla rumsareor stämmer |
| `TestTillgänglighet` | Gångbredd, vändcirklar, garderober, entréficka |
| `TestTrappMått` | Uppsteg, klätthöjd, trappglugg |
| `TestLoft` | Brutto, fri yta, netto efter trappglugg |

### Lägg till test vid varje måttändring
Varje ändring av mått i `scripts/generate_timmerhus_pdf.py` ska
åtföljas av uppdaterat eller nytt test i `tests/test_consistency.py`.

---

## Generera PDF

```bash
pip install reportlab
python scripts/generate_timmerhus_pdf.py
```

PDF sparas till `docs/Timmerhus-Konstruktionsdokument.pdf`.

---

## Taggning och releases

```bash
git checkout main
git pull origin main
git tag v[VERSION]
git push origin v[VERSION]
```

- En tag per godkänd version: `v1.0`, `v2.0`, `v3.0` etc.
- GitHub skapar automatiskt en release vid taggning
- Gamla docs-filer tas bort — versionshistorik finns i git-taggar

---

## Direktiv för Claude

Dessa direktiv gäller när Claude arbetar med detta projekt.

### Kommunikation
- Ställ **en fråga i taget** vid oklarheter — aldrig gissa
- Visa **alltid formeln** och bekräfta beräkning innan PDF uppdateras
- Visa **Tidigare/Nytt-tabell** innan varje måttändring genomförs
- Håll svar **korta och direkta** — ingen upprepning av vad användaren just sagt
- Uppdatera aldrig dokument utan bekräftelse när beräkning ingår

### Måttkedjor
- Kontrollera **alltid** att längdkedja = **8,66 m** och breddkedja = **7,46 m** efter varje ändring
- Tolerans: ±5 mm (0,005 m)
- Visa kedjeformeln explicit: `A + B + C + ... = 8,66 m ✓`

### Dokumentuppdateringar
- Uppdatera alltid PDF och tester **samtidigt** — aldrig ett utan det andra
- Kör alltid tester lokalt innan commit — 0 fel tolereras
- PDF-sökväg ska **alltid** vara relativ:
```python
os.path.join(os.path.dirname(__file__), '..', 'docs', 'Timmerhus-Konstruktionsdokument.pdf')
```
- Uppdatera `CONTRIBUTING.md` om nya direktiv tillkommer

### Tillgänglighet
- Kontrollera alltid vändcirkel (min **1,30 m**) vid möblerings- eller måttändringar
- Kontrollera alltid gångbredd (min **1,20 m**)
- Notera alltid om dörr öppnar in eller ut — påverkar fri yta

### Git-flöde

**Aldrig committa direkt på `main`** — alltid via feature-branch och PR.

```bash
# 1. Skapa branch
git checkout main
git pull origin main
git checkout -b feature/[beskrivning]

# 2. Gör ändringar, kör tester
python tests/test_consistency.py

# 3. Commit
git add -A
git commit -m "feat/fix/docs/ci: beskrivning"

# 4. Hitta ändrade filer för zip
git diff main..feature/[beskrivning] --name-only

# 5. Skapa zip med ENDAST ändrade filer
zip timmerhus-changes-YYYYMMDD-HHMM-[beskrivning].zip [filer]

# 6. Pusha och skapa PR
git push origin feature/[beskrivning]

# 7. Efter merge — städa upp
git checkout main
git pull origin main
git branch -D feature/[beskrivning]
git push origin --delete feature/[beskrivning]

# 8. Tagga godkänd version
git tag v[VERSION]
git push origin v[VERSION]
```

### Versionshantering
- Zip-filer innehåller **endast ändrade filer** vs `main`
- Zip-namn: `timmerhus-changes-YYYYMMDD-HHMM-[beskrivning].zip`
- Docs i git: enkla namn utan datum
- Gamla daterade docs-filer tas bort vid uppdatering
- Versionshistorik finns i git-taggar — inte i filnamn

### PR-beskrivning
Använd alltid `.github/PULL_REQUEST_TEMPLATE.md` och fyll i:
- Alla påverkade mått med Tidigare/Nytt
- Måttkedjekontroll (längd + bredd summerar ✓)
- Antal tester och resultat
