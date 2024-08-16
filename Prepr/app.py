import numpy as np
import mediapipe as mp
import math
import threading
from flask import Flask, jsonify, request
import os
import openai
import cv2 as cv
import multiprocessing
import speech_recognition as sr
import wave
import whisper
import secretkey
import gtts
from playsound import playsound
from flask_cors import CORS
import time


model = whisper.load_model('base')

# Constants for audio recording
FORMAT = sr.AudioData
CHANNELS = 1
RATE = 22000
RECORD_SECONDS = 45  

recognizer = sr.Recognizer()





mp_face_mesh = mp.solutions.face_mesh

app = Flask(__name__)
CORS(app)


interview_start_event = threading.Event()

eyePos = []
history = []
keyWords = ['teamwork', "communication", "problem-solving", "adaptability", "leadership", "punctuality", "initiative", "detail-oriented", "collaboration", "creativity", "critical-thinking", "decision-making", "conflict-resolution", "customer-service", "multitasking", "echnical-skills", "organization", "Self-motivation", "flexibility", "goal-oriented", "learning", "networking", "Project-management", "customer-focus", "innovation", "analysis", "empathy", "work-ethic", "resourcefulness", "professionalism"]
keyWordsHit = []
fillerWordsUsed = 0
count = 0
interviewDone = False
questionsForInterview = 1
openai.api_key = secretkey.SECRET_KEY
conversation = [{"role": "system", "content": "You are an interviewer for a company. You will ask behavioural questions similar to What is your biggest flaw or why do you want to work here. The first message you will say is Hello my name is Prepper and I will be your interviewer. Make sure to ask the questions one at a time and wait for the response. Make it seem like a natural conversation. Make sure the questions do not get too technical and if they do and you believe you cannot continue anymore say Alright and ask another behavioral question make sure you ask follow up questions based on the answers. MAKE SURE you also try and make it super casual, like you are my friend. Maybe even throw in a few jokes or something. After you believe the interview has gotten to a good ending point then you will say ONLY the phrase: ok then thank you so much for your time and have a nice day"}]



class chattingWork:

    interviewStart = 0

    def addUserConvo(self, message):
        conversation.append({"role": "user", "content": message})


    def addGPTConvo(self, response):
        conversation.append({"role": "user", "content": response["choices"][0]["message"]["content"]})


    def runConvo(self):
        inti = 0
        global questionsForInterview
        global interviewDone
        global count
        global fillerWordsUsed
        global conversation
        interview_start_event.wait() 
        while True:
            count += 1 
            if interviewDone == True:
                break
            if count >= questionsForInterview:
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You will say nothing except for the phrase: Unfortunatly we have run out of time. Thank you for taking the time to interview with us today Please make sure to press End Interview to ensure you get your results. Have a nice day!"}],
                temperature=0,
                )
                self.addGPTConvo(response)
                tts = gtts.gTTS(response["choices"][0]["message"]["content"], lang="en-GB", slow=False )
                tts.save("assets/bamzy.mp3")
                playsound("assets/bamzy.mp3")
                interviewDone = True
                break
            print("recording ... ")
            with sr.Microphone(sample_rate=RATE) as source:
                print("Recording...")
                audio = recognizer.listen(source)
            print("Recording stopped.")

            # Save the recorded audio to a WAV file
            with wave.open("assets/shamzy.mp3", 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.sample_width)
                wf.setframerate(RATE)
                wf.writeframes(audio.frame_data)

            result = model.transcribe('assets/shamzy.mp3', fp16 = False)
            self.addUserConvo(result['text'])
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0,
            )
            self.addGPTConvo(response)
            if(str.lower(response["choices"][0]["message"]["content"]) == "ok then thank you so much for your time and have a nice day"):
                break
            tts = gtts.gTTS(response["choices"][0]["message"]["content"], lang="en-GB", slow=False )
            tts.save("assets/bamzy.mp3")
            playsound("assets/bamzy.mp3")
            for word in result['text'].split():
                print(word)
                if word in keyWords and word not in keyWordsHit:
                    keyWordsHit.append(word)
                if str.lower(word) == 'um' or str.lower(word) == 'uh' or str.lower(word) == 'umm':
                    fillerWordsUsed += 1
            os.remove("assets/shamzy.mp3")
            os.remove("assets/bamzy.mp3")




