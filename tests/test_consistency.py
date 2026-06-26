"""
Timmerhus — Konstruktionsdokument Konsistenstester v4.0
=======================================================
Kör med: python tests/test_consistency.py
"""

import unittest
import math

# ── Grunddata ────────────────────────────────────────────────────────────────
YTTERVÄGG   = 0.170
INNERVÄGG   = 0.150

YTTRE_LÄNGD = 9.00
YTTRE_BREDD = 8.00

INV_LÄNGD   = YTTRE_LÄNGD - 2 * YTTERVÄGG   # 8.66 m
INV_BREDD   = YTTRE_BREDD - 2 * YTTERVÄGG   # 7.66 m

# Längdkedja
STORSTUGA   = 4.03
HJÄRTVÄGG   = 0.17
UTILITIES   = 1.30
MASTER_DJUP = 3.01

# Breddkedja
ÖVRE_BLOCK  = 2.96
GÅNG        = 1.20
NEDRE_BLOCK = 3.20

# Rum
MASTER_BREDD = ÖVRE_BLOCK
BADRUM_B    = NEDRE_BLOCK
BADRUM_D    = 1.70
LILLA_B     = NEDRE_BLOCK
LILLA_D     = 2.21

# Trappa
TRAPPA_BREDD  = 1.00
STEGHÖJD      = 0.196
STEGLÄNGD     = 0.245
ANTAL_STEG    = 12
STEG_LYFTS    = 10
KVARTSVARV    = TRAPPA_BREDD
KLÄTTHÖJD     = 2.734

# Loft
LOFT_BREDD    = INV_BREDD
LOFT_DJUP     = 4.06
FÖRVARING_DJUP = 1.03

# Entréficka
ENTRÉ_BREDD   = 0.55 + GÅNG
ENTRÉ_DJUP    = 0.85

# Sängar
SÄNG_M_B = 1.60
SÄNG_M_L = 2.00
SÄNG_L_B = 0.80
SÄNG_L_L = 2.00

# Kök
KÖK_LÄNGD = 0.60 + 0.60 + 0.30 + 0.80 + 0.45 + 0.45  # 3.20 m

TOLERANCE = 0.005


class TestMåttkedjor(unittest.TestCase):

    def test_invändig_längd(self):
        self.assertAlmostEqual(INV_LÄNGD, 8.66, delta=TOLERANCE)

    def test_invändig_bredd(self):
        self.assertAlmostEqual(INV_BREDD, 7.66, delta=TOLERANCE)

    def test_längdkedja(self):
        summa = STORSTUGA + HJÄRTVÄGG + UTILITIES + INNERVÄGG + MASTER_DJUP
        self.assertAlmostEqual(summa, INV_LÄNGD, delta=TOLERANCE,
            msg=f"Längdkedja: {summa:.3f} m, ska vara {INV_LÄNGD:.3f} m")

    def test_breddkedja(self):
        summa = ÖVRE_BLOCK + INNERVÄGG + GÅNG + INNERVÄGG + NEDRE_BLOCK
        self.assertAlmostEqual(summa, INV_BREDD, delta=TOLERANCE,
            msg=f"Breddkedja: {summa:.3f} m, ska vara {INV_BREDD:.3f} m")

    def test_utilities_djup(self):
        self.assertAlmostEqual(UTILITIES, 1.30, delta=TOLERANCE)

    def test_master_djup(self):
        self.assertAlmostEqual(MASTER_DJUP, 3.01, delta=TOLERANCE)


class TestRumsAreaer(unittest.TestCase):

    def test_storstuga_area(self):
        area = INV_BREDD * STORSTUGA
        self.assertAlmostEqual(area, 30.9, delta=0.1)

    def test_master_area(self):
        area = MASTER_BREDD * MASTER_DJUP
        self.assertAlmostEqual(area, 8.9, delta=0.1)

    def test_badrum_area(self):
        area = BADRUM_B * BADRUM_D
        self.assertAlmostEqual(area, 5.4, delta=0.1)

    def test_lilla_sovrum_area(self):
        area = LILLA_B * LILLA_D
        self.assertAlmostEqual(area, 7.1, delta=0.1)


