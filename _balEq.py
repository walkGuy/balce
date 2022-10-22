'''
Name : 化学方程式的配平
Author : Baolin Liao
Date : 2022/02/16 14:09

[输入]
化学方程式的格式与化学课本里的基本相同，详细描述如下：
	* 化学方程式由左右两个表达式组成，中间用至少1个等号=、中间带反应条件的2个等号、右箭头→或双向箭头⇋⇌↔⇄⇆⇔隔开
	 - 如：Mg+O2=△=MgO2，Mg+O2==MgO2, Mg+O2→MgO2
	* 表达式由若干部分组成，每部分由整数或空串与化学式组成，部分之间用加号+连接
	 - 如：2Mg+O2，MgO2
	* 化学式由若干部分构成，每部分顺次由项、系数、价数和0至1个上下箭头↑↓构成，部分之间直接连接
	 - 项是元素或以左右圆括号()或左右方括号[]括起来的或用间隔号·连接的化学式，如[Ru(C10H8N2)3]Cl2·6H2O
	 - 系数可以是一个整数，小数，unicode下标或空串
	 - 价数可用以下两种形式描述：
		· 异或符^或两个连续星号**与左右圆括号()括起来的整数、小数或空串与1个正负号+-的组合的组合
		· Unicode上标
	 - 如：MgO3.99, MgO₂；SO4.5²⁻, SO₄**(3.2-), SO₄²⁻, OH⁻, OH^(-)↑；Ca(OH)2, H(SO₄)₂⡀₉⁴⁻↓
	
[输出]
输出时默认会自动规范成unicode上下标形式
Example: 
>>> Mg+O2=点燃=MgO
2Mg+O₂=点燃=2MgO

[使用]
提供了一个函数balanceCE(formula, uni_form=True, memorization=None)，返回配平后的化学方程式
参数：
	* formula : str, 要配平的化学方程式
	* uni_form : bool, 是否自动优化成unicode上下标
	* memorization : str, 记忆化所用的文件，默认不记忆化
'''
import warnings
warnings.warn('from balce._balEq import * is deprecated with bugs on. Use from balce import * instead.',
			DeprecationWarning, 2)

from fmat import *
import re

SubscriptTable = '₀₁₂₃₄₅₆₇₈₉⡀' # even using `⡀` and not `ˎ` such is `⡀` cannot be matched by `\w` ...
SubscriptDict = {i: j for i, j in zip('0123456789.', SubscriptTable)}
SubscriptDicti = {j: i for i, j in SubscriptDict.items()}

def toSubscript(n: int or float or str)-> str :
	'''To translate a number to a unicode subscript str'''
	#return ''.join(SubscriptTable[10 if '.' in i else int(i)] for i in str(n))
	return ''.join(SubscriptDict[i] for i in str(n))

def sreSubscript(n: str)-> str :
	'''Return a subscript char'''
	#return ''.join('.' if SubscriptTable[10] in i else str(SubscriptTable.index(i)) for i in n)
	return ''.join(SubscriptDicti[i] for i in n)

SuperscriptTable = '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⠂'
SuperscriptDict = {i: j for i, j in zip('0123456789+-.', SuperscriptTable)}
SuperscriptDicti = {j: i for i, j in SuperscriptDict.items()}

def stoSuperscript(n: str)-> str :
	'''str(12.3+) -> ¹²⠂³⁺'''
	#return ''.join([SuperscriptTable[12 if '.' in i else int(i)] for i in n.strip('+-')] + [SuperscriptTable[10 if '+' in n else 11]])
	return ''.join(SuperscriptDict[i] for i in n)
	
def sreSuperscript(n: str)-> str :
	'''¹²⠂³⁺ -> str(12.3+)'''
	if not n : return ''
	#return ''.join('.' if SuperscriptTable[12] in i else str(SuperscriptTable.index(i)) for i in n.strip('⁺⁻')) + ('+' if SuperscriptTable[10] in n else '-')
	return ''.join(SuperscriptDicti[i] for i in n)

