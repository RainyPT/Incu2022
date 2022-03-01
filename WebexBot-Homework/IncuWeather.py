from flask import Flask, request
import requests
import json
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
                response= requests.get("http://api.weatherapi.com/v1/current.json?key="+weatherAPIKey+"&q="+args[2]+"&aqi=no")
                print(response)
                response=response.json()
                if "error" in response:
                    msg["markdown"]="ERROR: "+response["error"]["message"]
                else:
                    msg["markdown"] ="Its currently "+  str(response["current"]["temp_c"])+" °C in "+response["location"]["name"]+". Condition: "+ response["current"]["condition"]["text"]+"."
        if(command=="time"):
            response= requests.get("http://api.weatherapi.com/v1/timezone.json?key="+weatherAPIKey+"&q="+args[1])
            response=response.json()
            if "error" in response:
                msg["markdown"]="ERROR: "+response["error"]["message"]
            else:
                msg["markdown"] ="Its currently "+str(response["location"]["localtime"]).split(" ")[1]+" ("+str(response["location"]["localtime"]).split(" ")[0]+") in "+response["location"]["name"]+"."

        requests.post(url,data=json.dumps(msg), headers=header, verify=True)

def getMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
    get_msgs = requests.get(url, headers=header, verify=True)
    message = get_msgs.json()['text']
    return message

app.run(debug = True)