class TestTillgänglighet(unittest.TestCase):

    def test_gång_bredd(self):
        self.assertGreaterEqual(GÅNG, 1.20)

    def test_master_fri_sida_säng(self):
        fri_sida = MASTER_BREDD - SÄNG_M_B
        self.assertGreaterEqual(fri_sida, 0.90,
            msg=f"Master fri sida: {fri_sida:.2f} m")

    def test_master_fotända(self):
        fri_fotända = MASTER_DJUP - SÄNG_M_L
        self.assertGreaterEqual(fri_fotända, 1.00,
            msg=f"Master fotända: {fri_fotända:.2f} m")

    def test_master_garderober(self):
        garderob_yta = MASTER_DJUP - ENTRÉ_DJUP - INNERVÄGG - 1.00
        self.assertGreaterEqual(garderob_yta, 1.00,
            msg=f"Garderobsyta: {garderob_yta:.2f} m")

    def test_badrum_vändcirkel(self):
        self.assertGreaterEqual(BADRUM_B, 1.30)
        self.assertGreaterEqual(BADRUM_D, 1.30)

    def test_lilla_sovrum_fri_yta(self):
        fri_bredd = LILLA_B - SÄNG_L_B
        self.assertGreaterEqual(fri_bredd, 1.30,
            msg=f"Lilla sovrum fri bredd: {fri_bredd:.2f} m")

    def test_entréficka(self):
        self.assertAlmostEqual(ENTRÉ_BREDD, 1.75, delta=TOLERANCE)
        self.assertAlmostEqual(ENTRÉ_DJUP, 0.85, delta=TOLERANCE)


class TestKök(unittest.TestCase):

    def test_kök_längd(self):
        self.assertAlmostEqual(KÖK_LÄNGD, 3.20, delta=TOLERANCE,
            msg=f"Kök längd: {KÖK_LÄNGD:.3f} m, ska vara 3,20 m")

    def test_kök_ryms_i_nedre_blocket(self):
        self.assertLessEqual(KÖK_LÄNGD, NEDRE_BLOCK + TOLERANCE)


class TestTrappMått(unittest.TestCase):

    def test_steghöjd(self):
        beräknad = 2.35 / 12
        self.assertAlmostEqual(beräknad, STEGHÖJD, delta=0.001)

    def test_horisontell_längd(self):
        längd = ANTAL_STEG * STEGLÄNGD
        self.assertAlmostEqual(längd, 2.94, delta=TOLERANCE)

    def test_lyfthöjd(self):
        lyfthöjd = STEG_LYFTS * STEGLÄNGD
        self.assertAlmostEqual(lyfthöjd, 2.45, delta=TOLERANCE)

    def test_fri_gånghöjd(self):
        fri_höjd = STEG_LYFTS * STEGHÖJD
        self.assertGreaterEqual(fri_höjd, 1.90,
            msg=f"Fri gånghöjd: {fri_höjd:.3f} m")

    def test_trappglugg(self):
        glugg_längd = ANTAL_STEG * STEGLÄNGD + KVARTSVARV
        self.assertAlmostEqual(glugg_längd, 3.94, delta=TOLERANCE)

    def test_klätthöjd_uppbyggnad(self):
        total = 2.350 + 0.225 + 0.125 + 0.034
        self.assertAlmostEqual(total, KLÄTTHÖJD, delta=TOLERANCE)

    def test_trappvikt(self):
        densitet = 500
        steg_vikt = ANTAL_STEG * (TRAPPA_BREDD * STEGLÄNGD * 0.045) * densitet
        vagnstycke_längd = math.sqrt(2.94**2 + 2.156**2)
        vagnstycke_vikt = 2 * (0.051 * 0.254 * vagnstycke_längd) * densitet
        total = steg_vikt + vagnstycke_vikt + 15
        self.assertLess(total, 150, msg=f"Trappvikt: {total:.0f} kg")


class TestLoft(unittest.TestCase):

    def test_loft_bruttomått(self):
        area = LOFT_BREDD * LOFT_DJUP
        self.assertAlmostEqual(area, 31.1, delta=0.2)

    def test_loft_fri_golvyta(self):
        fri_bredd = LOFT_BREDD - 2 * FÖRVARING_DJUP
        self.assertAlmostEqual(fri_bredd, 5.60, delta=TOLERANCE)

    def test_loft_netto(self):
        fri_bredd = LOFT_BREDD - 2 * FÖRVARING_DJUP
        fri_yta = fri_bredd * LOFT_DJUP
        trappglugg = TRAPPA_BREDD * (ANTAL_STEG * STEGLÄNGD + KVARTSVARV)
        netto = fri_yta - trappglugg
        self.assertAlmostEqual(netto, 18.8, delta=0.3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
