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
@st.cache_data
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
                    `Gender` -  `From the message, kindly infer the gender if no gender can be infered \
                            return Not Stated``
                    `Surgical Status` - `Preoperative or Post operative or any name for the Surgical Status if no status can be infered \
                            return Not Stated`` 
                    
                    `Trauma Name`- `Using the message,Classify into one of the trauma categories.e.g Penetrating Trauma
                    `Trauma Description` - `A very short description of the situation in less than 100 characters`
                    `Physicians` - `= `Return a LIST of specially trained surgeons who are responsible for assessing, \
                                        managing, and performing surgery when necessary on patients who have sustained the stated traumatic injuries.
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
def timer(hospital_count,add_hospital,no_of_acceptance):
    #st.session_state.hospital_count#,st.session_state.no_of_acceptance
    #print(f'{hospital_count}:{add_hospital}')
    if (hospital_count+add_hospital) <= no_of_acceptance:
        return add_hospital