# 02 - Base de Conhecimento

## Dados Mockados
- transacoes.csv: Histórico de transações do João Silva
- perfil_investidor.json: Perfil de risco, objetivos e restrições
- produtos_financeiros.json: Produtos disponíveis
- historico_atendimento.csv: Interações anteriores

## Integração RAG
O agente utiliza RAG para fundamentar respostas, buscando informações nos arquivos acima antes de consultar o LLM.

## Exemplo de Consulta
- Pergunta: "Quais investimentos são recomendados para meu perfil?"
- Resposta: O agente analisa perfil_investidor.json e sugere produtos compatíveis, explicando o racional.