"""
Timmerhus — Konstruktionsdokument Konsistenstester
===================================================
Verifierar att alla mått, måttkedjor och tillgänglighetskrav stämmer.
Kör med: python tests/test_consistency.py
"""

import unittest

# ── Grunddata ────────────────────────────────────────────────────────────────
YTTERVÄGG       = 0.170  # m, blockat 7" timmer
INNERVÄGG       = 0.150  # m, brand/ljud

# Yttre mått
YTTRE_LÄNGD     = 9.00
YTTRE_BREDD     = 7.80

# Invändiga mått
INV_LÄNGD       = YTTRE_LÄNGD - 2 * YTTERVÄGG   # 8.66 m
INV_BREDD       = YTTRE_BREDD - 2 * YTTERVÄGG   # 7.46 m

# Längdkedja
STORSTUGA       = 4.03
HJÄRTVÄGG       = 0.17
UTILITIES       = 1.30
MASTER_DJUP     = 3.01

# Breddkedja
ÖVRE_BLOCK      = 3.46
GÅNG            = 1.20
NEDRE_BLOCK     = 2.50

# Rum
MASTER_BREDD    = ÖVRE_BLOCK
BADRUM_B        = NEDRE_BLOCK
BADRUM_D        = 1.70
LILLA_B         = NEDRE_BLOCK
LILLA_D         = 2.21
UTILITIES_B     = ÖVRE_BLOCK

# Trappa
TRAPPA_BREDD    = 0.90
STEGHÖJD        = 0.245
KLÄTTHÖJD       = 2.734
KVARTSVARV      = TRAPPA_BREDD

# Loft
LOFT_BREDD      = INV_BREDD
LOFT_DJUP       = 4.06
FÖRVARING_DJUP  = 1.03
TRAPPGLUGG_L    = (KLÄTTHÖJD / STEGHÖJD)  # antal steg

# Entréficka
ENTRÉ_BREDD     = 0.55 + GÅNG   # Master-sidan + gång
ENTRÉ_DJUP      = 0.85

# Säng Master
SÄNG_M_B        = 1.60
SÄNG_M_L        = 2.00

# Säng lilla sovrum
SÄNG_L_B        = 0.80
SÄNG_L_L        = 2.00

TOLERANCE = 0.005  # 5 mm tolerans


class TestMåttkedjor(unittest.TestCase):

    def test_invändig_längd(self):
        """Invändig längd = Yttre längd - 2 × yttervägg"""
        self.assertAlmostEqual(INV_LÄNGD, 8.66, delta=TOLERANCE,
            msg=f"Invändig längd ska vara 8,66 m, är {INV_LÄNGD:.3f} m")

    def test_invändig_bredd(self):
        """Invändig bredd = Yttre bredd - 2 × yttervägg"""
        self.assertAlmostEqual(INV_BREDD, 7.46, delta=TOLERANCE,
            msg=f"Invändig bredd ska vara 7,46 m, är {INV_BREDD:.3f} m")

    def test_längdkedja(self):
        """Storstuga + Hjärtvägg + Utilities + Innervägg + Master = 8,66 m"""
        summa = STORSTUGA + HJÄRTVÄGG + UTILITIES + INNERVÄGG + MASTER_DJUP
        self.assertAlmostEqual(summa, INV_LÄNGD, delta=TOLERANCE,
            msg=f"Längdkedja summerar till {summa:.3f} m, ska vara {INV_LÄNGD:.3f} m")

    def test_breddkedja(self):
        """Övre block + Innervägg + Gång + Innervägg + Nedre block = 7,46 m"""
        summa = ÖVRE_BLOCK + INNERVÄGG + GÅNG + INNERVÄGG + NEDRE_BLOCK
        self.assertAlmostEqual(summa, INV_BREDD, delta=TOLERANCE,
            msg=f"Breddkedja summerar till {summa:.3f} m, ska vara {INV_BREDD:.3f} m")

    def test_utilities_djup(self):
        """Utilities djup ska vara 1,30 m"""
        self.assertAlmostEqual(UTILITIES, 1.30, delta=TOLERANCE)

    def test_master_djup(self):
        """Master Bedroom djup ska vara 3,01 m"""
        self.assertAlmostEqual(MASTER_DJUP, 3.01, delta=TOLERANCE)


class TestRumsAreaer(unittest.TestCase):

    def test_storstuga_area(self):
        area = INV_BREDD * STORSTUGA
        self.assertAlmostEqual(area, 30.1, delta=0.1,
            msg=f"Storstuga area ska vara 30,1 m², är {area:.1f} m²")

    def test_master_area(self):
        area = MASTER_BREDD * MASTER_DJUP
        self.assertAlmostEqual(area, 10.4, delta=0.1,
            msg=f"Master Bedroom area ska vara 10,4 m², är {area:.1f} m²")

    def test_utilities_area(self):
        area = UTILITIES_B * UTILITIES
        self.assertAlmostEqual(area, 4.5, delta=0.1,
            msg=f"Utilities area ska vara 4,5 m², är {area:.1f} m²")

    def test_badrum_area(self):
        area = BADRUM_B * BADRUM_D
        self.assertAlmostEqual(area, 4.3, delta=0.1,
            msg=f"Badrum area ska vara 4,3 m², är {area:.1f} m²")

    def test_lilla_sovrum_area(self):
        area = LILLA_B * LILLA_D
        self.assertAlmostEqual(area, 5.5, delta=0.1,
            msg=f"Lilla sovrummet area ska vara 5,5 m², är {area:.1f} m²")


