from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from django.db import connection
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView


# View for getting user's details by id, updating and deleting particular user  
class UserOperationsView(APIView):   
    http_method_names = ['get', 'put', 'delete']
    
    # getting user data by id
    def get(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            data = UserSerializer(user)
            return Response(data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)})

    # updating data of particular user id
    def put(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            data = UserSerializer(instance=user, data=request.data, partial=True)
            if data.is_valid():
                data.save()
                response_data ={
                    "message":"record updated successfully",
                    "status_code":status.HTTP_200_OK
                }
                return Response(response_data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)})
        
    # deleting data of particular user id
    def delete(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            user.delete()
            response_data ={
                "message":"record deleted successfully",
                "status_code":status.HTTP_200_OK
            }
            return Response(response_data,status=status.HTTP_200_OK)        
        except Exception as e:
            return Response({"error":str(e)})


# View for listing user data and creating user
class UserListCreateView(APIView):
    http_method_names = ['get', 'post']

    # getting all user data
    def get(self, request):
        try:
            page = int(request.GET.get('page',1))
            limit = int(request.GET.get('limit',5))
            name = request.GET.get('name','')
            sort = request.GET.get('sort','')
            order = "desc" if sort.startswith('-') else "asc"
            sort = (sort.replace('-',"")).strip()

            from_page = ((page - 1) * limit) + 1 
            to_page = page * limit 
            between_string = f"where rnum between {from_page} and {to_page}"
            search_string = f"and (first_name ilike '%{name}%' or last_name ilike '%{name}%')" 
            sort_column_string  = f" order by {sort} {order}" if sort != '' else ''

            query = f'''WITH sorted_data AS (
                        SELECT *, 
                            ROW_NUMBER() OVER ({sort_column_string}) AS rnum
                        FROM user_user 
                        WHERE 1 = 1 {search_string}  
                    )
                    SELECT DISTINCT id, first_name, last_name, company_name, city, state, zip, email, web, age
                    FROM sorted_data
                    {between_string}
                    {sort_column_string};'''
            
            with connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
                if not data:
                    return JsonResponse([], safe=False)
                
                columns = [col[0] for col in cursor.description]        
                output_dict = [dict(zip(columns, row)) for row in data]

            return JsonResponse(output_dict,status=status.HTTP_200_OK,safe=False)
        
        except Exception as e:
            return Response({"error":str(e)})
     
    # creating user
    def post(self, request):
        try:
            user = UserSerializer(data=request.data)
        
            if User.objects.filter(**request.data).exists():
                raise serializers.ValidationError('This data already exists')
        
            if user.is_valid():
                user.save()
                response_data ={
                    "message":"record created successfully",
                    "status_code":status.HTTP_201_CREATED
                }
                return Response(response_data,status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error":str(e)})
       








