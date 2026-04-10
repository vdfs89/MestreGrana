import unittest
from decimal import Decimal
from examples.Salario import FolhaPagamento

class TestFolhaPagamento(unittest.TestCase):
    def setUp(self):
        self.folha = FolhaPagamento()

    def test_salario_negativo(self):
        with self.assertRaises(ValueError) as cm:
            self.folha.processar("-1000.00", "100.00")
        self.assertIn("Salário e benefícios não podem ser negativos.", str(cm.exception))

    def test_beneficios_negativos(self):
        with self.assertRaises(ValueError) as cm:
            self.folha.processar("1000.00", "-100.00")
        self.assertIn("Salário e benefícios não podem ser negativos.", str(cm.exception))

    def test_processamento_valido(self):
        res = self.folha.processar("2000,00", "500.00")
        self.assertEqual(res["bruto"], Decimal("2000.00"))
        self.assertEqual(res["beneficios"], Decimal("500.00"))
        # 2000 is between 1100 and 2500, so 10% tax -> 200.00
        self.assertEqual(res["imposto"], Decimal("200.00"))
        # 2000 - 200 + 500 = 2300
        self.assertEqual(res["liquido"], Decimal("2300.00"))

    def test_valores_invalidos(self):
        with self.assertRaises(ValueError) as cm:
            self.folha.processar("abc", "100")
        self.assertIn("Erro no processamento dos dados", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
