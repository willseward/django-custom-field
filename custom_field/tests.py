from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import CustomField, CustomFieldValue


class CustomFieldTest(TestCase):
    def test_validation(self):
        custom_field_ct = ContentType.objects.get(app_label="custom_field",
                                                  model="customfield")
        custom_field = CustomField.objects.create(
            name="test_field",
            content_type=custom_field_ct,
            field_type="i",
        )
        custom_value = CustomFieldValue.objects.create(
            field=custom_field,
            value='5.0',
            object_id=custom_field.id,
        )
        custom_value.clean()
        custom_value.save()
        self.assertEquals(custom_value.value, '5')
        custom_value.value = 'fdsf'
        try:
            custom_value.clean()
            self.fail('Was able to save string as custom integer field!')
        except ValidationError:
            pass
