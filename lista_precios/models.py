from django.db import models


# Create your models here.
class Provincia(models.Model):
    nombre = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(
        max_length=50
    )
    provincia = models.ForeignKey(
        'Provincia', 
        on_delete=models.CASCADE,
        related_name='sucursales'  # Nombre de la relación entre Provincia y Sucursal.
    )
    proveedores = models.ManyToManyField(
        'Proveedor',
        related_name='sucursales',
        through='ProveedorSucursal',
    )
    def __str__(self):
        return self.nombre + " - " + self.provincia.nombre


class CategoriaProveedor(models.Model):
    nombre = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(
        max_length=50
    )
    categoria = models.ForeignKey(
        'CategoriaProveedor',
        on_delete=models.CASCADE,
        related_name='proveedores',  # Nombre de la relación entre CategoriaProveedor y Proveedor.
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nombre
    

class ProveedorSucursal(models.Model):
    proveedor = models.ForeignKey(
        'Proveedor',
        on_delete=models.CASCADE,
        related_name='proveedor_sucursal'  # Nombre de la relación entre Proveedor y ProveedorSucursal.
        
    )
    sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        related_name='sucursal_proveedor'  # Nombre de la relación entre Sucursal y ProveedorSucursal.
    )
    
    # Añade related_name únicos para evitar conflictos
    lista_chatarra = models.ForeignKey(
        'Lista',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='proveedor_sucursal_chatarra',  # Nombre único para el accesor inverso
    )
    lista_metales = models.ForeignKey(
        'Lista',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='proveedor_sucursal_metales',  # Nombre único para el accesor inverso
    )
    
    def __str__(self):
        return self.proveedor.nombre + " - " + self.sucursal.nombre


class TipoArticulo(models.Model):
    nombre = models.CharField(
        max_length=50
    )
    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    nombre = models.CharField(
        max_length=50
    )
    tipo = models.ForeignKey(
        'TipoArticulo',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='articulos'
    )
    
    def __str__(self):
        return self.nombre + " - " + str(self.tipo)


class TipoLista(models.Model):
    nombre = models.CharField(
        max_length=50
    )
    
    def __str__(self) -> str:
        return self.nombre


class Lista(models.Model):
    tipo_lista = models.ForeignKey(
        'TipoLista',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='listas'
    )
    provincia = models.ForeignKey(
        'Provincia',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='listas'
    )
    proveedor = models.OneToOneField(
        'ProveedorSucursal',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lista_mayorista'
    )
    
    def __str__(self) -> str:
        if self.proveedor:
            return str(self.tipo_lista) + " - " + self.provincia.nombre + " - " + self.proveedor.proveedor.nombre + " - " + self.proveedor.sucursal.nombre
        else:
            return str(self.tipo_lista) + " - " + self.provincia.nombre
            


class HistorialPrecio(models.Model):
    articulo_lista = models.ForeignKey(
        'ArticuloLista', 
        on_delete=models.CASCADE, 
        related_name='historial_precios'
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    fecha_inicio = models.DateField(
        null=True,
        blank=True
    )
    fecha_fin = models.DateField(
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.articulo_lista} - {self.precio} desde {self.fecha_inicio}"


class ArticuloLista(models.Model):
    articulo = models.ForeignKey(
        'Articulo',
        on_delete=models.CASCADE,
        related_name='articulos_lista'
    )
    lista = models.ForeignKey(
        'Lista',
        on_delete=models.CASCADE,
        related_name='articulos_lista'
    )
    
    def __str__(self) -> str:
        return str(self.articulo) + " - " + str(self.lista)