from ..models import Student,Address
from ..utils.CustomAPIException import CustomAPIException
import json
from django.http import request
import traceback
from django.core.serializers import serialize
import pandas as pd
from django.db.models import Count
from django.forms.models import model_to_dict
import logging
from ..utils.LoggerFunction import log_invocation

logger = logging.getLogger('student_app')

@log_invocation
def createStudentRecords(request, data):
    try:
        print(" ===createStudentRecords=== ")
        student_record = data.get('student')       # Access JSON data
        address_record = data.get('address')

        student = Student.objects.create(**student_record)
        for address_data in address_record:
            address_type = address_data['address_type']
            #  # transforming data to retrieve enum value
            address_data['addr_type'] = Address.get_enum_value(address_type)
            del address_data['address_type']    #dropping dict key
            Address.objects.create(student=student,**address_data)
    except Exception as e:
        # Print the exception traceback
        traceback.print_exc()
        raise CustomAPIException(message=str(e), exception=type(e).__name__)
    
def fetchStudentRecords(request, data={}):
    try:

        # students = Student.objects.filter(address__city = 'Mumbai')
        # address = Address.objects.filter(student__name__contains='abcdefg')
        # students = Student.objects.annotate(num_addresses = Count('addresses')).filter(num_addresses__gt=1, addresses__city='Pune').prefetch_related('addresses')
        # address = Address.objects.filter(city__contains = 'Manipur',student__id= 44).prefetch_related('student').values_list('city','student__*')
        # address = Address.objects.filter(student__name__contains='abcdefg')
        # df = Address.convert_df(address)
        # df= pd.DataFrame(address)

        students = Student.objects.filter(name__contains='abcdefg').prefetch_related('address')
        student_df = Student.convert_df(students)
        print(student_df)

        # address_df  = Address.objects.filter(student__in = list(students.id))
        # print(address_df)

        #creating a common wholistic df
        # print(df)
        # df.to_csv('./student_app/ipynb_files/student.csv')    #dump to csv for Jupyter ipynb

        # result = df.to_json(orient='records')
        result ={'message':'Success'}
        return result
    except Exception as e:
        # Print the exception traceback
        traceback.print_exc()
        raise CustomAPIException(message=str(e), exception=type(e).__name__)
    
def fetch_students_package(request,data={}):
    try:
        # fetch all students and associated records
        students_all = Student.objects.filter(name__contains='abcdefg').prefetch_related('addresses')
        #convert the Queryset to individual df
        student_data = []
        address_data = []
        for student in students_all:
            student_data.append(model_to_dict(student))
            address_each_student = student.addresses.all()
            for address in address_each_student:
                address_dict = model_to_dict(address)
                address_dict['student_id'] = student.id
                address_data.append(address_dict)
        student_df = pd.DataFrame(student_data).set_index('id')
        address_df = pd.DataFrame(address_data).set_index('student_id')
        print(student_df)
        print(address_df)

        # creating a combined master list 
        student_address_list = []
        for student_id, student_row in student_df.iterrows():
            student_info = student_row.to_dict()
            try:
                student_info['addresses'] = address_df.loc[student_id].to_dict(orient='records')
            except KeyError:
                student_info['addresses']=[]
            student_address_list.append(student_info)
        result_df = pd.DataFrame(student_address_list)
        print(result_df)
        # convert list to df and then to json
        result_json = result_df.to_json(orient='records')
        result = result_json
        return result
    except Exception as e:
        # Print the exception traceback
        traceback.print_exc()
        raise CustomAPIException(message=str(e), exception=type(e).__name__)

@log_invocation
def fetch_address_with_student(request,data={}):
    try:
        # address = Address.objects.filter(city__contains='Mumbai').prefetch_related('student')
        address = Address.objects.filter(city__contains='Mumbai').select_related('student')
        address_df = Address.convert_df(address).set_index('student_id')
        student_list = []
        # print(address_df)
        for address_record in address:
            student_list.append(Student.convert_dict(address_record.student))
        student_df = pd.DataFrame(student_list).set_index('id')
        print(student_df)
        print(address_df)

        #combine df
        combined_df = pd.merge(student_df,address_df,left_index=True, right_index=True)
        print(combined_df)
        result = combined_df.to_json(orient='records')
        return result
    except Exception as e:
        # Print the exception traceback
        traceback.print_exc()
        raise CustomAPIException(message=str(e), exception=type(e).__name__)
    
def fetch_students_package_repetitive_blocks(request,data={}):
    try:
        # fetch all students and associated records
        students_all = Student.objects.filter(name__contains='abcdefg').prefetch_related('addresses')
        #convert the Queryset to individual df
        student_df = Student.convert_df(students_all).set_index('id')
        address_list=[]
        for student_record in students_all:
            for address in student_record.addresses.all():
                address_list.append(Address.convert_dict(address))
        address_df = pd.DataFrame(address_list).set_index('student')
        print(student_df)
        print(address_df)
        combined_df= pd.merge(student_df,address_df, left_index= True, right_index=True, how='left')
        print(combined_df)

        result = combined_df.to_json(orient='records')
        return result
    except Exception as e:
        # Print the exception traceback
        traceback.print_exc()
        raise CustomAPIException(message=str(e), exception=type(e).__name__)


