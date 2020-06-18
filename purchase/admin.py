""" Admin configuration for Purchases app """

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from django.forms import ModelForm, ChoiceField
from django.forms.models import BaseInlineFormSet
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from admin_totals.admin import ModelAdminTotals

from messaging.tasks import send_status_change_email, send_new_order_email
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


class PurchaseLineInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        for form in self.forms:
            # check if form is valid
            if not form.is_valid():
                return

            # get stock of product from form
            product = ProductInstance.objects.get(cylinder=form.instance.cylinder,
                                                  diopter=form.instance.diopter)

            # check stock of product
            quantity_in_hand = product.quantity_in_hand
            if form.instance.pk and form.instance.product == product:
                quantity_in_hand -= form.instance.last_quantity

            # validation error if quality = 0
            if form.instance.quantity == 0:
                msg = _('Quantity must be more then 0')
                form._errors["quantity"] = self.error_class([msg])

            # validation error if not enough in stock
            if form.instance.quantity + quantity_in_hand < 0:
                msg = _('Product is not enough in stock. Available - {}').format(quantity_in_hand)
                form._errors["quantity"] = self.error_class([msg])


class PurchaseLineInline(admin.TabularInline):

    model = PurchaseLine
    formset = PurchaseLineInlineFormSet
    fields = ['diopter', 'cylinder', 'quantity']
    autocomplete_fields = ['cylinder', 'diopter']
    extra = 0
    show_change_link = True


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """ Admin settings for Purchase table """
    list_display = [
        "invoice_number",
        "date_created",
        "created_by",
    ]
    fieldsets = [
        (None, {'fields': ['invoice_number',
                           'date_created',
                           'comment',
                           ]})
    ]
    readonly_fields = [
        "date_created",
    ]

    search_fields = ['invoice_number']
    date_hierarchy = 'date_created'
    list_filter = ('created_by',)
    ordering = ('-date_created',)
    inlines = [PurchaseLineInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(invoice_number="InProcess")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = request.user
            obj.invoice_number = obj.invoice_number_generate()

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # get stock of product from form
            product = ProductInstance.objects.get(cylinder=instance.cylinder, diopter=instance.diopter)

            # if product was changed add previous_quantity to previous_product
            if instance.pk and instance.product != product:
                instance.product.quantity_in_hand -= instance.last_quantity
                instance.product.save()

            # if purchaseline new or product changed - set product and unit_price and reduce stock
            if not instance.pk or instance.product != product:
                instance.product = product
                instance.product.quantity_in_hand += instance.quantity
                instance.unit_price = instance.product.price
            # else product exist and not changed - reduce stock
            else:
                instance.product.quantity_in_hand += instance.quantity - instance.last_quantity

            instance.product.save()

        # if product was deleted add previous_quantity to it
        for obj in formset.deleted_objects:
            product = ProductInstance.objects.get(pk=obj.product.pk)
            product.quantity_in_hand -= obj.quantity
            product.save()

        super().save_formset(request, form, formset, change)

    def delete_model(self, request, obj):
        # if purchase was deleted add previous_quantity to all purchaselines
        for line in obj.purchaseline_set.all():
            product = ProductInstance.objects.get(pk=line.product.pk)
            product.quantity_in_hand -= line.quantity
            product.save()
        super().delete_model(request, obj)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['comment'].help_text = self.instance.customer.comment

    # Exclude Order.InCart from STATUS_CHOICES field
    status = ChoiceField(
        choices=Order.STATUS_CHOICES[1:]
    )

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        self.instance.__status__ = status

        if self.instance.status == Order.NewOrder and \
            status not in [Order.NewOrder, Order.Confirmed, Order.Cancelled]:
            msg = _("New orders status can be changed to Confirmed or Canceled")
            self._errors["status"] = self.error_class([msg])

        if self.instance.status == Order.Confirmed and \
            status not in [Order.Confirmed, Order.Returned]:
            msg = _("Confirmed orders status can be changed only to Returned")
            self._errors["status"] = self.error_class([msg])

        if self.instance.status == Order.Cancelled and status != Order.Cancelled:
            msg = _("Cancelled orders can't be changed")
            self._errors["status"] = self.error_class([msg])

        if self.instance.status == Order.Returned and status != Order.Returned:
            msg = _("Returned orders can't be changed")
            self._errors["status"] = self.error_class([msg])

        if self.instance.status == Order.PreOrder and \
            status not in [Order.PreOrder, Order.NewOrder, Order.Confirmed, Order.Cancelled]:
            msg = _("Preorders status can be changed to NewOrder, Confirmed or Canceled")
            self._errors["status"] = self.error_class([msg])


class OrderLineInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        for form in self.forms:
            # check if form is valid
            if not form.is_valid():
                return

            # get stock of product from form
            product = ProductInstance.objects.get(cylinder=form.instance.cylinder,
                                                  diopter=form.instance.diopter)

            # check stock of product
            quantity_in_hand = product.quantity_in_hand
            if form.instance.pk and form.instance.product == product:
                quantity_in_hand += form.instance.last_quantity

            # validation error if quality = 0
            if form.instance.quantity == 0:
                msg = _('Quantity must be more then 0')
                form._errors["quantity"] = self.error_class([msg])

            # validation error if not enough in stock
            if form.instance.quantity > quantity_in_hand and \
                self.instance.__status__ in [Order.NewOrder, Order.Confirmed]:
                msg = _('Product is not enough in stock. Available - {}').format(quantity_in_hand)
                form._errors["quantity"] = self.error_class([msg])


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    formset = OrderLineInlineFormSet
    fields = ['diopter', 'cylinder', 'quantity', 'unit_price']
    readonly_fields = ['unit_price']
    autocomplete_fields = ['cylinder', 'diopter']
    extra = 0
    show_change_link = True


@admin.register(Order)
class OrderAdmin(ModelAdminTotals):
    """ Admin settings for Order table """

    def status_mark(self, obj):
        if obj.status == Order.NewOrder:
            return format_html('<div style="color:red;">%s</div>' % obj.get_status_display())
        elif obj.status == Order.Confirmed:
            return format_html('<div style="color:blue;">%s</div>' % obj.get_status_display())
        elif obj.status == Order.Returned:
            return format_html('<div style="color:orange;">%s</div>' % obj.get_status_display())
        elif obj.status == Order.PreOrder:
            return format_html('<div style="color:brown;">%s</div>' % obj.get_status_display())
        return obj.get_status_display()
    status_mark.allow_tags = True
    status_mark.short_description = 'Статус'

    form = OrderForm
    list_display = [
        "invoice_number",
        "customer",
        "date_created",
        "status_mark",
        "value",
        "lenses_sum",
        "created_by",
    ]
    list_totals = [('value', Sum), ('lenses_sum', Sum)]
    fieldsets = [
        (None, {'fields': ['customer',
                           'status',
                           'date_created',
                           'invoice_number',
                           'comment',
                           'value',
                           ]})
    ]
    readonly_fields = [
        "value",
        "invoice_number",
        "date_created",
    ]
    search_fields = ['invoice_number', 'value']
    date_hierarchy = 'date_created'
    list_filter = (ActiveValueFilter, ('customer', RelatedDropdownFilter))
    ordering = ('-date_created',)
    inlines = [OrderLineInline]


    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related('customer', 'created_by')
        return qs.exclude(status=Order.InCart)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set created_by during the first save.
            obj.created_by = request.user
            obj.invoice_number = obj.invoice_number_generate()
            # send new order email
            obj.save()
            send_new_order_email.delay(obj.pk)
        else:
            super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # get stock of product from form
            product = ProductInstance.objects.get(cylinder=instance.cylinder, diopter=instance.diopter)

            # if product was changed add previous_quantity to previous_product
            if instance.pk and instance.product != product:
                instance.product.quantity_in_hand += instance.last_quantity
                instance.product.save()

            # if orderline new or product changed - set product and unit_price and reduce stock
            if not instance.pk or instance.product != product:
                instance.product = product
                instance.product.quantity_in_hand -= instance.quantity
                instance.unit_price = instance.product.price
            # else product exist and not changed - reduce stock
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
        # when orderlines saved - calculate order total value
        super().save_related(request, form, formsets, change)
        form.instance.value = form.instance.value_total()
        form.instance.lenses_sum = form.instance.lenses_count()
        #check if order become Cancelled or Returned and restore stocks
        if form.instance.old_status in [Order.NewOrder, Order.Confirmed] and  \
            form.instance.status in [Order.Cancelled, Order.Returned, Order.PreOrder]:
            for line in form.instance.orderline_set.all():
                product = ProductInstance.objects.get(pk=line.product.pk)
                product.quantity_in_hand += line.quantity
                product.save()
        #check if order become NewOrder or Confirmed reduce stocks
        if form.instance.old_status in [Order.Cancelled, Order.Returned, Order.PreOrder] and  \
            form.instance.status in [Order.NewOrder, Order.Confirmed]:
            for line in form.instance.orderline_set.all():
                #change order_type to AvailableOrder
                if line.order_type == OrderLine.PreOrder:
                    line.order_type = OrderLine.AvailableOrder
                    line.save()
                #reduce stocks or product
                product = ProductInstance.objects.get(pk=line.product.pk)
                if product.quantity_in_hand >= line.quantity:
                    product.quantity_in_hand -= line.quantity
                    product.save()
                else:
                    raise ValidationError('Product not enough in stock')
        #check if status changed and send email
        if (form.instance.old_status == Order.NewOrder and \
                form.instance.status in [Order.Cancelled, Order.Confirmed]) or \
                (form.instance.old_status == Order.PreOrder and \
                form.instance.status in [Order.NewOrder, Order.Confirmed, Order.Cancelled]):
            send_status_change_email.delay(form.instance.pk)

        #save status as old_status
        form.instance.old_status = form.instance.status
        form.instance.save()

    def delete_model(self, request, obj):
        # if order was deleted add previous_quantity to all orderlines
        if obj.status not in [Order.Cancelled, Order.Returned]:
            for line in obj.orderline_set.all():
                product = ProductInstance.objects.get(pk=line.product.pk)
                product.quantity_in_hand += line.quantity
                product.save()
        super().delete_model(request, obj)
