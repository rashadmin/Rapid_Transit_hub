import json
import openai
import streamlit as st

@st.cache_data
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]
#@st.cache_data
def get_response(text):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "user",
          "content": f"""
                    You will be given a medical situation message : {text}. 
                    return JSON format with the following key value pairs in back ticks
                    
                    
                    `Situation`- `Emergency or Non-Emergency`
                    `Age`-`Based on the age in the given information classify them as pediatric,adult,geriatric, if no age can be infered \
                            return Not Stated`
                    `Gender` -  `From the medical situation message, kindly infer the gender if no gender can be infered \
                            return Not Stated``
                    `Surgical Status` - `Preoperative or Post operative or any name for the Surgical Status if no status can be infered \
                            return Not Stated`` 
                    
                    `Trauma Name`- `Using the message,Classify into one of the trauma categories.e.g Penetrating Trauma
                    `Trauma Description` - `A very short description of the situation in less than 100 characters`
                    `Physicians` - `= `Return a LIST of specially trained surgeons who are responsible for assessing, \
                                        managing, and performing surgery when necessary on patients who have sustained the stated traumatic injuries.
                    `Symptoms`- `Using the message , kindly state out atleast 5 possible observable symptoms that are likely to be a result of the medical situation in a python list`
                    - If the given message does not contain a medical related situation simply return `non medical related condition`
                    
                        
                        """
        }
      ],
      temperature=1
    )
    return response['choices'][0]['message']['content']
@st.cache_data
def return_output(json_string):
    data_dict = json.loads(json_string)
    return data_dict
@st.cache_data
def timer(hospital_count,add_hospital,no_of_acceptance,hospital_added_index):
    import numpy as np
    import random
    # Return index value for the selected hospital of size of the no of acceptance
    hospital_index = np.random.choice(range(1,501),size =no_of_acceptance,replace=False)
    #if number of current hospital+ number of hospital to be added is less than number of acceptance
    if ((hospital_count+add_hospital) <= no_of_acceptance):
        #if the added number is less than one
        if add_hospital < 0:
            try:
                #check if the len of the current hospital index is not equal to zero
                if len(hospital_added_index)!=0:
                    #random delete the specified number of hospital from the current hospital index
                    hospital_added_index = np.delete(hospital_added_index,np.random.choice(range(1,len(hospital_added_index)),size =(add_hospital*-1),replace=False).tolist())
                    # return the number added and the current hospital index
                    return add_hospital,hospital_added_index
            except ValueError:
                return None,None
        elif add_hospital >0:
            #print(len(hospital_added_index))
            if len(hospital_added_index)==0:
                hospital_added_index = np.random.choice(hospital_index,size=add_hospital)
            else:
                hospital_added_index = np.concatenate((hospital_added_index,np.random.choice(hospital_index,size=add_hospital)))
            return add_hospital,hospital_added_index
        else:
            return None,None
    
        
    else:
        return None,None
        
def generate_random_hospitals():
    import random
    import json

    # Function to generate a random hospital name
    def generate_hospital_name():
        prefixes = [
        "City", "County", "General", "Community", "Regional",
        "Metropolitan", "University", "Saint", "Memorial", "Sacred",
        "Mercy", "Children's", "Women's", "Veterans", "National",
        "Riverside", "Oak", "Park", "Green", "Blue",
        "Redwood", "Mountain", "Sunrise", "Sunset", "Golden"
            ]

        suffixes = [
        "Hospital", "Medical Center", "Clinic", "Health Center", "Care",
        "Center", "Institute", "Group", "Community Hospital", "Regional Medical Center",
        "General Hospital", "Memorial Hospital", "Children's Hospital", "Women's Hospital", "Veterans Hospital",
        "University Hospital", "Mercy Hospital", "Saint Hospital", "Surgical Center", "Wellness Center"
        ]

        name = f'{random.choice(prefixes)} {random.choice(suffixes)}'
        return name
    def hospital_address_gen():
        # List of common street prefixes
        prefixes = [
            "Main", "Elm", "Oak", "Maple", "Cedar", "Pine", "Birch", "Willow", "Cherry", "Sycamore",
            "Rose", "Magnolia", "Juniper", "Acacia", "Redwood", "Spruce", "Cypress", "Laurel", "Poplar", "Chestnut",
            "Fifth", "Juniper", "Palm", "Hickory", "Fern", "Linden", "Cottonwood", "Cedar", "Beech", "Sycamore",
            "Magnolia", "Peach", "Holly", "Fir", "Cottonwood", "Hickory", "Catalpa", "Alder", "Sycamore", "Cypress",
            "Aspen", "Cedar", "Beech", "Chestnut", "Fern", "Hickory", "Holly", "Juniper", "Linden", "Maple",
            "Mulberry", "Palm", "Pine", "Poplar", "Redwood", "Spruce", "Willow", "Cedar", "Birch", "Cherry",
            "Cypress", "Alder", "Holly", "Fir", "Peach", "Aspen", "Catalpa", "Cottonwood", "Beech", "Fern",
            "Hickory", "Magnolia", "Holly", "Fern", "Cottonwood", "Linden", "Pine", "Mulberry", "Maple", "Catalpa",
            "Peach", "Birch", "Fifth", "Aspen", "Alder", "Hickory", "Palm", "Juniper", "Chestnut", "Sycamore",
            "Redwood", "Holly", "Cypress", "Palm", "Cottonwood", "Pine", "Cedar", "Maple", "Mulberry", "Birch",
        ]
        
        # List of street suffixes
        suffixes = ["Street", "Avenue", "Lane", "Boulevard", "Way", "Road", "Drive", "Terrace", "Court", "Place"]
        
        # Generate a list of 500 street names by combining prefixes and suffixes
        name = f'{random.randint(1,100)}, {random.choice(prefixes)} {random.choice(suffixes)}'
        return name

    # Generate hospital data
    hospital_data = []
    max_distance = 5000.0  # Maximum distance in kilometers

    for _ in range(500):
        hospital_name = generate_hospital_name()
        hospital_address = hospital_address_gen()
        distance = round(random.uniform(0.1, max_distance), 2)  # Random distance between 0.1 and 5.0 km
        is_available = False  # Boolean value set to False

        hospital_entry = {
            "Hospital Name": hospital_name,
            'Hospital Address':hospital_address,
            "Distance (km)": distance,
            "Is Available": is_available
        }

        hospital_data.append(hospital_entry)

    # Save the data to a JSON file
    with open("hospital_data.json", "w") as json_file:
        json.dump(hospital_data, json_file, indent=2)

    #print("JSON file 'hospital_data.json' has been created with 500 entries.")
