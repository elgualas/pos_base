from django.shortcuts import render,redirect
from django.views import generic
from .models import Categoria,SubCategoria,Marca,UnidadMedida,Producto
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from .forms import CategoriaForm,SubCategoriaForm,MarcaForm,UMForm,ProductoForm
from bases.views import SinPrivilegios
# Create your views here.

#CATEGORIA
class CategoriaView(SinPrivilegios,generic.ListView):
    permission_required="inv.view_categoria"
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    

class CategoriaNew(SuccessMessageMixin,LoginRequiredMixin,generic.CreateView):
    model=Categoria
    template_name="inv/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("inv:categoria_list")
    success_message="Categoria Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class CategoriaEdit(SuccessMessageMixin,LoginRequiredMixin,generic.UpdateView):
    model=Categoria
    template_name="inv/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("inv:categoria_list")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
    
class CategoriaDel(SuccessMessageMixin,LoginRequiredMixin, generic.DeleteView):
    model=Categoria
    template_name='inv/catalogos_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("inv:categoria_list")
    success_message="Categoría Eliminada Satisfactoriamente"

#Subcategoria

class SubCategoriaView(SinPrivilegios ,generic.ListView):
    permission_required="inv.view_subcategoria"
    model = SubCategoria
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"

class SubCategoriaNew(LoginRequiredMixin,generic.CreateView):
    model=SubCategoria
    template_name="inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy("inv:subcategoria_list")
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class SubCategoriaEdit(LoginRequiredMixin,generic.UpdateView):
    model=SubCategoria
    template_name="inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy("inv:subcategoria_list")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class SubCategoriaDel(LoginRequiredMixin, generic.DeleteView):
    model=SubCategoria
    template_name='inv/catalogos_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("inv:subcategoria_list")
    success_message="SubCategoría Eliminada Satisfactoriamente"

#Marca

class MarcaView(SinPrivilegios,generic.ListView):
    permission_required="inv.view_marca"
    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"
    

class MarcaNew(LoginRequiredMixin,generic.CreateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = "obj"
    form_class=MarcaForm
    success_url=reverse_lazy("inv:marca_list")
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class MarcaEdit(LoginRequiredMixin,generic.UpdateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = "obj"
    form_class=MarcaForm
    success_url=reverse_lazy("inv:marca_list")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url="/login/")
@permission_required("inv.change_marca",login_url="/login/")
def marca_inactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/catalogos_del.html"

    if not marca:
        return redirect("inv:marca_list")

    if request.method=='GET':
        contexto={'obj':marca}
    
    if request.method=='POST':
        marca.estado=False
        marca.save()
        messages.success(request, 'Marca inactivada')
        return redirect("inv:marca_list")
    
    return render(request,template_name,contexto)

#Unidad de medida

class UMView(LoginRequiredMixin,generic.ListView):
    model = UnidadMedida
    template_name = "inv/um_list.html"
    context_object_name = "obj"
    login_url='bases:login'

class UMNew(LoginRequiredMixin,generic.CreateView):
    model=  UnidadMedida
    template_name="inv/um_form.html"
    context_object_name = "obj"
    form_class=UMForm
    success_url=reverse_lazy("inv:um_list")
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class UMEdit(LoginRequiredMixin,generic.UpdateView):
    model=  UnidadMedida
    template_name="inv/um_form.html"
    context_object_name = "obj"
    form_class=UMForm
    success_url=reverse_lazy("inv:um_list")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
    
def um_inactivar(request, id):
    um = UnidadMedida.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/catalogos_del.html"

    if not um:
        return redirect("inv:um_list")

    if request.method=='GET':
        contexto={'obj':um}
    
    if request.method=='POST':
        um.estado=False
        um.save()
        return redirect("inv:um_list")
    
    return render(request,template_name,contexto)

#Producto

class ProductoView(LoginRequiredMixin,generic.ListView):
    model = Producto
    template_name = "inv/producto_list.html"
    context_object_name = "obj"
    login_url='bases:login'

class ProductoNew(LoginRequiredMixin,generic.CreateView):
    model=  Producto
    template_name="inv/producto_form.html"
    context_object_name = "obj"
    form_class=ProductoForm
    success_url=reverse_lazy("inv:producto_list")
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class ProductoEdit(LoginRequiredMixin,generic.UpdateView):
    model=  Producto
    template_name="inv/producto_form.html"
    context_object_name = "obj"
    form_class=ProductoForm
    success_url=reverse_lazy("inv:producto_list")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
    
def producto_inactivar(request, id):
    prod = Producto.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/catalogos_del.html"

    if not prod:
        return redirect("inv:producto_list")

    if request.method=='GET':
        contexto={'obj':prod}
    
    if request.method=='POST':
        prod.estado=False
        prod.save()
        return redirect("inv:producto_list")
    
    return render(request,template_name,contexto)
