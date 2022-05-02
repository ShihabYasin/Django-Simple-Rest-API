# Django-Simple-Rest-API
A Simple Django Rest API (JSON formatted)

## How to run:
Give bellow commands.
```
1: python3 django_prepare_project.py --stage 1 --appname itemsapp
2: source v3/bin/activate
3: pip install -r requirements.txt
4: python3 django_prepare_project.py --stage 5 --appname itemsapp
5: Test Api as per below description in "API Endoint Response" section
```



## How to run from scratch:


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

## API Endoint Response:

1.```[GET]: http://127.0.0.1:8000/items/``` 

Returns all available items previously inserted.

```Response:``` 

```json
[
    {
        "id": 1,
        "name": "book",
        "price": 0
    },
    {
        "id": 2,
        "name": "book",
        "price": 0
    },
    {
        "id": 3,
        "name": "book",
        "price": 12
    },
    {
        "id": 4,
        "name": "book",
        "price": 12
    },
    {
        "id": 20,
        "name": "book",
        "price": 12
    }
]
``` 


2. ```[POST] http://127.0.0.1:8000/items/```
With Json Body:
```json
{
    "id": 21,
    "name": "this book",
    "price": 1522
}
``` 

On Success it returns the same as Json body. 

```Response:``` 

```json
{
    "id": 21,
    "name": "this book",
    "price": 1522
}
``` 
3. ```[GET] http://127.0.0.1:8000/item/20``` 
```Response:```  
```json
{
    "id": 20,
    "name": "book",
    "price": 12
}
``` 
4. ```[PUT] http://127.0.0.1:8000/item/20/``` 
With Json Body:
```json
{
    "id": 20,
    "name": "this is updated book",
    "price": 1520
}
``` 
Updates the record accordingly. 
5. ```[DELETE] http://127.0.0.1:8000/item/20/``` 
Deletes the record accordingly.