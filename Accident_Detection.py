import torch
from PIL import Image, ImageFile
from torch import nn
from torchvision import models, transforms
import cv2


class Accident_Detection:
    def __init__(self):
        print("Here")
        print(torch.__version__)
        self.Frame_Number_for_acc = 0
        total_accident_frames = 0
        total_accident_non = 0


    '''def accidents_predict(self, frame):
        train_on_gpu = torch.cuda.is_available()
        if not train_on_gpu:
            print('CUDA is not available.  Training on CPU ...')

        else:
            print('CUDA is available!  Training on GPU ...')
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        test_transforms = transforms.Compose([transforms.Resize(255),
                                              transforms.ToTensor(),
                                              ])
        model = models.densenet161()
        model.classifier = nn.Sequential(nn.Linear(2208, 1000),
                                         nn.ReLU(),
                                         nn.Dropout(0.2),
                                         nn.Linear(1000, 2),
                                         nn.LogSoftmax(dim=1))
        #model = model.cuda()
        model.load_state_dict(torch.load("Accident Model/tensorboardexp.pt",map_location=torch.device('cpu')))
        classes = ["accident", "noaccident"]
        count = 0
        counts = 1
        label_arr = []
        text = ""
        counter = 0
        img = Image.fromarray(frame)
        img = test_transforms(img)
        img = img.unsqueeze(dim=0)
        # img = img.cuda()
        model.eval()
        with torch.no_grad():
            output = model(img)
            _, predicted = torch.max(output, 1)
            index = int(predicted.item())
            if index == 0:
                count += 1
                if counts == 1:
                    counts += 1
            labels = classes[index]
        print(labels)
        text = labels
        label_arr.append(labels)
        if counter == 200:
            return label_arr
        return label_arr'''
    def predict_accident(self, frame):
        train_on_gpu = torch.cuda.is_available()
        count = 0
        counts = 1
        label_arr = []
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        test_transforms = transforms.Compose([transforms.Resize(255),
                                              transforms.ToTensor(),
                                              ])
        model = models.densenet161()
        model.classifier = nn.Sequential(nn.Linear(2208, 1000),
                                         nn.ReLU(),
                                         nn.Dropout(0.2),
                                         nn.Linear(1000, 2),
                                         nn.LogSoftmax(dim=1))
        # model = model.cuda()
        model.load_state_dict(torch.load("Accident Model/tensorboardexp.pt", map_location=torch.device('cpu')))
        classes = ["accident", "noaccident"]
        img = Image.fromarray(frame)
        img = test_transforms(img)
        img = img.unsqueeze(dim=0)
        # img = img.cuda()
        model.eval()
        with torch.no_grad():
            output = model(img)
            _, predicted = torch.max(output, 1)
            index = int(predicted.item())
            if index == 0:
                count += 1
                if counts == 1:
                    counts += 1
            labels = classes[index]

        # print(labels)
        label_arr.append(labels)
        total_accident_frames = 0
        total_accident_non = 0
        state_of_accident = ""
        for i in label_arr:
            if i == "accident":
                total_accident_frames += 1
            else:
                total_accident_non += 1
        if (total_accident_frames / (total_accident_frames + total_accident_non)) * 100 >= 15:
            state_of_accident = "ACCIDENT DETECTED"

        else:
            state_of_accident = "NO ACCIDENT DETECTED"
        return state_of_accident
