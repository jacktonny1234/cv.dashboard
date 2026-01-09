from api.yolo_engine import yolo_predict
from api.yolo_engine import streaming_video
from flask import Blueprint, request, current_app, jsonify, g
from utils import getfilepath

yolo_v1 = Blueprint(
    'yolo_v1', 'yolo_v1', url_prefix='/api/v1/yolo')

@yolo_v1.route('/', methods=['POST'])
def yolo():
    post_data = request.get_json()
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


