import os
import sys
import pytest

# Defina a DATABASE_URL aqui (não comitar este arquivo se contiver segredos)
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_3vMqVGnYgL0E@ep-damp-heart-acmtin3v-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# Executa pytest com os argumentos passados ao script
args = sys.argv[1:] or ['-q']
ret = pytest.main(args)
# Repassa o código de saída
sys.exit(ret)
