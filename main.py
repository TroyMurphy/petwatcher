import requests
import json
from bs4 import BeautifulSoup
from DogResult import DogResult
from emailer import send_mail_using_gmail
from texter import send_real_text


def main():
    print("working")

    URL = 'https://aarcs.ca/adoptable-dogs/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='main-content')
    job_elems = results.find_all('td', class_='many-animal-view')

    activeDogs = []

    for job_elem in job_elems:
        dog_name = job_elem.find('h2', class_="profile-name").text
        is_dog_active = job_elem.find(
            'div', string=lambda text: text and 'Pending Application' in text) is None
        if is_dog_active:
            dog_link = job_elem.find('a')['href']
            dog_image = job_elem.find('img')['src']
            activeDogs.append(DogResult(dog_name, dog_link, dog_image))

    savedDogs = get_saved_dogs()

    newlyAddedDogs = [x for x in activeDogs if x.name not in savedDogs]
    if (len(newlyAddedDogs)):
        send_email(newlyAddedDogs)
        send_real_text(
            "{0} new dogs have been added to AARCS! https://aarcs.ca/adoptable-dogs/".format(len(newlyAddedDogs)))

    write_saved_dogs([x.name for x in activeDogs])


def get_saved_dogs():
    with open('saved_dog_names.txt', 'r') as f:
        return json.loads(f.read())


def write_saved_dogs(dog_names):
    with open("saved_dog_names.txt", 'w') as f:
        f.write(json.dumps(dog_names))


def send_email(contents):
    #print("{0} new dogs have been added to AARCS!".format(len(contents)))
    # for dog in contents:
    #	print(dog.link)
    send_mail_using_gmail(contents)


if __name__ == "__main__":
    main()
