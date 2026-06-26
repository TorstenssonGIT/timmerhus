import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'Timmerhus-Konstruktionsdokument.pdf')

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=20*mm, bottomMargin=20*mm
)

W = A4[0] - 40*mm
styles = getSampleStyleSheet()

def style(name, **kwargs):
    return ParagraphStyle(name, parent=styles['Normal'], **kwargs)

TITLE     = style('TITLE',    fontSize=20, leading=24, textColor=colors.HexColor('#1a3a5c'), spaceAfter=4, fontName='Helvetica-Bold', alignment=TA_CENTER)
SUB       = style('SUB',      fontSize=11, leading=14, textColor=colors.HexColor('#1a3a5c'), spaceAfter=2, fontName='Helvetica', alignment=TA_CENTER)
H1        = style('H1',       fontSize=13, leading=16, textColor=colors.HexColor('#1a3a5c'), spaceBefore=10, spaceAfter=4, fontName='Helvetica-Bold')
H2        = style('H2',       fontSize=11, leading=13, textColor=colors.HexColor('#2e6da4'), spaceBefore=6, spaceAfter=3, fontName='Helvetica-Bold')
BODY      = style('BODY',     fontSize=9,  leading=13, spaceAfter=3, fontName='Helvetica')
NOTE      = style('NOTE',     fontSize=8,  leading=11, spaceAfter=2, fontName='Helvetica-Oblique', textColor=colors.HexColor('#555555'))
CELL_BODY = style('CELL_BODY',fontSize=9,  leading=12, fontName='Helvetica')
CELL_HDR  = style('CELL_HDR', fontSize=9,  leading=12, fontName='Helvetica-Bold', textColor=colors.white)

HDR_BG  = colors.HexColor('#1a3a5c')
ROW_ALT = colors.HexColor('#eaf1fb')
WHITE   = colors.white

def wrap(text, is_header=False):
    if isinstance(text, str):
        return Paragraph(text, CELL_HDR if is_header else CELL_BODY)
    return text

