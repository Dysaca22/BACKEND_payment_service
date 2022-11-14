> py -m venv venv
> .\venv\Scripts\activate
> py -m pip install --upgrade pip
> pip install -r .\requirements.txt

Iniciar servidor de la institución
> cd .\API\
> py .\manage.py runserver 8000

Iniciar servidor del banco
> cd ..\API_BANK\
> py .\manage.py runserver 8080