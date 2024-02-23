from flask import Flask,url_for,request,render_template,request,Response,make_response,send_from_directory
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
import PyPDF2 as pp

app = Flask(__name__)
app.static_url_path = "/"




@app.route('/', methods=["POST","GET"])
def index():
    return render_template('index.html')


@app.route("/merge", methods=["POST","GET"])
def mergeFiles():
    if request.method == "POST":
        pdfs = request.files.getlist("pdf")
        
        writer = pp.PdfWriter()
        for pdf in pdfs:
            writer.append(pdf)
        
        # print(savedpdfs)
        writer.write("myproject/static/Merged.pdf")
        # response = make_response("PDF MErged successfully")

        return url_for('static',filename="Merged.pdf")

    else:
        return render_template("mergefile.html")

@app.route("/gettext" ,methods=["POST","GET"])
def getText():
    if request.method == "POST":
        reader = pp.PdfReader(request.files.getlist("pdf")[0])
        def visitor_body(text, cm, tm, fontDict, fontSize):
            y = tm[5]
            if y > 50 and y < 720:
                parts.append(text)
        f = open("extract.txt","w")
        f.write(reader.pages[0].extract_text())
        f.close()
        return send_from_directory("extract.txt")
    else:
        return render_template("gettext.html")

@app.route("/getlast",methods=["POST","GET"])
def getLast():
    if request.method == "POST":
        reader = pp.PdfReader(request.files.getlist("pdf")[0])
        writer = pp.PdfWriter()
        writer.add_page(reader.pages[len(reader.pages)-1])
        writer.write("myproject/temp/lastpage.pdf")
        return '/temp/lastpage.pdf'
    else:
        return render_template("getlast.html")

@app.route("/splitpart" ,methods=["POST","GET"])
def splitpart():
    if request.method == "POST":
        return "File Here"
    else:
        return render_template("splitpart.html")

@app.route("/splitpdf",methods=["POST","GET"])
def splitPdf():
    if request.method == "POST":
        reader = pp.PdfReader(request.files.getlist("pdf")[0])
        # if(len(reader.pages) <= 25)
        
        for page in range(len(reader.pages)):
            writer = pp.PdfWriter()
            writer.add_page(reader.pages[page])
            writer.write(f"split/{page}.pdf")

        os.chdir(os.getcwd())
        os.system("python -m zipfile -c zips/split.zip 'split/'")


        return url_for("static",filename='zips/split.zip')
        # return send_from_directory(app.config["UPLOAD_PATH"],"split.zip")
    else:
        return render_template("splitpdf.html")

if __name__ == "__main__":
    app.run(debug=True)

# url_for() it builds the url for us. first arg = function name
# then the url parameters

with app.test_request_context():
    (url_for('static',filename="style.css"))