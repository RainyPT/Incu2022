from flask import Flask, request
import requests
import json
import mysql.connector

##DB Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="weatherbot"
)
mycursor = mydb.cursor()
############## Bot details ##############
bot_name = 'IncuWeather@webex.bot'
token = 'ODA3ZDliOWItZDY5NS00MjA0LTk1MWUtNmZmYzU5NmY1ZGE3OTNlZWI1ZTAtYWVh_P0A1_6e31fd08-63c5-45b0-9a66-10c03c54016e'
weatherAPIKey="bebb417ea93948cfb8f154013220103"
header = {"content-type": "application/json; charset=utf-8", 
 "authorization": "Bearer " + token}
 
############## Flask Application ##############
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def sendMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages'
    msg = {"roomId": webhook["data"]["roomId"]}
    sender = webhook["data"]["personEmail"]
    message = getMessage()
    command=message.split(" ")[0]
    args=message.split(" ")
    if (sender != bot_name):
        if(command=="help"):
                if(len(args)==1):
                    msg["text"]="BOT MADE BY Francisco Gonçalves.\nThis bot provides this set of commands:\n - save;\n - remove;\n - weather;\n - time.\n\n If you need help with any of these, please type: help <command>."
                elif(args[1]=="save"):
                    msg["text"]="This command can be used to save a city in the database. This is useful to check the current weather in each city saved in the database. \n---\nSyntax: save <city_name>"
                elif(args[1]=="remove"):
                    msg["text"]="This command can be used to remove a city from the database. \n---\nSyntax: remove <city_name>"
                elif(args[1]=="weather"):
                    msg["text"]="This command can be used to check a city's current weather, or get a 3 day forecast of it. \n---\nSyntax: \"weather current <city_name>/savedcities\" OR \"weather forecast <city_name>\""
                elif(args[1]=="time"):
                    msg["text"]="This command can be used to check the time in a certain city. \n---\nSyntax: \"time <city_name>\""
                else:
                    msg["text"]="Command arguments not found!"
        if(command== "remove"):
            if(args[1]!=""):
                sql="SELECT * FROM savedcities WHERE username=%s AND city=%s"
                val = (sender, args[1])
                mycursor.execute(sql,val)
                myresult = mycursor.fetchall()
                if(myresult==[]):
                    msg["markdown"]=args[1]+" was not found in database!"
                else:
                    sql="DELETE FROM savedcities WHERE username=%s AND city=%s"
                    val = (sender, args[1])
                    mycursor.execute(sql,val)
                    mydb.commit()
                    msg["markdown"]=args[1]+" was sucessfully deleted!"
        
        if(command== "save"):
            if(args[1]!=""):
                response= requests.get("http://api.weatherapi.com/v1/search.json?key="+weatherAPIKey+"&q="+args[1])
                response=response.json()
                if "error" in response:
                    msg["markdown"]="ERROR: "+response["error"]["message"]
                else:
                    sql="SELECT * FROM savedcities WHERE username=%s AND city=%s"
                    val = (sender, args[1])
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    if (myresult== []):
                        sql = "INSERT INTO savedcities (username, city) VALUES (%s, %s)"
                        val = (sender, args[1])
                        mycursor.execute(sql, val)
                        mydb.commit()
                        msg["markdown"]=args[1]+" was saved!"
                    else:
                        msg["markdown"]=args[1]+" was already saved!"
        
        if(command=="weather"):
            if(args[1]=="forecast"):
                response= requests.get("http://api.weatherapi.com/v1/forecast.json?key="+weatherAPIKey+"&q="+args[2]+"&days=3&aqi=no&alerts=no")
                response=response.json()
                if "error" in response:
                    msg["markdown"]="ERROR: "+response["error"]["message"]
                else:
                    msg["text"] = "Here is the forecast for the weather in "+response["location"]["name"]+" for the next 3 days: \n"
                    for date in response["forecast"]["forecastday"]:
                        msg["text"]+="On the "+ str(date["date"])+", the average temperature is expected to be: "+str(date["day"]["avgtemp_c"])+" °C\n"
                  
                    
            elif(args[1]=="current"):
                messagetosend=""
                if(len(args)==2):
                    msg["markdown"] ="Syntax: weather current <city_name>"
                else:
                    if(args[2]=="savedcities"):
                        sql="SELECT city FROM savedcities WHERE username='"+sender+"'"
                        mycursor.execute(sql)
                        myresult = mycursor.fetchall()
                        for city in myresult:
                            city="".join(city)
                            response= requests.get("http://api.weatherapi.com/v1/current.json?key="+weatherAPIKey+"&q="+city+"&aqi=no")
                            response=response.json()
                            if "error" in response:
                                messagetosend+="ERROR: "+response["error"]["message"]+""
                            else:
                                messagetosend+="Its currently "+  str(response["current"]["temp_c"])+" °C in "+response["location"]["name"]+". Condition: "+ response["current"]["condition"]["text"]+".\n"
                        msg["markdown"]=messagetosend
                    else:
                        if(args[2]!=""):
                            response= requests.get("http://api.weatherapi.com/v1/current.json?key="+weatherAPIKey+"&q="+args[2]+"&aqi=no")
                            response=response.json()
                            if "error" in response:
                                msg["markdown"]="ERROR: "+response["error"]["message"]
                            else:
                                msg["markdown"] ="Its currently "+  str(response["current"]["temp_c"])+" °C in "+response["location"]["name"]+". Condition: "+ response["current"]["condition"]["text"]+"."
        
        if(command=="time"):
            if(len(args)>1):
                response= requests.get("http://api.weatherapi.com/v1/timezone.json?key="+weatherAPIKey+"&q="+args[1])
                response=response.json()
                if "error" in response:
                    msg["text"]="ERROR: "+response["error"]["message"]
                else:
                    msg["text"] ="Its currently "+str(response["location"]["localtime"]).split(" ")[1]+" ("+str(response["location"]["localtime"]).split(" ")[0]+") in "+response["location"]["name"]+"."
            else:
                msg["text"]="Syntax: time <city_name>"
        requests.post(url,data=json.dumps(msg), headers=header, verify=True)

def getMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
    get_msgs = requests.get(url, headers=header, verify=True)
    message = get_msgs.json()['text']
    return message

app.run(debug = True)
