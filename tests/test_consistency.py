"""Timmerhus Konsistenstester v4.1"""
import unittest, math

YTTERVÄGG=0.170; INNERVÄGG=0.150
YTTRE_LÄNGD=9.00; YTTRE_BREDD=8.00
INV_LÄNGD=YTTRE_LÄNGD-2*YTTERVÄGG; INV_BREDD=YTTRE_BREDD-2*YTTERVÄGG
STORSTUGA=4.03; HJÄRTVÄGG=0.17; UTILITIES=1.30; MASTER_DJUP=3.01
ÖVRE_BLOCK=2.96; GÅNG=1.20; NEDRE_BLOCK=3.20
MASTER_BREDD=ÖVRE_BLOCK; BADRUM_B=NEDRE_BLOCK; BADRUM_D=1.70
LILLA_B=NEDRE_BLOCK; LILLA_D=2.21
TRAPPA_BREDD=1.00; STEGHÖJD=0.196; STEGLÄNGD=0.245
ANTAL_STEG=12; STEG_LYFTS=10; KVARTSVARV=TRAPPA_BREDD; KLÄTTHÖJD=2.734
LOFT_BREDD=INV_BREDD; LOFT_DJUP=4.06; FÖRVARING_DJUP=1.03
ENTRÉ_BREDD=0.55+GÅNG; ENTRÉ_DJUP=0.85
SÄNG_M_B=1.60; SÄNG_M_L=2.00; SÄNG_L_B=0.80
KÖK_LÄNGD=0.60+0.60+0.30+0.80+0.45+0.45
HÄVARM=1.30; FJÄDRAR=3; FJÄDER_KRAFT=45
TOLERANCE=0.005

class TestMåttkedjor(unittest.TestCase):
    def test_invändig_längd(self): self.assertAlmostEqual(INV_LÄNGD,8.66,delta=TOLERANCE)
    def test_invändig_bredd(self): self.assertAlmostEqual(INV_BREDD,7.66,delta=TOLERANCE)
    def test_längdkedja(self):
        s=STORSTUGA+HJÄRTVÄGG+UTILITIES+INNERVÄGG+MASTER_DJUP
        self.assertAlmostEqual(s,INV_LÄNGD,delta=TOLERANCE,msg=f"Längdkedja: {s:.3f}")
    def test_breddkedja(self):
        s=ÖVRE_BLOCK+INNERVÄGG+GÅNG+INNERVÄGG+NEDRE_BLOCK
        self.assertAlmostEqual(s,INV_BREDD,delta=TOLERANCE,msg=f"Breddkedja: {s:.3f}")
    def test_utilities_djup(self): self.assertAlmostEqual(UTILITIES,1.30,delta=TOLERANCE)
    def test_master_djup(self): self.assertAlmostEqual(MASTER_DJUP,3.01,delta=TOLERANCE)

class TestRumsAreaer(unittest.TestCase):
    def test_storstuga(self): self.assertAlmostEqual(INV_BREDD*STORSTUGA,30.9,delta=0.1)
    def test_master(self): self.assertAlmostEqual(MASTER_BREDD*MASTER_DJUP,8.9,delta=0.1)
    def test_badrum(self): self.assertAlmostEqual(BADRUM_B*BADRUM_D,5.4,delta=0.1)
    def test_lilla(self): self.assertAlmostEqual(LILLA_B*LILLA_D,7.1,delta=0.1)

class TestTillgänglighet(unittest.TestCase):
    def test_gång(self): self.assertGreaterEqual(GÅNG,1.20)
    def test_master_sida(self): self.assertGreaterEqual(MASTER_BREDD-SÄNG_M_B,0.90)
    def test_master_fotända(self): self.assertGreaterEqual(MASTER_DJUP-SÄNG_M_L,1.00)
    def test_master_garderober(self): self.assertGreaterEqual(MASTER_DJUP-ENTRÉ_DJUP-INNERVÄGG-1.00,1.00)
    def test_badrum_vändcirkel(self): self.assertGreaterEqual(BADRUM_B,1.30); self.assertGreaterEqual(BADRUM_D,1.30)
    def test_lilla_fri_yta(self): self.assertGreaterEqual(LILLA_B-SÄNG_L_B,1.30)
    def test_entréficka(self): self.assertAlmostEqual(ENTRÉ_BREDD,1.75,delta=TOLERANCE); self.assertAlmostEqual(ENTRÉ_DJUP,0.85,delta=TOLERANCE)

class TestKök(unittest.TestCase):
    def test_längd(self): self.assertAlmostEqual(KÖK_LÄNGD,3.20,delta=TOLERANCE)
    def test_ryms(self): self.assertLessEqual(KÖK_LÄNGD,NEDRE_BLOCK+TOLERANCE)

class TestTrappMått(unittest.TestCase):
    def test_steghöjd(self): self.assertAlmostEqual(2.35/12,STEGHÖJD,delta=0.001)
    def test_horisontell(self): self.assertAlmostEqual(ANTAL_STEG*STEGLÄNGD,2.94,delta=TOLERANCE)
    def test_lyfthöjd(self): self.assertAlmostEqual(STEG_LYFTS*STEGLÄNGD,2.45,delta=TOLERANCE)
    def test_fri_höjd(self): self.assertGreaterEqual(STEG_LYFTS*STEGHÖJD,1.90)
    def test_glugg(self): self.assertAlmostEqual(ANTAL_STEG*STEGLÄNGD+KVARTSVARV,3.94,delta=TOLERANCE)
    def test_klätthöjd(self): self.assertAlmostEqual(2.350+0.225+0.125+0.034,KLÄTTHÖJD,delta=TOLERANCE)
    def test_vikt(self):
        steg=ANTAL_STEG*(TRAPPA_BREDD*STEGLÄNGD*0.045)*500
        vagn=2*(0.051*0.254*math.sqrt(2.94**2+2.156**2))*500
        self.assertLess(steg+vagn+15,150)

class TestLyftsystem(unittest.TestCase):
    def test_lyftkraft(self):
        kraft=FJÄDRAR*FJÄDER_KRAFT
        self.assertGreaterEqual(kraft,128,msg=f"Lyftkraft: {kraft} kg")
    def test_restvikt(self):
        restvikt=FJÄDRAR*FJÄDER_KRAFT-128
        self.assertGreater(restvikt,0,msg="Trappan måste ligga kvar nere")
        self.assertLess(restvikt,30,msg=f"Restvikt {restvikt} kg — för tung att lyfta")
    def test_vajerlängd(self):
        längd=STEG_LYFTS*STEGLÄNGD*2
        self.assertAlmostEqual(längd,4.90,delta=0.05)
    def test_hävarm(self): self.assertAlmostEqual(HÄVARM,1.30,delta=TOLERANCE)

class TestLoft(unittest.TestCase):
    def test_brutto(self): self.assertAlmostEqual(LOFT_BREDD*LOFT_DJUP,31.1,delta=0.2)
    def test_fri_bredd(self): self.assertAlmostEqual(LOFT_BREDD-2*FÖRVARING_DJUP,5.60,delta=TOLERANCE)
    def test_netto(self):
        fri=(LOFT_BREDD-2*FÖRVARING_DJUP)*LOFT_DJUP
        glugg=TRAPPA_BREDD*(ANTAL_STEG*STEGLÄNGD+KVARTSVARV)
        self.assertAlmostEqual(fri-glugg,18.8,delta=0.3)

if __name__=='__main__': unittest.main(verbosity=2)
