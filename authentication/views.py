from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from psycopg2.extras import RealDictCursor
from django.views.decorators.csrf import csrf_exempt
from db import db_config
import bcrypt


# Create your views here.
@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        middle_name = request.POST.get("middle_name", None)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None).encode("utf-8")

        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        password_string = hash_password.decode("utf-8")

        try:
            connection = db_config.get_connection()

            cursor = connection.cursor(cursor_factory = RealDictCursor)

            query = "INSERT INTO users_tbl(first_name, last_name, middle_name, username, password) VALUES(%s, %s, %s, %s, %s)"

            values = [first_name, last_name, middle_name, username, password_string]

            cursor.execute(query, values)

            connection.commit()

            response = JsonResponse({

                "Message": "Sucess!"
            }, status = 200)

            return response

        except Exception as e:

            response = JsonResponse({

                "Error": f"{e}"
            }, status = 400)

            return response


