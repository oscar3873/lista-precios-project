from django.contrib import admin
from .models import Provincia, Sucursal, CategoriaProveedor, Proveedor, ProveedorSucursal, TipoArticulo, Articulo, TipoLista, Lista, HistorialPrecio, ArticuloLista
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models

# Inlines
class SucursalInline(admin.TabularInline):
    model = Sucursal
    extra = 1

class ProveedorSucursalInline(admin.TabularInline):
    model = ProveedorSucursal
    extra = 1
    autocomplete_fields = ['proveedor', 'sucursal']

class ArticuloListaInline(admin.TabularInline):
    model = ArticuloLista
    extra = 1
    autocomplete_fields = ['articulo', 'lista']

# Admin registration
@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    inlines = [SucursalInline]
    search_fields = ['nombre']

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'provincia']
    list_filter = ['provincia']
    search_fields = ['nombre', 'provincia__nombre']
    autocomplete_fields = ['provincia']

@admin.register(CategoriaProveedor)
class CategoriaProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nombre', 'categoria__nombre']
    inlines = [ProveedorSucursalInline]

@admin.register(TipoArticulo)
class TipoArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo']
    list_filter = ['tipo']
    search_fields = ['tipo__nombre']
    inlines = [ArticuloListaInline]

@admin.register(TipoLista)
class TipoListaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ['tipo_lista', 'provincia', 'proveedor']
    list_filter = ['tipo_lista', 'provincia', 'proveedor']
    search_fields = ['tipo_lista__nombre', 'provincia__nombre', 'proveedor__nombre']
    inlines = [ArticuloListaInline]

@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ['articulo_lista', 'precio', 'fecha_inicio', 'fecha_fin']
    search_fields = ['precio', 'fecha']

# Nota: Para ArticuloLista, como ya está incluido como un inline, puede que no necesites registrarla directamente a menos que quieras administrarla de forma independiente.
