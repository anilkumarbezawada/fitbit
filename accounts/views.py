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
from django.template.loader import render_to_string
from django.contrib.auth.models import User

import sys
sys.path.append( "/path/to/mysite" )
from mysite import settings

dbName     = settings.DATABASES['default']['NAME']
dbUsername = settings.DATABASES['default']['USER']
dbPassword = settings.DATABASES['default']['PASSWORD']
dbHost     = settings.DATABASES['default']['HOST']

def dbconnection():
    connection = pymysql.connect(host=dbHost,database=dbName,user=dbUsername,password=dbPassword)
    return connection


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
     connection = dbconnection()
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
    request.session['userId']=user_id
    request.session['acces_token']=request.GET['aacc']
    access_token=request.GET['aacc']
    reg_date_time = datetime.datetime.now()

    connection = dbconnection()
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
    print('getsleepdata USERID===>',request.session['userId'])
    if request.session['acces_token'] :

        url = "https://api.fitbit.com/1.2/user/-/sleep/date/"+request.POST['fdate']+"/"+request.POST['tdate']+".json"

        header = {
        "Content-Type":"application/json",
        "Authorization":"Bearer "+request.session['acces_token'],
        }

        response = requests.get(url,headers=header).json()
        print("Sleep Data")
        print("url===>",url)
        print('Sleep Data===>',response)
        if response['sleep']:
            for i in response['sleep']:
                sleep_date = i['dateOfSleep']
                start_time = i['startTime']
                # startTime = i['startTime']
                # start_time = datetime.datetime.strptime(startTime, '%Y-%m-%d').strftime('DD-MM-YYYY HH:mm     a')
                end_time = i['endTime']
                minutes_asleep = i['minutesAsleep']
                minutes_awake = i['minutesAwake']
                no_of_awakenings = i['minutesAwake']
                time_in_bed = i['timeInBed']
                abc = i['levels']['summary']
                if 'rem' in abc.keys():
                    minutes_rem = i['levels']['summary']['rem']['minutes']
                else:
                    minutes_rem = "N/A"

            if 'light' in abc.keys():
                minutes_light_sleep = i['levels']['summary']['light']['minutes']
            else:
                minutes_light_sleep = "N/A"

            if 'deep' in abc.keys():
                minutes_deep_sleep = i['levels']['summary']['deep']['minutes']
            else:
                minutes_deep_sleep = "N/A"
        

            connection = dbconnection()
            with connection.cursor() as cursor:
               sql = "INSERT INTO sleep_data (user_id,sleep_date,start_time,end_time,minutes_asleep,minutes_awake,no_of_awakenings,time_in_bed,minutes_rem,minutes_light_sleep,minutes_deep_sleep) VALUES ('"+str(request.session['userId'])+"','"+str(sleep_date)+"','"+str(start_time)+"','"+str(end_time)+"','"+str(minutes_asleep)+"','"+str(minutes_awake)+"','"+str(no_of_awakenings)+"','"+str(time_in_bed)+"','"+str(minutes_rem)+"','"+str(minutes_light_sleep)+"','"+str(minutes_deep_sleep)+"')"

               cursor.execute(sql)
               connection.commit()
               cursor.close()
               connection.close()
        else :
            print('NO Sleep Data===>',response)

        return JsonResponse({"getsleepdataresult":response}, status = 200)
    else :
       return JsonResponse({"getsleepdataresult":response}, status = 400)


def registeredUsersView(request):
    connection = dbconnection()
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