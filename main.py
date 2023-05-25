from langdetect import detect_langs
from textblob import TextBlob
from flask import Flask,request,jsonify
import time


app = Flask(__name__)
@app.route('/dt',methods=["GET"])
def detect_lang():
    if request.method =="GET":
        sent = request.json["sentence"]
        if sent.isnumeric():
            return jsonify({"language": "Not_Supported"})
        s = time.time()
        detections = str(detect_langs(sent)[0]).split(":")
        print(detections)
        e = time.time()
        if float(detections[1]) >= 0.6:
            return jsonify({"language": f"{detections[0]}","Time Take":f"{round(e-s,3)}"})
        else:
            return jsonify({"language": "Not-Sure", "Time Take": f"{round(e - s, 3)}"})



@app.route('/tr',methods=["GET"])
def translate_sent():
    if request.method =="GET":
        sent = request.json["sentence"]
        if sent.isnumeric():
            return jsonify({"language": "Not_Supported"})
        s = time.time()
        from_lang = str(detect_langs(sent)[0]).split(":")[0]
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

