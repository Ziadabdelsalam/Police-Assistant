import cv2
import numpy as np
from imageai.Detection.Custom import CustomVideoObjectDetection
#from RUN import *
class Fire_Detection:
    def __init__(self):
        self.state = ""
        self.total_fire_frames = 0
        self.total_non = 0



    def forFrame(self, frame_number, output_array, output_count, frame):
        # cv2.imshow("Streaming", frame)
        # cv2.waitKey(1)
        if bool(output_count):
            global total_fire_frames
            self.total_fire_frames += 1
        else:
            global total_non
            self.total_non += 1


    def detect_from_video(self, filepath):
        detector = CustomVideoObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(detection_model_path="FireModel/detection_model-ex-33--loss-4.97.h5")
        detector.setJsonPath(configuration_json="FireModel/detection_config.json")
        detector.loadModel()

        detector.detectObjectsFromVideo(input_file_path=filepath,
                                                              frames_per_second=30, minimum_percentage_probability=30,
                                                              log_progress=True, save_detected_video=False,return_detected_frame=True,
                                                              per_frame_function=self.forFrame,
                                        frame_detection_interval=100 )

        if (self.total_fire_frames / (self.total_fire_frames + self.total_non)) * 100 >= 15:
            self.state = "FIRE DETECTED"
            print("FIRE DETECTED")
        else:
            self.state = "NO FIRE DETECTED"
            print("NO FIRE DETECTED")
        return self.state