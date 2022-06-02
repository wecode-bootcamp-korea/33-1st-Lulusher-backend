import json, re, bcrypt, jwt
from json import JSONDecodeError

from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.views           import View
from django.conf            import settings

from .models         import User

class SignUpView(View):
    def post(self, request): 
        try: 
            input_data     = json.loads(request.body)
            email          = input_data['email']
            EMAIL_REGEX    = r"^[a-zA-Z0-9_-]+@[a-z]+.[a-z]+$"
            PASSWORD_REGEX = r"^(?=.{8,16}$)(?=.*[a-z])(?=.*[0-9]).*$"
            password       = input_data['password']
          
            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "THE_USER_EMAIL_ALREADY_EXISTS"}, status=400)

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message" : "INVALID_EMAIL_--_NEEDS_@_AND_."}, status=400)
         
            if not re.match(PASSWORD_REGEX, password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")

            User.objects.create(
                name            = input_data['name'],
                email           = email,
                password        = hashed_password,
                mobile_number   = input_data['mobile_number'],
                address         = input_data['address'],
                email_subscribe = input_data['email_subscribe']
            ) 
            return JsonResponse({"messsage" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "Key_Error"}, status=400)
    
class SignInView(View):
    def post(self, request):
        try:
<<<<<<< HEAD
            input_data = json.loads(request.body)

            email    = input_data['email']
            password = input_data['password']
            user     = User.objects.get(email = email)

            if bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8)')):
                token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
                return JsonResponse({'message' : "success", 'token' : token}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
=======
            data = json.loads(request.body) 
            
            email    = data['email']
            password = data['password']
            
            user = User.objects.get(email = email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'Message': 'Invalid Password'}, status = 401)
>>>>>>> main

            access_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            
            return JsonResponse({
                "Message"      : "success",
                "Access_token" : access_token
            }, status=200)
            
        except KeyError: 
            return JsonResponse({'Message': 'KEY_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid Email'}, status = 400)
