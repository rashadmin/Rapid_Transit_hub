import streamlit as st
import numpy as np
import openai
import json
import time as t
import random as rn
import threading
from functions import get_response,return_output,get_completion_from_messages,timer
from streamlit.runtime.scriptrunner import add_script_run_ctx
from info import video_url
import multiprocessing as mp
openai.api_key = st.secrets["openai_secret_key"]


st.markdown(
    """
    <style>
    .reportview-container {{
        background-color: red
    }}
   .sidebar .sidebar-content {{
        background-color: blue
    }}
    </style>
    """,
    unsafe_allow_html=True
)


if 'json' not in st.session_state:
    data_dict = {"Situation": None,
              "Age": None,
              "Gender": None,
              "Surgical Status": None,
              "Trauma Name": None,
              "Trauma Description": None,
              "Physicians": [],
              "Symptoms":[]
                }
    #Turn off after debugging
    st.session_state.json = data_dict
    st.session_state.count = 0
if 'start' not in st.session_state:
    st.session_state['start'] = 0
    # initialize the array of index of the hospital to be added.
    st.session_state.hospital_added_index = np.array([])
    # initialze the number of hospital that will accept the request
    st.session_state.no_of_acceptance = 0
    #initialize the number of hospital that has accepted
    st.session_state.hospital_count = 0
    #initiaze the average hospital per time
    st.session_state.average = 0 
    #initalize the total number of hospital receiving the request
    st.session_state.no_of_hospital =0
   
    #intialize the distance of the closest hospital
    st.session_state.in_km = 0
    #intialize the random addition of hospital
    st.session_state.add_hospital = 0
    try:
        with open('hospital_data.json', "r") as json_file:
            st.session_state.data = np.array(json.load(json_file))
    except FileNotFoundError:
        st.session_state.data = np.array([])
    #initialize the closest hospital name
    st.session_state.hospital_name = None
    st.session_state.data_dict = None
    st.session_state.symptoms = None
    st.session_state.col = st.empty()

def chatbot():
    # Initialize chat history
    st.markdown("#### CHATBOT")  
    for message in st.session_state.messages:
        if message['role'] != 'system' and message['content'] != 'Hello':
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
     # Display user message in chat message container 
    #Display symptoms
    if (st.session_state.count) > 0:
        st.session_state.symptoms = st.session_state.Symptoms.multiselect('Select the Observable Symptoms',st.session_state.data_dict['Symptoms'],key='cont')
        st.session_state.json['Symptoms'] = st.session_state.symptoms
            
            
    if prompt:= st.chat_input("What's Your Emergency?"):
        if st.session_state.count == 0:
            with st.status("Sending Data ...") as status:
                try:
                    st.session_state.no_of_hospital = rn.randint(250,500)
                    st.session_state.no_of_acceptance = rn.randint(1,st.session_state.no_of_hospital+1)
                    st.session_state.average = 60/st.session_state.no_of_acceptance
                    st.session_state.hospital_added_index = np.array([])
                    st.session_state.hospital_count = len(st.session_state.hospital_added_index)
                    json_string = get_response(prompt)
                    #st.write(json_string)
                    st.session_state.data_dict = return_output(json_string)
                    st.session_state.json = return_output(json_string)
                    status.update(label="Message Sent", state="complete", expanded=False)
                    st.session_state.count+=1
                except:
                    status.update(label="Error Sending messaage, Reloading Chatbot", state="error", expanded=False)
                    st.rerun()
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state.messages,
                    temperature = 0.4,
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    try:
        st.session_state.symptoms = st.session_state.Symptoms.multiselect('Select the Observable Symptoms',st.session_state.data_dict['Symptoms'],key='dir')
        st.session_state.json['Symptoms'] = st.session_state.symptoms
    except:
        st.session_state.json['Symptoms'] = st.session_state.symptoms

