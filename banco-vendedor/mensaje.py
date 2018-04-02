class Mensaje(object):
	"""docstring for mensaje"""
	def __init__(self, id, idVendedor, idComprador, monto, mensaje):
		self.id          = id
		self.idVendedor  = idVendedor
		self.idComprador = idComprador
		self.monto       = monto
		self.mensaje     = mensaje

class ResponseMessage(object):
	"""docstring for ResponseMessage"""
	def __init__(self, id, mensaje):
		self.id      = id
		self.mensaje = mensaje
		
		