def splitCE(formula, to_mal=False, with_stoi=False) :
	'''获得化学式的左右两边和反应条件
	to_mal: bool，False仅划分条件和两边，True精确到两边每个物质，记为list返回
	with_stoi: bool，是否在to_mal时带化学计量数
	'''
	left, conf, right = re.split(
		r'({0}{1}|{0}.+?{0}|{0}+)'.format('[=←→⇋⇌↔⇄⇆⇔]', '{2,}'), # To check `=`,`==`,`====` and `=???=` or `→` even `→???→` which `⇋⇌↔⇄⇆⇔`, etc.
		''.join(formula.split()), # To clear air chars
		maxsplit = 1
	)

	if to_mal :
		seeEachCF = re.compile(r'{}[\w\[(⡀.·⠂)\]⁺⁻↑↓]+(?:\^\([\d.]*[+-]\))?'.format('' if with_stoi else '(?![\d.])'))
		left, right = seeEachCF.findall(left), seeEachCF.findall(right)	

	return left, conf, right		

def formatEle(ele, to_nor=False) :
	'''单个化学式unicode上下标规范与普通规范的转换
	ele: str - 要转换的化学式
	to_nor: bool - True转成普通规范, False转成unicode上下标规范
	'''
	# to, be used while not to_nor
	def rcstoSubscript(n) :
		return re.sub(r'[\d.]+', 
			lambda n : toSubscript(n.group()), n.group())

	def rcstoSuperscript(n) :
		digit = re.search(r'[\d.]*[+-]', n.group()).group()
		return stoSuperscript(digit)	

	# re, be used while to_nor
	rreSubscript = lambda n : sreSubscript(n.group())
	rcreSuperscript = lambda n : '^(%s)' % sreSuperscript(n.group())
	
	ele = re.sub(r'[∙⋅ㆍ・･•‧・●]', '·', ele.replace('**', '^'))
	
	if to_nor :
		return re.sub(r'[{}]+'.format(SubscriptTable), rreSubscript,
			re.sub(r'[{}]+'.format(SuperscriptTable), rcreSuperscript, ele))
	else :
		return re.sub(r'(?![\d.])[\w\[()\].]+', rcstoSubscript, # to match a single material
			re.sub(r'\^\([\d.]*[+-]\)', rcstoSuperscript, ele)) # to match ele^(xxx) and change that to ele superscript

