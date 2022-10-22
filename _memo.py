__all__ = [
	'BCTMemo',
]

# i dont ever know how i wrote this.....

from os import stat
from hashlib import blake2s as hash_key_func
#hash_key_func = lambda obj : type('_', (), {'hexdigest': classmethod(lambda cls : str(hash(obj)))})

from json.decoder import JSONDecoder
from json.encoder import (
	JSONEncoder,
	c_make_encoder, _make_iterencode,
	encode_basestring, encode_basestring_ascii,
)

class BCTMemo(object) :
	__slots__ = ('file',)
	
	def __init__(self, file: str) :
		if file.__class__ not in (str, bytes) :
			raise ValueError('Unsupported object of file "%s", must be str or bytes' % \
				file.__class__.__name__)
	
		with open(file, 'ab') :
			self.file = file
			
	def __getitem__(self, key) :
		key = hash_key_func(key.encode()).hexdigest()
		
		return self._view()[key]
			
	def __setitem__(self, key, value,
			## Turn globals into locals
			_encodefunc = JSONEncoder(
				check_circular = False,
			).encode
		) :
		key = hash_key_func(key.encode()).hexdigest()
		
		data = self._view()
		if data :
			if key in data :
				if data[key] != value :
					data[key] = value
					self._write(data)
			else :
				with open(self.file, 'rb+') as f :
					f.seek(stat(self.file).st_size - 2)
					f.write(',\n\t"{}": {}\n}}'.format(
						key, _encodefunc(value)).encode())
		else :
			with open(self.file, 'rb+') as f :
				f.write('{{\n\t"{}": {}\n}}'.format(
					key, _encodefunc(value)).encode())
	
	def __delitem__(self, key) :
		key = hash_key_func(key.encode()).hexdigest()
	
		data = self._view()
		del data[key]
		self._write(data)
	
	def clear(self) :
		open(self.file, 'wb').close()
	
	def get(self, key, value=None) :
		return self._view().get(
			hash_key_func(key.encode()).hexdigest(), value)
		
	set, delete = \
		__setitem__, __delitem__
	
	def add(self, key, value,
			## Turn globals into locals
			_encodefunc = JSONEncoder(
				check_circular = False,
			).encode
		) :
		key, s = \
			hash_key_func(key.encode()).hexdigest().encode(), \
			stat(self.file).st_size
			
		with open(self.file, 'rb+') as f :
			if s > 9 :
				f.seek(s - 2)
				f.write(key.join((b',\n\t"',
					b'": %s\n}' % _encodefunc(value).encode())))
			else :
				f.write(key.join((b'{\n\t"',
					b'": %s\n}' % _encodefunc(value).encode())))
	
	def _write(self, obj,
			_iterenfunc = JSONEncoder(
				check_circular = False,
				indent = '\t',
			).iterencode
		) :
		chunks = _iterenfunc(obj)
		with open(self.file, 'w') as f :
			f.write(''.join(chunks)) # this is faster
			#fw = f.write
			#for chunk in chunks : fw(chunk)
	
	def _view(self,
			_default_decoder_loads = JSONDecoder(
				object_hook = None,
				object_pairs_hook = None,
			).scan_once
		) :
		try :
			with open(self.file, 'rb') as f :
				return _default_decoder_loads(f.read().decode(), 0)[0]
		except :
			with open(self.file, 'wb') :
				return {}
				