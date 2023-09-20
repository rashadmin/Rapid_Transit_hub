import openai,sys
import json
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
def add_to_json(diagnosis,physician):
    file_name = "history.json"

    try:
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []

    new_entry = {f'{diagnosis.strip()}':[f'{physician.strip()}']}

    new_key =list(new_entry.keys())[0]
    old_vals = [list(i.keys())[0] for i in data]
    if new_key not in old_vals:
        data.append(new_entry)
    elif new_key in old_vals:
        index = old_vals.index(new_key)
        new_val = list(new_entry.values())[0]
        current_val = data[index][new_key]
        if new_val[0] not in current_val:
            current_val.append(new_val[0])
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
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
        for j in range(len(physician)):
            prints(physician[j],'p')
            append('physician.txt',physician[j].strip())
            add_to_json(diagnosis[i],physician[j])
else:
	print('Wrong input')
