from ultralytics import YOLO
from subprocess import Popen, PIPE
import cv2

models_path = "./models/"

def yolo_predict(model_path="yolo11n.pt", source="", batch=1, max_det=300, classes=None, stream=False):
    """
    Predict using YOLO model.

    Parameters:
    model (str): Path to the model file.
    source (str): Path to the source image or video.
    batch (int): Batch size for prediction.
    max_det (int): Maximum number of detections per image.
    classes (list): List of class indices to filter by.
    stream (bool): Whether to stream the results.

    Returns:
    dict: Dictionary containing detections and class names.
    """
    # Load a model
    model = YOLO(models_path + model_path)

    if source == "":
        return None
    
    # predict on an image
    detections = model(source=source, batch=batch, max_det=max_det, classes=classes, stream=stream)

    rets = []
    for detection in detections:
		#print(detection.boxes)
		#detection.show()

        if detection.boxes is not None:
            xyxy = detection.boxes.xyxy.tolist()
            conf = detection.boxes.conf.tolist()
            cls = detection.boxes.cls.tolist()

        if detection.masks is not None:
            xy = []
            for m_xy in detection.masks.xy:
                xy.append(m_xy.tolist())

        if detection.keypoints is not None:
            xy = detection.keypoints.xy.tolist()
            conf = detection.keypoints.conf.tolist()

        if detection.probs is not None:
            top1 = detection.probs.top1
            top5 = detection.probs.top5

        if detection.obb is not None:
            conf = detection.obb.conf.tolist()
            cls = detection.obb.cls.tolist()
            xyxyxyxy = detection.obb.xyxyxyxy.tolist()

        ret = {
            "boxes": {"xyxy": xyxy, "conf": conf, "cls": cls} if detection.boxes is not None else None,  # Convert tensor to list if not None
            "masks": {"xy": xy} if detection.masks is not None else None,  # Convert tensor to list if not None
            "keypoints":{"xy": xy, "conf": conf} if detection.keypoints is not None else None,  # Convert tensor to list if not None
            "probs": {"top1": top1, "top5": top5} if detection.probs is not None else None,  # Convert tensor to list if not None
            "obb": {"xyxyxyxy": xyxyxyxy, "conf": conf, "cls": cls} if detection.obb is not None else None  # Convert tensor to list if not None
        }

        rets.append(ret)
        
    if detection is not None:
        #print(rets)
        return {
            "detections": rets,
            "names": detection.names
        }
    else:
        return None

def streaming_video(source, model="yolo11n.pt", batch=1, max_det=300, classes=None):
    """
    Stream video with YOLO predictions.

    Parameters:
    source (str): Path to the source video.
    model (str): Path to the model file.
    batch (int): Batch size for prediction.
    max_det (int): Maximum number of detections per image.
    classes (list): List of class indices to filter by.

    Returns:
    None
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    model = YOLO(models_path + model)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=5000', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = model(source=frame, batch=batch, max_det=max_det, classes=classes, stream=True)

        for detection in detections:
            for box in detection.boxes:
                for xyxy in box.xyxy:
                    x1, y1, x2, y2 = xyxy
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        out.write(frame)

        # cv2.imshow('YOLO Stream', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