class TestTillgänglighet(unittest.TestCase):

    def test_gång_bredd(self):
        """Gång ska vara minst 120 cm för rullstol"""
        self.assertGreaterEqual(GÅNG, 1.20,
            msg=f"Gång {GÅNG:.2f} m — för smal för rullstol (min 1,20 m)")

    def test_master_fri_sida_säng(self):
        """Fri sida om säng i Master ska vara minst 90 cm"""
        fri_sida = MASTER_BREDD - SÄNG_M_L
        self.assertGreaterEqual(fri_sida, 0.90,
            msg=f"Master fri sida om säng: {fri_sida:.2f} m — under 0,90 m minimum")

    def test_master_fotända(self):
        """Fri yta vid sängens fotända i Master"""
        fri_fotända = MASTER_DJUP - SÄNG_M_B
        self.assertGreaterEqual(fri_fotända, 1.20,
            msg=f"Master fotända: {fri_fotända:.2f} m")

    def test_lilla_sovrum_fri_yta_dörr_stängd(self):
        """Fri yta i lilla sovrummet med dörr stängd"""
        fri_bredd = LILLA_B - SÄNG_L_B
        self.assertGreaterEqual(fri_bredd, 1.30,
            msg=f"Lilla sovrum fri bredd: {fri_bredd:.2f} m — under vändcirkel 1,30 m")

    def test_lilla_sovrum_fri_yta_dörr_öppen(self):
        """Fri yta i lilla sovrummet med dörr öppen (dörrblad 0,40 m)"""
        dörrblad = 0.40
        fri_djup = LILLA_D - dörrblad
        fri_bredd = LILLA_B - SÄNG_L_B
        self.assertGreaterEqual(fri_djup, 1.30,
            msg=f"Lilla sovrum fri djup med dörr öppen: {fri_djup:.2f} m")
        self.assertGreaterEqual(fri_bredd, 1.30,
            msg=f"Lilla sovrum fri bredd: {fri_bredd:.2f} m")

    def test_entréficka_bredd(self):
        """Entréficka ska vara minst 1,75 m bred"""
        self.assertAlmostEqual(ENTRÉ_BREDD, 1.75, delta=TOLERANCE,
            msg=f"Entréficka bredd: {ENTRÉ_BREDD:.2f} m")

    def test_entréficka_djup(self):
        """Entréficka ska vara 0,85 m djup"""
        self.assertAlmostEqual(ENTRÉ_DJUP, 0.85, delta=TOLERANCE)


class TestTrappMått(unittest.TestCase):

    def test_antal_uppsteg(self):
        """Antal uppsteg ska vara 12"""
        import math
        uppsteg = math.ceil(KLÄTTHÖJD / STEGHÖJD)
        self.assertEqual(uppsteg, 12,
            msg=f"Antal uppsteg: {uppsteg}, ska vara 12")

    def test_horisontell_längd(self):
        """Trappans horisontella längd = 12 × 24,5 cm = 2,94 m"""
        längd = 12 * STEGHÖJD
        self.assertAlmostEqual(längd, 2.94, delta=TOLERANCE,
            msg=f"Horisontell längd: {längd:.3f} m, ska vara 2,94 m")

    def test_trappglugg(self):
        """Trappglugg = 0,90 × (2,94 + 0,90) = 0,90 × 3,84 m"""
        glugg_längd = 12 * STEGHÖJD + KVARTSVARV
        self.assertAlmostEqual(glugg_längd, 3.84, delta=TOLERANCE,
            msg=f"Trappglugg längd: {glugg_längd:.3f} m, ska vara 3,84 m")
        self.assertAlmostEqual(TRAPPA_BREDD, 0.90, delta=TOLERANCE)

    def test_klätthöjd_uppbyggnad(self):
        """Klätthöjd = innerhöjd + loftbalk + golvregel + golv"""
        innerhöjd   = 2.350
        loftbalk    = 0.225
        golvregel   = 0.125
        golv        = 0.034
        total = innerhöjd + loftbalk + golvregel + golv
        self.assertAlmostEqual(total, KLÄTTHÖJD, delta=TOLERANCE,
            msg=f"Klätthöjd uppbyggnad: {total:.3f} m, ska vara {KLÄTTHÖJD:.3f} m")


class TestLoft(unittest.TestCase):

    def test_loft_bruttomått(self):
        """Loft brutto = 7,46 × 4,06 m = 30,3 m²"""
        area = LOFT_BREDD * LOFT_DJUP
        self.assertAlmostEqual(area, 30.3, delta=0.1,
            msg=f"Loft brutto: {area:.1f} m²")

    def test_loft_fri_golvyta(self):
        """Fri golvyta efter förvaring båda sidor"""
        fri_bredd = LOFT_BREDD - 2 * FÖRVARING_DJUP
        fri_yta = fri_bredd * LOFT_DJUP
        self.assertAlmostEqual(fri_bredd, 5.40, delta=TOLERANCE,
            msg=f"Fri loftbredd: {fri_bredd:.2f} m")

    def test_loft_netto(self):
        """Netto loftyta efter trappglugg"""
        fri_bredd = LOFT_BREDD - 2 * FÖRVARING_DJUP
        fri_yta = fri_bredd * LOFT_DJUP
        trappglugg = TRAPPA_BREDD * (12 * STEGHÖJD + KVARTSVARV)
        netto = fri_yta - trappglugg
        self.assertAlmostEqual(netto, 18.5, delta=0.2,
            msg=f"Netto loftyta: {netto:.1f} m²")


if __name__ == '__main__':
    unittest.main(verbosity=2)
