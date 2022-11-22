####################################################
INICIO DE PROYECTO
####################################################

> py -m venv venv
> .\venv\Scripts\activate
> py -m pip install --upgrade pip
> pip install -r .\requirements.txt

####################################################
INICIO DE SERVIDORES
####################################################

Iniciar servidor de la institución
> cd .\API\
> py .\manage.py runserver 8000


Iniciar servidor de la pasarela
> cd .\API_PASSARELLA\
> py .\manage.py runserver 8010


Iniciar servidor del banco
> cd ..\API_BANK\
> py .\manage.py runserver 8020

####################################################
PROCESO DE PAGO
####################################################

(Institución)

1. Ver información de la institución (home)
    # http://localhost:8000/api/institution/ (GET)

2. Inicio de sesión del estudiante
    # http://localhost:8000/api/user/login (POST)

    {
        "username": "Dylanc",
        "password": "1234"
    }

    Guardar token access y colocarlo como header

3. Ver perfil del estudiante
    # http://localhost:8000/api/institution/student/profile (GET)

4. Ver servicios pagados y no pagados del estudiante
    # http://localhost:8000/api/institution/student/bills (GET)

5. Ver solo servicios que le falta por pagar a estudiante
    # http://localhost:8000/api/institution/student/bills_to_pay (GET)

6. Comenzar proceso de pago
    # http://localhost:8000/api/institution/student/bills_to_pay (POST)

    Se ingresan los id de los servicisos que se quieren pagar

    {
        "bills": [2]
    }

(Pasarela)

7. Obtención de la información de pago desde el servicio de la pasarela
    # http://localhost:8010/api/passarella/pay/<int:id> (GET)

8. Ingreso de datos de llenado de la fase 1 de la pasarela
    # http://localhost:8010/api/passarella/phase2 (POST)

    {
        "bank": "EB",
        "name": "Dylan",
        "lastname": "Cantillo",
        "number_id": "1001820511",
        "phone": "1234567890",
        "phase1": 4
    }

(Banco)

8.1 Inisio de sesión en el banco para proceso de consulta de tarjetas
    # http://localhost:8020/api/user/login (POST)

    {
        "username": "dysaca",
        "password": "1234"
    }

8.2 Consulta de tarjetas en el banco
    # http://localhost:8020/api/bank/service/pay_consult (GET)

    {
        "bank": "EB"
    }

9 Inisio de sesión en el banco para proceso de pago
    # http://localhost:8020/api/user/login (POST)

    {
        "username": "dysaca",
        "password": "1234"
    }

10. Obtención datos de la vista para pago en el banco
    # http://localhost:8020/api/bank/service/pay_consult (GET)

    {
        "bank": "EB",
        "conn_with_bank_id": "q9HpdiQS0n3P7a98TQ0mtS4wnfsQso9U"
    }

11. Ingreso de datos para pago
    # http://localhost:8020/api/bank/service/transaction (POST)

    {
        "conn_with_bank_id": "q9HpdiQS0n3P7a98TQ0mtS4wnfsQso9U",
        "card": "7833763455434912"
    }

12. Ver transacciones de la persona
    # http://localhost:8020/api/bank/service/transaction_list (GET)

(Institución)

12. Revisión de cambios en las cuentas de la institución 
    # http://localhost:8000/api/institution/student/bills (GET)