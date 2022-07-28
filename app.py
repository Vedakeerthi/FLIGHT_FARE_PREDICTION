from flask import Flask,request,render_template
import pickle
import pandas as pd

app = Flask(__name__)

file = open(r'Flight_fare_prediction.pkl','rb')
model = pickle.load(file)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        s_kolkata,s_chennai,s_banglore,s_delhi,s_mumbai=0,0,0,0,0
        d_cochin,d_delhi,d_hyderabad,d_kolkata,d_newdelhi,d_banglore = 0,0,0,0,0,0
        stops = 0
        air_india,goair,indigo,jet_airways,jet_airways_business,multiple_carriers,multiple_carriers_premium_economy, spicejet, trujet, vistara, vistara_premium_economy, airasia = 0,0,0,0,0,0,0,0,0,0,0,0
        
        # source
        source = request.form['source']
        if source=='Kolkata':
            s_kolkata=1
        elif source=='Chennai':
            s_chennai=1
        elif source=='Delhi':
            s_delhi = 1
        elif source=='Mumbai':
            s_mumbai =1
        else:
            s_banglore=1
         
        # destination
        destination = request.form['destination']
        if destination=='Cochin':
            d_cochin =1 
        elif destination=='Delhi':
            d_delhi=1
        elif destination=='Hyderabad':
            d_hyderabad=1
        elif destination=='Kolkata':
            d_kolkata = 1
        elif destination=='New Delhi':
            d_newdelhi = 1
        else:
            d_banglore=1
        
        # Journey day and month
        date_dep = request.form["departure"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        

        # Arrival
        date_arr = request.form["arrival"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min= int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        
        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        
        # stops
        no_of_stops = request.form['stops']
        if no_of_stops == '0':
            stops=0
        elif no_of_stops == '1':
            stops=1
        elif no_of_stops == '2':
            stops=2
        elif no_of_stops == '3':
            stops=3
        else:
            stops=4
        
        # Airline
        airline = request.form['airline']
        if airline=='Air India':
            air_india = 1
        elif airline=='GoAir':
            goair = 1
        elif airline=='IndiGo':
            indigo=1
        elif airline=='Jet Airways':
            jet_airways=1
        elif airline=='Jet Airways Business':
            jet_airways_business=1
        elif airline=='Multiple carriers':
            multiple_carriers=1
        elif airline=='Multiple carriers Premium economy':
            multiple_carriers_premium_economy=1
        elif airline=='SpiceJet':
            spicejet=1
        elif airline=='Trujet':
            trujet=1
        elif airline=='Vistara':
            vistara=1
        elif airline=='Vistara Premium economy':
            vistara_premium_economy=1
        else:
            airasia=1
                
    
        prediction = model.predict([[stops,Journey_day,Journey_month,Dep_hour,Dep_min,Arrival_hour,Arrival_min,dur_hour,dur_min,airasia,air_india,goair,
                                     indigo,jet_airways,jet_airways_business,multiple_carriers,multiple_carriers_premium_economy, spicejet, trujet, vistara, vistara_premium_economy,
                                     s_banglore,s_chennai,s_delhi,s_kolkata,s_mumbai,d_banglore,d_cochin,d_delhi,d_hyderabad,d_kolkata,d_newdelhi]])
        
        output = round(prediction[0],2)  
        if output<=0:
            return render_template('index.html',result = 'Check your input')
        else:
            return render_template('index.html',result = 'Your flight ticket costs Rs. {}'.format(output))
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


