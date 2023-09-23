video_url ={'Checking for responsiveness,CPR,breathing (PEDIATRIC)':'https://youtu.be/6THKEJ_Ciag?si=zSpovMTgjqagP1NB',
'Checking for pulse':'https://youtu.be/qaZrzoH8Jvk?si=ZSeejLc-QBh9Y7-Z',
'Checking for responsiveness':'https://youtu.be/9D9QQs4eBqE?si=iyznOw4349v57sfP',
'Checking for breathing': 'https://youtu.be/BAMsJDBgw0E?si=OYSeZCY4fUVlNVHb',
'Cpr adult':'https://youtu.be/1Zj-TyYzUis?si=2YfsWCy6Nkp4nLLW',
'Cpr Children':'https://youtu.be/Ll4qRB3kBGQ?list=PLf-OY7KYIoQrPGSiB63d3zi1y5OpMNLlf',
'Cpr Infant less than 1 year':'https://youtu.be/fJKHNh2BkQE?list=PLf-OY7KYIoQrPGSiB63d3zi1y5OpMNLlf'}

import streamlit as st
import openai
import time as t
import random as rn
from threading import Timer
from functions import get_response,return_output,get_completion_from_messages,timer
openai.api_key = "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"


st.title("RAPID CARE HUB")
if 'json' not in st.session_state:
    data_dict = {"Situation": None,
              "Age": None,
              "Gender": None,
              "Surgical Status": None,
              "Trauma Name": None,
              "Trauma Description": None,
              "Physicians": []}
    st.session_state.json = data_dict
    st.session_state.count = 0
if 'metric' not in st.session_state:
    st.session_state.no_of_acceptance = 0
    st.session_state.hospital_count = 0
    st.session_state.average = 0 
    st.session_state.start = 0
    st.session_state.add_hospital = 0
    st.session_state.metric = st.empty() #st.metric('Hospital', f'{st.session_state.hospital_count}/{st.session_state.no_of_acceptance}', delta=0, delta_color="off", help=None, label_visibility="visible")


st.markdown("### THE INFORMATION TO BE SENT TO THE HOSPITAL")

# Set OpenAI API key from Streamlit secrets
#openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"



st.json(st.session_state.json)
    
# Initialize chat history
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
        st.session_state.messages.append({'role':'assistant','content':get_completion_from_messages(st.session_state.messages)})
        status.update(label="Loading complete!", state="complete", expanded=False)
        
st.markdown("#### CHATBOT")    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message['role'] != 'system' and message['content'] != 'Hello':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
 # Display user message in chat message container
if prompt:= st.chat_input("What's Your Emergency?"):
    if st.session_state.count == 0:
        with st.status("Sending Data ..."):
            st.session_state.no_of_hospital = rn.randint(25,50)
            st.session_state.no_of_acceptance = rn.randint(1,st.session_state.no_of_hospital)
            st.session_state.average = 60/st.session_state.no_of_acceptance
            st.session_state.start = 0
            st.session_state.hospital_count = 0
            json_string = get_response(prompt)
       	    data_dict = return_output(json_string)
        
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
    
    while st.session_state.start < 60:
        st.write(st.session_state.start)
        add_time = int(st.session_state.average)
        st.session_state.add_hospital = rn.randint(1,4)
        st.session_state.start+=add_time
        t.sleep(add_time)
        #t = Timer(st.session_state.start, timer,[st.session_state.add_hospital]).start()
        st.session_state.hospital_count += timer(st.session_state.add_hospital,st.session_state.add_hospital,st.session_state.no_of_acceptance)
        st.session_state.metric.metric('Hospital', f'{st.session_state.hospital_count}/{st.session_state.no_of_hospital}',delta=st.session_state.add_hospital, delta_color="normal", help=None,label_visibility="visible")
        #st.rerun()

