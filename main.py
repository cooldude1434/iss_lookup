import time

import requests
from datetime import datetime
import smtplib

MY_LAT = 12.7328844 # Your latitude
MY_LONG = 77.8309478 # Your longitude

my_email = "birthday.source@gmail.com"
password = "Birthday@123!"
receive_email = "kailashpatil143123@gmail.com"

def iss_closer_to_myplace():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if iss_longitude+5.0 == MY_LONG or iss_longitude-5.0 == MY_LONG:
        if iss_latitude+5.0 == MY_LAT or iss_latitude-5.0 == MY_LAT:
            return True

def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
         connection.starttls()   #*make it secure connection */
         connection.login(user=my_email,password=password)
         connection.sendmail(from_addr=my_email,
                         to_addrs=receive_email,
                         msg=f"Subject:Time to look up sky \n\nISS above")


#Your position is within +5 or -5 degrees of the ISS position.

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if iss_closer_to_myplace():
        if time_now.hour > sunset and time_now.hour < sunrise:
            return True

while True:
    time.sleep(60)
    if iss_closer_to_myplace() and is_night():
        send_email()



#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



