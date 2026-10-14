from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe

from .models import Categoria, Producto


@require_safe
def inventario(request):
    q = request.GET.get('q', '').strip()[:120]
    categoria = request.GET.get('categoria', '')
    try:
        categoria = str(int(categoria)) if 0 < int(categoria) < 2**63 else ''
    except (ValueError, TypeError):
        categoria = ''
    estado = request.GET.get('estado', '')
    if estado not in ('disponible', 'bajo', 'agotado'):
        estado = ''
    orden = request.GET.get('orden', 'recientes')
    ordenes = {'recientes': '-id', 'nombre': Lower('nombre'), 'stock': '-cantidad'}
    if orden not in ordenes:
        orden = 'recientes'
    productos = Producto.objects.select_related('categoria', 'marca')
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q) | Q(marca__nombre__icontains=q) | Q(ubicacion__icontains=q))
    if categoria:
        productos = productos.filter(categoria_id=int(categoria))
    if estado == 'disponible':
        productos = productos.filter(cantidad__gt=0)
    elif estado == 'bajo':
        productos = productos.filter(cantidad__gt=0, cantidad__lte=F('stock_minimo'))
    elif estado == 'agotado':
        productos = productos.filter(cantidad=0)
    pagina = Paginator(productos.order_by(ordenes[orden], 'pk'), 24).get_page(request.GET.get('pagina'))
    resumen = Producto.objects.aggregate(
        referencias=Count('id'), unidades=Sum('cantidad', default=0),
        disponibles=Count('id', filter=Q(cantidad__gt=0)),
        reponer=Count('id', filter=Q(cantidad__lte=F('stock_minimo'))),
    )
    # Conserva solo los filtros que realmente se aplicaron.
    params = {key: value for key, value in {
        'q': q, 'categoria': categoria, 'estado': estado, 'orden': orden,
    }.items() if value and (key != 'orden' or value != 'recientes')}
    return render(request, 'Core/inventario.html', {
        'pagina': pagina, 'resumen': resumen, 'categorias': Categoria.objects.order_by('nombre'),
        'q': q, 'categoria_activa': categoria, 'estado': estado, 'orden': orden,
        'filtros_activos': bool(q or categoria or estado), 'parametros': urlencode(params),
    })


@require_safe
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto.objects.select_related('categoria', 'marca'), pk=pk)
    return render(request, 'Core/producto_detalle.html', {'producto': producto})
