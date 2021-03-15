from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('Rfmodel.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


# ['km_driven', 'YearOld', 'fuel_Diesel', 'fuel_Electric', 'fuel_LPG',
#        'fuel_Petrol', 'seller_type_Individual', 'seller_type_Trustmark Dealer',
#        'transmission_Manual', 'owner_Fourth & Above Owner',
#        'owner_Second Owner', 'owner_Test Drive Car', 'owner_Third Owner']


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    # Fuel_Type=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        km_driven=int(request.form['km_driven'])
        Owner=request.form['Owner']
        if (Owner=="owner_Fourth_&_Above Owner"):
            owner_Fourth__Above_Owner=1
            owner_Second_Owner=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
        elif (Owner=="owner_Second_Owner"):
            owner_Fourth__Above_Owner=0
            owner_Second_Owner=1
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
        elif (Owner=="owner_Test_Drive_Car"):
            owner_Second_Owner=0
            owner_Test_Drive_Car=1
            owner_Third_Owner=0
            owner_Fourth__Above_Owner = 0
            
        else:
            owner_Fourth__Above_Owner=0
            owner_Second_Owner=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=1
        
        fuel=request.form['fuel']
        if(fuel=='Petrol'):
            Fuel_Type_Petrol=1
            fuel_Diesel=0
            fuel_Electric=0
            fuel_LPG=0
        elif(fuel=='Diesel'):
            Fuel_Type_Petrol=0
            fuel_Diesel=1
            fuel_Electric=0
            fuel_LPG=0
        elif(fuel=='LPG'):
            Fuel_Type_Petrol=0
            fuel_Diesel=0
            fuel_Electric=0
            fuel_LPG=1
        else:
            Fuel_Type_Petrol=0
            fuel_Diesel=0
            fuel_Electric=1
            fuel_LPG=0
       
        Year=2021-Year
        Seller_Type =request.form['Seller_Type']
        if(Seller_Type=='Individual'):
            seller_Type_Individual=1
            seller_type_Trustmark_Dealer=0
        else:
            seller_type_Trustmark_Dealer=1
            seller_Type_Individual=0
        transmission_Manual=request.form['transmission_Manual']
        if(transmission_Manual=='Mannual'):
            transmission_Manual=1
        else:
            transmission_Manual=0
        prediction=model.predict([[km_driven, Year, fuel_Diesel, fuel_Electric, fuel_LPG,
        Fuel_Type_Petrol, seller_Type_Individual, seller_type_Trustmark_Dealer,
        transmission_Manual, owner_Fourth__Above_Owner,
        owner_Second_Owner, owner_Test_Drive_Car, owner_Third_Owner]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
