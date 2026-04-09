# Teste de conexão MongoDB Atlas

from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

# Tente ler do .env ou variável de ambiente
MONGO_URI = os.environ.get("MONGODB_ATLAS_URI")
if not MONGO_URI:
    print("Erro: MONGODB_ATLAS_URI não encontrada.")
    exit(1)

try:
    client = MongoClient(MONGO_URI, tls=True)
    dbs = client.list_database_names()
    print("Conexão bem-sucedida! Bancos disponíveis:", dbs)
except Exception as e:
    print("Erro ao conectar no MongoDB Atlas:", e)
