import unittest

from flujo import calcular_flujo_maximo, calcular_flujo_y_corte
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

        # La primera busqueda toma S-A-C-T
        # El segundo aumento usa C-A para cancelar el flujo en A-C
        valor, flujos = calcular_flujo_maximo(red, "S", "T")

        self.assertEqual(valor, 2)
        self.assertEqual(flujos["A", "C"], 0)
        self.assertNotIn(("C", "A"), flujos)

    def test_caso_manual_con_alcance_por_un_arco_residual_inverso(self):
        red = Red(
            ("O", "A", "B", "C", "J"),
            (
                ("O", "A", 1),
                ("O", "B", 2),
                ("A", "C", 1),
                ("B", "C", 1),
                ("B", "J", 1),
                ("C", "J", 1),
            ),
        )

        # Al terminar se llega a A desde O por O-B-C-A
        # El ultimo arco es el inverso residual de A-C
        valor, flujos, corte = calcular_flujo_y_corte(red, "O", "J")

        self.assertEqual(flujos, {
            ("O", "A"): 1,
            ("O", "B"): 1,
            ("A", "C"): 1,
            ("B", "C"): 0,
            ("B", "J"): 1,
            ("C", "J"): 1,
        })
        self.assertEqual(corte, {
            "S": {"O", "A", "B", "C"},
            "T": {"J"},
            "arcos": {("B", "J"): 1, ("C", "J"): 1},
            "capacidad": 2,
        })
        self.assertEqual(valor, corte["capacidad"])
