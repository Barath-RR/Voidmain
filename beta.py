import http
from flask import Flask, request
import requests
import json
import time
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml
from collections import defaultdict
from googleplaces import GooglePlaces, types, lang
from geopy.geocoders import Nominatim

chats = defaultdict(list)

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/bot', methods=['GET','POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    print(chats)

    # Option A
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'A':
            loc = Nominatim(user_agent="GetLoc")
            # entering the location name
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 1000,types =[types.TYPE_LODGING])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 


        
    # # Double previous message
    # if len(chats[request.values["WaId"]]) >= 2:
    #     if chats[request.values["WaId"]][-2] == 'A':
    #         r = requests.get('')
    #         print(r.status_code)
    #         if r.status_code == 200:
    #             data = r.json()
    #             text = f''[:100]
    #         else:
    #             text = 'I could not retrieve the results at this time, sorry.'
    #         print("text",text)
    #         msg.body(text)
    #         responded = True

    # option E
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'E':

            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 3000,types =[types.TYPE_HOSPITAL])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 

    # option F
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'F':

            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_POLICE])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 

    # option G 
    if chats[request.values["WaId"]] :
        if chats[request.values["WaId"]][-1] == 'G':
                msg.body('Enter currency to be converted 💲')
                responded = True

    if len(chats[request.values["WaId"]]) >= 2:
         if chats[request.values["WaId"]][-2] == 'G':
                msg.body('Enter amount💲')
                responded = True
        
    if len(chats[request.values["WaId"]]) > 2:
         if chats[request.values["WaId"]][-3] == 'G':
                amnt = incoming_msg
                current = chats[request.values["WaId"]][-2]
                convert = chats[request.values["WaId"]][-1]

                url = "https://currency-converter-by-api-ninjas.p.rapidapi.com/v1/convertcurrency"
                querystring = {"have":{current},"want":{convert},"amount":{amnt}}
                headers = {
                    "X-RapidAPI-Key": "312d1c6896msh13cea70bb1fbf03p10cdbcjsn8ce1bc900f33",
                    "X-RapidAPI-Host": "currency-converter-by-api-ninjas.p.rapidapi.com"
                }

                r = requests.request("GET", url, headers=headers, params=querystring)
                value = r.json()
                text = f' *Conversion Details* \n{value["old_currency"]} : {value["old_amount"]} Converted to {value["new_currency"]} : {value["new_amount"]}   '
                msg.body(text)
                msg.media('https://user-images.githubusercontent.com/118819185/204077246-1421948e-a188-48c7-a8a4-a59ad46179af.jpeg')
                responded = True

    # ATM
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'O':
            msg.body('Enter your location 📍')
            responded = True
    
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '1') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_ATM])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 

    # Bus Station
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '2') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_BUS_STATION])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 

    # Railway Station
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '3') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_TRAIN_STATION])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 

    # Pharmacy
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '4') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_PHARMACY])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 
        
    # Restraunt
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '5') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_RESTAURANT])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            responded = True 

    # Train Status
    if chats[request.values["WaId"]]:
        if (chats[request.values["WaId"]][-1] == 'C') :
            msg.body('Enter your train number / Enter your PNR number to check train status  ')
            responded = True


    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'C') and (chats[request.values["WaId"]][-1] == '1') :
            url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
            querystring = {"trainNo":{incoming_msg}}
            headers = {
                "X-RapidAPI-Key": "86138dc677msh8b2ae445bd9ca15p1b1764jsn26e7b65023ff",
                "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
            }
            r = requests.request("GET", url, headers=headers, params=querystring)
            value = r.json()
            value1 = value["data"]["train_number"]
            value2 = value["data"]["train_name"]
            value3 = value["data"]["source"]
            value4 = value["data"]["destination"]
            value5 = value["data"]["new_message"]
            text = f'*Train Details* \n\n 1. Train number : *{value1}* \n 2. Train name : *{value2}* \n 3. Source : *{value3}* \n 4. Destination : *{value4}* \n 5. Addtional Information : *{value5}* '
            msg.body(text)
            msg.media('https://user-images.githubusercontent.com/118819185/204075125-5a7aef3c-f4d8-4c1a-9b23-ceba67e81334.jpg')
            responded = True

    # Train Schedule
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'C') and (chats[request.values["WaId"]][-1] == '2') :

            url = "https://irctc1.p.rapidapi.com/api/v1/getTrainSchedule"
            querystring = {"trainNo":{incoming_msg}}
            headers = {
                "X-RapidAPI-Key": "41b98c9488msh6809117dba036c7p13f74djsn23764292092b",
                "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
            }
            r = requests.request("GET", url, headers=headers, params=querystring)
            value = r.json()
            x = value["data"]["route"]
            values = ""
            for i in range (len(x)):
                name = x[i]["station_name"]
                platform = x[i]["platform_number"]
                if platform !=0 :
                    values += "📍"+ name + " - Platform number : " +  str(platform)
                    values += "\n"
            msg.body(values)
            msg.media('https://user-images.githubusercontent.com/118819185/204075125-5a7aef3c-f4d8-4c1a-9b23-ceba67e81334.jpg')
            responded = True

    # PNR Status
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'C') and (chats[request.values["WaId"]][-1] == '3') :

            url = "https://pnr-status-indian-railway.p.rapidapi.com/pnr-check/4339976864"
            headers = {
                "X-RapidAPI-Key": "312d1c6896msh13cea70bb1fbf03p10cdbcjsn8ce1bc900f33",
                "X-RapidAPI-Host": "pnr-status-indian-railway.p.rapidapi.com"
            }
            r = requests.request("GET", url, headers=headers)
            value = r.json()
            print(value)
            text = f' *Seat Info* \nCoach : *{value["data"]["seatInfo"]["coach"]}* \nBerth : *{value["data"]["seatInfo"]["berth"]}* \nNo.of Seats : *{value["data"]["seatInfo"]["noOfSeats"]}* \n\n*Train Info* \nTrain number : *{value["data"]["trainInfo"]["trainNo"]}* \nTrain name : *{value["data"]["trainInfo"]["name"]}* '
            msg.body(text)
            msg.media('https://user-images.githubusercontent.com/118819185/204075125-5a7aef3c-f4d8-4c1a-9b23-ceba67e81334.jpg')
            responded = True




    # Main message body       
    if not responded and 'Hi' in incoming_msg or 'Hey' in incoming_msg or 'hi' in incoming_msg or 'Menu' in incoming_msg:
        text = f'Do you enjoy travelling ? I like assisting travellers like you ! 🤜🤛 \n\n 👋 Hey there I\'m Voyager , your pocket friendly and personalized travel assistant 🧳 \n\n Please select one of the following option 👇 \n *A* -> Check the availability of hotels 🛌 \n *B* -> Check availability of flight tickets 🛫 \n *C* -> Avail Train Services 🚃 \n *D* -> Itinerary planner 🗓️ \n *E* -> Nearest Hospitals 🏥 \n *F* -> Nearest Police Station 🚨 \n *G* -> Currency conversion 💰 \n *O* -> Avail Other Services 📱 \n\n *_“The journey of a thousand miles begins with a single step.”_*'
        msg.media('https://user-images.githubusercontent.com/118819185/203973014-77eaee6b-b2ae-4ce4-86f6-dc6a7c895f88.jpg')
        msg.body(text)
        responded = True


    elif 'A' == incoming_msg:
        msg.body('Enter your location 📍')
        responded = True


    elif 'B' == incoming_msg:
        #body goes here 
        responded = True


    elif 'C' == incoming_msg:
        text = f' Select the Railway service you would like to avail from below 👇 \n\n *1* -> Live Train Status \n *2* -> Train Schedule \n *3* -> Check PNR Status  \n\n 🚂🚂🚂'
        msg.media('https://user-images.githubusercontent.com/118819185/204074983-8471acf4-f6d5-4988-8631-8e90fdce75e1.jpg')
        msg.body(text)
        responded = True


    elif 'D' == incoming_msg :
        text = f'To get the best plan, click here 👇 \nhttps://touristbot-jd.herokuapp.com/ '
        msg.body(text)
        responded = True

    elif 'E' == incoming_msg :
        text = f'Enter your location 📍'
        msg.body(text)
        responded = True

    elif 'F' == incoming_msg:
        text = f'Enter your location 📍'
        msg.body(text)
        responded = True

    elif 'G' == incoming_msg:
        text = f'*Use currency code*  \nEnter current currency used 💲'
        msg.body(text)
        responded = True

    elif 'O' == incoming_msg:
        text = f' Select the nearest service you would like to avail from below 👇 \n\n *1* -> ATM 🏧 \n *2* -> Bus Station 🚍 \n *3* -> Railway Station 🚟 \n *4* -> Pharmacy 💊 \n *5* -> Restraunt 🍱\n\n *_"A smile is a curve that sets things straight."_* 😉 '
        msg.media('https://user-images.githubusercontent.com/118819185/204011481-1c5d431b-2eda-435e-9e7f-95379391dc2b.jpg')
        msg.body(text)
        responded = True


    if responded == False:
        msg.body('Oops ! I guess I\'m mystified right now 😵‍💫 \n\nPlease enter *Menu* or *hi* so I\'ll assist you in advancing 😬')
        msg.media('https://user-images.githubusercontent.com/118819185/204075533-f349eb6b-2a76-45d1-a537-4c2d886658af.jpg')

    chats[request.values["WaId"]].append(incoming_msg)
    print("end",incoming_msg)
    return str(resp)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
