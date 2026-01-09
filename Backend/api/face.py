from flask import Blueprint, request, current_app, jsonify, g
# from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy
# from flask_cors import CORS
from datetime import datetime
# from bson.json_util import dumps
#from db import db, get_db, get_books, add_books
#from utils import expect
from utils import getfilepath
import subprocess
import io
from flask.wrappers import Request
import os
import ctypes
#import base64
#import datetime
#import random, string
import math
#from google.cloud import storage
#from app import app

face_v1 = Blueprint(
    'face_v1', 'face_v1', url_prefix='/api/v1/face')


@face_v1.route('/facialfeatures', methods=['POST'])
def facialfeatures():
    """ #for test
    filepath = os.path.abspath(os.path.dirname(__file__) + '/../uploads/photo1.jpg')

    faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
    faceSDKExt.InitFunctions()

    arr = (ctypes.c_int*144)()
    angle = (ctypes.c_float*1)()
    faceSDKExt.FaceDetectFromFileName(filepath, arr, angle)

    features = []
    i = 4
    while i < 144:
        features.append([arr[i], arr[i + 1]])
        i += 2
    
    ret = {
        "xc": arr[0],
        "yc": arr[1],
        "w": arr[2],
        "padding": arr[3],
        "angle": angle[0],
        "features": features
    }
    
    return jsonify(ret), 200
    """
    post_data = request.get_json()
    try:
        if 'data' in post_data:
            pic_data = post_data['data']
        filepath = getfilepath(pic_data)
        if filepath[0]:

            faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
            faceSDKExt.InitFunctions()

            arr = (ctypes.c_int*144)()
            angle = (ctypes.c_float*1)()
            faceSDKExt.FaceDetectFromFileName(filepath, arr, angle)

            features = []
            i = 4
            while i < 144:
                features.append([arr[i], arr[i + 1]])
                i += 2
            
            ret = {
                "xc": arr[0],
                "yc": arr[1],
                "w": arr[2],
                "padding": arr[3],
                "angle": angle[0],
                "features": features
            }
            
            return jsonify(ret), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    #"""


@face_v1.route('/age', methods=['POST'])
def age():
    """ #for test
    filepath = os.path.abspath(os.path.dirname(__file__) + '/../uploads/photo1.jpg')

    faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
    faceSDKExt.InitFunctions()

    arr = (ctypes.c_float*500)()
    faceCount = faceSDKExt.AgeGenderExpressionDetectFromFileName(filepath, arr)

    ages = []
    i = 0
    while i < faceCount:
        ages.append(math.ceil(arr[i * 5]))
        i += 1
    
    ret = {
        "ages": ages
    }

    return jsonify(ret), 200
    """
    post_data = request.get_json()
    try:
        if 'data' in post_data:
            pic_data = post_data['data']
        filepath = getfilepath(pic_data)
        if filepath[0]:

            faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
            faceSDKExt.InitFunctions()

            arr = (ctypes.c_float*500)()
            faceCount = faceSDKExt.AgeGenderExpressionDetectFromFileName(filepath, arr)

            ages = []
            i = 0
            while i < faceCount:
                ages.append(math.ceil(arr[i * 5]))
                i += 1
            
            ret = {
                "ages": ages
            }
            
            return jsonify(ret), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    #"""


@face_v1.route('/gender', methods=['POST'])
def gender():
    """ #for test
    filepath = os.path.abspath(os.path.dirname(__file__) + '/../uploads/photo1.jpg')

    faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
    faceSDKExt.InitFunctions()

    arr = (ctypes.c_float*500)()
    faceCount = faceSDKExt.AgeGenderExpressionDetectFromFileName(filepath, arr)

    genders = []
    i = 0
    while i < faceCount:
        if arr[i * 5 + 1] > arr[i * 5 + 2]:
            genders.append("Male " + str(math.floor(arr[i * 5 + 2]*100))+"%")
        else:
            genders.append("Female " + str(math.floor(arr[i * 5 + 2]*100))+"%")
        i += 1
    
    ret = {
        "genders": genders
    }

    return jsonify(ret), 200
    """
    post_data = request.get_json()
    try:
        #pic_data = expect(post_data.get('data'), str, 'data')
        if 'data' in post_data:
            pic_data = post_data['data']
        filepath = getfilepath(pic_data)
        if filepath[0]:

            faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
            faceSDKExt.InitFunctions()

            arr = (ctypes.c_float*500)()
            faceCount = faceSDKExt.AgeGenderExpressionDetectFromFileName(filepath, arr)

            genders = []
            i = 0
            while i < faceCount:
                if arr[i * 5 + 1] > arr[i * 5 + 2]:
                    genders.append("Male " + str(math.floor(arr[i * 5 + 2]*100))+"%")
                else:
                    genders.append("Female " + str(math.floor(arr[i * 5 + 2]*100))+"%")
                i += 1
            
            ret = {
                "genders": genders
            }
            
            return jsonify(ret), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    #"""

@face_v1.route('/expression', methods=['POST'])
def expression():
    """ #for test
    filepath = os.path.abspath(os.path.dirname(__file__) + '/../uploads/photo1.jpg')

    faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
    faceSDKExt.InitFunctions()

    arr = (ctypes.c_float*500)()
    faceCount = faceSDKExt.AgeGenderExpressionDetectFromFileName(filepath, arr)

    expressions = []
    i = 0
    while i < faceCount:
        expressions.append("Smile: " + str(math.floor(arr[i * 5 + 3]*100))+"%,  Blink open: " + str(math.floor(arr[i * 5 + 4]*100))+"%")
        i += 1
    
    ret = {
        "expressions": expressions
    }

    return jsonify(ret), 200
    """
    post_data = request.get_json()
    try:
        if 'data' in post_data:
            pic_data = post_data['data']
        filepath = getfilepath(pic_data)
        if filepath[0]:

            faceSDKExt = ctypes.CDLL(os.path.dirname(__file__) + '/../libFaceSDKExt.so')
            faceSDKExt.InitFunctions()

            arr = (ctypes.c_float*500)()
            faceCount = faceSDKExt.AgeGenderExpressionDetectFromFileName(filepath, arr)

            expressions = []
            i = 0
            while i < faceCount:
                expressions.append("Smile: " + str(math.floor(arr[i * 5 + 3]*100))+"%,  Blink open: " + str(math.floor(arr[i * 5 + 4]*100))+"%")
                i += 1
            
            ret = {
                "expressions": expressions
            }
            
            return jsonify(ret), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    #"""

