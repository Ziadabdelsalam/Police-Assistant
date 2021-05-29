# from Accident_Detection import *
# from Fire_Detection import *
import cv2
from Car_Plate_Detection import *
from Get_Plate_Characters import *
from Recognize_Faces import *
from Mask_Detection import *
from Accident_Detection import *
from Fire_Detection import *
from Check_Stolen_Plates import *

Detect_Accidents = Accident_Detection()
Detect_fire = Fire_Detection()
Car_Plate_Detection = Car_Plate_Detection()
Get_Plate_Characters = Get_Plate_Characters()
Recognize_Faces = Recognize_Faces()
Mask_Detection = Mask_Detection()

Frame_Number_For_Plate = 0
Frame_Number_For_Face = 0
Frame_Number_For_Accident = 0
Frame_Number_For_Fire = 0
Plate_Number = 0
Plate = []
Plates_detected = []
Stolen_Plates_detected = []
Plate_String = ""
Face_Number = 0
Wanted_Name = ""
state_of_accident = ""
filepath = "crash 4.mp4"
camera = cv2.VideoCapture(filepath)
for i in range(len(Stolen_Plates)):
    Stolen_Plates_detected.append(str(Stolen_Plates[i]))

# detect fire
state = Detect_fire.detect_from_video(filepath)
while camera.isOpened():

    ret, frame = camera.read()
    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    Frame_Number_For_Plate += 1
    Frame_Number_For_Face += 1
    Frame_Number_For_Accident += 1
    Frame_Number_For_Fire += 1
    if ret:
        # Detect Plates
        if Frame_Number_For_Plate == 20:
            Plate_Found = Car_Plate_Detection.Detect_Plate(frame, Plate_Number)
            if Plate_Found:
                Plate, image = Get_Plate_Characters.GetPlateChars(Plate_Number)
                Plates_detected.append(Plate)

                Plate_Number += 1
            Frame_Number_For_Plate = 0

        # Detect Mask
        frame, Face_Found = Mask_Detection.Detect_Mask(frame, Face_Number, Frame_Number_For_Face)
        if Face_Found == True:
            Wanted_Name = Recognize_Faces.Recognize_Face(Face_Number)
            Face_Number += 1
            Frame_Number_For_Face = 0

        if Frame_Number_For_Accident == 20:
            state_of_accident = Detect_Accidents.predict_accident(frame)
            print(state_of_accident)
            Frame_Number_For_Accident = 0

        frame = cv2.resize(frame, (1000, 1000))
        frame = cv2.putText(frame, str(Wanted_Name), (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2, cv2.LINE_AA, False)
        frame = cv2.putText(frame, state, (00, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2, cv2.LINE_AA, False)
        frame = cv2.putText(frame, state_of_accident, (00, 115), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2, cv2.LINE_AA, False)
        cv2.imshow("Streaming", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.waitKey()
camera.release()
cv2.destroyAllWindows()
