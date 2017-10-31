import requests
from bs4 import BeautifulSoup as BS4

def get_totalPages(str1):
    sub = ""
    num1 = 0
    of_found = False
    for i in range(0,len(str1)):
        if str1[i] == " ":
            if of_found == True:
               break
            else:
                if sub == "of":
                    of_found = True
                sub = ""
        else:
            sub+=str1[i]
    new_sub = ""
    for i in sub:
        if i !=",":
            new_sub+=i
    return int(new_sub)


def parseIndeed(id):
    response = {}
    r = requests.get(id)
    c = r.content
    soup = BS4(c,"html.parser")
    find_total = soup.find('div',{"id":"searchCount"}).text
    iterations = get_totalPages(find_total)
    bad_words = ["mentor", "mentoring", "Mentor","Mentoring","Guiding more junior peers","couch junior","guide junior","help junior", "teach junior", "assist junior"]
    junior_dict ={}
    add_count = 0
    page_var = ""
    count = 0

    while add_count * 15 <= iterations:
        if add_count>0:
            num_holder = 10 * add_count
            page_var = "&start=" + str(num_holder)
        r = requests.get(str(id)+page_var)
        c = r.content

        soup = BS4(c ,"html.parser")
        a_list = []
        b_list = []
        for i, j in zip(soup.find_all("a",{"data-tn-element":"jobTitle"}),soup.find_all("span",{'class':'company'})):
            if i != None and "senior" not in i.text.lower() and "sr." not in i.text.lower() and "lead" not in i.text.lower() and "principal" not in i.text.lower() and "Sr" not in i.text:
                count+=1
                a_list.append(i)
                b_list.append(j.text)
        for x, y, z in zip(soup.find_all("span",{"class":"summary"}),a_list,b_list):

            was_bad = False
            for b in bad_words:
                if b in x.text:
                    was_bad = True
            if was_bad == False:
                junior_dict[y.text]= [y["href"], z]

        add_count+=1
    return [junior_dict,iterations,len(junior_dict)]
