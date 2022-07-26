import datetime
import json
import sys,os
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from numpy import var
import pymysql
import requests
from werkzeug import Response
from django.template.loader import render_to_string
import xlwt
from django.contrib.auth.models import User
# Create your views here.

# os.environ['acces_token'] = ''
# os.environ['userId'] = ''
connection = pymysql.connect(host='ls-77c7e05b4574ff02a4834ae4adfcf619696ab334.cpozemxa631v.ap-south-1.rds.amazonaws.com',database='fitbitdb',user='dbmasteruser',password='PuA<#-i?uf|tJ3u`kT~XrLAR*FUn2kpE')


def indexView(request):
    return render(request,'index.html')

def redirectView(request):
    print(request.method)
    print('Redirect Page')
    if request.method == "POST":
     global response
     request.session['acces_token'] = request.POST.get('productId', 'default')
     request.session['userId'] = request.POST.get('userId', 'default')
     
     print('Redirect Page Token====>',request.session['acces_token'])
     print('Redirect Page userId====>',request.session['userId'])
     url = "https://api.fitbit.com/1/user/-/profile.json"     
     header = {
     "Content-Type":"application/json",
     "Authorization":"Bearer "+request.session['acces_token'],
     }
     response = requests.get(url,headers=header).json()
     print('Profile result===>',response)
     name = response['user']['fullName']
     age = response['user']['age']
     user_id = response['user']['encodedId']
     request.session['acces_token']=request.session['acces_token']
     access_token=request.session['acces_token']
     reg_date_time = datetime.datetime.now()        
     connection = pymysql.connect(host='ls-77c7e05b4574ff02a4834ae4adfcf619696ab334.cpozemxa631v.ap-south-1.rds.amazonaws.com',database='fitbitdb',user='dbmasteruser',password='PuA<#-i?uf|tJ3u`kT~XrLAR*FUn2kpE')
     with connection.cursor() as cursor:
         cursor.execute("select user_id from profile_token where user_id=%s", (str(request.session['userId']),))
         row = cursor.fetchone()
         print('row--------',row)
         if row is not None:
             sql_update_query = ("update profile_token set access_token='"+str(access_token)+"',name='"+str(name)+"',age='"+str(age)+"' where user_id='"+(str(request.session['userId']))+"'")
             cursor.execute(sql_update_query)
             connection.commit()
             cursor.close()
             connection.close()
         else:
             sql = "INSERT INTO profile_token (user_id,access_token,reg_date_time,name,age) VALUES ('"+str(user_id)+"','"+str(access_token)+"','"+str(reg_date_time)+"','"+str(name)+"','"+str(age)+"')"
             cursor.execute(sql)
             connection.commit()
             cursor.close()
             connection.close()
    return render(request,'dashboard.html',{'profileResult':response})
                
       

def profiledashboard(request):
    print('profiledashboard===>ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg')
    url = "https://api.fitbit.com/1/user/-/profile.json"

    header = {
    "Content-Type":"application/json",
    "Authorization":"Bearer "+request.GET['aacc'],
    }
  
    response = requests.get(url,headers=header).json()
    # print("Fitbit User Profile Data")
    print('Profile result===>',response)
    #return render(request,'dashboard.html',{'profileResult':response})
    
    name = response['user']['fullName']
    age = response['user']['age']
    user_id = response['user']['encodedId']
    request.session['acces_token']=request.GET['aacc']
    access_token=request.GET['aacc']
    reg_date_time = datetime.datetime.now()

    connection = pymysql.connect(host='ls-77c7e05b4574ff02a4834ae4adfcf619696ab334.cpozemxa631v.ap-south-1.rds.amazonaws.com',database='fitbitdb',user='dbmasteruser',password='PuA<#-i?uf|tJ3u`kT~XrLAR*FUn2kpE')
    with connection.cursor() as cursor:
        cursor.execute("select user_id from profile_token where user_id=%s", (str(request.GET['user_id']),))
        row = cursor.fetchone()
        print('row--------',row)
        if row is not None:
            sql_update_query = ("update profile_token set access_token='"+str(access_token)+"',name='"+str(name)+"',age='"+str(age)+"' where user_id='"+(str(request.GET['user_id']))+"'")
            cursor.execute(sql_update_query)
            connection.commit()
            cursor.close()
            connection.close()
        else:
            sql = "INSERT INTO profile_token (user_id,access_token,reg_date_time,name,age) VALUES ('"+str(user_id)+"','"+str(access_token)+"','"+str(reg_date_time)+"','"+str(name)+"','"+str(age)+"')"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
    # del request.session['userId']  
    # return JsonResponse({"profileResult":response}, status = 200)
    return render(request,'dashboard.html',{'profileResult':response})
        
