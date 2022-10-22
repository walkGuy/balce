__all__ = ['BalceCtx', 'bct']

from functools import wraps as funcWraps

class BalceCtx(object) :
	__slots__ = ('ballog', 'cntlog', 'ignore',
		'_orig')
	
	def __init__(ctx) :
		ctx.ballog = False
		ctx.cntlog = False
		ctx.ignore = False
		
		ctx._orig = None
		
	def __call__(ctx, **kwargs) :
		def w(f) :
			def g(*args, **kwds) :
				origin = {}
				for k,v in kwargs.items() :
					origin[k] = getattr(ctx, k)
					setattr(ctx, k, v)
				try :
					return f(*args, **kwds)
				finally :
					for k,v in origin.items() :
						setattr(ctx, k, v)
			return funcWraps(f)(g)
		return w
		
	def __enter__(ctx) :
		ctx._orig = tuple(getattr(ctx, i) for i in ctx.__slots__)
		
	def __exit__(ctx, exc_type, exc_val, exc_tb) :
		for i,j in zip(ctx.__slots__, ctx._orig) :
			setattr(ctx, i, j)
		return False
		
	__repr__ = __str__ = lambda ctx : \
		'<--\n' + '\n'.join(
			'\t{} = {}'.format(i, getattr(ctx, i))
			for i in ctx.__slots__
		) + '\n-->'
		
bct = BalceCtx()
