from . import *

def main(memo=None, form='uni', *, info=False, gui=False, cntlog=False, ballog=False) :
	cnt = 1
	inpart = ''

	print(f'Balce v{__version__}')
	if memo is not None :
		print(f'* memo = "{memo}"')
	print(f'* info = {info}')
	print(f'* form = {form}')
	print()

	with bct :
		bct.cntlog = cntlog
		bct.ballog = ballog
		while True :
			try :
				if not inpart :
					inp = input(f'Inp[{cnt}]: ')
					
				else :
					inp = input(f'... ')
					if inp :
						inpart += inp
					else :
						inp, inpart = inpart, ''

				if inp in {'quit', 'q', 'Q'} :
					print("you can use either {quit, q, Q} to quit.")
					return 0

				eq = CEquation(inp, form=form)
				if not inpart and info :
					print(f'\ti{cnt}.IsBalanced - {eq.check()}')
				eq.balance(memorization=memo)

				print('Oup[{}]: {}'.format(cnt, eq))
				cnt += 1
				if inpart : inpart = ''

			except ValueError as ve :
				if 'not enough values to unpack' in str(ve) :
					if not inpart :
						inpart = inp

			except BaseException as e :
				if inpart : continue
				print('\tFailed -> {}: {}'.format(type(e).__name__, e))

if __name__ == "__main__" :
	try :
		import fire
		fire.Fire(main)()

	except ModuleNotFoundError :
		main()

	except :
		...
