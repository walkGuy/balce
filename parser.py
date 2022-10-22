__all__ = [
	'SubscriptTable',
	'toSubscript',
	'sreSubscript',
	
	'SuperscriptTable',
	'stoSuperscript',
	'sreSuperscript',
	
	'splitCE',
	'formatNum',
	'formatEle',
	'formatCE',
	'countEle'
]

SubscriptTable = '₀₁₂₃₄₅₆₇₈₉⡀' # The `⡀` cannot be matched by `\w` ...
SubscriptDict = {
	i: j for i, j in zip(
		'0123456789.'+SubscriptTable,
		SubscriptTable+'0123456789.')
}

SuperscriptTable = '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⠂'
SuperscriptDict = {
	i: j for i, j in zip(
		'0123456789+-.'+SuperscriptTable,
		SuperscriptTable+'0123456789+-.')
}

def toSubscript(n: int or float or str)-> str :
	'''To translate a number to a unicode subscript str'''
	#return ''.join(SubscriptTable[10 if '.' in i else int(i)] for i in str(n))
	return ''.join(map(SubscriptDict.__getitem__, str(n)))

def sreSubscript(n: str)-> str :
	'''Return a subscript char'''
	#return ''.join('.' if SubscriptTable[10] in i else str(SubscriptTable.index(i)) for i in n)
	return ''.join(map(SubscriptDict.__getitem__, n))

def stoSuperscript(n: str)-> str :
	'''str(12.3+) -> ¹²⠂³⁺'''
	#return ''.join([SuperscriptTable[12 if '.' in i else int(i)] for i in n.strip('+-')] + [SuperscriptTable[10 if '+' in n else 11]])
	return ''.join(map(SuperscriptDict.__getitem__, n))
	
def sreSuperscript(n: str)-> str :
	'''¹²⠂³⁺ -> str(12.3+)'''
	if not n : return ''
	#return ''.join('.' if SuperscriptTable[12] in i else str(SuperscriptTable.index(i)) for i in n.strip('⁺⁻')) + ('+' if SuperscriptTable[10] in n else '-')
	return ''.join(map(SuperscriptDict.__getitem__, n))

from re import (
	compile as reCOMPILE,
	match   as reMATCH
)

_CHEMICAL_EQUATION_SPLIT = reCOMPILE(
	# To check `=`,`==`,`====` and `=???=` or `→` even `→???→` which `⇋⇌↔⇄⇆⇔`, etc.
	r'({0}{{2,}}|{0}.+?{0}|{0}+)'.format('[=←→⟶⇋⇌↔⇄⇆⇔≜]')
)

__CM_FORMAT_WS_REGEX_STRING = \
	r'[\w\[(⡀.·⠂)\]⁺⁻↑↓?]+(?:\^\(?[\d.]*[+-]\)?)?(?:\(?[a-z]+\)?)?'
_CHEMICAL_MATERIAL_FORMAT_WS = reCOMPILE(
	__CM_FORMAT_WS_REGEX_STRING)
_CHEMICAL_MATERIAL_FORMAT_WOS = reCOMPILE(
	r'(?![\d.])' + __CM_FORMAT_WS_REGEX_STRING)
	
# This got more useful.
_COEFFICIENT_FORMAT_NOR = reCOMPILE(
	r'(?<=[A-Za-z(\[\])_])[\d.]+')
_EXPONENT_FORMAT_NOR = reCOMPILE(
	r'\^\(?(?P<exp>[\d.]*[+-])\)?')

# Do not use it except at formatting.
_COEFFICIENT_FORMAT_UNI = reCOMPILE(
	SubscriptTable.join('[]') + '+')
_EXPONENT_FORMAT_UNI = reCOMPILE(
	SuperscriptTable.join('[]') + '+')
	
_COUNT_ELEMENT_NOR = reCOMPILE(
	r'([A-Z?][a-z]?)([\d.]*)|([\[(])|([)\]])([\d.]*)')

def splitCE(formula, to_mal=False, with_stoi=False) :
	'''获得化学式的左右两边和反应条件
	to_mal: bool，False仅划分条件和两边，True精确到两边每个物质，记为list返回
	with_stoi: bool，是否在to_mal时带化学计量数
	'''
	left, conf, right = _CHEMICAL_EQUATION_SPLIT.split(
		''.join(formula.split()), # To clear air chars
		maxsplit = 1
	)

	if to_mal :
		left, right = (
			_CHEMICAL_MATERIAL_FORMAT_WS.findall(left),
				_CHEMICAL_MATERIAL_FORMAT_WS.findall(right)) \
			if with_stoi else (
			_CHEMICAL_MATERIAL_FORMAT_WOS.findall(left),
				_CHEMICAL_MATERIAL_FORMAT_WOS.findall(right))

	return left, conf, right

