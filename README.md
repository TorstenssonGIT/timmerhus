# Timmerhus — Handikappanpassat Fritidshus

Konstruktionsdokument och projektfiler för handikappanpassat fritidshus i blockat 7" timmer.

## Projektfakta

| Parameter | Värde |
|---|---|
| Byggnadsarea (BYA) | 9,00 × 7,80 m = 70,2 m² |
| Invändig yta, nedre plan | 8,66 × 7,46 m = 64,6 m² |
| Stomme | Blockat 7" timmer (170 mm) |
| Tillgänglighet | Fullt handikappanpassat (rullstolsstandard) |
| Version | v2.0 |

## Struktur

```
timmerhus/
├── docs/                          # Konstruktionsdokument och beskrivningar
│   ├── Timmerhus-Konstruktionsdokument-YYYYMMDD-HHMM.pdf
│   └── Timmerhus-Projektbeskrivning-YYYYMMDD-HHMM.md
├── scripts/
│   └── generate_timmerhus_pdf.py  # PDF-generator (Python/ReportLab)
└── .github/
    └── PULL_REQUEST_TEMPLATE.md
```

## Namnkonvention

Alla filer namnges: `Timmerhus-[Beskrivning]-YYYYMMDD-HHMM-v[VERSION].[ext]`

## Generera PDF

```bash
pip install reportlab
python scripts/generate_timmerhus_pdf.py
```

## Versionshistorik

| Version | Datum | Ändringar |
|---|---|---|
| v1.0 | 2026-06-23 | Initial version — 7,40×9,00 m |
| v1.1–v1.5 | 2026-06-23 | Dörrkorrigeringar, trappdetaljer, loftmått |
| v2.0 | 2026-06-25 | Bredd utökad till 7,80 m, hjärtvägg flyttad 40 cm |
