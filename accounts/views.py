import datetime
import json
from queue import Empty
import sys,os
from urllib import response
from wsgiref.util import FileWrapper
import django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
import pymysql
import requests
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
import csv

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

def loginView(request):
    print('medhoddddddd',request.method)
    reg_name = request.POST.get('reg_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    conf_password = request.POST.get('conf_password')
    reg_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print('reg_date_timeeeeeeeeeeeeeeeeeeee===>',reg_date_time)

    print('name===>',reg_name)
    print('email===>',email)
    print('password===>',password)
    print('conf_password===>',conf_password)

    if reg_name is not None:
        connection = dbconnection()
        with connection.cursor() as cursor:
            cursor.execute("select email from doctor_reg where email=%s", (str(email),))
            row = cursor.fetchone()
            print('doctor registration row--------',row)
            if row is not None:
                print('Email alredy exists')
            else:
                print('INSERT INTO doctor_reg')
                sql = "INSERT INTO doctor_reg (name,email,password,created_date) VALUES ('"+str(reg_name)+"','"+str(email)+"','"+str(password)+"','"+str(reg_date_time)+"')"
                cursor.execute(sql)
                connection.commit()
                cursor.close()
                connection.close()

    return render(request,'login.html')

def indexView(request):
    return render(request,'index.html')

def redirectView(request):
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

    #  print('redirectView Profile result===>',response)

     name = response['user']['fullName']
     age = response['user']['age']
     user_id = response['user']['encodedId']
     request.session['acces_token']=request.session['acces_token']
     access_token=request.session['acces_token']
     reg_date_time = datetime.datetime.now()  

     getbulksleepdata(request);      
     
     connection = dbconnection()
     with connection.cursor() as cursor:
         cursor.execute("select user_id from profile_token where user_id=%s", (str(request.session['userId']),))
         row = cursor.fetchone()
         print('redirect profile row--------',row)
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
    print('profileeeeeeeeeeedashboarddddddddddddddddddd============>')
    url = "https://api.fitbit.com/1/user/-/profile.json"

    header = {
    "Content-Type":"application/json",
    "Authorization":"Bearer "+request.GET['aacc'],
    }
  
    response = requests.get(url,headers=header).json()
    # print("Fitbit User Profile Data")
    # print('Profile result===>',response)
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
        print('view details profile row--------',row)
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
    getbulksleepdata(request);
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
        # print('Sleep Data===>',response)

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
        # print('users-row--------',usersRows)
        if usersRows is not None:
            user_list = [dict(zip(("name","reg_date_time"),vv)) for vv in usersRows]
            print('user_list--------',user_list)
        else:
            print('users-row--------NO RECORDS FOUND')
    # return render(request,'registered_users.html')
    return render(request,'registered_users.html',{'usersListResonse':usersRows})


def getbulksleepdata(request):

    from_date = datetime.date.today() - relativedelta(months=1)
    to_date = datetime.datetime.now().strftime ("%Y-%m-%d")
    print('#####from_date&&&to_date#####',from_date,to_date)

    print('getbulksleepdata TOKEN===>',request.session['acces_token'])
    print('getbulksleepdata USERID===>',request.session['userId'])

    if request.session['acces_token'] :

        url = "https://api.fitbit.com/1.2/user/-/sleep/date/"+str(from_date)+"/"+str(to_date)+".json"

        header = {
        "Content-Type":"application/json",
        "Authorization":"Bearer "+request.session['acces_token'],
        }

        response = requests.get(url,headers=header).json()
        print("Export Sleep Data")
        print("url===>",url)
        # print('getbulksleepdata===>',response)
        if response['sleep']:
            for i in response['sleep']:
                sleep_date = i['dateOfSleep']
                start_time = i['startTime']
                # startTime = i['startTime']
                # start_time = datetime.datetime.strptime(startTime, '%Y-%m-%d').strftime('DD-MM-YYYY HH:mm     a')
                end_time = i['endTime']
                minutes_asleep = i['minutesAsleep']
                minutes_awake = i['minutesAwake']
                # no_of_awakenings = i['minutesAwake']
                time_in_bed = i['timeInBed']
                abc = i['levels']['summary']

                if 'awake' in abc.keys():
                    no_of_awakenings = i['levels']['summary']['awake']['count']
                elif 'wake' in abc.keys():
                    no_of_awakenings = i['levels']['summary']['wake']['count']
                else:
                    no_of_awakenings = "N/A"


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
                    cursor.execute("select user_id, sleep_date from sleep_data where user_id=%(user_id)s and sleep_date=%(sleep_date)s",{'user_id': str(request.session['userId']),'sleep_date': str(sleep_date)})
                    row = cursor.fetchall()
                    print('sleep-date-row--------',row)

                if row == ():
                    connection = dbconnection()
                    with connection.cursor() as cursor:
                       sql = "INSERT INTO sleep_data (user_id,sleep_date,start_time,end_time,minutes_asleep,minutes_awake,no_of_awakenings,time_in_bed,minutes_rem,minutes_light_sleep, minutes_deep_sleep)     VALUES ('"+str(request.session['userId'])+"','"+str(sleep_date)+"','"    +str(start_time)+"','"+str (end_time)+"','"+str(minutes_asleep)+"','"+str(minutes_awake)+"', '"+str(no_of_awakenings)+"','"+str (time_in_bed)+"','"+str(minutes_rem)+"','"+str (minutes_light_sleep)+"','"+str(minutes_deep_sleep)+"')   "

                       cursor.execute(sql)
                       connection.commit()
                       cursor.close()
                       connection.close()
                else:
                    print('Data exists on date===>',sleep_date)
        else :
            print('NO Sleep Data===>',response)

        return JsonResponse({"getsleepdataresult":response}, status = 200)
        # return render(request,'registered_users.html',{'response':response})
    else :
       return JsonResponse({"getsleepdataresult":response}, status = 400)

def exportsleepdata(request):
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename= output.csv'
    
    print('exportsleepdata===>')

    connection = dbconnection()
    with connection.cursor() as cursor:
        # cursor.execute("SELECT user_id,sleep_date,start_time,end_time,minutes_asleep, minutes_awake,no_of_awakenings,time_in_bed,minutes_deep_sleep,minutes_rem,minutes_light_sleep FROM sleep_data")
        cursor.execute("SELECT user_id,sleep_date,start_time,end_time,minutes_asleep, minutes_awake,no_of_awakenings,time_in_bed,minutes_deep_sleep,minutes_rem,minutes_light_sleep FROM sleep_data")
        exportsleepdataRows = cursor.fetchall()
        connection.commit()
        connection.close()
        # print('exportsleepdata-row--------',exportsleepdataRows)
        if exportsleepdataRows is not None:
            exportsleepdata_list = [dict(zip(("user_id","sleep_date","start_time","end_time","minutes_asleep", "minutes_awake","no_of_awakenings","time_in_bed","minutes_deep_sleep","minutes_rem","minutes_light_sleep" ),vv)) for vv in exportsleepdataRows]
            
            response = exportsleepdata_list
            # print('exportsleepdata response--------',response)
            
            
            # with open('output.csv', 'w', newline='') as file:
            #     writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            
            #     writer.writerow(['id', 'User Id', 'Date of Sleep', 'Start Time','End Time','Minutes Asleep','Minutes Awake', 'Number of Awakenings','Time in Bed','Minutes REM Sleep','Minutes Light Sleep','Minutes Deep Sleep'])

            #     for i in response:
            #         id = i["id"]
            #         user_id = i["user_id"]
            #         sleep_date = i["sleep_date"]
            #         start_time = i["start_time"]
            #         end_time = i["end_time"]
            #         minutes_asleep = i["minutes_asleep"]
            #         minutes_awake = i["minutes_awake"]
            #         no_of_awakenings = i["no_of_awakenings"]
            #         time_in_bed = i["time_in_bed"]
            #         minutes_rem = i["minutes_rem"]
            #         minutes_light_sleep = i["minutes_light_sleep"]
            #         minutes_deep_sleep = i["minutes_deep_sleep"]
                    
            #         print('------------row--------',sleep_date)

            #         writer.writerow([id,user_id,sleep_date,start_time,end_time,minutes_asleep,minutes_awake,no_of_awakenings,time_in_bed,minutes_rem,minutes_light_sleep,minutes_deep_sleep])

        else:
            print('exportsleepdata-row--------NO RECORDS FOUND')

    return JsonResponse({"getsleepdataresult":response}, status = 200)