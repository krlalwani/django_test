from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.shortcuts import render
from django.http import JsonResponse
import json
from .db_handlers.createStudents import *
from .utils.CustomAPIException import CustomAPIException
from django.http import request
import pandas as pd
import traceback
from django.core.serializers import serialize
from .utils.LoggerFunction import log_http_request

# Create your views here.
@ensure_csrf_cookie
def startApp(request): #method to get a csrf cookie for subsequent POST requests
    return JsonResponse({'message': 'Success'},status=200)

@csrf_protect
def get_students(request):
    try:
        students = fetch_students_package(request)
        # students = fetch_students_package_repetitive_blocks(request)

        return JsonResponse({'data':json.loads(students)}, safe=False,status=200)
        # return JsonResponse({'message': 'Success'},status=200)
    except CustomAPIException as e:
        return JsonResponse({'status': 'FAILURE','exception': e.exception,'error': e.message}, status=e.status_code)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'FAILURE','exception': type(e).__name__,'error': str(e)}, status=500)

@log_http_request
def get_address(request):
    try:
        address = fetch_address_with_student(request)
        return JsonResponse({'data':json.loads(address)}, safe=False,status=200)
        # return JsonResponse({'message': 'Success'},status=200)
    except CustomAPIException as e:
        return JsonResponse({'status': 'FAILURE','exception': e.exception,'error': e.message}, status=e.status_code)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'FAILURE','exception': type(e).__name__,'error': str(e)}, status=500)

@csrf_protect
def create_students(request):
    try:
        if(request.method != 'POST'): raise CustomAPIException(message='Method Not Supported', status_code=403)
        json_data = request.body.decode('utf-8')   # Read JSON data from request body
        data = json.loads(json_data)    # Parse JSON data
        print(data)

        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        print(df)
        # ## filter and transform the df 
        # ##### sh    
        # ######## OR
        # ####### should you break into multiple df basis json tree and subsequently create a unified json for data update

        # objective: creative a wholistic dataframe for AI
        # from json break into various dataframes with proper referencing
        ## send the df OR JSON to db handlers for updating tables
        createStudentRecords(request, data)
        return JsonResponse({'status': 'SUCCESS'}, status=200)
    except CustomAPIException as e:
        return JsonResponse({'status': 'FAILURE','exception': e.exception,'error': e.message}, status=e.status_code)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'FAILURE','exception': type(e).__name__,'error': str(e)}, status=500)

    
