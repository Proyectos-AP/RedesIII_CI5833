import bdBancoVendedor 
from pony.orm import *


@db_session
def add_cuenta(idVendedor,monto,idComprador):

	bdBancoVendedor.Cuenta(idVendedor = idVendedor,
    					monto = monto,
    					idComprador = idComprador)

	commit()

#--------------------------------------------------------

add_cuenta("R1234",10000,"R1234")