def hospital_addition():
    if st.session_state.json['Situation'] is not None:
        while st.session_state['start'] < 60:
            add_time = rn.randint(1,int(st.session_state.average)+1)
            choice = list(range(-2,6))
            choice.remove(0)
            st.session_state.add_hospital = rn.choice(choice)
            try:
                s = timer(st.session_state.hospital_count,st.session_state.add_hospital,st.session_state.no_of_acceptance,st.session_state.hospital_added_index)#0]
                #return none
                if (s[0] is not None) and (s[1] is not None):
                    st.session_state.add_hospital = s[0]
                    st.session_state.hospital_added_index = s[1]
                    st.session_state.hospital_count += st.session_state.add_hospital
                    with  st.session_state.col[0]:
                        st.session_state.metric.metric('No of Hospital Accepted',f'{st.session_state.hospital_count}/{st.session_state.no_of_hospital}',delta=st.session_state.add_hospital,delta_color="normal", help=None,label_visibility="visible")
                    st.session_state.index = np.array([i['Distance (km)'] for i in st.session_state.data[st.session_state.hospital_added_index]]).argmin()
                    st.session_state.in_km = st.session_state.data[st.session_state.hospital_added_index][st.session_state.index]['Distance (km)']
                    st.session_state.hospital_name = st.session_state.data[st.session_state.hospital_added_index][st.session_state.index]['Hospital Name']
                    with  st.session_state.col[1]:
                        st.session_state.distance.metric('Distance',f'{st.session_state.in_km}',delta=None)
                    with  st.session_state.col[2]:
                        st.session_state.name.metric('Hospital Name',f'{st.session_state.hospital_name}',delta=None)
                    #t.write(st.session_state.data[st.session_state.hospital_added_index])
                    st.session_state['start']+=1
                    t.sleep(add_time+2)
                else:
                    pass
            except TypeError:
                pass

        
        
        



    
    


def main():
   
    st.title("RAPID CARE HUB")
    st.session_state.col = st.columns(3)
    #Check if json state in running in current session state

    
    with  st.session_state.col[0]:
        st.session_state.metric = st.metric('No of Hospital Accepted',f'{st.session_state.hospital_count}/{st.session_state.no_of_hospital}',delta=st.session_state.add_hospital,delta_color="off", help=None,label_visibility="visible")
    with  st.session_state.col[1]:
        st.session_state.distance = st.metric('Distance',f'{st.session_state.in_km}',delta=None)
    with  st.session_state.col[2]:
        st.session_state.name =  st.metric('Hospital Name',f'{st.session_state.hospital_name}',delta=None)
    st.session_state.Symptoms = st.empty()
    st.session_state.check = st.empty()
        
        
    st.markdown("### THE INFORMATION TO BE SENT TO THE HOSPITAL")

    # Set OpenAI API key from Streamlit secrets
    #openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "shared" not in st.session_state:
        st.session_state["shared"] = True


    if "messages" not in st.session_state:
        st.session_state.messages = []
        bot = f"""
                You are First Aid Bot Bot, an automated service to help with medical emergency till professional help arrives. \
                You first greet the customer, then collects the medical emergency, \
                Then you say this `Thank you for sharing that, the information has been sent to the nearest hospital requiring their assitant.\
                I'll provide you with guidance while we wait for professional assistance.Remember, your safety is our top priority.\
                Now, let's focus on getting you the first aid medical assistance you need.\`
                if a child was mentioned, then you ask if the child is less than a year or more than a year. \
                You return a first aid guidance according to the medical emergency in numerical order, add an entire line filled with asterisk after each number so as to ensure visibility.\
                You respond in a short, very conversational friendly style. \
                if they ask for an explanation from your guidance, you can return a link to a youtube video by \
                checking the dictionary {video_url} that contain all youtube links with the keys being similar to what they asked for\
                You can pick from it with respect to the question they asked you.\
                If the given message does not contain a medical related situation simply return `non medical related condition`
                """
        # Add user message to chat history
        st.session_state.messages.append({"role": "system", "content": bot})
        st.session_state.messages.append({"role": "user", "content": 'Hello'})
        with st.status("loading Chatbot...") as status:
            try:
                st.session_state.messages.append({'role':'assistant','content':get_completion_from_messages(st.session_state.messages)})
                status.update(label="Loading complete!", state="complete", expanded=False)
            except:
                status.update(label="Error Loading chatbot", state="error", expanded=False)
                st.stop()

    thread1 = threading.Thread(target=chatbot)#mp.Process(target=chatbot
    thread2 = threading.Thread(target=hospital_addition)
    add_script_run_ctx(thread1) 
    add_script_run_ctx(thread2) 
    thread1.start()
    thread2.start()
    #st.json(st.session_state.json)
    thread1.join()
    thread2.join()
    
    #
    
    # Start the threads
    
    #thread2.start()

    # Wait for both threads to finish
    
    #
if __name__ == "__main__":
    main()
