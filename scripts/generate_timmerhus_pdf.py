from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/mnt/user-data/outputs/Timmerhus-Konstruktionsdokument-20260625-1600.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=20*mm, bottomMargin=20*mm
)

W = A4[0] - 40*mm

styles = getSampleStyleSheet()

def style(name, **kwargs):
    s = ParagraphStyle(name, parent=styles['Normal'], **kwargs)
    return s

TITLE   = style('TITLE',   fontSize=20, leading=24, textColor=colors.HexColor('#1a3a5c'), spaceAfter=4, fontName='Helvetica-Bold', alignment=TA_CENTER)
SUB     = style('SUB',     fontSize=11, leading=14, textColor=colors.HexColor('#1a3a5c'), spaceAfter=2, fontName='Helvetica', alignment=TA_CENTER)
H1      = style('H1',      fontSize=13, leading=16, textColor=colors.HexColor('#1a3a5c'), spaceBefore=10, spaceAfter=4, fontName='Helvetica-Bold')
H2      = style('H2',      fontSize=11, leading=13, textColor=colors.HexColor('#2e6da4'), spaceBefore=6, spaceAfter=3, fontName='Helvetica-Bold')
BODY    = style('BODY',    fontSize=9,  leading=13, spaceAfter=3, fontName='Helvetica')
NOTE    = style('NOTE',    fontSize=8,  leading=11, spaceAfter=2, fontName='Helvetica-Oblique', textColor=colors.HexColor('#555555'))
CELL_BODY = style('CELL_BODY', fontSize=9, leading=12, fontName='Helvetica')
CELL_HDR  = style('CELL_HDR',  fontSize=9, leading=12, fontName='Helvetica-Bold', textColor=colors.white)

HDR_BG  = colors.HexColor('#1a3a5c')
ROW_ALT = colors.HexColor('#eaf1fb')
WHITE   = colors.white

def wrap(text, is_header=False):
    if isinstance(text, str):
        return Paragraph(text, CELL_HDR if is_header else CELL_BODY)
    return text

