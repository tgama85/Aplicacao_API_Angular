#Para funcionamento deste código deve-se fazer o comando abaixo
#pip install Werkzeug==0.16.0

#Para execução do código digite no terminal:
#No Windows: set FLASK_APP=app.py
#No Linux: export FLASK_APP=app.py

#Após a execução do terminal (Com o ambiente virtual ativado e dentro da pasta da aplicação) excute: flask run
#Obs: se necessário use o path do arquivo da aplicação para rodar o export FLASK_APP ou set FLASK_APP

#import das bibliotecas
from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy import Column, Table, Integer, String, Date, MetaData, Boolean, ForeignKey
import psycopg2

#conexão api
app_flask = Flask(__name__)
app = Api(app = app_flask,
        version = "1.0",
        title = "Imobiliaria tgama85",
        description = "Sistema para venda de imóveis")
CORS(app_flask)

#declaração das name_spaces
name_space_endereco = app.namespace('api', description='Gerencia os endereços')
name_space_cliente = app.namespace('api', description='Gerencia os clientes')
name_space_proprietario = app.namespace('api', description='Gerencia os proprietarios')
name_space_vendedor = app.namespace('api', description='Gerencia os vendedores')
name_space_tipo = app.namespace('api', description='Gerencia os tipos de imóvel')
name_space_imovel = app.namespace('api', description='Gerencia os imóveis')
name_space_banco = app.namespace('api', description='Gerencia os bancos')
name_space_financ = app.namespace('api', description='Gerencia os financiamentos')
name_space_solic = app.namespace('api', description='Gerencia os tipos de imóvel')

#Model do endereço

model_endereco = app.model('endereco', 
                        {'id_endereco': fields.Integer(required = True, 
                                description="ID do endereço", 
                                help="Campo não pode estar branco."),
                        'rua': fields.String(required = True, 
                                description="Rua", 
                                help="Campo não pode estar branco."),
                        'numero': fields.Integer(required = True, 
                                description="Número do endereço", 
                                help="Campo não pode estar branco."),
                        'andar': fields.Integer(required = True, 
                                description="Andar do endereço", 
                                help="Campo não pode estar branco."),
                        'bloco': fields.String(required = True, 
                                description="Bloco do endereço", 
                                help="Campo não pode estar branco."),
                        'bairro': fields.String(required = True, 
                                description="Bairro do endereço", 
                                help="Campo não pode estar branco."),
                        'cidade': fields.String(required = True, 
                                description="Cidade do endereço", 
                                help="Campo não pode estar branco."),
                        'uf': fields.String(required = True, 
                                description="UF do endereço", 
                                help="Campo não pode estar branco."),
                        'cep': fields.String(required = True, 
                                description="CEP do endereço", 
                                help="Campo não pode estar branco.")                                       
                                })


