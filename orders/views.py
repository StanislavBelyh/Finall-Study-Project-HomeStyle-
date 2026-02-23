from email import message

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:profile")

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    # Создаем заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data["phone_number"],
                        requires_delivery=form.cleaned_data["requires_delivery"],
                        delivery_address=form.cleaned_data["delivery_address"],
                        payment_on_get=form.cleaned_data["payment_on_get"],
                    )
                    # Создаем элементы заказа на основе товаров в корзине и связываем их с заказом
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.price
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(
                                f"Недостаточно товара {product.name} на складе!\nДоступно: {product.quantity}, запрошено: {quantity}"
                            )

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save(update_fields=["quantity"])

                    # Очищаем корзину после создания заказа
                    cart_items.delete()

                    messages.success(self.request, "Ваш заказ успешно создан!")
                    return redirect("users:profile")
        except ValidationError as e:
            messages.error(self.request, f"Ошибка при создании заказа: {e}")
            return redirect("cart:order")

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании заказа")
        return redirect("orders:create_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HomeStyle - Оформление заказа"
        context["order"] = True
        return context


# @login_required
# def create_order(request):
#     if request.method == "POST":
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     cart_items = Cart.objects.filter(user=request.user)

#                     if cart_items.exists():
#                         # Создаем заказ
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data["phone_number"],
#                             requires_delivery=form.cleaned_data["requires_delivery"],
#                             delivery_address=form.cleaned_data["delivery_address"],
#                             payment_on_get=form.cleaned_data["payment_on_get"],
#                         )
#                         # Создаем элементы заказа на основе товаров в корзине и связываем их с заказом
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             price = cart_item.product.price
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise ValidationError(
#                                     f"Недостаточно товара {product.name} на складе!\nДоступно: {product.quantity}, запрошено: {quantity}"
#                                 )

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#                             product.quantity -= quantity
#                             product.save(update_fields=["quantity"])

#                         # Очищаем корзину после создания заказа
#                         cart_items.delete()

#                         messages.success(request, "Ваш заказ успешно создан!")
#                         return redirect("users:profile")
#             except ValidationError as e:
#                 messages.error(request, f"Ошибка при создании заказа: {e}")
#                 return redirect("cart:order")
#     else:
#         initial = {
#             "first_name": request.user.first_name,
#             "last_name": request.user.last_name,
#         }

#         form = CreateOrderForm(initial=initial)

#     context = {
#         "title": "HomeStyle - Оформление заказа",
#         "form": form,
#         "order": True,
#     }

#     return render(request, "orders/create_order.html", context=context)
