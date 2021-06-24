import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""
thousand = 1000

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

def get_checklist(on_db):
    result=[]
    # print(on_db)
    for category in on_db:
        title, upvote, tag, url = None,None,f"r/{category}", None
        req = requests.get(f"https://www.reddit.com/r/{category}/top/?t=month", headers=headers) #체크 항목 사이트 request하기
        html = BeautifulSoup(req.text, 'html.parser').find_all(class_ = "_1oQyIsiPHYt6nx7VOmd1sz")#html얻기
        
        for li in html:# 변수구하기. 게시글 박스들을 반복문으로 조사
            ad = li.find("span", class_ = "_2oEYZXchPfHwcf9mTMGMg8") #광고글이 유일하게 가지고 있는 span이다.
            if ad is None: #광고글이 아니라면
                title = li.find("h3", class_ = "_eYtD2XCVieq6emjKBH3m").text #title 값
                upvote = li.find("div", class_ = "_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo").text #upvote값
                url = li.find("a", class_= "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE").attrs["href"] #url값
                if "k" in upvote: #k단위로 나타나는 값들을 숫자값으로로 치환
                    upvote = float(upvote.replace("k", ""))*thousand
            extracted = {"title":title, "upvote":int(upvote), "tag":tag, "url":url}
            if extracted not in result: #중복 검사
                result.append(extracted) #조건을 잘 거친 항목을 result에 추가
    result.sort(key=lambda x:x["upvote"], reverse=True) #upvote 내림차순으로 정렬
    return result 

        
        
    #배열에 게시글에 필요한 값을 얻어서 넣기(제목이랑 upvotes값 얻어야함)

#배열에 모든 게시글데이터를 얻었으면 득표수를 기준으로 하여 sort하기
#배열 반환하기
    

app = Flask("DayEleven")



@app.route("/")
def home():
    return render_template("home.html", subreddits=subreddits)

@app.route("/read")
def show():
    on_db = []
    for arg in subreddits:
        if request.args.get(arg): #on으로 되어있는 데이터의 key값을 얻기
            on_db.append(arg)
    result = get_checklist(on_db)
    return render_template("read.html", meta=result, db_list=on_db)
app.run()