@name_space_endereco.route("/endereco")
#classe com os campos da tabela endereco
class Endereco(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_endereco = Table('endereco', meta, Column('id_endereco', Integer, primary_key=True), Column('rua', String), Column('numero', Integer), Column('andar', String), Column('bloco', String), Column('cidade', String), Column('uf', String), Column('cep', String))

  #Executa a solicitação dos dados da tabela endereço
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_endereco': 'Especifica o Id associado com o endereço' })
  def get(self):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_endereco.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_enderecos = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_enderecos)
        return jsonify(lista_enderecos)

    except KeyError as e:
      print(e)
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      print(e)
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela endereço
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_endereco': 'Especifica o Id associado com o endereço' })
  @app.expect(model_endereco)
  def post(self):
    try:
      json_data = request.json
      rua = json_data['rua']
      numero = json_data['numero'] 
      andar = json_data['andar'] 
      bloco = json_data['bloco']
      bairro = json_data['bairro'] 
      cidade = json_data['cidade']
      uf = json_data['uf']
      cep = json_data['cep']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_endereco.insert().returning(self.tab_endereco.c.id_endereco).values(rua=rua, numero=numero, andar=andar, bloco=bloco, bairro=bairro, cidadade=cidadade, uf=uf, cep=cep)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})
                          
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela endereço
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_endereco': 'Especifica o Id associado com o endereço' })
  @app.expect(model_endereco)
  def put(self, id_endereco):
    try:
      json_data = request.json
      rua = json_data['rua']
      numero = json_data['numero'] 
      andar = json_data['andar'] 
      bloco = json_data['bloco']
      bairro = json_data['bairro'] 
      cidade = json_data['cidade']
      uf = json_data['uf']
      cep = json_data['cep']
      
      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_endereco.update().returning(self.tab_endereco.c.id_endereco).values(rua=rua, numero=numero, andar=andar, bloco=bloco, bairro=bairro, cidadade=cidadade, uf=uf, cep=cep)
        result = conn.execute(atualiza_declaracao)
        return jsonify({'result': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela endereço
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_endereco': 'Especifica o Id associado com o endereço' })
  @app.expect(model_endereco)             
  def delete(self, id_endereco):
    try:
      json_data = request.json
      rua = json_data['rua']
      numero = json_data['numero'] 
      andar = json_data['andar'] 
      bloco = json_data['bloco']
      bairro = json_data['bairro'] 
      cidade = json_data['cidade']
      uf = json_data['uf']
      cep = json_data['cep']
      
      with self.db.connect() as conn:
        exclui_declaracao = self.tab_endereco.delete().returning(self.tab_endereco.c.id_endereco).values(rua=rua, numero=numero, andar=andar, bloco=bloco, bairro=bairro, cidadade=cidadade, uf=uf, cep=cep)
        result = conn.execute(exclui_declaracao)
        return jsonify({'result': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do cliente
model_cliente = app.model('cliente', 
                {'id_cliente': fields.Integer(required = True, 
                                        description="ID do cliente", 
                                        help="Campo não pode estar branco."),
                'id_endereco': fields.Integer(required = True, 
                                        description="ID do endereço do cliente", 
                                        help="Campo não pode estar branco."),
                'nome': fields.String(required = True, 
                                        description="Nome do cliente", 
                                        help="Campo não pode estar branco."),
                'data_nascimento': fields.Date(required = True, 
                                        description="Data de nascimento do cliente", 
                                        help="Campo não pode estar branco."),
                'telefone': fields.Integer(required = True, 
                                        description="Telefone do cliente", 
                                        help="Campo não pode estar branco."),
                'email': fields.String(required = True, 
                                        description="E-mail do cliente", 
                                        help="Campo não pode estar branco."),
                'cpf': fields.String(required = True, 
                                        description="CPF do cliente", 
                                        help="Campo não pode estar branco."),
                'rg': fields.String(required = True, 
                                        description="RG do cliente", 
                                        help="Campo não pode estar branco."),
                'estado_civil': fields.String(required = True, 
                                        description="Estado civil do cliente", 
                                        help="Campo não pode estar branco."),
                'profissao': fields.String(required = True, 
                                        description="Profissão do cliente", 
                                        help="Campo não pode estar branco.")                                      
                                        })

#Cliente
@name_space_cliente.route("/cliente")
#classe com os campos da tabela cliente
class Cliente(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_cliente = Table('cliente', meta, Column('id_cliente', Integer, primary_key=True), Column('id_endereco', Integer, foreign_key=True), Column('nome', String), Column('data_nascimento', Date), Column('telefone', Integer), Column('email', String), Column('cpf', String), Column('rg', String), Column('estado_civil', String), Column('profissao', String))

  #Executa a solicitação dos dados da tabela cliente
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_cliente': 'Especifica o Id associado com o cliente' })
  def get(self, id_cliente):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_cliente.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_cliente = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_cliente)
        return jsonify(lista_cliente)

    except KeyError as e:
      print(e)
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      print(e)
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela cliente
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_cliente': 'Especifica o Id associado com o cliente' })
  @app.expect(model_cliente)
  def post(self, id_cliente):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      estado_civil = json_data['estado_civil']
      profissao = json_data['profissao']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_cliente.insert().returning(self.tab_cliente.c.id_cliente).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, estado_civil=estado_civil, profissao=profissao)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela cliente
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_cliente': 'Especifica o Id associado com o cliente' })
  @app.expect(model_cliente)
  def put(self, id_cliente):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      estado_civil = json_data['estado_civil']
      profissao = json_data['profissao']
      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_cliente.update().returning(self.tab_cliente.c.id_cliente).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, estado_civil=estado_civil, profissao=profissao)
        results = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in results]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela cliente
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_cliente': 'Especifica o Id associado com o cliente' })
  @app.expect(model_cliente)             
  def delete(self, id_cliente):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      estado_civil = json_data['estado_civil']
      profissao = json_data['profissao']
      
      with self.db.connect() as conn:
        exclui_declaracao = self.tab_cliente.delete().returning(self.tab_cliente.c.id_cliente).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, estado_civil=estado_civil, profissao=profissao)
        result = conn.execute(exclui_declaracao)
        return jsonify({'result': [dict(row) for row in result]})
            
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do proprietario
model_proprietario = app.model('proprietario', 
                {'id_proprietario': fields.Integer(required = True, 
                                        description="ID do proprietario", 
                                        help="Campo não pode estar branco."),
                'id_endereco': fields.Integer(required = True, 
                                        description="ID do endereço do proprietario", 
                                        help="Campo não pode estar branco."),
                'nome': fields.String(required = True, 
                                        description="Nome do proprietario", 
                                        help="Campo não pode estar branco."),
                'data_nascimento': fields.Date(required = True, 
                                        description="Data de nascimento do proprietario", 
                                        help="Campo não pode estar branco."),
                'telefone': fields.Integer(required = True, 
                                        description="Telefone do proprietario", 
                                        help="Campo não pode estar branco."),
                'email': fields.String(required = True, 
                                        description="E-mail do proprietario", 
                                        help="Campo não pode estar branco."),
                'cpf': fields.String(required = True, 
                                        description="CPF do proprietario", 
                                        help="Campo não pode estar branco."),
                'rg': fields.String(required = True, 
                                        description="RG do proprietario", 
                                        help="Campo não pode estar branco."),
                'estado_civil': fields.String(required = True, 
                                        description="Estado civil do proprietario", 
                                        help="Campo não pode estar branco."),
                'tempo_imovel': fields.String(required = True, 
                                        description="Profissão do proprietario", 
                                        help="Campo não pode estar branco.")                                      
                                        })