class iris_recognition:

    cap = cv.VideoCapture(0)

    LEFT_IRIS = [474, 475, 476, 477]
    RIGHT_IRIS = [469, 470, 471, 472]

    L_H_LEFT = [33]     
    L_H_RIGHT = [133]  
    R_H_LEFT = [362]    
    R_H_RIGHT = [263]  

    def euclidean_distance(self, point1, point2):
        x1, y1 =point1.ravel()
        x2, y2 =point2.ravel()
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance

    def iris_position(self, iris_center, right_point, left_point):
        center_to_right_dist = self.euclidean_distance(iris_center, right_point)
        total_distance = self.euclidean_distance(right_point, left_point)
        ratio = center_to_right_dist/total_distance
        iris_position =""
        if ratio >= 2.2 and ratio <= 2.7:
            iris_position = "right"
        elif ratio >= 2.95 and ratio <= 3.2:
            iris_position = "left"
        else:
            iris_position = "center"
        return iris_position, ratio
    
    def runFullIris(self):
        global interviewDone
        with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
            count = 0
            while True:
                if interviewDone:
                    gpt_thread.join()
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = cv.flip(frame, 1)
                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  
                img_h, img_w = frame.shape[:2]
                results = face_mesh.process(rgb_frame)
                if results.multi_face_landmarks:
                    mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])

                    (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[self.LEFT_IRIS])
                    (r_cx,r_cy), r_radius = cv.minEnclosingCircle(mesh_points[self.RIGHT_IRIS])

                    center_left = np.array([l_cx, l_cy], dtype=np.int32)
                    center_right = np.array([r_cx, r_cy], dtype=np.int32)

                    cv.circle(frame, center_left, int(l_radius), (255, 0, 255), 1, cv.LINE_AA)
                    cv.circle(frame, center_right, int(r_radius), (255, 0, 255), 1, cv.LINE_AA)

                    cv.circle(frame, mesh_points[self.R_H_RIGHT][0], 3, (255, 255, 255), -1, cv.LINE_AA)
                    cv.circle(frame, mesh_points[self.R_H_LEFT][0], 3, (0, 255, 255), -1, cv.LINE_AA)

                    iris_pos, ratio = self.iris_position(center_right, mesh_points[self.R_H_RIGHT], mesh_points[self.R_H_LEFT][0])

                    # print(iris_pos)
                    # print(count)
                    count += 1
                if count % 30 == 0 and count != 0:
                    eyePos.append(iris_pos)
                cv.imshow("img", frame)
                key = cv.waitKey(1)
                if key ==ord("q"):
                    x = calcPercentage(eyePos, "center")
                    print("THE ACCURACY IS ", x , "%")
                    print(keyWordsHit)
                    break
        self.cap.release()
        cv.destroyAllWindows()

def calcPercentage(arr, target):
    num = 0
    if len(arr) > 0:
        for x in arr:
            if x == target:
                num += 1
        return (num/len(arr)) * 100
    else:
        return 0


def runIris():
    ir = iris_recognition()
    ir.runFullIris()

def runGPT():
    gpt = chattingWork()
    gpt.runConvo()


@app.route('/GetContactPercentage', methods = ['POST', 'GET'])
def getContactPercentage():
    try:
        return jsonify(float(round(calcPercentage(eyePos, "center"), 2))), 200
    except:
        return jsonify({'message': 'There was a problem getting the eye contact accuracy'}), 400
    

@app.route('/getKeyWordUsage', methods = ['GET'])
def getKeyWordUsage():
    try:

        return jsonify(keyWordsHit), 200
    except:
        return jsonify({'message': 'There was a problem getting the key words used'}), 400
    

@app.route('/getFillerWordsUsed', methods = ['GET'])
def getFillerWordUsage():
    try:

        return jsonify(fillerWordsUsed), 200
    except:
        return jsonify({'message': 'There was a problem getting the number of filler words used'}), 400



    
@app.route('/StartInterview', methods=['POST', 'GET'])
def startInterview():
    global conversation
    global count
    try:
        eyePos.clear()
        keyWordsHit.clear()
        conversation = [{"role": "system", "content": "You are an interviewer for a company. ..."}]
        count = 0
        interview_start_event.set()  # Set the event to start the interview
        print("Interview started")
        return jsonify({'message': 'Interview was started'}), 200
    except:
        return jsonify({'message': 'There was a problem starting the interview'}), 400
    
@app.route('/EndInterview', methods=['POST', 'GET'])
def endInterview():
    global interviewDone
    try:
        interviewDone = True
        return jsonify({'message': 'Interview was ended'}), 200
    except:
        return jsonify({'message': 'There was a problem ending the interview'}), 400

@app.route('/isInterviewDone', methods = ['POST', 'GET'])
def isInterviewDone():
    try:
        jsonify({'message': interviewDone}), 200
    except:
        return jsonify({'message': 'There was a problem getting the status of the interview'}), 400

    




if __name__ == "__main__":
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=2516))
    gpt_thread = threading.Thread(target=runGPT)


    flask_thread.daemon = True
    gpt_thread.daemon = True

    gpt_process = multiprocessing.Process(target=runGPT)

    flask_thread.start()
    gpt_thread.start()
    runIris()