def getsleepdata(request):
    print('getsleepdata===>',request.session['acces_token'])
    if request.session['acces_token'] :

        url = "https://api.fitbit.com/1.2/user/-/sleep/date/"+request.POST['fdate']+"/"+request.POST['tdate']+".json"

        header = {
        "Content-Type":"application/json",
        "Authorization":"Bearer "+request.session['acces_token'],
        }

        response = requests.get(url,headers=header).json()
        print("Sleep Data")
        print("url===>",url)
        print('Sleep Data result===>',response)

        # numberOfDestinationNeeded = 4 # change this number according to your need
        # for i in range(numberOfDestinationNeeded):     
        #     print(response["sleep"])

        # start_time = response['sleep']['startTime']
        # end_time = response['sleep']['endTime']
        # minutes_asleep = response['sleep']['minutesAsleep']
        # minutes_awake = response['sleep']['minutesAwake']
        # no_of_awakenings = response['sleep']['minutesAwake']
        # time_in_bed = response['sleep']['timeInBed']
        # minutes_rem = response['sleep']['summary']['rem']
        # minutes_light_sleep = response['sleep']['summary']['light']
        # minutes_deep_sleep = response['sleep']['summary']['deep']

        # connection = pymysql.connect(host='ls-77c7e05b4574ff02a4834ae4adfcf619696ab334.cpozemxa631v.ap-south-1.rds.amazonaws.com',database='fitbitdb',user='dbmasteruser',password='PuA<#-i?uf|tJ3u`kT~XrLAR*FUn2kpE')
        # with connection.cursor() as cursor:
        #     sql = "INSERT INTO sleep_data VALUES ('"+str(sleep_date)+"','"+str(start_time)+"','"+str(end_time)+"','"+str(minutes_asleep)+"','"+str(minutes_awake)+"','"+str(minutes_awake)+"')"
        #     cursor.execute(sql)
        #     connection.commit()
        #     cursor.close()
        #     connection.close()




        return JsonResponse({"getsleepdataresult":response}, status = 200)
    else :
       return JsonResponse({"getsleepdataresult":response}, status = 400)


def registeredUsersView(request):
    connection = pymysql.connect(host='ls-77c7e05b4574ff02a4834ae4adfcf619696ab334.cpozemxa631v.ap-south-1.rds.amazonaws.com',database='fitbitdb',user='dbmasteruser',password='PuA<#-i?uf|tJ3u`kT~XrLAR*FUn2kpE')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM profile_token")
        usersRows = cursor.fetchall()
        connection.commit()
        connection.close()
        print('users-row--------',usersRows)
        if usersRows is not None:
            user_list = [dict(zip(("name","reg_date_time"),vv)) for vv in usersRows]
            print('user_list--------',user_list)
        else:
            print('users-row--------NO RECORDS FOUND')
    # return render(request,'registered_users.html')
    return render(request,'registered_users.html',{'usersListResonse':usersRows})


def export_sleep_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['DATE','START TIME','END TIME','Minutes Asleep','Minutes Awake','Number of Awakenings','Time in Bed','Minutes REM Sleep','Minutes Light Sleep','Minutes Deep Sleep']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

# def dashboardView_sleep(request):
#     print('dashboardView_sleep===>',request.session['acces_token'])
#     if request.session['acces_token'] :

#         url = "https://api.fitbit.com/1.2/user/-/sleep/date/2022-07-10/2022-07-20.json"

#         header = {
#         "Content-Type":"application/json",
#         "Authorization":"Bearer "+request.session['acces_token'],
#         }

#         response = requests.get(url,headers=header).json()
#         print("Sleep Data")
#         # print('Sleep Data result===>',response)
#         #return render(request,'dashboard.html',{'sleepResult':response})
#         return render(request,'dashboard.html')
#     else :
#         return render(request,'index.html')