def formatEle(ele, to_nor=False) :
	'''单个化学式unicode上下标规范与普通规范的转换
	ele: str - 要转换的化学式
	to_nor: bool - True转成普通规范, False转成unicode上下标规范
		如果为2, 则使用element^exponent而非element^(exponent)
	'''
	ele = \
	 ele.replace('**', '^').replace('_', '') \
		.replace('∙', '·') \
		.replace('⋅', '·') \
		.replace('ㆍ', '·') \
		.replace('・', '·') \
		.replace('･', '·') \
		.replace('•', '·') \
		.replace('‧', '·') \
		.replace('・', '·') \
		.replace('●', '·')
	
	if to_nor :
		return _COEFFICIENT_FORMAT_UNI.sub(
			lambda n : sreSubscript(n.group()),
			_EXPONENT_FORMAT_UNI.sub(
				lambda n : ('^%s ' if to_nor==2 else '^(%s)') % sreSuperscript(n.group()),
				ele))
	else :
		return _COEFFICIENT_FORMAT_NOR.sub(
			lambda n : toSubscript(n.group()), # to match a single material
			_EXPONENT_FORMAT_NOR.sub(
				lambda n : stoSuperscript(n.group('exp')),
				ele)) # to match ele^(xx+-)/xx+- and change that to ele superscript

def formatCE(formula, to_nor=False, compact=False) :
	'''化学方程式unicode上下标式规范与普通规范的转换
	formula: str - 要转换的方程式
	to_nor: bool - True转成普通规范, False转成unicode上下标规范
	compact: bool - False在加号后添空格，True不添
	'''
	l, conf, r = splitCE(formula)

	if compact :
		return ' '.join(
			(formatEle(l, to_nor), conf, formatEle(r, to_nor))
		)
	else :
		left, right = \
			formatEle(l).replace('+', '+ '), formatEle(r).replace('+', '+ ')
		if to_nor :
			left, right = \
				formatEle(left, to_nor), formatEle(right, to_nor)

		return ' '.join((left, conf, right))

from decimal import Decimal

def formatNum(n) :
	if type(n) is not str :
		n = str(n)
	try :
		return int(n)
	except :
		return Decimal(n)

def countEle(ele, with_stoi=False) :
	'''统计 (NH3)3[(PO)4·12MoO3·2NH3]5·3H2O^(4+)↑ 等等单个化学式的元素数、电子数等
	参考：https://blog.csdn.net/qq_41314786/article/details/104835495?spm=1001.2101.3001.6650.9
	'''
	def getExp(n: str)-> int :
		'''str("12.3-") -> formatNum("-12.3")'''
		if n in '+-' :
			return (int(n in '+') << 1) - 1
		return formatNum(n[-1]+n[:-1])
	
	def handleDot(ele) :
		'''To turn  `Al·2H2O·3MoO3` into `Al(H2O)2(MoO3)3`'''
		if '·' not in ele :
			return ele
			
		new, dep, deps = ele, 0, [[]]
		for i,j in enumerate(ele) :
			if j in '([' :
				dep = dep + 1
				deps.append([])

			elif j in ')]' :
				dep = dep - 1
				
			if '·' == j :
				# three elements
				# start, coefficient, whole to change chunk - position
				deps[dep].append([i, i+1, i])
			
			if deps[dep] :
				deps[dep][-1][2] = i+1
				if ele[deps[dep][-1][1]] in '0123456789.' :
					deps[dep][-1][1] = i+1
			
		for i in deps :
			for j,k,u in i :
				new = new.replace(
					ele[j:u],
					'({}){}'.format(ele[k:u], ele[j+1:k]),
					1
				)
		return new
	
	_exp = _EXPONENT_FORMAT_NOR.search(ele)
	#ele = (ele.replace(_exp.group(), '') if _exp else ele).replace('↑', '').replace('↓', '')
	ele = ele[:ele.find('^')] if _exp else ele.replace('↑', '').replace('↓', '')
	
	stacks = [{'e': (getExp(_exp.group('exp')) if _exp else 0)}]
	for element, suffix, parL, parR, parSuffix in _COUNT_ELEMENT_NOR.findall(handleDot(ele)) :
		if parL : # 进栈
			stacks.append({})
		elif parR : # 出栈
			parSuffix = formatNum(parSuffix) if parSuffix else 1
			for k,v in stacks.pop().items() :
				stacks[-1][k] = stacks[-1].get(k, 0) + v*parSuffix
		else :
			stacks[-1][element] = stacks[-1].get(element, 0) + (formatNum(suffix) if suffix else 1)
			
	if with_stoi :
		coef_term = reMATCH(r'[\d.]+', ele)
		coef_term = formatNum(coef_term.group()) if coef_term else 1
		for k in stacks[-1] :
			stacks[-1][k] *= coef_term
			
	return dict(sorted(stacks.pop().items(), key=lambda n:-n[1]))
