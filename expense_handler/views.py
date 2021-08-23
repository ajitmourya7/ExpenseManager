import datetime

from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from expense_handler.models import Category, Expense
from expense_handler.serializers import CategorySerializer, ExpenseSerializer


def token_verifier(token):
    try:
        return Token.objects.get(key=token)
    except:
        return None


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def user_registration(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username and password:
        if not (User.objects.filter(username=username).count() > 0):
            user = User.objects.create(username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'error': [],
                'data': {
                    'token': token.key,
                    'username': user.username
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': ErrorDetail('User name is Already Exist', code='required')},
                status=status.HTTP_200_OK)
    return Response({
        'error': ErrorDetail('Please Provide Credential', code='required')},
        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def user_login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print(username)
    print(password)
    if username and password:
        user = User.objects.filter(username=username).first()
        if (user is not None) and (user.password == password):
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'error': [],
                'data': {
                    'token': token.key,
                    'username': user.username
                }
            }, status=status.HTTP_200_OK)
    return Response({
        'error': ErrorDetail('Please Provide Proper Credential', code='required')},
        status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_category(request):
    print(request.headers.get('Authorization'))
    t = request.headers.get('Authorization')
    name = request.POST.get('name')
    print("t", t)
    if t:
        check_token = token_verifier(t.replace("Bearer ", ""))
        if check_token:
            if name:
                category, created = Category.objects.get_or_create(name=name, created_by=check_token.user)
                serializer = CategorySerializer(category)
                return Response({
                    'error': [],
                    'data': {
                        'category': [serializer.data]
                    }
                }, status=status.HTTP_200_OK)
    return Response({
        'error': ErrorDetail('Please Provide Proper Credential', code='required')},
        status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def category_list(request):
    print(request.headers.get('Authorization'))
    t = request.headers.get('Authorization')
    check_token = token_verifier(t.replace("Bearer ", ""))
    if check_token:
        category = Category.objects.filter(created_by=check_token.user)
        serializer = CategorySerializer(category, many=True)
        return Response({
            'error': [],
            'data': {
                'category_list': serializer.data
            }
        }, status=status.HTTP_200_OK)
    return Response({
        'error': ErrorDetail('Please Provide Proper Credential', code='required')},
        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def add_expense(request):
    print(request.headers.get('Authorization'))
    t = request.headers.get('Authorization')
    check_token = token_verifier(t.replace("Bearer ", ""))
    if check_token:
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')
        descriptions = request.POST.get('descriptions')
        category_id = request.POST.get('category_id')
        print(amount)
        print(expense_type)
        print(descriptions)
        print(category_id)
        expense = Expense.objects.create(amount=amount,
                                         expense_type=expense_type,
                                         descriptions=descriptions,
                                         category_id=category_id,
                                         created_by=check_token.user)
        serializer = ExpenseSerializer(expense)
        return Response({
            'error': [],
            'data': {
                'expense': serializer.data
            }
        }, status=status.HTTP_200_OK)
    return Response({
        'error': ErrorDetail('Please Provide Proper Credential', code='required')},
        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def view_expense(request):
    print(request.headers.get('Authorization'))
    t = request.headers.get('Authorization')
    check_token = token_verifier(t.replace("Bearer ", ""))
    if check_token:
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y")
            expense = Expense.objects.filter(created_at__range=[start_date, end_date],
                                             created_by=check_token.user)
        else:
            expense = Expense.objects.filter(created_by=check_token.user)
        serializer = ExpenseSerializer(expense, many=True)
        return Response({
            'error': [],
            'data': {
                'expense_list': serializer.data
            }
        }, status=status.HTTP_200_OK)
    return Response({
        'error': ErrorDetail('Please Provide Proper Credential', code='required')},
        status=status.HTTP_400_BAD_REQUEST)
