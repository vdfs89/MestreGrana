def calcular_imposto(salario):
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Tuple, Dict

class FolhaPagamento:
    """
    Classe para cálculo de folha de pagamento com precisão financeira e tabela dinâmica de impostos.
    """
    def __init__(self):
        # Tabela de faixas: (Limite Máximo, Alíquota)
        self._tabela_imposto: List[Tuple[Decimal, Decimal]] = [
            (Decimal("1100.00"), Decimal("0.05")),
            (Decimal("2500.00"), Decimal("0.10")),
            (Decimal("999999999"), Decimal("0.15"))  # Limite alto para "acima de 2500"
        ]

    def calcular_imposto(self, salario: Decimal) -> Decimal:
        """
        Calcula o imposto devido conforme a tabela de faixas.
        """
        for limite, aliquota in self._tabela_imposto:
            if salario <= limite:
                return (salario * aliquota).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Decimal("0.00")

    def processar(self, salario_base: str, beneficios: str) -> Dict[str, Decimal]:
        """
        Processa o cálculo do pagamento, recebendo valores como string (suporta vírgula ou ponto).
        """
        try:
            s_base = Decimal(salario_base.replace(',', '.'))
            s_ben = Decimal(beneficios.replace(',', '.'))
            if s_base < 0 or s_ben < 0:
                raise ValueError("Salário e benefícios não podem ser negativos.")

            imposto = self.calcular_imposto(s_base)
            liquido = s_base - imposto + s_ben
            return {
                "bruto": s_base,
                "imposto": imposto,
                "beneficios": s_ben,
                "liquido": liquido
            }
        except Exception as e:
            raise ValueError(f"Erro no processamento dos dados: {e}")

def exibir_detalhes_pagamento(res: Dict[str, Decimal]) -> None:
    """
    Exibe os detalhes do pagamento de forma formatada.
    """
    print(f"\n✅ Detalhes do Pagamento:")
    print(f"Salário Bruto:   R$ {res['bruto']:10.2f}")
    print(f"Imposto Retido:  R$ {res['imposto']:10.2f} (-)")
    print(f"Benefícios:      R$ {res['beneficios']:10.2f} (+)")
    print("-" * 35)
    print(f"VALOR A RECEBER: R$ {res['liquido']:10.2f}")

def executar_calculo() -> None:
    """
    Executa o fluxo principal do sistema de folha de pagamento.
    """
    print("--- 💰 Sistema de Folha de Pagamento ---")
    sistema = FolhaPagamento()
    while True:
        try:
            entrada_salario = input("Digite o valor do salário bruto (ex: 2000.00): ")
            entrada_beneficios = input("Digite o valor dos benefícios (ex: 400.00): ")
            res = sistema.processar(entrada_salario, entrada_beneficios)
            exibir_detalhes_pagamento(res)
        except ValueError as e:
            print(f"\n❌ Erro: {e}")

        repetir = input("\nDeseja calcular outro pagamento? (s/n): ").strip().lower()
        if repetir != 's':
            print("\nEncerrando o sistema. Obrigado!")
            break

if __name__ == "__main__":
    executar_calculo()