def formatCE(formula, to_nor=False, compact=False) :
	'''化学方程式unicode上下标式规范与普通规范的转换
	formula: str - 要转换的方程式
	to_nor: bool - True转成普通规范, False转成unicode上下标规范
	compact: bool - True在加号后添空格，False不添
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
				formatEle(left, True), formatEle(right, True)

		return ' '.join((left, conf, right))

from collections import Counter

def countEle(ele, with_stoi=False) :
	'''统计 (NH3)3[(PO)4·12MoO3(NH3)2]5((H2)3)2·6H2O^(+)↑ 等等单个化学式的元素数、电子数等
	参考：https://dwz.mk/fUNvQ3
	'''
	def getExp(n: str)-> int :
		'''str("12.3-") -> toC("-12.3")'''
		isPos = (int('+' in n) << 1) - 1
		if n in '+-' :
			return isPos
		return toC(''.join(str(i) for i in n.strip('+-')))*isPos
			
	def handleDot(ele) :
		if '·' not in ele :
			return ele
		new = ele
		dep = maxdep = 1
		for i in ele :
			dep = dep+int(i in '([')-int(i in ')]')
			maxdep = max(dep, maxdep)
		for depth in range(maxdep) :
			coe, toRepl, repled = [], [], []
			lastdep = dep = 0
			bhDot = bhLetter = False
			onDepth = True
			for i, j in enumerate(ele) :
				dep = dep+int(j in '([')-int(j in ')]')
				if dep >= depth and onDepth:
					if dep == depth and j == '·' :
						coe.append('')
						toRepl.append('')
						repled.append('')
						bhDot = True
						bhLetter = False
					if bhDot :
						toRepl[-1] += j
						if j.isalpha() :
							bhLetter = True
					if bhLetter :
						repled[-1] += j
					elif bhDot and (j.isdigit() or j == '.') :
						coe[-1] += j
				if dep < depth and lastdep < depth  :
					bhDot = bhLetter = onDepth = False
				elif dep > lastdep and dep == depth :
					onDepth = True
				lastdep = dep
			for i, j, k in zip(coe, toRepl, repled) :
				new = new.replace(j, '({}){}'.format(k, i))
		return new
	
	_exp = re.search(r'(?<=\^\()[\d.]*[+-](?=\))', ele)
	expCnt = Counter({'e': (getExp(_exp.group()) if _exp else 0)})
	
	stacks = [expCnt]
	for element, suffix, parL, parR, parSuffix in re.findall(r'([A-Z][a-z]?)([\d.]*)|([\[(])|([)\]])([\d.]*)', handleDot(re.sub(r'\^\([\d.]*[+-]\)|[↑↓]', '', ele))) :
		if parL:  # 进栈
			stacks.append(Counter())
		elif parR:  # 出栈
			t = stacks.pop()
			for k in t.keys() :
				if parSuffix :
					t[k] *= toC(parSuffix)
			stacks[-1] += t
		else:
			stacks[-1][element] += toC(suffix) if suffix else 1
	
	if with_stoi :
		coef_term = re.match(r'[\d.]+', ele)
		coef_term = toC(coef_term.group()) if coef_term else 1
		for k in stacks[-1] :
			stacks[-1][k] *= coef_term
			
	return stacks.pop()
	
from itertools import chain	

from json import load, dump
from os.path import getsize as filesize, isfile

def balanceCE(formula, uni_form=True, memorization=None) :
	def analysisCE(formula, with_stoi=False) :
		'''解析方程式
		得到左右两边所有物质,列出元素个数矩阵
		See https://www.zhihu.com/answer/157207788
		* 注: 己归边,即x=y -> x-y=0(给右项系数取反)
		'''
		leles, conf, reles = splitCE(
			formatCE(formula, to_nor=True, compact=True),
			to_mal=True, with_stoi=with_stoi
		)
	
		_get = \
			[countEle(i, with_stoi) for i in leles] + \
			[{k: -v for k,v in countEle(i, with_stoi).items()} for i in reles]
		_find_toeles = sorted(set(chain(*[i.keys() for i in _get])))	
		
		elesMat = Mat([
			[
				dict.get(toele, 0)
				for dict in _get
			]
			for toele in _find_toeles
		])
	
		return leles, conf, reles, elesMat
		
	def getCoes(m: Mat)-> list :
		'''取出零空间矩阵里的系数'''
		return [str(toC(str(i))) for i in m]

	def interCoeEle(coes: list, eles: list)-> list :
		'''input: (['1', '6', '7'], ['H', 'CO', 'Mg'])
		output: ['H', '6CO', '7Mg']
		'''
		return [j if '1'==i else i+j for i,j in zip(coes, eles)]	

	def isallpos(n) :
		try :
			for i in n :
				if i <= 0 :
					return False
		except :
			for i in n :
				if toC(i) <= 0 :
					return False
		return True

	CENoSolutions, CENoData = 2832, 7627
	
	def setData(left: list, right: list, bleft=CENoSolutions, bright=CENoSolutions) :
		if not memorization : return
		with open(memorization, 'r+') as df :
			if filesize(memorization) > 3145728 : df.truncate()
			try :
				data = load(df)
				data['+'.join(left+['=']+right)] = (bleft, bright)
				df.seek(0)
			except :
				df.seek(0)
				df.truncate()
				data = {'+'.join(left+['=']+right): (bleft, bright)}
			dump(data, df, indent='\t')
				
	def getData(left, right) :
		if not memorization : return
		try :
			with open(memorization, 'r') as df :
				data = load(df).get('+'.join(left+['=']+right))
				if CENoSolutions not in data :
					return data
		except :
			if not isfile(memorization) :
				with open(memorization, 'x') : ...
		return
		
	leles, conf, reles, elesMat = analysisCE(formula)
	
	redata = getData(leles, reles)
	if redata :
		return formatCE(conf.join(redata), not uni_form)
	
	solution_null = elesMat.nullspace() # 得到零空间基
	if len(solution_null) > 1 : # 多组基
		combination = solution_null.pop()
		while solution_null :
			combination.colinsert(solution_null.pop())
		
		try :
			_, vals = Mat.ones(1, combination.cols).branch_bound(-combination, -Mat.ones(1, combination.rows))
			combination = sum(combination.col(i)*vals.get(i+1, 0) for i in range(combination.cols))
		except :
			setData(leles, reles)
			raise SystemError('Please make sure your chemical equation is solvable!')

		combination = ratioSimp(combination, True)
		coes = getCoes(combination)
		if not isallpos(coes) :
			setData(leles, reles)
			raise SystemError('Please make sure your chemical equation is solvable!')

	elif solution_null : # 唯一
		coes = getCoes(solution_null.pop())

	else : # 无解
		setData(leles, reles)
		raise SystemError('Please check your chemical formula. No solution system!')
	
	elenl = len(leles)
	left = '+'.join(interCoeEle(coes[: elenl], leles))
	right = '+'.join(interCoeEle(coes[elenl: ], reles))	

	setData(leles, reles, left, right)
	
	return formatCE(conf.join((left, right)), not uni_form)

def completeCE(formula) :
	def analysisCE(formula, with_stoi=False) :
		'''解析方程式
		得到左右两边所有物质,列出元素个数矩阵
		See https://www.zhihu.com/answer/157207788
		* 注: 己归边,即x=y -> x-y=0(给右项系数取反)
		'''
		leles, conf, reles = splitCE(
			formatCE(formula, to_nor=True, compact=True),
			to_mal=True, with_stoi=with_stoi
		)
	
		_get = \
			[countEle(i, with_stoi) for i in leles] + \
			[{k: -v for k,v in countEle(i, with_stoi).items()} for i in reles]
		_find_toeles = sorted(set(chain(*[i.keys() for i in _get])))	
		
		elesMat = Mat([
			[
				dict.get(toele, 0)
				for dict in _get
			]
			for toele in _find_toeles
		])
	
		return leles, conf, reles, elesMat
		
	leles, conf, reles, emat = analysisCE(formula, True)
	s = sum(emat.col(i) for i in range(emat.cols))
	print(s)
	...

				
class ChemEq(object) :
	def __init__(self, eq, form='uni') :
		self.__ce, self.form = eq, form		

	def split(self, to_mal=False, with_stoi=False) :
		return splitCE(self.__ce, to_mal, with_stoi)
	
	def count(self, with_stoi=True) :
		left, conf, right = ChemEq(self.__ce, 'nor').split(True, with_stoi)
		return sum((countEle(i, True) for i in left), Counter()), \
			sum((countEle(i, True) for i in right), Counter())
	
	def check(self) :
		left, right = self.count()
		left['e'] = right['e'] = 0
		return not (left - right)
		
	def balance(self, memorization=None) :
		self.__ce = balanceCE(self.__ce, self.form=='uni', memorization)
		return self
		
	def __len__(self) :
		'''return material number of chemical equation both left and right'''
		l, m, r = self.split(True)
		return len(l) + len(r)
		
	def __getitem__(self, key) :
		left, conf, right = self.split(True, True)
		l, c, r = left, conf, right
		try    : return (l+[c]+r)[key]
		except : return eval(key)
		
	def __setitem__(self, key, value) :
		self.__ce = self.__ce.replace(self[key] if isinstance(key, int) else formatEle(key, self.form=='nor'), value)
		
	form = property(lambda self : self.__form)
		
	@form.setter
	def form(self, form) :
		self.__form, self.__ce = form, formatCE(self.__ce, form=='nor')
	
	__str__ = lambda self : str(self.__ce)
	__repr__ = lambda self : self.__class__.__name__ + '(%s)' % repr(self.__ce)
