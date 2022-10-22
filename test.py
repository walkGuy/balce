__all__ = ['main']

from .core import *
from .parser import *

from fmat import *
from fmat.test import gt

from os import stat
# os.stat(filename).st_size

@bct(
	#cntlog=True,
	#ballog=True,
)
def main(print=gt.putout) :
	'''
	my_style = CreatePEP8Style(
		CONTINUATION_ALIGN_STYLE='VALIGN-RIGHT',
		CONTINUATION_INDENT_WIDTH=8,
		FORCE_MULTILINE_DICT=True,
		SPACE_BETWEEN_ENDING_COMMA_AND_CLOSING_BRACKET=False,
		SPLIT_ALL_COMMA_SEPARATED_VALUES=False,
		USE_TABS=True,
	)
	'''
	cesTest, memo_dir = (
		# Risteski I B. New very hard problems of balancing chemical reactions[J]. Chemistry, 2012, 21(4).
		'C₂₉₅₂H₄₆₆₄N₈₁₂O₈₃₂S₈Fe₄+Na₂C₄H₃O₄SAu+Fe(SCN)₂+(NH₄)₂Fe(SO₄)₂(H₂O)₆+C₄H₈SCl₂+MgC₈H₁₂N₂O₈ ==== MgC₅₅H₇₂N₄+Na₃⡀₉₉(Fe(CN)₆)+Au₀⡀₉₈₇C₆H₁₁O₅S+HClO₄+H₂S',
		#'CaBeAsSAtCsF₁₃+W₂Cl₈(NSeInCl₃)₂+Ca(GaH₂S₄)₂+(NH₄)₂MoO₄+K₄(Fe(CN)₆)+MgS₂O₃+Na₃PO₄+LaTlS₃+H₂CO₃+HoHS₄+CeCl₃+SnSO₄+ZrO₂+Cu₂O+Al₂O₃+Bi₂O₃+SiO₂+CdO+Au₂O+Hg₂S → P₄Mo₁₂O₄₀(NH₃)₃+LaHgTlZrS₆+CdIn₃CeCl₁₂+Na₂AuC₄H₃OS₇+KAu(CN)₂+MgFe₂(SO₄)₄+Sn₃Bi(AsO₄)₃At₃+CsCuCl₃+GaHoH₂S₄+SiN₂Se₆+CaAl₀⡀₉₇F₅+BeSiO₃+HClO+W₂O',
	  #'''7731000CaBeAsSAtCsF₁₃+ 1502160[Ru(C₁₀H₈N₂)₃]Cl₂·6H₂O+ 9273600W₂Cl₈(NSeInCl₃)₂+ 12369600Ca(GaH₂S₄)₂+ 1560720(NH₄)₂MoO₄+ 12054510K₄Fe(CN)₆+ 375540Na₂Cr₂O₇+ 6027255MgS₂O₃+ 37709196LaTlS₃+ 520240Na₃PO₄+ 751080Ag₂PbO₂+ 7731000SnSO₄+ 24739200HoHS₄+ 6182400CeCl₃+ 37709196ZrO₂+ 3865500Cu₂O+ 9748791Al₂O₃+ 1288500Bi₂O₃+ 10822200SiO₂+ 25438050Au₂O+ 12017280TeO₃+ 6182400CdO+ 18854598Hg₂S
			#→ 130060(NH₃)₃[(PO)₄·12MoO₃]+ 37709196LaHgTlZrS₆+ 6182400In₃CdCeCl₁₂+ 1502160AgRuAuTe₈+ 1155900C₄H₃AuNa₂OS₇+ 48218040KAu(CN)₂+ 6027255MgFe₂(SO₄)₄+ 2577000Sn₃(AsO₄)₃BiAt₃+ 7731000CuCsCl₃+ 24739200GaHoH₂S₄+ 3091200N₂SiSe₆+ 20100600CaAl₀⡀₉₇F₅+ 751080PbCrO₄+ 16332180H₂CO₃+ 7731000BeSiO₃+ 54000120HClO+ 9273600W₂O''',

		'4Au6.976577+8NaCN+2H2O+O2=4Na(Au6.976577(CN)2)+4NaOH',
		'MnO4^(-)+2SO3^(2-)+H^(+) → Mn^(2+)+SO4^(2-)+H2O',
		'P4+P2I4+H2O = PH4I+H3PO4',
		'K4Fe(CN)6+KMnO4+H2SO4==CO2+KNO3+H2O+K2SO4+MnSO4+Fe2(SO4)3',
		'Ru+Cl2+C5H4N+H2O = [Ru(C10H8N2)3]5Cl2·6.5H2O+Ru2.5',
		'3HClO3 → HClO4+ Cl2↑+ 2O2↑+ H2O',
		'KMnO4+H2O2+H2SO4 → K2SO4+MnSO4+O2+H2O',
		'MnO4^(-)+ H^(+)+ H2O2 = Mn2^(2+)+ O2+ H2O',
		'[Cr(N2H4CO)6]4[Cr(CN)6]3 + KMnO4+H2SO4 → K2Cr2O7 + MnSO4 + CO2 + KNO3 + K2SO4 + H2O',
		'''30448582 C2952H4664N812O832S8Fe4 + 10833308052 Na2C4H3O4SAu + 3899586588 Fe(SCN)2
			+ 1408848684 Fe(NH4)2(SO4)2∙6H2O + 5568665015C4H8Cl2S + 1379870764 C8H12MgN2O8
		→ 1379870764 C55H72MgN4 + 5430229600 Na3.99Fe(CN)6
			+ 10975996000 Au0.987SC6H11O5 + 11137330030 HClO4 + 16286436267 H2S''',
		'KClO3+ 6HCl → KCl+ 3Cl2↑+ 3H2O',
		'AlCl3+3NaOH=Al (OH)3↓+3NaCl',
	),  '/storage/emulated/0/.ChemicalEquationSolutions.dat'
	
	(print)(
		*cesTest,
		sep = '', end = '',
		func = lambda n : str([
			print(
				CEquation(n).check(),
				n[:16]+'...\n',
				(CEquation(n).balanced)(memo_dir), '\n',
				#' → {}k'.format(stat(memo_dir).st_size/1024)
			), '',
		].pop()),
	)
	
	print(
		#bct(ignore=True)(completeCE)('P4+P2I4+H2O+? = PH4I+?'),
		#CEquation('2NaN3===2Na+3?').completed(),
		#CEquation('KClO3 →MnO2&△→ KCl+ O2').balanced(),
		sep = '\n', end = '',
	)
	