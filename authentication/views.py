from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from psycopg2.extras import RealDictCursor
from django.views.decorators.csrf import csrf_exempt
from db import db_config
import bcrypt
import uuid

SESSION = {}


# Create your views here.
@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        
        username = request.POST.get("username", None)
        password = request.POST.get("password", None).encode("utf-8")

        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        password_string = hash_password.decode("utf-8")

        try:
            connection = db_config.get_connection()

            cursor = connection.cursor(cursor_factory = RealDictCursor)

            query = "INSERT INTO users_tbl(username, password) VALUES(%s, %s, %s, %s, %s)"

            values = [username, password_string]

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

@csrf_exempt
def login(request):
    if request.method == "POST":

        username = request.POST.get("username", None)
        password = request.POST.get("password", None).encode("utf-8")

        try:

            connection = db_config.get_connection()

            cursor = connection.cursor(cursor_factory = RealDictCursor)

            query = "SELECT * FROM users_tbl WHERE username = %s"

            values = [username]

            cursor.execute(query, values)

            connection.commit()

            user = cursor.fetchone()

            if user != None:
                if bcrypt.checkpw(password, user.get("password").encode("utf-8")):

                    SESSION_ID = str(uuid.uuid4())

                    SESSION[SESSION_ID] = user

                    print(SESSION)

                    response = JsonResponse({

                        "message": "Welcome!"

                    }, status = 200)

                    response.set_cookie(

                        key="session_id",
                        value=SESSION_ID,
                        max_age=86400,
                        httponly=True,
                        secure=True
                    )

                    return response

                else:

                    response = JsonResponse({

                        "message": "Pasword Incorect"
                    }, status = 401)

                    return response
            else:
                
                response = JsonResponse({

                    "message": f"No user with username {username}"
                }, status = 401)

                return response

        except Exception as e:

            response = JsonResponse({

                "message": f"{e}"
            }, status = 500)

            return response

