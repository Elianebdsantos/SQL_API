#Importe para trabalhar com o Json
import json
from flask import Flask, Response, request
#Ferramenta que o python disponibiliza 
from flask_sqlalchemy import SQLAlchemy

# sempre tem que colocar o app = Flask para indicar que será utilizado o modelo Flask
app= Flask('carros')
#Haverá modificações no nosso banco de dados
#Por padrão em aplicações em produção, isso fica False para não alterar, ex qdo uso alguma api para pegar algum dado
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# configura o banco, sempre que tiver @ na senha precisa colocar %40, local host. Estrutrura senha, local host e nome do banco 
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:senai%40134@127.0.0.1/bd_carro'

# Configuramos a variavel que representará o banco
mybd = SQLAlchemy(app)

# definimos a estrutura da tabela, para cada tabela precisa criar essa estrutura, a estrutura do class precisa ser identica ao banco, ou seja, o mesmo número de colunas tem que ter no mesmo padrão
class Carros(mybd.Model): #Nome da class precisa ser iniciada sempre por maiusculo
    __tablename__ = 'tb_carro'
    id = mybd.Column(mybd.Integer, primary_key = True) #nome da coluna, precisa colocar o nome da variavel que vai representar banco, neste modelo foi considerado como mybd
    marca = mybd.Column(mybd.String(100)) 
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(50))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd. Column(mybd.String(10))

#Convertemos a tabela em Json
    def to_json(self):
        return{"id": self.id, "marca": self.marca, "modelo": self.modelo, "valor": self.valor, "cor": self.cor, "numero_vendas": self.numero_vendas, "ano": self.ano}




# ******************CRIANDO A API ****************************
# Selecionar Tudo (GET) serve para visualizar podendo ser tudo ou parte do dado

@app.route("/carros", methods=["GET"]) 
def selecionar_carros():
    carro_objetos = Carros.query.all() # query.all indica que vai selecionar tudo. Seria uma consulta de todos os registros na tabela e imprime
# o retorno da consulta anterior deverá ser armazenada dentro do objeto, mas depois preciso converter para json devido ser uma api, o modelo de api só trabalha com json
    carro_json = [carro.to_json() for carro in carro_objetos]

    return gera_response(200, "carros", carro_json) # retorno 200 sempre vai indicar que funcionou


# Selecionar individual (Por ID)
@app.route("/carros/<id>", methods= ["GET"])
def seleciona_carro_id(id):
    carro_objeto = Carros.query.filter_by(id=id).first()
    carro_json = carro_objeto.to_json()

    return gera_response(200, "carro", carro_json)

#Cadastrar
@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()
    try:
        carro = Carros(id=body["id"], marca=body["marca"], modelo=body["modelo"], valor=body["valor"], cor=body["cor"], numero_vendas=body["numero_vendas"], ano=body["ano"])
        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carros", carro.to_json(), "Criado com sucesso!!!")
    
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "carros", {}, "Erro ao cadastrar!!!")
    
# Atualizar
@app.route("/carros/<id>", methods= ["PUT"])
def atualizar_carro(id):
   carro_objeto = Carros.query.filter_by(id=id).first() #sempre que for consultar por ID é essa estrutura
   body = request.get_json() # Sempre que for consultar o corpo da requisição é esse modelo 

   try: 
        if('marca' in body):
           carro_objeto.marca = body['marca'] #neste função ele vai substituir o dados desde que o item selecionado esteja dentro do banco  
        if('modelo' in body):
           carro_objeto.modelo = body['modelo']
        if('valor' in body):
            carro_objeto.valor = body['valor']
        if('cor' in body):
            carro_objeto.cor = body['cor']
        if('numero_vendas' in body):
            carro_objeto.numero_vendas = body['numero_vendas']
        if('ano' in body):
            carro_objeto.ano = body['ano']

        mybd.session.add(carro_objeto)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objeto.to_json(), "Atualizado com sucesso!")
   
   except Exception as e:
       print('Erro', e)
       return gera_response(400, "carros", {}, "Erro ao atualizar")
   
#Deletar
@app.route("/carros/<id>", methods=["DELETE"])
def deletar_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    try:
        mybd.session.delete(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objetos.to_json(), "Deletado com sucesso")
       
    except Exception as e:
        print("Erro", e)
        return gera_response(400, "carro", {}, "Erro ao deletar")


  







def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json") # funcionalidade do dumps é converter a mensagem em json

app.run(port=5000, host='localhost', debug=True)