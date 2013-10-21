django-custom-field
===================

Allow end users to create easy (but slower to work with) fields attached to any Django model. Includes support so fields show up in the admin interface and helper functions that make it easy to access any custom fields programmatically.

Does not alter sql when adding a new field. Does not allow you use to custom fields in django ORM mymodel.objects.filter(custom_field_x=Whatever)

[![Build Status](https://travis-ci.org/burke-software/django-custom-field.png?branch=master)](https://travis-ci.org/burke-software/django-custom-field)
 
# Installation

pip install django-custom-field
Add 'custom_field' to settings.INSTALLED_APPS
Optional: Edit the change_form.html and add

    {% include "admin/includes/custom_field_fieldset.html" with custom_form=custom_form %}

to it, probably after fieldsets. If you don't already have a change_form.html you will need to extend contrib.admin's template and place it in /templates/admin/change_form.html
You might even want to further customize this. Here is an example for Grappelli 2.4

```bash
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
```

Optional: For shortcut methods to get and set custom fields, extend models you want to use it with like

    from custom_field.custom_field import CustomFieldModel
    class MyModel(CustomFieldModel):
   
Optional: For admin models you want to have custom fields shown on extend the ModelAdmin? like

    from custom_field.custom_field import CustomFieldAdmin
    class MyModelAdmin(CustomFieldAdmin):
   
#Django-SIS Useage
The custom fields option allows schools additional flexibility with regards to storing information to a particular model (student, applicants, student worker, etc.). 

Under Admin > Custom Fields, the custom fields creation screen displays:
![Alt text](https://raw.github.com/burke-software/django-custom-field/master/screencaps/customfield1.png)

Required fields:

Name- Refers to the name of the custom field. Note: this name will be visible to other users

Content Type- Designates which model to affix the custom field to. (Student, Alumni, Applicant, Faculty, etc.)

Field Type- Text, Integer, and Boolean- select the type of custom field.

NB: Boolean refers to a simple checkbox. The box can be checked or unchecked when created based on preference. Leave blank for unchecked and enter "1" for checked under the "Default Value" in the creation screen shown above.

#Example
This example will demonstrate custom fields for a school that would like to attach additional information to the incoming applicants page.

In sum, the school wants three additional items of information: who an applicant was referred by, whether or not financial aid is needed, and how many times the applicant has visited the school.

Accordingly, three custom fields will need to be generated under Admin > Custom Fields > Add, formatted as follows:

Who the applicant was referred by:

 
![Alt text](https://raw.github.com/burke-software/django-custom-field/master/screencaps/customfield2.png)

Number of visits to the school:


![Alt text](https://raw.github.com/burke-software/django-custom-field/master/screencaps/customfield3.png)

Whether or not financial aid is needed:


![Alt text](https://raw.github.com/burke-software/django-custom-field/master/screencaps/customfield4.png)

The end result will look like the image below where end users will see the custom fields attached to the Applicant model and can then enter the appropiate information


![Alt text](https://raw.github.com/burke-software/django-custom-field/master/screencaps/customfield5.png)
