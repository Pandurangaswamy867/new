from flask import Flask,render_template
app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def start ():
    return "Hello what ever"
if __name__ =="__main__":
     app.run(debug=True,host="0.0.0.0",port=2000)
