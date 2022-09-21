from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from webapp.forms import OrderForm
from webapp.models import Product, Order, OrderProduct


class CartAddView(View):

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        qty = int(self.request.POST.get("qty"))
        if qty > product.amount:
            return HttpResponseBadRequest(
                f"Количество товара {product.name} всего {product.amount}. Добавить {qty} штук не получится")
        else:
            cart = self.request.session.get("cart", {})
            if str(product.pk) in cart:
                cart[str(product.pk)] += qty
            else:
                cart[str(product.pk)] = qty
            self.request.session['cart'] = cart
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("webapp:index")


class CartView(TemplateView):
    template_name = "cart/cart_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})
        products = []
        total = 0
        for pk, qty in cart.items():
            product = Product.objects.get(pk=pk)
            product_total = qty * product.price
            total += product_total
            products.append({"product": product, "qty": qty, "product_total": product_total})
        # products = Product.objects.filter(id__in=cart.keys()).annotate(total=F("price") * cart["pk"])
        context['cart'] = products
        context['total'] = total
        context['form'] = OrderForm()
        return context


class CartDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        cart = self.request.session.get("cart", {})
        if str(pk) in cart:
            cart.pop(str(pk))
            self.request.session['cart'] = cart
        return redirect("webapp:cart")


class CartDeleteOneView(View):
    def get(self, request, pk, *args, **kwargs):
        cart = self.request.session.get("cart", {})
        if str(pk) in cart:
            cart[str(pk)] -= 1
            if cart[str(pk)] < 1:
                cart.pop(str(pk))
            self.request.session['cart'] = cart
        return redirect("webapp:cart")


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        order = form.save(commit=False)
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order.save()
        products = []
        order_products = []
        cart = self.request.session.get("cart", {})
        if cart:
            for pk, qty in cart.items():
                product = Product.objects.get(pk=pk)
                order_products.append(OrderProduct(product=product, qty=qty, order=order))
                product.amount -= qty
                products.append(product)

            OrderProduct.objects.bulk_create(order_products)
            Product.objects.bulk_update(products, ("amount",))
            self.request.session.pop("cart")
        return HttpResponseRedirect(self.success_url)
