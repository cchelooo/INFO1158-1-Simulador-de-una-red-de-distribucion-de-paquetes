import unittest

from flujo import calcular_flujo_maximo
from red import Red


class PruebasFlujoMaximo(unittest.TestCase):
    def test_redirige_flujo_por_un_arco_residual_inverso(self):
        red = Red(
            ("S", "A", "B", "C", "D", "T"),
            (
                ("S", "A", 1),
                ("S", "B", 1),
                ("A", "C", 1),
                ("A", "D", 1),
                ("B", "C", 1),
                ("C", "T", 1),
                ("D", "T", 1),
            ),
        )

        # BFS toma primero S-A-C-T. El segundo aumento usa C-A para
        # cancelar el flujo en A-C y dejar pasar S-B-C-T y S-A-D-T.
        valor, flujos = calcular_flujo_maximo(red, "S", "T")

        self.assertEqual(valor, 2)
        self.assertEqual(flujos["A", "C"], 0)
        self.assertNotIn(("C", "A"), flujos)
