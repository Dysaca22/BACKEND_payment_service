from requests import put


def update_statud_connection(conn_with_bank, status, number_bill):
    conn_with_bank._status = status
    conn_with_bank.save()

    update_data = {
        'status': status,
        'id': conn_with_bank.passarella_id,
        'number_bill': number_bill,
    }
    put('http://localhost:8010/api/passarella/finallize', data=update_data)