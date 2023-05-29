from langdetect import detect_langs
from textblob import TextBlob
from flask import Flask,request,jsonify
import time
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")


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
            if from_lang == "ar":
                tokenizer.src_lang = "ar_AR"
                encoded_ar = tokenizer(sent, return_tensors="pt")
                generated_tokens = model.generate(**encoded_ar, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
                translated_sentence = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
                e = time.time()
                return jsonify({"language": f"{translated_sentence}","Time Taken":f"{round(e-s,3)}"})
            else:
                tokenizer.src_lang = "en_XX"
                encoded_ar = tokenizer(sent, return_tensors="pt")
                generated_tokens = model.generate(**encoded_ar, forced_bos_token_id=tokenizer.lang_code_to_id["ar_AR"])
                translated_sentence = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
                e = time.time()
                return jsonify({"language": f"{translated_sentence}", "Time Taken": f"{round(e - s, 3)}"})
        else:
            return jsonify({"language": "Not_Supported"})

if __name__ == '__main__':
    app.run(debug=True,port=5000)

