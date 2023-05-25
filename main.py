from langdetect import detect
from textblob import TextBlob
from flask import Flask,request,jsonify
import time


app = Flask(__name__)
@app.route('/detect_language',methods=["GET"])
def detect_lang():
    if request.method =="GET":
        sent = request.json["sentence"]
        s = time.time()
        detection = detect(sent)
        e = time.time()
        try:
            return jsonify({"language": f"{detection}","Time Take":f"{round(e-s,3)}"})
        except Exception as ex:
            print(ex)
            return jsonify({"language": "Unknown","Time Take":f"{round(e-s,3)}"})

@app.route('/translate_sentence',methods=["GET"])
def translate_sent():
    if request.method =="GET":
        sent = request.json["sentence"]
        s = time.time()
        from_lang = detect(sent)

        print(from_lang)
        if from_lang == "ar" or from_lang == "en":
            sent = TextBlob(sent)
            if from_lang == "ar":
                translated_sentence = sent.translate(from_lang=from_lang,to="en")
                e = time.time()
                return jsonify({"language": f"{translated_sentence}","Time Taken":f"{round(e-s,3)}"})
            else:
                translated_sentence = sent.translate(from_lang=from_lang, to="ar")
                e = time.time()
                return jsonify({"language": f"{translated_sentence}","Time Taken":f"{round(e-s,3)}"})

        else:
            return jsonify({"language": "Not_Supported"})

if __name__ == '__main__':
    app.run(debug=True,port=5000)

