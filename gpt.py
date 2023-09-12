import openai,sys

openai.api_key = "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"

def reformat_text(x):
    text = ""
    for i in x:
        text+=f'{i} '
    return text
def prints(data,string):
    if string == 'p':
        print(f'Physician : {(data.strip())}')
    elif string == 'd':
        print(f'Diagnosis : {data.strip()}')

def append(filename,instance):
    with open(f'../Project_Files/{filename}','r+') as f:
        instances = f.readlines()
        f.close()
    if f'{instance}\n'not in instances:
        instances.append(f'{instance}\n')
        instances.sort()
        with open(f'../Project_Files/{filename}','w') as f:
            f.write(''.join(instances))
        print(f"Added 1 new instance, the total number of instances are {len(instances)}")
        f.close()
    else:
        print(f"Added 0 new instance, the total number of instances are {len(instances)}")
        f.close()
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "id be asking you some medical conditions, i want you to write by the side, the surgeon that should do it, if a GS can do it, add it to the list, just reply with the format \"DIAGNOSIS : medical_condition or injury that could have happened seperated by a comma \n PHYSICIAN : doctors_responsible for treating it,seperated by a comma \" and nothing else. if the message asked is wrong, return pleasse enter a correct medical issue, Thank you"
    },
    {
      "role": "user",
      "content": reformat_text(sys.argv[1:])
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
if len(response['choices'][0]['message']['content'].split('\n')) == 2:
    physician = [i.split(':')[1] for i in response['choices'][0]['message']['content'].split('\n')][1].split(',')
    diagnosis = [i.split(':')[1] for i in response['choices'][0]['message']['content'].split('\n')][0].split(',')
    for i in range(len(diagnosis)):
        prints(diagnosis[i],'d')
        append('emergency_data.txt',diagnosis[i].strip())
    for i in range(len(physician)):
        prints(physician[i],'p')
        append('physician.txt',physician[i].strip())
else:
	print('Wrong input')
