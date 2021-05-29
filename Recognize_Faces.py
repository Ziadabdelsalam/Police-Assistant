import face_recognition
class Recognize_Faces:
    def __init__(self):
        #Add Criminal Names

        Hossam_image = face_recognition.load_image_file("Wanted Criminals/Hossam Ahmed.jpg")
        Zeze_image = face_recognition.load_image_file("Wanted Criminals/Ziad Ahmed.jpg")
        Hossam_face_encoding = face_recognition.face_encodings(Hossam_image)[0]
        Zeze_face_encoding = face_recognition.face_encodings(Zeze_image)[0]
        self.known_faces = [Hossam_face_encoding, Zeze_face_encoding]
        self.Wanted_Criminals = ["Hossam Ahmed", "Ziad Ahmed"]

    def Recognize_Face(self, Face_Number):
        label = ""
        unknown_image = face_recognition.load_image_file("Non Masked Faces/" + str(Face_Number) + ".jpg")
        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        except IndexError:
            results = []
            return results
        results = face_recognition.compare_faces(self.known_faces, unknown_face_encoding)
        for i in range(len(results)):
            if results[i] == True:
                print(self.Wanted_Criminals[i])
                label = self.Wanted_Criminals[i]
        return label
