# -*- coding: UTF-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

the_books=[]

#srch_url=r"http://book.douban.com/subject_search?search_text=python"
srch_url=r"http://book.douban.com/subject_search"
keyword="Python"

if len(sys.argv)>2:
    print "This script only support 0 or 1 arguments!"
    sys.exit()

if len(sys.argv)==2:
    keyword=sys.argv[1]

print "the Keywork you indicated is: ", keyword
print "------------------------------------------------"
print "pages:"

while True:

    page=len(the_books)
    src_load={"start":page,"search_text":keyword,"cat":"1001"}

    req=requests.get(srch_url,params=src_load)
    #print req.url
    print page,
    sys.stdout.flush()

    soup=BeautifulSoup(req.text,'html.parser')

    #print soup(class_="subject-item")[12].prettify()
    #Rprint soup.prettify()

    #建立图书词典的列表
    for book_item in soup(class_="subject-item"):
        book_name=book_item(class_="info")[0].a.get_text("",strip=True)
        book_pic=book_item(class_="pic")[0].img["src"]
        book_link=book_item(class_="info")[0].a["href"]

        try:
            book_rating=book_item(class_="rating_nums")[0].get_text()
        except:
            book_rating="0"

        the_books.append({"book_name":book_name,"book_pic":book_pic,\
                          "book_link":book_link,"book_rating":book_rating})


    if (not soup(class_="next")) or (not soup(class_="next")[0].find_all("a")):
        print "no next page"
        break

print "------------------------------------------------------------------------------"

sorted_books=sorted(the_books,key=lambda book: book["book_rating"],reverse=True)

for book in sorted_books:
    print book["book_rating"].ljust(8),book["book_name"].ljust(30),book["book_link"]


print "total: "+str(len(the_books))+" books"

#for Mac using, no need to convert to gbk
#keyword_gbk=keyword.decode("utf-8").encode("gbk")
keyword_gbk=keyword

file_name=os.sep.join([os.getcwd(),keyword_gbk+".txt"])
with open(file_name,"w") as file_handle:
    for book in sorted_books:
        file_handle.write("".join([book["book_rating"].ljust(8),book["book_name"].ljust(30),book["book_link"]])+"\n")

    file_handle.write("------------------------------------------\n")
    file_handle.write("total:"+str(len(the_books))+" books")

