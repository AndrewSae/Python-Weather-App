import tkinter as tk
import customtkinter
import requests, json
from PIL import ImageTk, Image

# sets the GUI theme
customtkinter.set_appearance_mode("Dark")  

app = customtkinter.CTk()  
app.geometry("500x500") # windo size
app.minsize(600, 400) # min window size 
app.maxsize(600, 400) # max window size
app.title("Focus Weather") #tite of the app
app.iconphoto(False, tk.PhotoImage(file='icon.png')) # app icon

api_key = "386e2c2f3de6015759fa8439c9f005e0"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# converts kelvin into fahrenheit
def k_to_f(k):
    return  1.8*(k-273) + 32
  
# clears the frame 
def clear_home():
   for widgets in app.winfo_children():
      widgets.pack_forget()

# clears all the weather data from the window
def clear_data():
   for widgets in app.winfo_children():
      widgets.destroy()

def qw():
    clear_data()
    home()
    
# convent degree angle into a compass direction 
def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]
  
# convert meters per second to miles per hour
def mps_to_mph(speed):
    return speed*2.237
  
# gets snd shows the weather data
def get_data():
    # makes the url and gets the json info 
    city = entry.get().strip()
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()

    if entry.get() != "":
        if data["cod"] != "404" and data["cod"] != "400":
            clear_home()
            main = data["main"]
            weather = data["weather"]

            # town name
            town = data["name"]

            # the icon id for the curent weather
            icon_id = weather[0]['icon']
            path = "weather_icons/%s.png" % (icon_id)
            global icon_
            icon_ = tk.PhotoImage(file = path)

            # weather description
            desc = weather[0]["description"].capitalize()
        
            # temp info
            temp = round(k_to_f(main["temp"]))
            feels = round(k_to_f(main["feels_like"]))
            min_ = round(k_to_f(main["temp_min"]))
            max_ = round(k_to_f(main["temp_max"]))


            # current humidity
            humid = main['humidity']

            # wind info
            wind = data['wind']
            ws = round(mps_to_mph(wind['speed']))
            wd = degToCompass(wind['deg'])

        # town name label
            town = customtkinter.CTkLabel(master=app, 
                                        text=town,
                                        text_font=("Arial", 18))
            # icon label
            global icon
            icon = customtkinter.CTkLabel(master=app, image=icon_)
            # weather description label
            weather_desc = customtkinter.CTkLabel(master=app,
                                                text=desc,
                                                text_font=("Arial", 18))
        
            # temp info labels
            curent_temp = customtkinter.CTkLabel(master=app,
                                            text=str(temp)+"°",
                                            text_font=("Arial", 20))
            feels_like = customtkinter.CTkLabel(master=app,
                                            text="Feels Like: " + str(feels)+"°",
                                            text_font=("Arial", 14))
            max_temp = customtkinter.CTkLabel(master=app,
                                            text="High: " + str(max_)+"°",
                                            text_font=("Arial", 14))
            min_temp = customtkinter.CTkLabel(master=app,
                                            text="Low: " + str(min_)+"°",
                                            text_font=("Arial", 14))
            humidity_per = customtkinter.CTkLabel(master=app,
                                            text="Humidity: " + str(humid)+"%",
                                            text_font=("Arial", 14))
            # END

            # wind info labels
            wind_speed = customtkinter.CTkLabel(master=app,
                                            text="Wind speed: " + str(ws)+" mph",
                                            text_font=("Arial", 14))
            wind_direction = customtkinter.CTkLabel(master=app,
                                            text="Wind direction: " + str(wd),
                                            text_font=("Arial", 14))
            # END
        
            # back button 
            back_btn = customtkinter.CTkButton(master=app,
                                            text="Back",
                                            width=75,
                                            height=50,
                                            corner_radius=0,
                                            command=qw)


            # # place the town name label
            town.place(x=300, y=25, anchor=tk.CENTER)

            # place the icon label
            icon.place(x=300, y=95, anchor=tk.CENTER)

            # # place the weather description label
            weather_desc.place(x=300, y=150, anchor=tk.CENTER)
        
            # # place the temp related labels
            curent_temp.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            max_temp.place(relx=0.3, y=250, anchor=tk.CENTER)
            min_temp.place(relx=0.7, y=250, anchor=tk.CENTER)
            feels_like.place(relx=0.3, y=300, anchor=tk.CENTER)
        
            # # # place the humidity label
            humidity_per.place(relx=0.7, y=300, anchor=tk.CENTER)
            # # # place te wind related labels
            wind_speed.place(relx=0.3, y=350, anchor=tk.CENTER)
            wind_direction.place(relx=0.7, y=350, anchor=tk.CENTER)
        
            # place the back button
            back_btn.place(x=35, y=25, anchor=tk.CENTER)

        else:
            clear_home()
            home()
            error = customtkinter.CTkLabel(master=app,
                                        text="City not found pls try again:",
                                        text_font=("Arial", 20),
                                        text_color="red")
            error.pack()
    else:
            clear_home()
            home()
            error = customtkinter.CTkLabel(master=app,
                                        text="You must enter a city:",
                                        text_font=("Arial", 20),
                                        text_color="red")
            error.pack()

 

def home():
    label = customtkinter.CTkLabel(master=app,
                                    text="Focus Weather",
                                    text_font=("Arial", 25))
    global entry
    entry = customtkinter.CTkEntry(master=app,
                                    placeholder_text="Enter City",
                                    width=250,
                                    height=35)
    
    button = customtkinter.CTkButton(master=app,
                                    text="Search",
                                    width=75,
                                    height=50,
                                    corner_radius=0,
                                    command=get_data)
    label.pack(side="top", expand=True)
    entry.pack(side='top', expand=True)
    button.pack(side='top', expand=True)

home()
app.mainloop()
