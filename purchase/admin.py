""" Admin configuration for Purchases app """

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.forms import ModelForm, ChoiceField
from django.forms.models import BaseInlineFormSet
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from purchase.models import Order, OrderLine, Purchase, PurchaseLine
from product.models import ProductInstance


class ActiveValueFilter(admin.SimpleListFilter):
    """ Show only list_filter options which is presented in queryset """
    title = _('Order status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of Order.STATUS_CHOICES without InCart status.
        """
        qs = model_admin.get_queryset(request)
        statuses_list = []
        for status in Order.STATUS_CHOICES[1:]:
            if qs.filter(status=status[0]).exists():
                statuses_list.append(status)
        return statuses_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            return queryset.all()
        return queryset.filter(status=self.value())


class PurchaseLineInline(admin.TabularInline):

    model = PurchaseLine
    fields = ['cylinder', 'diopter', 'quantity', 'unit_price']
    autocomplete_fields = ['cylinder', 'diopter']
    extra = 0
    show_change_link = True


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """ Admin settings for Purchase table """
    list_display = [
        "invoice_number",
        "invoice_date",
        "value",
        "created_by",
    ]
    fieldsets = [
        (None, {'fields': [('invoice_number', 'invoice_date'),
                           ('value'),
                           ('created_by'),
                           ('date_created', 'date_updated'),
                           ]})
    ]
    readonly_fields = [
        "created_by",
        "date_created",
        "date_updated",
    ]
    search_fields = ['invoice_number', 'value']
    date_hierarchy = 'invoice_date'
    list_filter = ('created_by',)
    ordering = ('-date_created',)
    inlines = [PurchaseLineInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class OrderLineInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        for form in self.forms:
            # check if form is valid
            if not form.is_valid():
                return

            # get data from form
            quantity = form.cleaned_data.get('quantity')
            diopter = form.cleaned_data.get('diopter')
            cylinder = form.cleaned_data.get('cylinder')

            # get stock of product from form
            product = ProductInstance.objects.get(cylinder=cylinder, diopter=diopter)

            # check stock of product
            quantity_in_hand = product.quantity_in_hand
            if form.instance.pk and form.instance.product == product:
                quantity_in_hand += form.instance.last_quantity

            # validation error if quality = 0
            if quantity == 0:
                msg = _('Quantity must be more then 0')
                form._errors["quantity"] = self.error_class([msg])

            # validation error if not enough in stock
            if quantity > quantity_in_hand:
                msg = _('Product is not enough in stock. Available - {}').format(quantity_in_hand)
                form._errors["quantity"] = self.error_class([msg])

            # check instance is existing and product was changed
            form.instance.__product_changed__ = False
            if form.instance.pk:
                if form.instance.product != product:
                    form.instance.__product_changed__ = True
                    form.instance.__previous_product__ = form.instance.product


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    formset = OrderLineInlineFormSet
    fields = ['cylinder', 'diopter', 'quantity', 'unit_price']
    readonly_fields = ['unit_price']
    autocomplete_fields = ['cylinder', 'diopter']
    extra = 0
    show_change_link = True


class OrderAdminForm(ModelForm):
    """ Exclude Order.InCart from STATUS_CHOICES field """
    class Meta:
        model = Order
        fields = "__all__"

    status = ChoiceField(
        choices=Order.STATUS_CHOICES[1:]
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Admin settings for Order table """
    form = OrderAdminForm
    list_display = [
        "customer",
        "status",
        "invoice_number",
        "invoice_date",
        "value",
        "created_by",
    ]
    readonly_fields = [
        "value",
        "invoice_number",
        "invoice_date",
        "created_by",
        "date_created",
        "date_updated",
    ]
    search_fields = ['invoice_number', 'value']
    date_hierarchy = 'invoice_date'
    list_filter = (ActiveValueFilter, ('customer', RelatedDropdownFilter))
    ordering = ('-date_created',)
    inlines = [OrderLineInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(status=Order.InCart)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set created_by during the first save.
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # get stock of product from form
            product = ProductInstance.objects.get(cylinder=instance.cylinder, diopter=instance.diopter)
            quantity_in_hand = product.quantity_in_hand

            # set product and unit_price
            if not instance.pk or instance.__product_changed__:
                instance.product = product
                instance.unit_price = instance.product.price

            # if product was changed add previous_quantity to previous_product
            if instance.__product_changed__:
                instance.__previous_product__.quantity_in_hand += instance.last_quantity
                instance.__previous_product__.save()

            # reduce stocks
            if instance.__product_changed__:
                instance.product.quantity_in_hand -= instance.quantity
            else:
                instance.product.quantity_in_hand -= instance.quantity - instance.last_quantity

            instance.product.save()

        # if product was deleted add previous_quantity to it
        for obj in formset.deleted_objects:
            product = ProductInstance.objects.get(pk=obj.product.pk)
            product.quantity_in_hand += obj.quantity
            product.save()

        super().save_formset(request, form, formset, change)


    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.value = form.instance.value_total()
        form.instance.save()
