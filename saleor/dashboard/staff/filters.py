from django import forms
from django.utils.translation import npgettext, pgettext_lazy
from django_filters import ModelMultipleChoiceFilter, ChoiceFilter, OrderingFilter

from ...account.models import User
from ...core.permissions import get_permissions
from ..customer.filters import UserFilter
from ..forms import PermissionMultipleChoiceField


SORT_BY_FIELDS = (
    ('email', 'email'),
    ('default_billing_address__first_name', 'name'),
    ('default_billing_address__city', 'location'),
    ('is_seller', 'seller'))

SORT_BY_FIELDS_LABELS = {
    'email': pgettext_lazy(
        'Customer list sorting option', 'email'),
    'default_billing_address__first_name': pgettext_lazy(
        'Customer list sorting option', 'name'),
    'default_billing_address__city': pgettext_lazy(
        'Customer list sorting option', 'location'),
    'seller': pgettext_lazy(
        'Customer list sorting option', 'seller')}

IS_SELLER_CHOICES = (
    ('1', pgettext_lazy('Is seller filter choice', 'Seller')),
    ('0', pgettext_lazy('Is seller filter choice', 'Not Seller')))

class PermissionMultipleChoiceFilter(ModelMultipleChoiceFilter):
    field_class = PermissionMultipleChoiceField

class StaffFilter(UserFilter):
    is_seller = ChoiceFilter(
        label=pgettext_lazy('Customer list filter label', 'Is Seller'),
        choices=IS_SELLER_CHOICES,
        empty_label=pgettext_lazy('Filter empty choice label', 'All'),
        widget=forms.Select)
    user_permissions = PermissionMultipleChoiceFilter(
        label=pgettext_lazy('Group list filter label', 'Permissions'),
        field_name='user_permissions',
        queryset=get_permissions())
    sort_by = OrderingFilter(
        label=pgettext_lazy('Staff list filter label', 'Sort by'),
        fields=SORT_BY_FIELDS,
        field_labels=SORT_BY_FIELDS_LABELS)

    class Meta:
        model = User
        fields = []

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard staff members list',
            'Found %(counter)d matching staff member',
            'Found %(counter)d matching staff members',
            number=counter) % {'counter': counter}