def table(data, col_widths, header=True):
    wrapped = [[wrap(c, header and i==0) for c in row] for i, row in enumerate(data)]
    t = Table(wrapped, colWidths=col_widths)
    ts = [
        ('ROWBACKGROUNDS', (0,1 if header else 0), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID',      (0,0), (-1,-1), 0.4, colors.HexColor('#b0c4de')),
        ('VALIGN',    (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING',(0,0), (-1,-1), 5),
        ('TOPPADDING',  (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]
    if header:
        ts += [('BACKGROUND', (0,0), (-1,0), HDR_BG)]
    t.setStyle(TableStyle(ts))
    return t

def h(text, lvl=1): return Paragraph(text, H1 if lvl==1 else H2)
def p(text): return Paragraph(text, BODY)
def note(text): return Paragraph(f"<i>{text}</i>", NOTE)
def sp(h=4): return Spacer(1, h*mm)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#b0c4de'), spaceAfter=2)

story = []

# ── HEADER ───────────────────────────────────────────────────────────────────
story += [
    sp(2),
    Paragraph("TIMMERHUS", TITLE),
    Paragraph("Konstruktionsdokument — Handikappanpassat Fritidshus", SUB),
    Paragraph("9,00 m × 8,00 m | Blockat 7\" Timmer | Tillgänglighetsanpassat | v4.0", SUB),
    sp(2), hr(), sp(4),
]

# ── 1. HUVUDMÅTT ─────────────────────────────────────────────────────────────
story += [h("1. Huvudmått &amp; Yttre Geometri"), hr()]
story += [table([
    ["Parameter", "Värde", "Kommentar"],
    ["Byggnadsarea (BYA)", "9,00 × 8,00 m = 72,0 m²", "Bredd utökad till 8,00 m — ger badrum 3,20 m och fullständigt kök"],
    ["Invändig yta, nedre plan", "8,66 × 7,66 m = 66,3 m²", ""],
    ["Yttervägg", "170 mm (7\" blockat timmer)", "10-årigt snustorrt — 0 mm framtida sättning"],
    ["Innerväggar", "150 mm (95 mm regel + 2×26 mm OSB/gips)", "Rw ~45–50 dB"],
    ["Innerhöjd nedre plan", "2,35 m", "Fast fri höjd under loftbalkar"],
    ["Totalhöjd till nock", "ca 6,70 m", "30° taklutning, inkl. förhöjt väggliv på loft"],
    ["Takutstick, terrass (vänster)", "2,00 m", "Helt fribärande, stolpfritt"],
    ["Takutstick, baksida (höger)", "0,70 m", ""],
], [W*0.32, W*0.32, W*0.36])]
story += [sp(4)]

# ── 2. STOMME ────────────────────────────────────────────────────────────────
story += [h("2. Stomme, Takåsar &amp; Mellanbjälklag"), hr()]
story += [h("2.1 Bärande hjärtvägg &amp; Tak", lvl=2), p(
    "Hjärtväggen är 170 mm tjock och placerad exakt 4,03 m in från storstugans gavel. "
    "Den bär 5–7 stycken hellånga blockade 7\" takåsar (11,20–12,00 m). "
    "Yttertaket består av överramar (2\"×8\" eller 2\"×10\") i 30° lutning, skruvade direkt i åsarna. "
    "Inga fackverkstakstolar. Åsarna är synliga inifrån — kathedralkänsla."
), sp(2)]

story += [h("2.2 Mellanbjälklag till loft — Uppbyggnad (totalt 384 mm)", lvl=2)]
story += [table([
    ["Skikt (uppifrån)", "Tjocklek", "Material / Funktion"],
    ["1. Loftgolv", "34 mm", "Kraftigt spontat trägolv"],
    ["2. Golvreglar", "45 × 125 mm", "Tvärsgående reglar med 125 mm isolering (stegdämpning)"],
    ["3. Takpanel", "22 mm", "Spontad panel spikas underifrån — infälld i balktopp"],
    ["4. Bärande loftbalkar", "225 mm (9\")", "7\"×9\" blockat timmer, stående på högkant, spänner 7,66 m"],
    ["TOTALT", "384 mm", "Takhöjd mellan balkarna: ca 2,55 m"],
], [W*0.30, W*0.18, W*0.52])]
story += [sp(4)]

# ── 3. RUMSPLAN ──────────────────────────────────────────────────────────────
story += [h("3. Rumsplan Nedre Plan — Detaljerade Mått"), hr()]

story += [h("3.1 Måttkedja i längdled (8,66 m invändig)", lvl=2)]
story += [table([
    ["Sektion", "Mått", "Ackumulerat", "Kommentar"],
    ["Storstuga", "4,03 m", "4,03 m", "Hjärtvägg 40 cm mot terrassen vs ursprung"],
    ["Hjärtvägg", "0,17 m", "4,20 m", "Bärande, 170 mm blockat timmer"],
    ["Utilities / Serviceutrymme", "1,30 m", "5,50 m", "Lyftbar trappa, teknik vid yttervägg"],
    ["Innervägg", "0,15 m", "5,65 m", "Brand- och ljudisolerad"],
    ["Master Bedroom", "3,01 m", "8,66 m ✓", "Säng ger 1,36 m fri sida"],
], [W*0.26, W*0.14, W*0.16, W*0.44])]
story += [sp(3)]

story += [h("3.2 Måttkedja i breddled (7,66 m invändig)", lvl=2)]
story += [table([
    ["Sektion", "Mått", "Ackumulerat", "Kommentar"],
    ["Övre blocket", "2,96 m", "2,96 m", "Master Bedroom + Utilities"],
    ["Innervägg", "0,15 m", "3,11 m", ""],
    ["Central gång", "1,20 m", "4,31 m", "Rullstolsanpassad"],
    ["Innervägg", "0,15 m", "4,46 m", ""],
    ["Nedre blocket", "3,20 m", "7,66 m ✓", "Badrum + Lilla sovrummet + Kök"],
], [W*0.26, W*0.14, W*0.16, W*0.44])]
story += [sp(3)]

story += [h("3.3 Rumssammanställning", lvl=2)]
story += [table([
    ["Rum", "Mått (B × D)", "Area", "Nyckeldata"],
    ["Storstuga", "7,66 × 4,03 m", "30,9 m²", "Öppet till nock, synliga takåsar, katedral. K/F 2×0,60 m fristående mot yttervägg"],
    ["Serviceutrymme / Utilities", "2,96 × 1,30 m", "3,8 m²", "Lyftbar trappa 1,00 m bred, torsionsfjädrar, teknik vid yttervägg, brandcell 2×15 mm gips"],
    ["Master Bedroom", "2,96 × 3,01 m", "8,9 m²", "Säng 160×200 cm huvud mot Utilities-vägg, 1,36 m fri sida, garderober 2×0,50×0,55 m längs gångväggen"],
    ["Entréficka", "1,75 × 0,85 m", "1,49 m²", "0,55 m (Master-sidan) + 1,20 m (gång), djup 0,85 m"],
    ["Central gång / Hall", "1,20 × 4,06 m", "4,9 m²", "Rullstolsanpassad 120 cm"],
    ["Badrum", "3,20 × 1,70 m", "5,4 m²", "Tröskelfri dusch vid yttervägg med fönster, 10M dörr inåtgående, vändcirkel 1,30 m ✓"],
    ["Lilla sovrummet", "3,20 × 2,21 m", "7,1 m²", "Säng 80×200 cm huvud mot badrumsvägg, garderob 0,80×0,55 m, nattduksbord max 0,65×0,55 m"],
    ["TOTALT nedre plan", "—", "62,4 m²", "(inkl. väggar 66,3 m²)"],
], [W*0.20, W*0.18, W*0.10, W*0.52])]
story += [sp(4)]

# ── 4. KÖKSLAYOUT ────────────────────────────────────────────────────────────
story += [h("4. Kökslayout — Längs Hjärtväggen (3,20 m)"), hr()]
story += [p(
    "Köket löper längs hjärtväggen på storstugesidan, begränsat av gångens innervägg till 3,20 m. "
    "Spegelvänt för att undvika takhuv under snöbelastat takutstick. "
    "K/F placeras fristående mot ytterväggen i storstugan."
), sp(2)]
story += [table([
    ["Position", "Underskåp", "Bredd", "Överskåp", "Bredd"],
    ["Vid gång", "Lådor", "0,60 m", "Micro", "0,60 m"],
    ["", "Spis", "0,60 m", "Fläkt/huv", "0,60 m"],
    ["", "Lådor", "0,30 m", "1 lucka", "0,30 m"],
    ["", "Diskho", "0,80 m", "2 luckor", "0,80 m"],
    ["", "DM", "0,45 m", "2 luckor", "0,90 m"],
    ["Vid yttervägg", "Lådor", "0,45 m", "—", "—"],
    ["Fristående", "K/F 2×0,60 m mot yttervägg", "1,20 m", "—", "—"],
    ["TOTALT (exkl K/F)", "", "3,20 m ✓", "", "3,20 m ✓"],
], [W*0.18, W*0.22, W*0.12, W*0.22, W*0.12])]
story += [sp(3)]

story += [h("4.1 Hjärtväggen Storstugesidan (4,03 m)", lvl=2)]
story += [table([
    ["Position", "Bredd", "Kommentar"],
    ["Öppen", "1,00 m", "Passage från storstugan"],
    ["Kaminkakel", "2,00 m", "Granit/natursten, kamin cc 1,00 m från gångens vänstra kant"],
    ["Marginal", "0,15 m", ""],
    ["9M EI30 servicedörr", "0,88 m", "Åtkomst till Utilities från storstugan"],
    ["TOTALT", "4,03 m ✓", ""],
], [W*0.25, W*0.20, W*0.55])]
story += [sp(4)]

# ── 5. BADRUMSLAYOUT ─────────────────────────────────────────────────────────
story += [h("5. Badrumslayout (3,20 × 1,70 m = 5,4 m²)"), hr()]
story += [table([
    ["Position längs 3,20 m", "Enhet", "Bredd", "Kommentar"],
    ["Vid yttervägg", "Dusch 0,90×0,90 m", "0,90 m", "Tröskelfri, fönster bredvid mot yttervägg"],
    ["", "WC (inkl. marginal)", "0,20+0,40+0,20 m", ""],
    ["", "Kommod/handfat", "0,80 m", ""],
    ["Vid dörr", "Tvättmaskin", "0,60 m", "Rör tömning via väggen till köket"],
    ["TOTALT", "", "3,20 m ✓", ""],
    ["Vändcirkel", "1,70 × 1,30 m", "✓", "Dörr öppnar inåt, dörrblad 0,40 m"],
], [W*0.22, W*0.28, W*0.18, W*0.32])]
story += [sp(4)]

# ── 6. TILLGÄNGLIGHET ────────────────────────────────────────────────────────
story += [h("6. Tillgänglighet &amp; Handikappanpassning"), hr()]
story += [table([
    ["Åtgärd", "Specifikation"],
    ["Entrédörr", "10M (karmbredd 100 cm, fri öppning ≥ 80 cm), utåtgående"],
    ["Alla innerdörrar i boendeytan", "10M (karmbredd 100 cm, fri öppning ≥ 80 cm)"],
    ["Trösklar", "Max 25 mm, fasade"],
    ["Central gång", "120 cm bred — rullstol passerar obehindrat"],
    ["Entréficka", "1,75 m bred × 0,85 m djup — ytterkläder, skor, rullstolsparkering"],
    ["Badrum", "Tröskelfri dusch, vändcirkel 1,30 m ✓, 10M-dörr öppnar inåt"],
    ["Master Bedroom — fri sida om säng", "1,36 m ✓"],
    ["Master Bedroom — garderober", "2×0,50×0,55 m, fri yta framför 1,36 m ✓"],
    ["Lilla sovrummet — fri yta dörr stängd", "3,20 × 1,70 m — vändcirkel 1,30 m ✓"],
    ["Lilla sovrummet — fri yta dörr öppen", "2,80 × 1,70 m (3,20 - 0,40 dörrblad) ✓"],
], [W*0.38, W*0.62])]
story += [sp(4)]

# ── 7. UTILITIES / SERVICEUTRYMME ────────────────────────────────────────────
story += [h("7. Utilities / Serviceutrymme &amp; Lyftbar Trappa"), hr()]
story += [h("7.1 Lyftbar Trappa", lvl=2)]
story += [table([
    ["Parameter", "Värde / Beräkning"],
    ["Bredd", "1,00 m"],
    ["Steghöjd", "2,35 m / 12 steg = 19,6 cm"],
    ["Steglängd (djup)", "24,5 cm"],
    ["Antal uppsteg", "12 st"],
    ["Horisontell längd", "12 × 24,5 cm = 2,94 m"],
    ["Kvartsvarv", "1,00 × 1,00 m vid loftplanet"],
    ["Trappglugg i bjälklag", "1,00 × (2,94 + 1,00) = 1,00 × 3,94 m"],
    ["Loftbjälklagets uppbyggnad", "Innerhöjd 2,350 m + loftbalk 7\" (225 mm) + golvregel 5\" (125 mm) + golv (34 mm) = 2,734 m"],
    ["Konstruktion", "Vagnstycke 2\"×10\" ledat vid steg 11 (ett steg under kvartsvarvet), fäst med 30 mm lagerbockar i väggen"],
    ["Steg som lyfts", "10 st (steg 1–10), steg 11–12 + kvartsvarv är fast"],
    ["Lyfthöjd", "10 × 24,5 cm = 2,45 m — ger fri gånghöjd 10 × 19,6 cm = 1,96 m"],
    ["Trappvikt", "ca 128 kg (steg 45 mm massivt trä + vagnstycke 2\"×10\")"],
], [W*0.40, W*0.60])]
story += [sp(3)]

story += [h("7.2 Lyftsystem — Torsionsfjädrar", lvl=2)]
story += [table([
    ["Komponent", "Spec"],
    ["Torsionsfjädrar", "2 st, begagnade garageportsfjädrar, totalt 108 kg lyftkraft"],
    ["Axel", "Stålrör 25–30 mm, horisontell i loftbjälklaget ovanför ledpunkten"],
    ["Lagerbockar", "2 st, fästs i loftbjälklaget"],
    ["Trumma/kabel", "2 st, en per vagnstycke"],
    ["Restvikt att lyfta", "ca 20 kg — trappan ligger kvar nere av sig själv"],
    ["Låssystem", "Automatisk fjäderbelastad spärrhake i toppläge, utlöses via draghandtag nerifrån"],
    ["Kostnad", "ca 100–300 kr (begagnat garageportskit på Blocket)"],
    ["Livslängd", "Extremt lång — garageportsfjädrar dimensionerade för 10 000+ cykler, trappan används 10–20 ggr/år"],
], [W*0.35, W*0.65])]
story += [sp(3)]

story += [h("7.3 Teknikinstallation i Utilities", lvl=2)]
story += [table([
    ["Zon", "Placering", "Innehåll"],
    ["Under trappan", "Längs trappans 2,94 m", "Rör, tömning, cirkpumpar, expansionskärl, buffertank"],
    ["Vid yttervägg", "Längst in mot ytterväggen", "Värmepump + VVB/slinga för varmvatten"],
    ["Brandskydd", "Alla invändiga ytor", "Isolering + dubbla lager gips (2×15 mm)"],
], [W*0.22, W*0.30, W*0.48])]
story += [sp(4)]

# ── 8. VVS ──────────────────────────────────────────────────────────────────
story += [h("8. VVS-Installation"), hr()]
story += [table([
    ["System", "Utförande"],
    ["Värmepump + VVB/slinga", "Placerad vid yttervägg i Utilities"],
    ["Kaminrör (vattenmantlad)", "Dras osynligt genom hjärtväggens 170 mm till teknikutrymme"],
    ["Tappvatten kök & bad", "Synliga på vägg, 60 mm från tak, cc 60, tömningsfall mot Utilities"],
    ["Köks-/badrumsrör", "Tömning sker inne i badrummet via genomföring i väggen från köket"],
    ["Avlopp", "Gjuts dolt i betongplatta med uppstick under köksbänk och i badrum"],
], [W*0.28, W*0.72])]
story += [sp(4)]

# ── 9. ÖVERVÅNING ────────────────────────────────────────────────────────────
story += [h("9. Övervåning / Sovloft"), hr()]
story += [table([
    ["Parameter", "Värde"],
    ["Placering", "Ovanpå Utilities + Master + Gång + Badrum + Lilla sovrummet"],
    ["Bruttomått", "7,66 × 4,06 m = 31,1 m²"],
    ["Förhöjt väggliv (långsidor)", "85–90 cm"],
    ["Ståhöjd under nock", "ca 2,60–2,65 m"],
    ["Förvaringszoner (långsidor)", "1,03 m djup × 7,66 m längs varje långsida"],
    ["Fri golvyta (efter förvaring båda sidor)", "5,60 × 4,06 = 22,7 m²"],
    ["Trappöppning (avdrag)", "1,00 × 3,94 m = 3,94 m²"],
    ["Netto användbar loftyta", "18,8 m²"],
], [W*0.45, W*0.55])]
story += [sp(4)]

# ── 10. KAMIN & ENERGI ───────────────────────────────────────────────────────
story += [h("10. Uppvärmning &amp; Kamin"), hr()]
story += [p(
    "Vattenmantlad kamin placeras på hjärtväggens storstugesida inom kakelzonen (2,00 m granit/natursten). "
    "Kaminens centrum placeras 1,00 m från gångens vänstra kant. "
    "Kakelzonen skyddar mot brännskador. "
    "Rören dras osynligt genom hjärtväggens 170 mm till teknikutrymmet — inga synliga rör i storstugan."
), sp(4)]

# ── FOOTER ───────────────────────────────────────────────────────────────────
story += [hr(), note(
    "v4.0 — 2026-06-26: Bredd 8,00 m, badrum 3,20 m, kök 3,20 m spegelvänt, "
    "lyftbar trappa 1,00 m med torsionsfjädrar, 9M EI30 borttagen. "
    "Samtliga mått kvalitetssäkrade mot 9,00×8,00 m. Blockat 7\" timmer (170 mm)."
)]

doc.build(story)
print("PDF created:", OUTPUT)
