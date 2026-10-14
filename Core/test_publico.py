from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Marca, Producto


class InventarioPublicoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.audio = Categoria.objects.create(nombre='Audio')
        cls.cuerdas = Categoria.objects.create(nombre='Cuerdas')
        cls.marca = Marca.objects.create(nombre='Marca musical')
        cls.disponible = Producto.objects.create(codigo='AMP-01', nombre='Amplificador', categoria=cls.audio, marca=cls.marca, ubicacion='A1', cantidad=20, stock_minimo=5)
        cls.bajo = Producto.objects.create(codigo='GTR-01', nombre='Guitarra', categoria=cls.cuerdas, ubicacion='B2', cantidad=3, stock_minimo=5)
        cls.agotado = Producto.objects.create(codigo='MIC-01', nombre='Microfono', categoria=cls.audio, ubicacion='C1', cantidad=0, stock_minimo=2)

    def test_visitante_ve_datos_reales_y_totales(self):
        r = self.client.get('/')
        self.assertContains(r, 'Amplificador')
        self.assertEqual(r.context['resumen'], dict(referencias=3, unidades=23, disponibles=2, reponer=2))
        self.assertNotContains(r, 'Registrar producto')

    def test_busqueda_categoria_y_estado_combinados(self):
        r = self.client.get('/', {'q': 'Marca musical', 'categoria': self.audio.pk, 'estado': 'disponible'})
        self.assertEqual(list(r.context['pagina']), [self.disponible])
        for estado, esperados in [('bajo', [self.bajo]), ('agotado', [self.agotado])]:
            r = self.client.get('/', {'estado': estado})
            self.assertEqual(list(r.context['pagina']), esperados)

    def test_parametros_invalidos_y_sin_resultados(self):
        r = self.client.get('/', {'categoria': '9' * 100, 'orden': 'incorrecto', 'estado': 'invalido', 'pagina': 'x'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['pagina'].paginator.count, 3)
        self.assertContains(self.client.get('/', {'q': 'no-existe'}), 'No encontramos productos')

    def test_paginacion_conserva_busqueda_y_orden(self):
        Producto.objects.bulk_create([Producto(codigo=f'P-{i}', nombre=f'Prueba {i:02}', categoria=self.audio, ubicacion='A', cantidad=i) for i in range(26)])
        r = self.client.get('/', {'q': 'Prueba', 'orden': 'nombre'})
        self.assertEqual(len(r.context['pagina']), 24)
        self.assertContains(r, 'q=Prueba&amp;orden=nombre&amp;pagina=2')
        r = self.client.get('/', {'q': 'Prueba', 'orden': 'nombre', 'pagina': 2})
        self.assertEqual(len(r.context['pagina']), 2)
        self.assertEqual(r.context['pagina'][0].nombre, 'Prueba 24')

    def test_ficha_publica_no_permite_modificar(self):
        url = reverse('producto_detalle', args=[self.bajo.pk])
        self.assertContains(self.client.get(url), 'Guitarra')
        self.assertNotContains(self.client.get(url), 'Administrar producto')
        self.assertEqual(self.client.post(url, {'cantidad': 999}).status_code, 405)
        self.assertEqual(self.client.post('/').status_code, 405)
        self.bajo.refresh_from_db()
        self.assertEqual(self.bajo.cantidad, 3)
        self.assertEqual(self.client.get('/productos/999999/').status_code, 404)

    def test_contenido_se_escapa_y_estado_vacio(self):
        self.bajo.nombre = '<script>alert(1)</script>'
        self.bajo.save()
        r = self.client.get(reverse('producto_detalle', args=[self.bajo.pk]))
        self.assertContains(r, '&lt;script&gt;alert(1)&lt;/script&gt;')
        Producto.objects.all().delete()
        self.assertContains(self.client.get('/'), 'Tu inventario empieza aquí')

    def test_enlaces_conservan_solo_filtros_validos(self):
        r = self.client.get('/', {'q': '  Amplificador  ', 'estado': 'incorrecto', 'extra': 'descartar'})
        self.assertEqual(r.context['parametros'], 'q=Amplificador')

    def test_buscar_producto_por_ubicacion(self):
        r = self.client.get('/', {'q': 'B2'})
        self.assertEqual(list(r.context['pagina']), [self.bajo])
