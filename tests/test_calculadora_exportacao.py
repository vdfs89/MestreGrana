import unittest
from produtora_exportadora_papeis import CalculadoraExportacao

class TestCalculadoraExportacao(unittest.TestCase):
    def setUp(self):
        self.calc = CalculadoraExportacao()

    def test_novo_cliente(self):
        self.assertAlmostEqual(self.calc.calcular(10, 500, "Novo cliente"), 5000.00, places=2)

    def test_cliente_fidelizado(self):
        self.assertAlmostEqual(self.calc.calcular(8, 600, "Cliente fidelizado"), 4560.00, places=2)

    def test_cliente_premium(self):
        self.assertAlmostEqual(self.calc.calcular(12, 400, "Cliente premium"), 4320.00, places=2)

    def test_tipo_cliente_invalido(self):
        # Deve aplicar desconto 0.0 para tipo desconhecido
        self.assertAlmostEqual(self.calc.calcular(5, 100, "Outro"), 500.00, places=2)

    def test_peso_negativo(self):
        with self.assertRaises(ValueError):
            self.calc.calcular(-1, 100, "Novo cliente")

    def test_preco_negativo(self):
        with self.assertRaises(ValueError):
            self.calc.calcular(1, -100, "Novo cliente")

    def test_peso_nan(self):
        with self.assertRaises(ValueError):
            self.calc.calcular(float('nan'), 100, "Novo cliente")

    def test_preco_inf(self):
        with self.assertRaises(ValueError):
            self.calc.calcular(10, float('inf'), "Novo cliente")

if __name__ == "__main__":
    unittest.main()
