import cv2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from tensorflow.keras.models import load_model

class Mask_Detection:
	def __init__(self):
		#Model Configuration for Mask Model
		prototxtPath = "MaskModel/deploy.prototxt"
		weightsPath = "MaskModel/res10_300x300_ssd_iter_140000.caffemodel"
		self.faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
		self.maskNet = load_model("MaskModel/mask_detector.model")

	def detect_and_predict_mask(self, frame, faceNet, maskNet):
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
		faceNet.setInput(blob)
		detections = faceNet.forward()
		faces = []
		locs = []
		preds = []
		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > 0.75:
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				(startX, startY) = (max(0, startX), max(0, startY))
				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
				face = frame[startY:endY, startX:endX]
				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
				face = cv2.resize(face, (224, 224))
				face = img_to_array(face)
				face = preprocess_input(face)
				faces.append(face)
				locs.append((startX, startY, endX, endY))
		if len(faces) > 0:
			faces = np.array(faces, dtype="float32")
			preds = maskNet.predict(faces, batch_size=32)
		return (locs, preds)

	def Detect_Mask(self, frame, Face_number, Frame_number):
		frame = cv2.resize(frame, (400, frame.shape[0]))
		(locs, preds) = self.detect_and_predict_mask(frame, self.faceNet, self.maskNet)
		ToSaveLabel = False
		for (box, pred) in zip(locs, preds):
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred

			label = "Mask" if mask > withoutMask else "No Mask"
			if label == "No Mask" and Frame_number >= 20:
				cv2.imwrite("Non Masked Faces/" + str(Face_number) + ".jpg", frame)
				ToSaveLabel = True
			color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
			label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
			cv2.putText(frame, label, (startX, startY - 10),
						cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

		return frame, ToSaveLabel
