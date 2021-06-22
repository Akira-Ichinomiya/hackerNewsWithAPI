import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story" #new 기준 사이트 주소

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story" #popular 기준 사이트 주소

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

app = Flask("Day 9 News")

db = [requests.get(popular).json(), requests.get(new).json()]

@app.route("/")
def home(): #default는 popular이므로 popular을 기준으로 기사 리스트를 보여줌
    try:
        if request.args["order_by"] == "new":
            return render_template("detail.html", data=db[1], isPopular=False)
        elif request.args["order_by"] == "popular":
            return render_template("detail.html", data=db[0], isPopular=True)
        else:
            return render_template("detail.html", data=db[0], isPopular=True)
    except:
            return render_template("detail.html", data=db[0], isPopular=True)

@app.route("/<int:param>") # id에 해당하는 기사의 덧글들을 detail에 추가 후 detail.html 반환
def newsComments(param):
    urlForComment = make_detail_url(f"{param}")
    urlForComment = requests.get(urlForComment).json()
    return render_template("comment.html", data=urlForComment, id=param)


app.run()