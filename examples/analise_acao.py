def analisar_acao(abertura: int, fechamento: int) -> str:
    """
    Compara os preços de abertura e fechamento de uma ação.
    Retorna 'ALTA', 'BAIXA' ou 'ESTAVEL'.
    """
    if fechamento > abertura:
        return "ALTA"
    elif fechamento < abertura:
        return "BAIXA"
    else:
        return "ESTAVEL"

def main():
    entrada = input()
    abertura_str, fechamento_str = entrada.split()
    abertura = int(abertura_str)
    fechamento = int(fechamento_str)
    # Validação simples (opcional)
    if abertura <= 0 or fechamento <= 0:
        print("Valores devem ser inteiros positivos.")
        return
    print(analisar_acao(abertura, fechamento))

if __name__ == "__main__":
    main()