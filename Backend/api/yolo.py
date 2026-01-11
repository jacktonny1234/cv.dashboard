from api.yolo_engine import yolo_predict
from api.yolo_engine import streaming_video
from flask import Blueprint, request, current_app, jsonify, g
from utils import getfilepath

yolo_v1 = Blueprint(
    'yolo_v1', 'yolo_v1', url_prefix='/api/v1/yolo')

@yolo_v1.route('/xx', methods=['POST'])
def yolo_test():
    print("xxxx")

@yolo_v1.route('/', methods=['POST', 'GET'])
def yolo():
    print("=" * 50)
    print("YOLO endpoint called")
    print(f"Request method: {request.method}")
    print(f"Request URL: {request.url}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request content type: {request.content_type}")
    print("=" * 50)
    
    if request.method == 'OPTIONS':
        print("OPTIONS request received")
        return jsonify({'status': 'ok'}), 200
    
    post_data = request.get_json()
    print("POST data received:", post_data)
    
    if post_data is None:
        print("ERROR: No JSON data received in request")
        return jsonify({'error': 'No JSON data received'}), 400
    
    try:
        if 'model' in post_data:
            model = post_data['model']
        if 'param' in post_data:
            param = post_data['param']
        if 'data' in post_data:
            pic_data = post_data['data']
        filepath = getfilepath(pic_data)
        if filepath[0]:

            batch =1
            max_det=300
            classes=None
            stream=False
            if 'batch' in param:
                batch = param['batch']
            if 'max_det' in param:
                max_det = param['max_det']
            if 'classes' in param:
                classes = param['classes']
            if 'stream' in param:
                stream = param['stream']
                
            return  jsonify(yolo_predict(model, filepath, batch, max_det, classes, stream)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

#result = yolo_predict(model="yolo11n.pt", source="tests/video.mp4", stream=True)
#result = streaming_video(model="yolo11n.pt", source="tests/test2.mp4", batch=32)

#print(result)


