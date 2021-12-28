import json
from uuid import uuid4, UUID
from decimal import Decimal
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import os
from django.urls import reverse
from django.shortcuts import render

from account.account import Account
from database.database import ObjectNotFound
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.ram import AccountDatabaseRAM
from transaction.transaction import Transaction

dbname: str = "postgres"
if dbname == "":
    database = AccountDatabaseRAM()
    print("Using RAM")
else:
    port: int = 5433
    user = "postgres"
    password = "admin"
    host: str = "localhost"
    connection_str = f"dbname={dbname} port={port} user={user} password={password} host={host}"
    database = AccountDatabasePostgres(connection=connection_str)


def accounts_list(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()
    return render(request, "base.html", context={"accounts": accounts})


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")
#     return HttpResponse(content="""
#     {{% include "templates/header.html" }}
#     <html>
#         <body>
#            <h1>Hello, World!</h1>
#            <h3>Try to access <a href="/api/accounts/">/api/accounts/</a></h3>
#         </body>
#     </html>
#     """)

def account_detail(request, id_):
    try:
        account = database.get_object(id_)
        accounts = database.get_objects()
        return render(request, "details.html", context={"account": account, "accounts": accounts})
    except Exception as e:
        return HttpResponse(e)


def post_account(request):
    try:
        choice = request.POST["currency"]
        id_ = uuid4()
        account = Account(
            id_= id_,
            currency= choice,
            balance=Decimal(0),
        )
        database.save(account)
        return HttpResponseRedirect(reverse('account_detail', args=(id_,)))
    except Exception as e:
        return HttpResponse(e)

def post_trs(request, id_):
    try:
        choice = request.POST["idd"]
        id_ = UUID(choice)
        trs = Transaction(
            id_= id_,
            currency= choice,
        )
        database.save(trs)
        return HttpResponseRedirect(reverse('account_detail', args=(id_,)))
    except Exception as e:
        return HttpResponse(e)



def create_account(request: HttpRequest) -> HttpResponse:
    return render(request, "account_create.html")

def accounts(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()
    if request.method == "GET":
        json_obj = [account.to_json() for account in accounts]
        return HttpResponse(content=json.dumps(json_obj))

    if request.method == "POST":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            account.id_ = uuid4()
            try:
                database.get_object(account.id_)
                return HttpResponse(content=f"Error: object already exists, use PUT to update", status=400)
            except ObjectNotFound:
                database.save(account)
                return HttpResponse(content=account.to_json_str(), status=201)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)

    if request.method == "PUT":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            database.get_object(account.id_)
            database.save(account)
            return HttpResponse(content="OK", status=200)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)
