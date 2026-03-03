# 01 - Documentação do Agente FinanceForge

## Visão Geral
O FinanceForge é um agente financeiro consultivo, resiliente e anti-alucinação, desenvolvido para o desafio Santander DIO. Utiliza dados reais mockados, failover multi-LLM e interface acessível.

## Persona
Cliente: João Silva
Perfil: Conservador, busca orientação para investir com segurança.

## Diagrama de Arquitetura (Mermaid)

```mermaid
graph TD
    subgraph Usuário
        U1[João Silva]
    end
    subgraph Interface
        S1[Streamlit]
        A1[Áudio TTS]
    end
    subgraph Agente
        AG1[FinanceForge]
        F1[Failover LLM]
        R1[RAG]
    end
    subgraph Dados
        D1[transacoes.csv]
        D2[perfil_investidor.json]
    end
    U1 --> S1
    S1 --> AG1
    AG1 --> F1
    AG1 --> R1
    R1 --> D1
    R1 --> D2
    AG1 --> A1
```

## Fluxo
1. Usuário interage via chat/voz
2. Agente consulta dados mockados
3. Resposta gerada por LLM (com failover)
4. Sugestão proativa e áudio
