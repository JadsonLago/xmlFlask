from peewee import *

# Conexão com o banco de dados SQLite
db = SqliteDatabase('database.db')



class Emitente(Model):
    emit_cnpj = CharField()
    emit_nome = CharField()
    emit_ie = CharField()

    class Meta:
        database = db    


# Definindo o modelo da tabela de NFe
class NFe(Model):
    n_nota = CharField()
    data_emit = CharField()
    valor_total = FloatField()
    emitente = ForeignKeyField(Emitente)

    class Meta:
        database = db                    

# Criando as tabelas
def create_tables():
    with db:
        db.create_tables([Emitente])
        db.create_tables([NFe])
