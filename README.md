django-custom-field
===================

Allow end users to create easy (but slower to work with) fields attached to any Django model. Includes support so fields show up in the admin interface and helper functions that make it easy to access any custom fields programmatically.

Does not alter sql when adding a new field. Does not allow you use to custom fields in django ORM mymodel.objects.filter(custom_field_x=Whatever)

 
# Installation

pip install django-custom-field
Add 'custom_field' to settings.INSTALLED_APPS
Optional: Edit the change_form.html and add
   {% include "admin/includes/custom_field_fieldset.html" with custom_form=custom_form %}
to it, probably after fieldsets. If you don't already have a change_form.html you will need to extend contrib.admin's template and place it in /templates/admin/change_form.html
You might even want to further customize this. Here is an example for Grappelli 2.4

{% spaceless %}
{% if custom_form.fields %}
    <div class="grp-group">
        <fieldset class="grp-module">
            <h2 class="collapse-handler">Custom Fields</h2>
            {% for field in custom_form %}
                <div class="grp-row grp-cells-1 {{ custom_form.prefix }}-{{ field.name }}">
                    <div class="column span-4">
                        {{ field.label_tag }}
                    </div>
                    <div class="column span-flexible">
                        {{ field }}
                    </div>  
                </div>
            {% endfor %}
        </fieldset>
    </div>
{% endif %}
{% endspaceless %}
Optional: For shortcut methods to get and set custom fields, extend models you want to use it with like
   from custom_field.custom_field import CustomFieldModel
   class MyModel(CustomFieldModel):
Optional: For admin models you want to have custom fields shown on extend the ModelAdmin? like
   from custom_field.custom_field import CustomFieldAdmin
   class MyModelAdmin(CustomFieldAdmin):
   
#Django-SIS Useage
The custom fields option allows schools additional flexibility with regards to storing information to a particular root model (student, applicants, student worker, etc.). Under Admin > Custom Fields, the custom fields creation screen displays:
![Alt text](https://raw.github.com/burke-software/django-custom-field/master/screencaps/customfield1.png)

For example, for private schools with tuition- they may opt to have a custom boolean field denoting via a check whether or not the student's family will use financial aid, as shown below:


#Custom field options
Three custom field options are available: text, integer and boolean.