@name_space_proprietario.route("/proprietario")
#classe com os campos da tabela proprieatio
class Proprietario(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_proprietario = Table('proprietario', meta, Column('id_proprietario', Integer, primary_key=True), Column('id_endereco', Integer, foreign_key=True), Column('nome', String), Column('data_nascimento', Date), Column('telefone', Integer), Column('email', String), Column('cpf', String), Column('rg', String), Column('estado_civil', String), Column('tempo_imovel', String))

  #Executa a solicitação dos dados da tabela proprietario
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_proprietario': 'Especifica o Id associado com o proprietario' })
  def get(self, id_proprietario):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_proprietario.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_proprietario = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_proprietario)
        return jsonify(lista_proprietario)

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela proprietario
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_proprietario': 'Especifica o Id associado com o proprietario' })
  @app.expect(model_proprietario)
  def post(self, id_proprietario):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      estado_civil = json_data['estado_civil']
      tempo_imovel = json_data['tempo_imovel']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_proprietario.insert().returning(self.tab_proprietario.c.id_proprietario).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, estado_civil=estado_civil, tempo_imovel=tempo_imovel)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})
            
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela proprietario
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_proprietario': 'Especifica o Id associado com o proprietario' })
  @app.expect(model_proprietario)
  def put(self, id_proprietario):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      estado_civil = json_data['estado_civil']
      tempo_imovel = json_data['tempo_imovel']
      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_proprietario.update().returning(self.tab_proprietario.c.id_proprietario).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, estado_civil=estado_civil, tempo_imovel=tempo_imovel)
        results = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in results]})
            
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela proprietario
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_proprietario': 'Especifica o Id associado com o proprietario' })
  @app.expect(model_proprietario)             
  def delete(self, id_proprietario):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      estado_civil = json_data['estado_civil']
      tempo_imovel = json_data['tempo_imovel']
      
      with self.db.connect() as conn:
        exclui_declaracao = self.tab_proprietario.delete().returning(self.tab_proprietario.c.id_proprietario).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, estado_civil=estado_civil, tempo_imovel=tempo_imovel)
        result = conn.execute(exclui_declaracao)
        return jsonify({'result': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do vendedor
model_vendedor = app.model('vendedor', 
                {'id_vendedor': fields.Integer(required = True, 
                                        description="ID do vendedor", 
                                        help="Campo não pode estar branco."),
                'id_endereco': fields.Integer(required = True, 
                                        description="ID do endereço do vendedor", 
                                        help="Campo não pode estar branco."),
                'nome': fields.String(required = True, 
                                        description="Nome do vendedor", 
                                        help="Campo não pode estar branco."),
                'data_nascimento': fields.Date(required = True, 
                                        description="Data de nascimento do vendedor", 
                                        help="Campo não pode estar branco."),
                'telefone': fields.Integer(required = True, 
                                        description="Telefone do vendedor", 
                                        help="Campo não pode estar branco."),
                'email': fields.String(required = True, 
                                        description="E-mail do vendedor", 
                                        help="Campo não pode estar branco."),
                'cpf': fields.String(required = True, 
                                        description="CPF do vendedor", 
                                        help="Campo não pode estar branco."),
                'rg': fields.String(required = True, 
                                        description="RG do vendedor", 
                                        help="Campo não pode estar branco."),
                'cargo': fields.String(required = True, 
                                        description="Cargo do vendedor", 
                                        help="Campo não pode estar branco.")                                      
                                        })


@name_space_vendedor.route("/vendedor")
#classe com os campos da tabela vendedor
class Vendedor(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_vendedor = Table('vendedor', meta, Column('id_vendedor', Integer, primary_key=True), Column('id_endereco', Integer, foreign_key=True), Column('nome', String), Column('data_nascimento', Date), Column('telefone', Integer), Column('email', String), Column('cpf', String), Column('rg', String), Column('estado_civil', String), Column('cargo', String))

  #Executa a solicitação dos dados da tabela vendedor
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_vendedor': 'Especifica o Id associado com o vendedor' })
  def get(self, id_vendedor):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_vendedor.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_vendedor = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_vendedor)
        return jsonify(lista_vendedor)

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela vendedor
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_vendedor': 'Especifica o Id associado com o vendedor' })
  @app.expect(model_proprietario)
  def post(self, id_vendedor):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      cargo = json_data['cargo']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_vendedor.insert().returning(self.tab_vendedor.c.id_vendedor).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, cargo=cargo)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela vendedor
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_vendedor': 'Especifica o Id associado com o vendedor' })
  @app.expect(model_vendedor)
  def put(self, id_vendedor):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      cargo = json_data['cargo']
      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_vendedor.update().returning(self.tab_vendedor.c.id_vendedor).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, cargo=cargo)
        results = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in results]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela vendedor
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_vendedor': 'Especifica o Id associado com o vendedor' })
  @app.expect(model_vendedor)             
  def delete(self, id_vendedor):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco']
      nome = json_data['nome'] 
      data_nascimento = json_data['data_nascimento'] 
      telefone = json_data['telefone']
      email = json_data['email'] 
      cpf = json_data['cpf']
      rg = json_data['rg']
      cargo = json_data['cargo']
      
      with self.db.connect() as conn:
        exclui_declaracao = self.tab_vendedor.delete().returning(self.tab_vendedor.c.id_vendedor).values(id_endereco=id_endereco, nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, cpf=cpf, rg=rg, cargo=cargo)
        result = conn.execute(exclui_declaracao)
        return jsonify({'result': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do tipo_imovel
model_tipo = app.model('tipo_imovel', 
                {'id_tipo': fields.Integer(required = True, 
                                        description="ID do tipo de imovel", 
                                        help="Campo pode estar branco."),
                'casa': fields.Boolean(required = True or False, 
                                        description="Escolha a casa", 
                                        help="Campo não pode estar branco."),
                'apartamento': fields.Boolean(required = True or False, 
                                        description="Escolha o apartamento", 
                                        help="Campo pode estar branco."),
                'kitnet': fields.Boolean(required = True or False, 
                                        description="Escola a kitnet", 
                                        help="Campo pode estar branco.")
                                        })


@name_space_tipo.route("/tipos")
#classe com os campos da tabela tipo_imovel
class Tipos(Resource):
        
  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_tipos = Table('tipo_imovel', meta, Column('id_tipo', Integer, primary_key=True), Column('casa', String), Column('apartamento', String), Column('kitnet', String))

  #Executa a solicitação dos dados da tabela tipo_imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_tipo': 'Especifica o Id associado com o tipo de imovel' })
  def get(self, id_tipo):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_tipos.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_tipos = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_tipos)
        return jsonify(lista_tipos)

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela tipo_imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_tipo': 'Especifica o Id associado com o tipo de imovel' })
  @app.expect(model_tipo)
  def post(self, id_tipo):
    try:
      json_data = request.json
      casa = json_data['casa'] 
      apartamento = json_data['apartamento'] 
      kitnet = json_data['kitnet']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_tipos.insert().returning(self.tab_tipos.c.id_tipo).values(casa=casa, apartamento=apartamento, kitnet=kitnet)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela tipo_imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_tipo': 'Especifica o Id associado com o tipo de imovel' })
  @app.expect(model_tipo)
  def put(self, id_tipo):
    try:
      json_data = request.json
      casa = json_data['casa'] 
      apartamento = json_data['apartamento'] 
      kitnet = json_data['kitnet']

      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_tipos.update().returning(self.tab_tipos.c.id_tipo).values(casa=casa, apartamento=apartamento, kitnet=kitnet)
        results = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in results]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela tipo_imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_tipo': 'Especifica o Id associado com o tipo de imovel' })
  @app.expect(model_tipo)             
  def delete(self, id_tipo):
    try:
      json_data = request.json
      casa = json_data['casa'] 
      apartamento = json_data['apartamento'] 
      kitnet = json_data['kitnet']

      with self.db.connect() as conn:
        exclui_declaracao = self.tab_tipos.delete().returning(self.tab_tipos.c.id_tipo).values(casa=casa, apartamento=apartamento, kitnet=kitnet)
        result = conn.execute(exclui_declaracao)
        return jsonify({'result': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do imovel
model_imovel = app.model('imovel', 
                {'id_imovel': fields.Integer(required = True, 
                                        description="ID do tipo de imovel", 
                                        help="Campo não pode estar branco."),
                'id_endereco': fields.Integer(required = True, 
                                        description="ID do tipo de endereco", 
                                        help="Campo não pode estar branco."),
                'id_proprietario': fields.Integer(required = True, 
                                        description="ID do tipo de proprietario", 
                                        help="Campo não pode estar branco."),
                'id_tipo': fields.Integer(required = True, 
                                        description="ID do tipo de imovel", 
                                        help="Campo não pode estar branco."),
                'valor_luz': fields.String(required = True, 
                                        description="Valor do gasto com luz", 
                                        help="Campo não pode estar branco."),
                'valor_agua': fields.String(required = True, 
                                        description="Valor do gasto com água", 
                                        help="Campo pode estar branco."),
                'condominio': fields.String(required = True, 
                                        description="Valor do gasto com condominio", 
                                        help="Campo pode estar branco."),
                'propaganda': fields.String(required = True, 
                                        description="Valor do gasto com propaganda", 
                                        help="Campo pode estar branco."),
                'preco_total': fields.String(required = True, 
                                        description="Valor do preço total", 
                                        help="Campo pode estar branco.")
                                        })


@name_space_imovel.route("/imoveis")
#classe com os campos da tabela imovel
class Imoveis(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_imoveis = Table('imovel', meta, Column('id_imovel', Integer, primary_key=True), Column('id_endereco', Integer, foreign_key=True), Column('id_proprietario', Integer, foreign_key=True), Column('id_tipo', Integer, foreign_key=True), Column('valor_luz', String), Column('valor_agua', String), Column('condominio', String), Column('propaganda', String), Column('preco_total', String))

  #Executa a solicitação dos dados da tabela imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_imovel': 'Especifica o Id associado com o imovel' })
  def get(self, id_imovel):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_imoveis.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_imoveis = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_imoveis)
        return jsonify(lista_imoveis)

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_tipo': 'Especifica o Id associado com o imovel' })
  @app.expect(model_imovel)
  def post(self, id_imovel):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco'] 
      id_proprietario = json_data['id_proprietario'] 
      id_tipo = json_data['id_tipo']
      valor_luz = json_data['valor_luz']
      valor_agua = json_data['valor_agua']
      condominio = json_data['condominio']
      propaganda = json_data['propaganda']
      preco_total = json_data['preco_total']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_imoveis.insert().returning(self.tab_imoveis.c.id_imovel).values(id_endereco=id_endereco, id_proprietario=id_proprietario, id_tipo=id_tipo, valor_luz=valor_luz, valor_agua=valor_agua, condominio=condominio, propaganda=propaganda, preco_total=preco_total)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_tipo': 'Especifica o Id associado com o imovel' })
  @app.expect(model_imovel)
  def put(self, id_imovel):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco'] 
      id_proprietario = json_data['id_proprietario'] 
      id_tipo = json_data['id_tipo']
      valor_luz = json_data['valor_luz']
      valor_agua = json_data['valor_agua']
      condominio = json_data['condominio']
      propaganda = json_data['propaganda']
      preco_total = json_data['preco_total']
      
      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_imoveis.update().returning(self.tab_imoveis.c.id_imovel).values(id_endereco=id_endereco, id_proprietario=id_proprietario, id_tipo=id_tipo, valor_luz=valor_luz, valor_agua=valor_agua, condominio=condominio, propaganda=propaganda, preco_total=preco_total)
        result = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela imovel
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_tipo': 'Especifica o Id associado com o imovel' })
  @app.expect(model_imovel)             
  def delete(self, id_imovel):
    try:
      json_data = request.json
      id_endereco = json_data['id_endereco'] 
      id_proprietario = json_data['id_proprietario'] 
      id_tipo = json_data['id_tipo']
      valor_luz = json_data['valor_luz']
      valor_agua = json_data['valor_agua']
      condominio = json_data['condominio']
      propaganda = json_data['propaganda']
      preco_total = json_data['preco_total']

      with self.db.connect() as conn:
        exclui_declaracao = self.tab_imoveis.delete().returning(self.tab_imoveis.c.id_imovel).values(id_endereco=id_endereco, id_proprietario=id_proprietario, id_tipo=id_tipo, valor_luz=valor_luz, valor_agua=valor_agua, condominio=condominio, propaganda=propaganda, preco_total=preco_total)
        results = conn.execute(exclui_declaracao)
        return jsonify({'result': [dict(row) for row in results]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do banco
model_banco = app.model('imovel', 
                {'id_banco': fields.Integer(required = True, 
                                        description="ID do banco", 
                                        help="Campo não pode estar branco."),
                'nome_banco': fields.String(required = True, 
                                        description="Nome do banco", 
                                        help="Campo não pode estar branco.")
                                        })


@name_space_banco.route("/bancos")
#classe com os campos da tabela banco
class Bancos(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_bancos = Table('banco', meta, Column('id_banco', Integer, primary_key=True), Column('nome_banco', String))

  #Executa a solicitação dos dados da tabela banco
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_banco': 'Especifica o Id associado com o banco' })
  def get(self, id_banco):
    try:
      
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        print(id_banco)
        seleciona_declaracao = f"SELECT * FROM public.banco WHERE id_banco = {id_banco}"
        resulta = conn.execute(seleciona_declaracao)
        lista_bancos = [{key: value for (key, value) in row.items()} for row in resulta]
        return jsonify(lista_bancos)

    except KeyError as e:
      print(e)
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      print(e)
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela banco
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' })
  @app.expect(model_banco)
  def post(self):
    try:
      json_data = request.json
      nome_banco = json_data['nome_banco']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_bancos.insert().returning(self.tab_bancos.c.id_banco).values(nome_banco=nome_banco)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela banco
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_banco': 'Especifica o Id associado com o banco' })
  @app.expect(model_banco)
  def put(self):
    try:
      json_data = request.json
      nome_banco = json_data['nome_banco']

      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_bancos.update().returning(self.tab_bancos.c.id_banco).values(nome_banco=nome_banco)
        result = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

#Executa a exclusão dos dados da tabela banco
@app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_banco': 'Especifica o Id associado com o banco' })
@app.expect(model_banco)             
def delete(self, id_banco):
  try:
    json_data = request.json
    nome_banco = json_data['nome_banco']

    with self.db.connect() as conn:
      exclui_declaracao = self.tab_bancos.delete().returning(self.tab_bancos.c.id_banco).values(nome_banco=nome_banco)
      results = conn.execute(exclui_declaracao)
      return jsonify({'resultado': [dict(row) for row in results]})
  
  except KeyError as e:
    name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
  except Exception as e:
    name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do financiamento
model_financiamento = app.model('financiamento', 
                {'id_financiamento': fields.Integer(required = True, 
                                        description="ID do financiamento", 
                                        help="Campo não pode estar branco."),
                'id_banco': fields.Integer(required = True, 
                                        description="ID do banco", 
                                        help="Campo não pode estar branco."),
                'valor_financiado': fields.String(required = True, 
                                        description="Valor financiado", 
                                        help="Campo não pode estar branco."),
                'valor_entrada': fields.String(required = True, 
                                        description="Valor de entrada do financiamento", 
                                        help="Campo não pode estar branco."),
                'quantidade_parcela': fields.String(required = True, 
                                        description="Quantidade de parcelas do financiamento", 
                                        help="Campo não pode estar branco.")
                                        })


@name_space_financ.route("/financiamentos")
#classe com os campos da tabela financiamento
class Financiamentos(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_financs = Table('financiamento', meta, Column('id_financiamento', Integer, primary_key=True), Column('id_banco', Integer, primary_key=True), Column('valor_financiado', String), Column('valor_entrada', String), Column('quantidade_parcela', String))

  #Executa a solicitação dos dados da tabela financiamento
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_financiamento': 'Especifica o Id associado com o financiamento' })
  def get(self, id_financiamento):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_financs.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_financ = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_financ)
        return jsonify(lista_financ)

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela financiamento
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_financiamento': 'Especifica o Id associado com o financiamento' })
  @app.expect(model_financiamento)
  def post(self, id_financiamento):
    try:
      json_data = request.json
      id_banco = json_data['id_banco']
      valor_financiado = json_data['valor_financiado']
      valor_entrada = json_data['valor_entrada']
      quantidade_parcela = json_data['quantidade_parcela']


      with self.db.connect() as conn:
        insere_declaracao = self.tab_financs.insert().returning(self.tab_financs.c.id_financiamento).values(id_banco=id_banco, valor_financiado=valor_financiado, valor_entrada=valor_entrada, quantidade_parcela=quantidade_parcela)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela financiamento
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_financiamento': 'Especifica o Id associado com o financiamento' })
  @app.expect(model_financiamento)
  def put(self, id_financiamento):
    try:
      json_data = request.json
      id_banco = json_data['id_banco']
      valor_financiado = json_data['valor_financiado']
      valor_entrada = json_data['valor_entrada']
      quantidade_parcela = json_data['quantidade_parcela']
      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_financs.update().returning(self.tab_financs.c.id_financiamento).values(id_banco=id_banco, valor_financiado=valor_financiado, valor_entrada=valor_entrada, quantidade_parcela=quantidade_parcela)
        result = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in result]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela financiamento
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_financiamento': 'Especifica o Id associado com o financiamento' })
  @app.expect(model_financiamento)             
  def delete(self, id_financiamento):
    try:
      json_data = request.json
      id_banco = json_data['id_banco']
      valor_financiado = json_data['valor_financiado']
      valor_entrada = json_data['valor_entrada']
      quantidade_parcela = json_data['quantidade_parcela']
      with self.db.connect() as conn:
        exclui_declaracao = self.tab_financs.delete().returning(self.tab_financs.c.id_financiamento).values(id_banco=id_banco, valor_financiado=valor_financiado, valor_entrada=valor_entrada, quantidade_parcela=quantidade_parcela)
        results = conn.execute(exclui_declaracao)
        return jsonify({'resultado': [dict(row) for row in results]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")


#Model do solicitacao_compra
model_solicitacao = app.model('solicitacao_compra', 
                {'id_solicitacao': fields.Integer(required = True, 
                                        description="ID do financiamento", 
                                        help="Campo não pode estar branco."),
                'id_tipo': fields.Integer(required = True, 
                                        description="ID do banco", 
                                        help="Campo não pode estar branco."),
                'id_cliente': fields.Integer(required = True, 
                                        description="Valor financiado", 
                                        help="Campo não pode estar branco."),
                'id_vendedor': fields.Integer(required = True, 
                                        description="Valor de entrada do financiamento", 
                                        help="Campo não pode estar branco."),
                'id_financiamento': fields.Integer(required = True, 
                                        description="Quantidade de parcelas do financiamento", 
                                        help="Campo não pode estar branco."),
                'valor_venda': fields.String(required = True, 
                                        description="Quantidade de parcelas do financiamento", 
                                        help="Campo não pode estar branco.")
                                        })


@name_space_solic.route("/solicitacoes")
#classe com os campos da tabela solicitacao_compra
class Solicitacao(Resource):

  db_string = "postgresql://postgres:postgres@localhost:5432/imobiliaria"
  db = create_engine(db_string)
  meta = MetaData(db)
  tab_solics = Table('solicitacao_compra', meta, Column('id_solicitacao', Integer, primary_key=True), Column('id_tipo', Integer, primary_key=True), Column('id_cliente', Integer, primary_key=True), Column('id_vendedor', Integer, primary_key=True), Column('id_financiamento', Integer, primary_key=True), Column('id_imovel', Integer, primary_key=True), Column('valor_venda', String), Column('pagamento_vista', String))

  #Executa a solicitação dos dados da tabela solicitacao_compra
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_solicitacao': 'Especifica o Id associado com a solicitação' })
  def get(self, id_solicitacao):
    try:
      with self.db.connect as conn:
        #Executa a leitura dos parâmetros da tabela
        seleciona_declaracao = self.tab_solics.select()
        resulta = conn.execute(seleciona_declaracao)
        lista_solics = [{key: value for (key, value) in row.items()} for row in resulta]
        print(lista_solics)
        return jsonify(lista_solics)

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a criação dos dados da tabela solicitacao_compra
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_solicitacao': 'Especifica o Id associado com o solicitação' })
  @app.expect(model_solicitacao)
  def post(self, id_solicitacao):
    try:
      json_data = request.json
      id_tipo = json_data['id_tipo']
      id_cliente = json_data['id_cliente']
      id_vendedor = json_data['id_vendedor']
      id_financiamento = json_data['id_financiamento']
      valor_venda = json_data['valor_venda']

      with self.db.connect() as conn:
        insere_declaracao = self.tab_solics.insert().returning(self.tab_solics.c.id_solicitacao).values(id_tipo=id_tipo, id_cliente=id_cliente, id_vendedor=id_vendedor, id_financiamento=id_financiamento, valor_venda=valor_venda)
        resultado = conn.execute(insere_declaracao)
        return jsonify({'resultado': [dict(row) for row in resultado]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a atualização dos dados da tabela solicitacao_compra
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_solicitacao': 'Especifica o Id associado com a solicitação' })
  @app.expect(model_solicitacao)
  def put(self, id_solicitacao):
    try:
      json_data = request.json
      id_tipo = json_data['id_tipo']
      id_cliente = json_data['id_cliente']
      id_vendedor = json_data['id_vendedor']
      id_financiamento = json_data['id_financiamento']
      valor_venda = json_data['valor_venda']

      with self.db.connect() as conn:
        atualiza_declaracao = self.tab_solics.update().returning(self.tab_solics.c.id_solicitacao).values(id_tipo=id_tipo, id_cliente=id_cliente, id_vendedor=id_vendedor, id_financiamento=id_financiamento, valor_venda=valor_venda)
        result = conn.execute(atualiza_declaracao)
        return jsonify({'resultado': [dict(row) for row in result]})

    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")

  #Executa a exclusão dos dados da tabela solicitacao_compra
  @app.doc(responses={ 200: 'OK', 400: 'Argumento Inválido', 500: 'Mapeando a chave de erro' }, params={ 'id_solicitacao': 'Especifica o Id associado com a solicitação' })
  @app.expect(model_solicitacao)             
  def delete(self, id_solicitacao):
    try:
      json_data = request.json
      id_tipo = json_data['id_tipo']
      id_cliente = json_data['id_cliente']
      id_vendedor = json_data['id_vendedor']
      id_financiamento = json_data['id_financiamento']
      valor_venda = json_data['valor_venda']

      with self.db.connect() as conn:
        exclui_declaracao = self.tab_solics.delete().returning(self.tab_solics.c.id_solicitacao).values(id_tipo=id_tipo, id_cliente=id_cliente, id_vendedor=id_vendedor, id_financiamento=id_financiamento, valor_venda=valor_venda)
        results = conn.execute(exclui_declaracao)
        return jsonify({'resultado': [dict(row) for row in results]})
    except KeyError as e:
      name_space.abort(500, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "500")
    except Exception as e:
      name_space.abort(400, e.__doc__, status = "Informação não pode ser recuperada", statusCode = "400")