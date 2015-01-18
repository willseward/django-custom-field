from django import forms
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes import generic

from .models import CustomField, CustomFieldValue


class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable


class CustomFieldModel(object):
    """
    Abstract class adds some helper functions a Model
    """
    @property
    def get_custom_fields(self):
        """ Return a list of custom fields for this model """
        return CustomField.objects.filter(
            content_type=ContentType.objects.get_for_model(self))

    def get_model_custom_fields(self):
        """ Return a list of custom fields for this model, directly callable
        without an instance. Use like Foo.get_model_custom_fields(Foo)
        """
        return CustomField.objects.filter(
            content_type=ContentType.objects.get_for_model(self))
    get_model_custom_fields = Callable(get_model_custom_fields)

    def get_custom_field(self, field_name):
        """ Get a custom field object for this model
        field_name - Name of the custom field you want.
        """
        content_type = ContentType.objects.get_for_model(self)
        return CustomField.objects.get(
            content_type=content_type, name=field_name)

    def get_custom_value(self, field_name):
        """ Get a value for a specified custom field
        field_name - Name of the custom field you want.
        """
        custom_field = self.get_custom_field(field_name)
        return CustomFieldValue.objects.get_or_create(
            field=custom_field, object_id=self.id)[0].value

    def set_custom_value(self, field_name, value):
        """ Set a value for a specified custom field
        field_name - Name of the custom field you want.
        value - Value to set it to
        """
        custom_field = self.get_custom_field(field_name)
        custom_value = CustomFieldValue.objects.get_or_create(
            field=custom_field, object_id=self.id)[0]
        custom_value.value = value
        custom_value.save()


class CustomFieldValueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomFieldValueForm, self).__init__(*args, **kwargs)
        if self.instance:
            try:
                if self.instance.field.field_type == "b":
                    check_choices = (('True', 'True'), ('False', 'False'))
                    self.fields['value'] = forms.ChoiceField(choices=check_choices)
            except ObjectDoesNotExist:
                pass


class CustomInline(generic.GenericTabularInline):
    model = CustomFieldValue
    form = CustomFieldValueForm
    can_delete = False
    readonly_fields = ('field',)
    fields = ('field', 'value')
    extra = 0
    max_num = 0

    def has_change_permission(self, request, obj=None):
        """ Need to always allow changing custom values """
        return True


class CustomFieldAdmin(ModelAdmin):
    """ Abstract class addes functionality to deal with custom fields in
    Django admin.
    """
    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    def get_inline_instances(self, request, obj=None):
        inline_instances = []

        inlines = self.inlines
        if CustomInline not in inlines:
            inlines += [CustomInline]

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not isinstance(inline, CustomInline):
                    if not (inline.has_add_permission(request) or
                            inline.has_change_permission(request) or
                            inline.has_delete_permission(request)):
                        continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)
        return inline_instances

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            content_type = ContentType.objects.get_for_model(obj)
            custom_fields = CustomField.objects.filter(
                content_type=content_type)
            for custom_field in custom_fields:
                try:
                    field_value, created = CustomFieldValue.objects.get_or_create(
                        content_type=content_type,
                        object_id=obj.id,
                        field=custom_field,
                    )
                except IntegrityError:
                    # This can happen because content_type is really a
                    # cache field and didn't always exist
                    field_value, created = CustomFieldValue.objects.get_or_create(
                        object_id=obj.id,
                        field=custom_field,
                    )
                    field_value.content_type = content_type
                    field_value.save()
                if created:
                    if field_value.field.default_value:
                        field_value.value = field_value.field.default_value
                        field_value.save()
        return super(CustomFieldAdmin, self).get_form(request, obj, **kwargs)
