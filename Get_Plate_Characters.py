from Extract_Character import *
from Character_Recognizer import *
from digit_recognizer_ import *
from Check_Stolen_Plates import *
class Get_Plate_Characters:
    def __init__(self):
        self.cr = Character_Recognizer()
        self.nr = Number_Recognizer()
        self.Ec = Extract_Characters()
        self.stolen_plates = []

    def GetPlateChars(self, PlateNumber):
        image = cv2.imread("Plates From Model/" + str(PlateNumber) + ".png")
        numbers, characters = self.Ec.extract(image)
        self.word = []
        for i in range(len(numbers)):
            self.word.append(self.nr.ocr(numbers[i]))

        for i in range(len(characters)):
            self.word.append(self.cr.ocr(characters[i]))
        print(self.word)
        self.word.reverse()
        Found = Compare_Plates(self.word)
        if Found == True:
            print("Is Stolen" + str(self.word))
        self.stolen_plates.append(self.word)


        return self.word, image
