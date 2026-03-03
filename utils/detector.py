from ultralytics import YOLO
import cv2

model = YOLO("model/best.pt")

def detect_image(input_path, output_path):
    
    results = model.predict(
        source=input_path,
        conf=0.25,   
        iou=0.5,
        save=False
    )

    img = cv2.imread(input_path)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            label = f"{model.names[cls]} {conf:.2f}"

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imwrite(output_path, img)
