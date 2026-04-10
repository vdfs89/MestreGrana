import math
from typing import Dict

class CalculadoraExportacao:
    """
    Calculadora de exportação para produtora e exportadora de papéis.

    Métodos
    -------
    calcular(peso: float, preco: float, tipo_cliente: str) -> float
        Calcula o valor final da remessa com desconto conforme o tipo de cliente.
    """

    def __init__(self):
        """
        Inicializa a tabela de descontos.
        """
        self._tabela_descontos: Dict[str, float] = {
            "Novo cliente": 0.0,
            "Cliente fidelizado": 0.05,
            "Cliente premium": 0.10
        }

    def calcular(self, peso: float, preco: float, tipo_cliente: str) -> float:
        """
        Calcula o valor final da remessa.

        Args:
            peso (float): Peso da carga em toneladas (deve ser > 0).
            preco (float): Preço por tonelada em dólares (deve ser > 0).
            tipo_cliente (str): Tipo de cliente.

        Returns:
            float: Valor final da exportação com desconto.

        Raises:
            ValueError: Se peso ou preço forem menores ou iguais a zero, ou se não forem números válidos.
        """
        if not math.isfinite(peso) or not math.isfinite(preco):
            raise ValueError("Peso e preço devem ser números válidos e finitos.")

        if peso <= 0 or preco <= 0:
            raise ValueError("Peso e preço devem ser maiores que zero.")

        desconto = self._tabela_descontos.get(tipo_cliente, 0.0)
        valor_bruto = peso * preco
        return valor_bruto * (1 - desconto)

if __name__ == "__main__":
    app = CalculadoraExportacao()
    try:
        p_input = input("Peso: ").replace(',', '.')
        pr_input = input("Preço: ").replace(',', '.')

        p = float(p_input)
        pr = float(pr_input)

        cli = input("Tipo de Cliente: ").strip()
        resultado = app.calcular(p, pr, cli)
        print(f"\n✅ Valor Final da Remessa: ${resultado:.2f}")
    except ValueError as e:
        print(f"❌ Erro de Entrada ou Negócio: {e}")
    except Exception as e:
        print(f"⚠️ Erro Inesperado: {e}")
