from decimal import Decimal
from pony.orm import *


db = Database()

class Cuenta(db.Entity):
    id = PrimaryKey(int, auto=True)
    idVendedor = Required(str)
    monto = Optional(Decimal)
    idComprador = Optional(str)

db.bind(provider='sqlite', filename='db-bancoVendedor.sqlite', create_db=True)

db.generate_mapping(create_tables=True)
