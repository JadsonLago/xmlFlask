from peewee import *

# Conexão com o banco de dados SQLite
db = SqliteDatabase('database.db')

# Definindo o modelo da tabela de NFe
class NFe(Model):
    invoice_number = CharField()
    issue_date = CharField()
    total_value = FloatField()

    class Meta:
        database = db

# Criando as tabelas
def create_tables():
    with db:
        db.create_tables([NFe])
