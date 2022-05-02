1. https://www.askpython.com/django/django-rest-api
2. https://www.askpython.com/django/django-class-based-views
3. http://www.tomchristie.com/rest-framework-2-docs/tutorial/1-serialization




## How to run:


1. Set PROJECT_NAME = 'yourprojectname' , VIR_ENV = 'v3' and etl_script_name (if need) in ```django_prepare_project.py```
2. ```python3 django_prepare_project.py --stage n --appname itemsapp```
Choose stage step by step n = 1 -> 6
```
1: # Creates virtual envs
2: # Crates Project, and an app
3: # Creates dummy app urls, register app in admin.py
4: # Plug app and appurls in project
5: # Make migrations and do migrations
6: # Run project
7: # Run ETL Script
```

Choose project name , app name as per your choice.