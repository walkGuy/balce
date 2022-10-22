__all__ = [
	'completeCE'
]

from .parser import *
from .contexts import bct

from fmat import *

def analysisCE(formula) :
	'''Analysis a chemical equation.
	Should enter a chemical equation.
	'''
	leles, conf, reles = splitCE(
		formatCE(formula, to_nor=True, compact=True),
		to_mal=True, with_stoi=True
	)

	_get = \
		[countEle(i, True) for i in leles] + \
		[{i: j if i=='?' else -j for i,j in countEle(i, True).items()} for i in reles]
	
	s = {}
	for i in _get :
		for j,k in i.items() :
			try : s[j] += k
			except : s[j] = k
	
	return leles, conf, reles, sorted(s.keys()), s, _get
	
def completeCE(formula, to_nor=False) :
	if not bct.ignore :
		raise NotImplementedError('Someday it will be completed, just not yet :)  → %s' % formula)
	
	'''This function can complete a chemical equation.
	The smart algorithm let it work well.
	
	It is easy to use. Only need to set the character `?` to
		the chemical equation, like Mg+O2→MgO2 to Mg+?→MgO2.
	The smart algorithm will solve that system automatically,
		and if system is unsolvable, the algorithm will raise 
		the SystemError.
	Sometime the system has more than 1 solution, but the
		complete algorithm usually finds the best one.
		
	Examples
	>>> from balce import *
	
	>>> completeCE('Mg+? → MgO2', to_nor=True)
	Mg+ O2 → MgO2
	
		Suppose not only 1 unknown
		
	>>> completeCE('Mg+? → MgO2', to_nor=True)
	
	
	'''
	leles, conf, reles, toeles, still, vars = analysisCE(formula)
	print(still, vars, sep='\n')
	return leles, conf, reles, toeles
	