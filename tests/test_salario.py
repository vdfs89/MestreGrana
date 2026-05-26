import unittest
from decimal import Decimal
from examples.Salario import FolhaPagamento

class TestFolhaPagamento(unittest.TestCase):
    def setUp(self):
        self.folha = FolhaPagamento()

    def test_calcular_imposto_faixa_1(self):
        # 1100.00 * 0.05 = 55.00
        salario = Decimal("1000.00")
        imposto = self.folha.calcular_imposto(salario)
        self.assertEqual(imposto, Decimal("50.00"))

    def test_calcular_imposto_limite_faixa_1(self):
        salario = Decimal("1100.00")
        imposto = self.folha.calcular_imposto(salario)
        self.assertEqual(imposto, Decimal("55.00"))

    def test_calcular_imposto_faixa_2(self):
        # 2000.00 * 0.10 = 200.00
        salario = Decimal("2000.00")
        imposto = self.folha.calcular_imposto(salario)
        self.assertEqual(imposto, Decimal("200.00"))

    def test_calcular_imposto_faixa_3(self):
        # 3000.00 * 0.15 = 450.00
        salario = Decimal("3000.00")
        imposto = self.folha.calcular_imposto(salario)
        self.assertEqual(imposto, Decimal("450.00"))

    def test_processar_com_virgula(self):
        res = self.folha.processar("2000,00", "500,00")
        self.assertEqual(res["bruto"], Decimal("2000.00"))
        self.assertEqual(res["imposto"], Decimal("200.00"))
        self.assertEqual(res["beneficios"], Decimal("500.00"))
        self.assertEqual(res["liquido"], Decimal("2300.00"))

    def test_processar_valores_negativos(self):
        with self.assertRaises(ValueError):
            self.folha.processar("-1000", "500")
        with self.assertRaises(ValueError):
            self.folha.processar("1000", "-500")

    def test_processar_entrada_invalida(self):
        with self.assertRaises(ValueError):
            self.folha.processar("abc", "500")

if __name__ == "__main__":
    unittest.main()
