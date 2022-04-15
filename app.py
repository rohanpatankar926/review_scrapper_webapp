from math import prod
from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
import requests
from flask_cors import CORS, cross_origin
from urllib.request import urlopen as ureq

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET"])
@cross_origin()
def home_page():
    return render_template("index.html")


@app.route("/review", methods=["GET", "POST"])
@cross_origin()
def index():
        if request.method == "POST":
            try:

                search_string = request.form["content"].replace(" ", "")
                flipkart_url = "https://www.flipkart.com/search?q="+search_string
                uclient = ureq(flipkart_url)
                flipkart_page = uclient.read()
                uclient.close()
                flipkart_html_render = bs(flipkart_page, "html.parser")
                whole_box = flipkart_html_render.findAll(
                    "div", {"class": "_1AtVbE col-12-12"})
                del whole_box[0:3]
                box = whole_box[0]
                product_link = "https://www.flipkart.com" + \
                    box.div.div.div.a["href"]
                prod_res = requests.get(product_link)
                product_html = bs(prod_res.text, "html.parser")
                print(product_html)
                comment_box = product_html.find_all(
                    'div', {'class': '_16PBlm'})
                filename = search_string + ".csv"
                fw = open(filename, "w")
                headers = "Product, Customer Name, Rating, Heading, Comment \n"
                fw.write(headers)
                reviews = []
                for commentbox in comment_box:
                    try:
                        name = commentbox.div.div.find_all(
                            'p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                    except:
                        name = 'No Name'

                    try:
                        # rating.encode(encoding='utf-8')
                        rating = commentbox.div.div.div.div.text

                    except:
                        rating = 'No Rating'

                    try:
                        # commentHead.encode(encoding='utf-8')
                        commentHead = commentbox.div.div.div.p.text

                    except:
                        commentHead = 'No Comment Heading'
                    try:
                        comtag = commentbox.div.div.find_all(
                            'div', {'class': ''})
                        # custComment.encode(encoding='utf-8')
                        custComment = comtag[0].div.text
                    except Exception as e:
                        print("Exception while creating dictionary: ", e)

                    mydict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}

                    reviews.append(mydict)
                return render_template("results.html", reviews=reviews[0:(len(reviews)-1)])
            except Exception as e:
                error = e
                error = {"error": error}
                return render_template("c404.html", error=error)
        else:
            return render_template("index.html")
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True,port=5000)
