""" Admin configuration for Purchases app """

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.forms import ModelForm, ChoiceField
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from purchase.models import Order, OrderLine, Purchase, PurchaseLine
from product.models import Cylinder, DiopterPower


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


class OrderLineInline(admin.TabularInline):

    model = OrderLine
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
            # Only set added_by during the first save.
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
