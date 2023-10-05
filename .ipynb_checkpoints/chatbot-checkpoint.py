

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

openai.api_key = "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"



def chatbot():
    # Initialize chat history
    
    st.markdown("#### CHATBOT")  
    for message in st.session_state.messages:
        if message['role'] != 'system' and message['content'] != 'Hello':
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
     # Display user message in chat message container
    if prompt:= st.chat_input("What's Your Emergency?"):
        if st.session_state.count == 0:
            with st.status("Sending Data ..."):
                st.session_state.no_of_hospital = rn.randint(250,500)
                st.session_state.no_of_acceptance = rn.randint(60,st.session_state.no_of_hospital+1)
                st.session_state.average = 60/st.session_state.no_of_acceptance
                st.session_state.start = 0
                st.session_state.hospital_added_index = np.array([])
                st.session_state.hospital_count = len(st.session_state.hospital_added_index)
                json_string = get_response(prompt)
                data_dict = return_output(json_string)
                symptoms = st.session_state.symptoms.multiselect('Select the Observable Symptoms',data_dict['Symptoms'])
                if st.button("Done"):
                    data_dict['Symptoms'] = symptoms
                    st.session_state.json = data_dict

            st.session_state.count+=1
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state.messages,
                    temperature = 0.8,
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
def hospital_addition():
    #st.write(st.session_state.no_of_acceptance)
    add_time = rn.randint(1,int(st.session_state.average)+1)
    st.session_state.add_hospital = rn.randrange(-2,6)
    st.session_state.start+=add_time
    #t = Timer(st.session_state.start, timer,[st.session_state.add_hospital]).start()
    try:
        s = timer(st.session_state.hospital_count,st.session_state.add_hospital,st.session_state.no_of_acceptance,st.session_state.hospital_added_index)#0]
        #return none
        if (s[0] is not None) and (s[1] is not None):
            st.session_state.add_hospital = s[0]
            st.session_state.hospital_added_index = s[1]
            st.session_state.hospital_count += st.session_state.add_hospital
            with col1:
                st.session_state.metric.metric('No of Hospital Accepted',f'{st.session_state.hospital_count}/{st.session_state.no_of_hospital}',delta=st.session_state.add_hospital,delta_color="normal", help=None,label_visibility="visible")
            t.sleep(add_time)
            st.session_state.index = np.array([i['Distance (km)'] for i in st.session_state.data[st.session_state.hospital_added_index]]).argmin()
            st.session_state.in_km = st.session_state.data[st.session_state.hospital_added_index][st.session_state.index]['Distance (km)']
            st.session_state.hospital_name = st.session_state.data[st.session_state.hospital_added_index][st.session_state.index]['Hospital Name']
            with col2:
                st.session_state.distance.metric('Distance',f'{st.session_state.in_km}',delta=None)
            with col3:
                st.session_state.name.metric('Hospital Name',f'{st.session_state.hospital_name}',delta=None)
            #t.write(st.session_state.data[st.session_state.hospital_added_index])
        else:
            pass
    except TypeError:
        pass
            

            
            

def main():
    st.title("RAPID CARE HUB")
    col1, col2, col3 = st.columns(3)

    if 'json' not in st.session_state:
        data_dict = {"Situation": None,
                  "Age": None,
                  "Gender": None,
                  "Surgical Status": None,
                  "Trauma Name": None,
                  "Trauma Description": None,
                  "Physicians": []
                    }
        st.session_state.json = data_dict
        st.session_state.count = 0
    if 'metric' not in st.session_state:
        st.session_state.hospital_added_index = np.array([])
        st.session_state.no_of_acceptance = 0
        st.session_state.hospital_count = 0#len(st.session_state.hospital_added_index)
        st.session_state.average = 0 
        st.session_state.no_of_hospital =0
        st.session_state.start = 0
        st.session_state.in_km = 0
        st.session_state.add_hospital = 0
        st.session_state.hospital_name = None

        try:
            with open('hospital_data.json', "r") as json_file:
                st.session_state.data = np.array(json.load(json_file))
        except FileNotFoundError:
            st.session_state.data = np.array([])
        with col1:
            st.session_state.metric = st.metric('No of Hospital Accepted',f'{st.session_state.hospital_count}/{st.session_state.no_of_hospital}',delta=st.session_state.add_hospital,delta_color="off", help=None,label_visibility="visible")
        with col2:
            st.session_state.distance = st.metric('Distance',f'{st.session_state.in_km}',delta=None)
        with col3:
            st.session_state.name =  st.metric('Hospital Name',f'{st.session_state.hospital_name}',delta=None)
        st.session_state.symptoms = st.empty()

    st.markdown("### THE INFORMATION TO BE SENT TO THE HOSPITAL")

    # Set OpenAI API key from Streamlit secrets
    #openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "shared" not in st.session_state:
        st.session_state["shared"] = True

    st.json(st.session_state.json,expanded=False)

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

    thread1 = threading.Thread(target=chatbot)
    add_script_run_ctx(thread1) 
    thread1.start()
    thread1.join()
    thread2 = threading.Thread(target=hospital_addition)
    add_script_run_ctx(thread2) 
    
    # Start the threads
    
    thread2.start()

    # Wait for both threads to finish
    
    thread2.join()
    
if __name__ == "__main__":
    main()
# Display chat messages from history on app rerun

