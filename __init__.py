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

from .core import *
from .core import __all__ as _c_all

__all__ = _c_all.copy()
