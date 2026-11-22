import unittest

from flujo import calcular_flujo_maximo, calcular_flujo_y_corte
from red import CENTROS_INICIALES, RUTAS_INICIALES, Red


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

    def test_tres_configuraciones_del_informe(self):
        inicial = Red(CENTROS_INICIALES, RUTAS_INICIALES)
        inicial.validar_configuracion_inicial("A", "J")
        sin_ruta = Red(CENTROS_INICIALES, RUTAS_INICIALES)
        sin_ruta.desactivar_ruta("A", "B")
        con_aumento = Red(CENTROS_INICIALES, RUTAS_INICIALES)
        con_aumento.modificar_capacidad("A", "C", 12)

        casos = (
            ("Inicial", inicial, 14, {("A", "B"): 8, ("A", "C"): 6}),
            ("Sin A-B", sin_ruta, 6, {("A", "C"): 6}),
            ("A-C con 12", con_aumento, 16, {
                ("F", "I"): 4, ("G", "I"): 3, ("H", "J"): 7, ("E", "I"): 2,
            }),
        )
        for nombre, red, esperado, arcos_esperados in casos:
            with self.subTest(configuracion=nombre):
                valor, flujos, corte = calcular_flujo_y_corte(red, "A", "J")
                self.assertEqual(valor, esperado)
                self.assertEqual(corte["arcos"], arcos_esperados)
                self.assertEqual(corte["capacidad"], valor)

                # En el saldo restamos lo que sale y sumamos lo que llega
                saldo = dict.fromkeys(red.centros, 0)
                capacidades = red.rutas_activas()
                self.assertEqual(flujos.keys(), capacidades.keys())
                for (inicio, fin), flujo in flujos.items():
                    self.assertTrue(0 <= flujo <= capacidades[inicio, fin])
                    saldo[inicio] -= flujo
                    saldo[fin] += flujo
                saldo_esperado = dict.fromkeys(red.centros, 0)
                saldo_esperado.update({"A": -valor, "J": valor})
                self.assertEqual(saldo, saldo_esperado)
