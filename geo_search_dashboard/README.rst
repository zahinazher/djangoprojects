=====
Filterable Search Dashboard
=====

Filterable Search Dashboard is a Django app to filter data from DB sqlite3.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "searchdata" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'searchdata',
    ]

2. Include the index URLconf in your project urls.py like this::

    path('index/', include('index.urls')),

3. Run ``python manage.py migrate`` to create the Searchdata models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/index/ to apply filter to fetch data via ajax calls.