import re
from django import forms
from django.forms import widgets


class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[("0", "Нет"), ("1", "Да")])
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", "Нет"),
            ("1", "Да"),
        ],
    )

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]

        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")

        pattern = re.compile(r"^\d{12}$")
        if not pattern.match(data):
            raise forms.ValidationError("Номер телефона должен содержать 12 цифр.")

        return data

    # Вариант фронтенда в бэкенде, который не используется, но может пригодиться.

    # first_name = forms.CharField(
    #     widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"})
    # )
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "Фамилия"}
    #     )
    # )
    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "Номер телефона"}
    #     )
    # )
    # requires_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", "Нет"),
    #         ("1", "Да"),
    #     ],
    #     initial="0",
    # )
    # delivery_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             "class": "form-control",
    #             "id": "delivery_address",
    #             "rows": "2",
    #             "placeholder": "Адрес доставки",
    #         }
    #     ),
    #     required=False,
    # )
    # payment_on_get = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", "Нет"),
    #         ("1", "Да"),
    #     ],
    #     initial="card",
    # )
