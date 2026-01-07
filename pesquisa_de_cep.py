# input python - cep
# 	Aceitar tamanho de 8 digitos

# Como solicitar e receber informações do viacep

# consulta via web na via cep https://viacep.com.br/ 
	
# salva no banco de dados - usando mysql conector

# Dados que desejo salvar e exibir
#      "cep": "01001-000",
#       "logradouro": "Praça da Sé",
#       "complemento": "lado ímpar",
#       "bairro": "Sé",
#       "localidade": "São Paulo",
#       "uf": "SP",

# Como solicitar e receber

#contar o tamanho da variavel, ex 8 caracteres

#----------
# pip install requests mysql-connector-python
# v env      17 a 5 

import requests
import mysql.connector


# 1. Solicitar e validar CEP

while True:
    cep = input("Informe o seu CEP (somente números): ")

    if len(cep) == 8 and cep.isdigit():
        print(f"O CEP {cep} é válido. Consultando ViaCEP...")
        break
    else:
        print("CEP inválido, tente novamente.\n")


# 2. Consultar API ViaCEP

url = f"https://viacep.com.br/ws/{cep}/json/"

response = requests.get(url)

if response.status_code != 200:
    print("Erro ao consultar o ViaCEP.")
    exit()

dados = response.json()

if "erro" in dados:
    print("CEP não encontrado no ViaCEP.")
    exit()

print("\n===== Dados retornados =====")
for chave, valor in dados.items():
    print(f"{chave}: {valor}")


# 3. Salvar no MySQL

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sua_senha",
        database="via_cep_db"
    )

    cursor = conexao.cursor()

    # Criar tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enderecos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cep VARCHAR(9),
            logradouro VARCHAR(255),
            complemento VARCHAR(255),
            bairro VARCHAR(255),
            localidade VARCHAR(255),
            uf VARCHAR(2)
        )
    """)

    # Inserir dados
    sql = """
        INSERT INTO enderecos
        (cep, logradouro, complemento, bairro, localidade, uf)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores = (
        dados["cep"],
        dados["logradouro"],
        dados["complemento"],
        dados["bairro"],
        dados["localidade"],
        dados["uf"]
    )

    cursor.execute(sql, valores)
    conexao.commit()

    print("\n✔ Dados salvos no MySQL com sucesso!")

except mysql.connector.Error as erro:
    print("Erro ao conectar ou inserir no MySQL:", erro)

finally:
    if 'conexao' in globals() and conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão com MySQL encerrada.")
