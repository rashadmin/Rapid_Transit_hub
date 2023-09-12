# Trying to get all medical terms for a given medical html page
import bs4, sys

with open(f'/home/py_sama/Project_Files/index?letter={sys.argv[1]}', 'r') as f:
    webpage = f.read()#.decode('utf-8')
# open web page for scraping
soup = bs4.BeautifulSoup(webpage,features="lxml")
# Get all medical term link name
lists = soup.find_all('a',{'class':'cmp-anchor--plain cmp-button cmp-button__link cmp-result-name__link'})
for i in lists:
    with open('/home/py_sama/Project_Files/emergencies.txt', "a+") as f:
        #append to files
        f.write(f'{i.text}\n')
# Get all the medical term with paragraph tags
lists_p = soup.find_all('p','cmp-results-with-primary-name__label')
# Get all the medical term with paragraph tags(alternative in the a tag)
lists_a = soup.find_all('a','cmp-anchor--plain cmp-button cmp-button__link cmp-results-with-primary-name__see-link')
for i,j in zip(lists_p,lists_a):
    with open('/home/py_sama/Project_Files/emergencies_alternative.txt', "a+") as f: 
        #append them to a new file with the name and the alternative name for it
        f.write(f'{i.text},{j.text}\n')
