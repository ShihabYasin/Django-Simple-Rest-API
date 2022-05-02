#!/usr/bin/env python
import argparse
import os
import shutil, ast

################################################################################
PROJECT_NAME = 'restapitest'
VIR_ENV = 'v3'
etl_script_name = 'scripts/etl.py'  # Change accordingly
add_apps = ['livereload', 'django_extensions']


################################################################################

def add_useful_apps(apps_to_add, project_name):
    a_file = open (project_name + '/settings.py', "r")
    list_of_lines = a_file.readlines ()
    lsstr = ''
    # for x in apps_to_add:
    #     lsstr += "    '" + x + "'" + ',\n'
    lsstr = ''
    for idx, line in enumerate (list_of_lines):
        if 'INSTALLED_APPS' in line:
            # print('Found')
            flag = True
            for x in apps_to_add:
                # print(x)
                for ln in list_of_lines[idx + 1:]:
                    # print(ln.strip())
                    if x in ln.strip ():
                        flag = False
                        break
                    if ']' in ln.strip ():
                        break
                if flag:
                    lsstr += "    '" + x + "'" + ',\n'

            list_of_lines[idx] = line + lsstr
            break

    a_file = open (project_name + '/settings.py', "w")
    a_file.writelines (list_of_lines)
    a_file.close ()


def _add_useful_apps(apps_to_add, project_name):
    a_file = open (project_name + '/settings.py', "r")
    list_of_lines = a_file.readlines ()
    lsstr = ''
    for x in apps_to_add:
        lsstr += "    '" + x + "'" + ',\n'

    for idx, line in enumerate (list_of_lines):
        if 'INSTALLED_APPS' in line:
            list_of_lines[idx] = line + lsstr
            break

    a_file = open (project_name + '/settings.py', "w")
    a_file.writelines (list_of_lines)
    a_file.close ()


def create_virtual_env(virtual_env):
    print (f'Creating virtual env: {virtual_env} ... ')
    if os.path.isdir (virtual_env):
        os.system (f'rm -rf {virtual_env}')
    if not os.path.isdir (virtual_env):
        os.system (f'python3 -m venv {virtual_env}')

    print (f' ===>   PLZ ACTIVATE VIR ENV {virtual_env} ...  <=== ')


def create_a_django_project(project_name, app_name, virtual_env, requirements_file):
    if virtual_env == os.environ.get ("VIRTUAL_ENV").split ('/')[-1]:
        os.system (f'pip install -r {requirements_file}')
        os.system (f'django-admin startproject {project_name} .')
        os.system (f'python manage.py startapp {app_name}')
        os.system (f'python manage.py migrate')
        os.system (f'python manage.py createsuperuser')
        os.system (f'python manage.py check')
        os.system (f'python manage.py runserver')
    else:
        print (f' ===>   PLZ ACTIVATE VIR ENV {virtual_env} ...  <=== ')


def create_appurls_and_register_appmodels_in_app(app_name):
    with open (app_name + '/urls.py', 'w') as f:
        f.writelines (["from django.urls import path\nfrom .views import * # Import/Change as per need \n\n\n", "urlpatterns = [ path ('', ''), ]  # Add URL & Views as per need"])

    def depth_ast(root):
        return 1 + max (map (depth_ast, ast.iter_child_nodes (root)), default=0)

    p = ast.parse (open (f"{app_name}/models.py", "r").read ())
    classes = [node.name for node in ast.walk (p) if isinstance (node, ast.ClassDef) and node.name != 'Meta']
    print (f'Registering Class: {classes} from app {app_name}')
    ls_to_write = []
    with open (app_name + '/admin.py', 'w') as f:
        ls_to_write.append (f"from django.contrib import admin\n")
        for item in classes:
            ls_to_write.append (f"from .models import {item}\n")
        ls_to_write.append (f"\n\n\n\n")
        for item in classes:
            ls_to_write.append (f"admin.site.register({item})\n")

        f.writelines (ls_to_write)  # Add URL & Views as per need"])


def plug_appurls_and_app_in_project(project_name, app_name):
    add_useful_apps (apps_to_add=[app_name], project_name=project_name)
    write = True
    with open (project_name + '/urls.py', 'r') as f:
        for line in f:
            # print(line.strip())
            if "from django.urls import include" == line.strip ():
                write = False
            if not write and f"urlpatterns.append(path('', include('{app_name}.urls')))" in line:
                return

    with open (project_name + '/urls.py', 'a') as f:
        if write:
            f.writelines (["\nfrom django.urls import include\n", f"urlpatterns.append(path('', include('{app_name}.urls')))\n"])
        else:
            f.writelines ([f"\nurlpatterns.append(path('', include('{app_name}.urls')))\n"])


def clear_dir(virtual_env, project_name, app_name):
    try:
        shutil.rmtree (virtual_env)
    except:
        pass
    try:
        os.remove ('manage.py')
    except:
        pass
    try:
        os.remove ('db.sqlite3')
    except:
        pass
    try:
        shutil.rmtree (project_name)
    except:
        pass
    try:
        shutil.rmtree (app_name)
    except:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser ("Give stage count.")
    parser.add_argument ('-s', "--stage", help="Provide setup Stage to be executed.", type=int)
    parser.add_argument ('-a', "--appname", help="Provide app name.", type=str)
    args = parser.parse_args ()
    if args.stage is None:
        print ('Plz provide setup stage e.g. python3 django_prepare_project.py --stage 1 --appname itemsapp')
        exit (0)

    if args.appname is None:
        print ('Plz provide appname e.g. python3 django_prepare_project.py --stage 1 --appname itemsapp')
        exit (0)

    APP_NAME = args.appname
    run_setup_stage = int (args.stage)

    # Init setups
    if run_setup_stage == 1:  # Creates virtual envs
        os.system (f'chmod u+x {os.path.basename (__file__)}')
        clear_dir (virtual_env=VIR_ENV, project_name=PROJECT_NAME, app_name=APP_NAME)
        create_virtual_env (virtual_env=VIR_ENV)

    elif run_setup_stage == 2:  # Crates Project, and an app
        create_a_django_project (virtual_env=VIR_ENV, project_name=PROJECT_NAME, app_name=APP_NAME, requirements_file='requirements.txt')
        add_useful_apps (apps_to_add=add_apps, project_name=PROJECT_NAME)


    # project Specific Setups
    elif run_setup_stage == 3: # Creates dummy app urls, register app in admin.py
        create_appurls_and_register_appmodels_in_app (app_name=APP_NAME)

    elif run_setup_stage == 4:  # Plug app and appurls in project
        plug_appurls_and_app_in_project (project_name=PROJECT_NAME, app_name=APP_NAME)

    elif run_setup_stage == 5:  # Make migrations and do migrations
        os.system ('python manage.py syncdata')
        os.system (f'python manage.py makemigrations {APP_NAME}')
        os.system ('python manage.py migrate')

    # Run , ETL etc.
    elif run_setup_stage == 6:  # Run project
        os.system ('xterm -e nohup python manage.py livereload')  # Reload debug mode
        os.system ('python manage.py runserver')

    elif run_setup_stage == 7:  # Run ETL Script
        os.system (f'python manage.py runscript {etl_script_name}')