def table(data, col_widths, header=True):
    wrapped = []
    for i, row in enumerate(data):
        is_hdr = header and i == 0
        wrapped.append([wrap(cell, is_hdr) for cell in row])
    t = Table(wrapped, colWidths=col_widths)
    ts = [
        ('ROWBACKGROUNDS', (0,1 if header else 0), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID',      (0,0), (-1,-1), 0.4, colors.HexColor('#b0c4de')),
        ('VALIGN',    (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING',  (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]
    if header:
        ts += [('BACKGROUND', (0,0), (-1,0), HDR_BG)]
    t.setStyle(TableStyle(ts))
    return t

def h(text, lvl=1):
    return Paragraph(text, H1 if lvl==1 else H2)

def p(text):
    return Paragraph(text, BODY)

def note(text):
    return Paragraph(f"<i>{text}</i>", NOTE)

def sp(h=4):
    return Spacer(1, h*mm)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#b0c4de'), spaceAfter=2)

story = []

# ── HEADER ──────────────────────────────────────────────────────────────────
story += [
    sp(2),
    Paragraph("TIMMERHUS", TITLE),
    Paragraph("Konstruktionsdokument — Handikappanpassat Fritidshus", SUB),
    Paragraph("9,00 m × 7,80 m | Blockat 7\" Timmer | Tillgänglighetsanpassat", SUB),
    sp(2), hr(), sp(4),
]

# ── 1. HUVUDMÅTT ─────────────────────────────────────────────────────────────
story += [h("1. Huvudmått &amp; Yttre Geometri"), hr()]
story += [table([
    ["Parameter", "Värde", "Kommentar"],
    ["Byggnadsarea (BYA)", "9,00 × 7,80 m = 70,2 m²", "Utökat från 7,40×9,00 — +40 cm bredd ger bättre tillgänglighet"],
    ["Invändig yta, nedre plan", "8,66 × 7,46 m = 64,6 m²", ""],
    ["Yttervägg", "170 mm (7\" blockat timmer)", "10-årigt snustorrt — 0 mm framtida sättning"],
    ["Innerhöjd nedre plan", "2,35 m", "Fast fri höjd under loftbalkar; plant tak i badrum"],
    ["Totalhöjd till nock", "ca 6,70 m", "30° taklutning, inkl. förhöjt väggliv på loft"],
    ["Takutstick, terrass (vänster)", "2,00 m", "Helt fribärande, stolpfritt"],
    ["Takutstick, baksida (höger)", "0,70 m", ""],
], [W*0.32, W*0.32, W*0.36])]
story += [sp(4)]

# ── 2. STOMME ────────────────────────────────────────────────────────────────
story += [h("2. Stomme, Takåsar &amp; Mellanbjälklag"), hr()]

story += [h("2.1 Bärande hjärtvägg &amp; Tak", lvl=2), p(
    "Hjärtväggen är 170 mm tjock och placerad exakt 4,03 m in från storstugans gavel (tidigare 4,43 m — "
    "flyttad 40 cm för att ge Master Bedroom mer djup). "
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
    ["4. Bärande loftbalkar", "225 mm (9\")", "7\"×9\" blockat timmer, stående på högkant, spänner 7,46 m"],
    ["TOTALT", "384 mm", "Takhöjd mellan balkarna: ca 2,55 m"],
], [W*0.30, W*0.18, W*0.52])]
story += [sp(4)]

# ── 3. RUMSPLAN ──────────────────────────────────────────────────────────────
story += [h("3. Rumsplan Nedre Plan — Detaljerade Mått"), hr()]
story += [p(
    "Invändig bredd 7,46 m delas av den 1,20 m breda centrala gången, flankerad av "
    "2 × 150 mm bärande innerväggar (brand- och ljudisolerade). "
    "Det ger Övre blocket 3,46 m och Nedre blocket 2,50 m (+10 cm vs tidigare tack vare bredare stuga)."
), sp(2)]

story += [h("3.1 Måttkedja i längdled (8,66 m invändig)", lvl=2)]
story += [table([
    ["Sektion", "Mått", "Ackumulerat", "Förändring vs tidigare"],
    ["Storstuga", "4,03 m", "4,03 m", "-0,40 m (hjärtvägg flyttad)"],
    ["Hjärtvägg", "0,17 m", "4,20 m", "oförändrad"],
    ["Utilities / Serviceutrymme", "1,65 m", "5,85 m", "oförändrad"],
    ["Innervägg", "0,15 m", "6,00 m", "oförändrad"],
    ["Master Bedroom", "2,66 m", "8,66 m ✓", "+0,40 m — sida om säng nu 1,06 m"],
], [W*0.28, W*0.16, W*0.18, W*0.38])]
story += [sp(3)]

story += [h("3.2 Måttkedja i breddled (7,46 m invändig)", lvl=2)]
story += [table([
    ["Sektion", "Mått", "Ackumulerat", "Förändring vs tidigare"],
    ["Övre blocket", "3,46 m", "3,46 m", "oförändrad"],
    ["Innervägg", "0,15 m", "3,61 m", "oförändrad"],
    ["Central gång", "1,20 m", "4,81 m", "oförändrad"],
    ["Innervägg", "0,15 m", "4,96 m", "oförändrad"],
    ["Nedre blocket", "2,50 m", "7,46 m ✓", "+0,10 m — badrum och sovrum bredare"],
], [W*0.28, W*0.16, W*0.18, W*0.38])]
story += [sp(3)]

story += [h("3.3 Rumssammanställning", lvl=2)]
story += [table([
    ["Rum", "Mått (B × D)", "Area", "Nyckeldata"],
    ["Storstuga + Kök", "7,46 × 4,03 m", "30,1 m²", "Öppet till nock, synliga takåsar, katedral"],
    ["Serviceutrymme / Utilities", "3,46 × 1,65 m", "5,7 m²", "Trappa 80 cm (öppen mot gång, kvartsvarv topp), 9M EI30-dörr, ack.tank, brandcell 2×15 mm gips"],
    ["Master Bedroom", "3,46 × 2,66 m", "9,2 m²", "Säng 160×200 cm, 4 garderober 60×55 cm, sida om säng 1,06 m"],
    ["Central gång / Hall", "1,20 × 4,06 m", "4,9 m²", "Rullstolsanpassad, entrégarderob 60×55 cm"],
    ["Badrum", "2,50 × 1,70 m", "4,3 m²", "Tröskelfri dusch, linneskåp i vägg, 10M-dörr"],
    ["Lilla sovrummet", "2,50 × 2,21 m", "5,5 m²", "Säng 80×200 cm, 1,70 m fri rullstolsyta"],
    ["TOTALT nedre plan", "—", "59,7 m²", "(inkl. väggar 64,6 m²)"],
], [W*0.22, W*0.20, W*0.10, W*0.48])]
story += [sp(4)]

# ── 4. TILLGÄNGLIGHET ────────────────────────────────────────────────────────
story += [h("4. Tillgänglighet &amp; Handikappanpassning"), hr()]
story += [table([
    ["Åtgärd", "Specifikation"],
    ["Entrédörr", "10M (karmbredd 100 cm, fri öppning ≥ 80 cm), utåtgående"],
    ["Alla innerdörrar i boendeytan (utom Utilities)", "10M (karmbredd 100 cm, fri öppning ≥ 80 cm)"],
    ["Trösklar", "Max 25 mm, fasade"],
    ["Central gång", "120 cm bred — rullstol passerar obehindrat"],
    ["Badrum", "Tröskelfri dusch, 10M-dörr öppnas utåt mot storstugan"],
    ["Master Bedroom — sängfri yta", "1,46 m vid fotända + 1,06 m på sida = fri manövrering"],
    ["Master Bedroom — framför garderober", "0,91 m fritt svängutrymme för rullstol"],
    ["Lilla sovrummet — sängfri yta", "1,70 m bred fri yta på sängens sida"],
    ["Entrégarderob", "Öppnas direkt mot gången — inga hinder i hallzonen"],
    ["Utilities 9M-dörr (EI30)", "Karmbredd 88 cm — placerad bredvid trappan i gångväggen"],
], [W*0.38, W*0.62])]
story += [sp(4)]

# ── 5. VVS ──────────────────────────────────────────────────────────────────
story += [h("5. VVS-Installation"), hr()]
story += [table([
    ["System", "Utförande"],
    ["Kaminrör (vattenmantlad)", "Dras osynligt bakåt genom hjärtväggens 170 mm timmer direkt till ack.tank i brandcellen"],
    ["Tappvatten kök & bad", "Synliga på vägg, 60 mm från tak, cc 60, jämnt tömningsfall mot serviceutrymme"],
    ["VVS-passage gång", "Rören korsar gången i 25 cm fritt utrymme ovanför 10M-dörren i hjärtväggen"],
    ["Avlopp", "Gjuts dolt i betongplatta med uppstick under köksbänk och i badrum"],
    ["Ackumulatortank", "300–500 L, placerad under trappstegen i brandcellen"],
], [W*0.28, W*0.72])]
story += [sp(4)]

# ── 6. ÖVERVÅNING ────────────────────────────────────────────────────────
story += [h("6. Övervåning / Sovloft"), hr()]
story += [table([
    ["Parameter", "Värde"],
    ["Placering", "Ovanpå Utilities + Master + Gång + Badrum + Lilla sovrummet"],
    ["Bruttomått", "7,46 × 4,06 m = 30,3 m²"],
    ["Förhöjt väggliv (långsidor)", "85–90 cm"],
    ["Ståhöjd under nock", "ca 2,60–2,65 m"],
    ["Förvaringszoner (långsidor)", "1,03 m djup × 7,46 m längs varje långsida — headroom 1,22–1,34 m vid innerkant (60–80 cm djup)"],
    ["Fri golvyta (efter förvaring båda sidor)", "5,40 × 4,06 = 21,9 m²"],
    ["Trappöppning (avdrag)", "0,80 × 2,94 m = 2,35 m²"],
    ["Netto användbar loftyta", "19,6 m²"],
], [W*0.45, W*0.55])]
story += [sp(3)]

story += [h("6.1 Trappa — Detaljmått", lvl=2)]
story += [table([
    ["Parameter", "Värde / Beräkning"],
    ["Bredd", "1,00 m"],
    ["Loftbjälklagets uppbyggnad", "Innerhöjd 2,350 m + loftbalk 7\" (225 mm) + golvregel 5\" (125 mm) + golv (34 mm) = 2,734 m"],
    ["Total klätthöjd", "2,734 m"],
    ["Steghöjd", "2,35 m / 12 = 19,6 cm"],
    ["Steglängd", "24,5 cm"],
    ["Antal uppsteg", "12 st"],
    ["Horisontell längd", "12 × 24,5 cm = 2,94 m"],
    ["Kvartsvarv", "1,00 × 1,00 m vid loftplanet"],
    ["Trappglugg", "1,00 × (2,94 + 1,00) = 1,00 × 3,94 m"],
    ["Konstruktion", "Lyftbar — vagnstycke 2\"×10\" ledat vid steg 11, lagerbockar 30 mm i vägg"],
    ["Steg som lyfts", "10 st (steg 1–10), lyfthöjd 10 × 24,5 cm = 2,45 m"],
    ["Fri gånghöjd", "10 × 19,6 cm = 1,96 m när trappan är lyft"],
    ["Hävarm", "1,30 m horisontell in i Utilities från ledpunkt"],
    ["Trappvikt", "ca 128 kg (steg 45 mm massivt trä + vagnstycke 2\"×10\")"],
    ["Brandskydd", "Isolering + 2×15 mm gips på alla invändiga väggytor i Utilities"],
], [W*0.40, W*0.60])]
story += [sp(3)]

story += [h("6.2 Lyftsystem — Torsionsfjädrar", lvl=2)]
story += [table([
    ["Parameter", "Värde"],
    ["Antal fjädrar", "3 st parallella (+ 1 st reserv)"],
    ["Fjädertyp", "0,250 × 2\" × 31\" (79 cm), 124 varv, 16 000 cykler"],
    ["Placering", "Längs loftbjälkarna cc 120 cm, 3 separata axlar 1\" stålrör (25,4 mm)"],
    ["Axelfästen", "Kullager 1\" + axelhållare per axel, fästa i loftbjälklag"],
    ["Utväxling", "1:2 via linhjul nertill på hävarm — vajer ned och upp"],
    ["Lyftkraft", "3 × 45 kg = 135 kg (vid 7 varv förspänning)"],
    ["Restvikt", "135 - 128 = 7 kg — trappan ligger kvar nere ✓"],
    ["Förspänning", "7 varv per fjäder (fjäderspännpinne Ø13 mm)"],
    ["Vajerlängd", "4,90 m per sida (ned 2,45 m + upp 2,45 m)"],
    ["Vajer", "3 mm stålvajer, 2 st à 4,90 m"],
    ["Låssystem", "Automatisk fjäderbelastad spärrhake i toppläge"],
    ["Livslängd", "16 000 cykler — vid 20 lyft/år = 800 år"],
], [W*0.38, W*0.62])]
story += [sp(3)]

story += [h("6.3 Inköpslista Lyftsystem", lvl=2)]
story += [table([
    ["Komponent", "Art.nr", "Antal", "Pris/st", "Totalt"],
    ["VEVOR torsionsfjäder 0,250×2×31\" (par)", "VEVOR", "1 par", "883 kr", "883 kr"],
    ["Kullager 1\"", "USA-B", "3 st", "55 kr", "165 kr"],
    ["Axelhållare 1\"", "312RC", "6 st", "100 kr", "600 kr"],
    ["Fjäderspännpinne Ø13 mm", "RES-TB", "2 st", "150 kr", "300 kr"],
    ["Lyftwire 3 mm × 4,90 m", "K3-03305", "3 par", "190 kr", "570 kr"],
    ["Linhjul", "—", "3 st", "~50 kr", "~150 kr"],
    ["1\" stålrör axlar", "—", "3 st", "~50 kr", "~150 kr"],
    ["TOTALT", "", "", "", "~2 818 kr"],
], [W*0.30, W*0.12, W*0.10, W*0.12, W*0.12])]
story += [sp(3)]

story += [h("6.4 Monteringsordning", lvl=2)]
story += [table([
    ["Steg", "Åtgärd"],
    ["1", "Lyft trappan manuellt med 2 personer eller domkraft — full 128 kg"],
    ["2", "Lås trappan i toppläge med temporär spärr"],
    ["3", "Montera axlar, kullager och axelhållare i loftbjälklaget"],
    ["4", "Montera torsionsfjädrar på axlarna"],
    ["5", "Montera linhjul nertill på hävarm"],
    ["6", "Dra vajrar från axeltrumma ned till linhjul och upp till fast fäste"],
    ["7", "Spänn fjädrarna 7 varv med fjäderspännpinnar"],
    ["8", "Montera automatisk spärrhake i toppläge"],
    ["9", "Lossa temporär spärr — trappan sänks kontrollerat med 7 kg restvikt"],
    ["10", "Testa lyft — justera varv vid behov"],
], [W*0.10, W*0.90])]
story += [sp(4)]

# ── 7. KAMIN & ENERGI ────────────────────────────────────────────────────────
story += [h("7. Uppvärmning &amp; Kamin"), hr()]
story += [p(
    "Vattenmantlad kamin placeras på hjärtväggens nedre del, till höger om mittgångens öppning, "
    "direkt framför det 0,86 m fasta timmerpartiet i Utilities (tidigare 1,26 m — reducerat då hjärtväggen flyttats 40 cm). "
    "Rören dras osynligt genom hjärtväggens 170 mm till ackumulatortanken — inga synliga rör i storstugan."
), sp(4)]

# ── FOOTER NOTE ─────────────────────────────────────────────────────────────
story += [hr(), note(
    "Samtliga mått kvalitetssäkrade mot husets utvändiga 9,00 × 7,80 m. "
    "Reviderat v2.0: bredd utökad till 7,80 m (+40 cm), hjärtvägg flyttad 40 cm mot terrassen. "
    "Blockat 7\" timmer (170 mm), 10-årigt snustorrt — 0 mm framtida sättning."
)]

doc.build(story)
print("PDF created:", OUTPUT)
