import os
import json

class FurnitureLoader():
    def __init__(self, furniture=None):
        self.index = 1;
        if furniture is None:
            self.furniture="table"
        else:
            self.furniture = furniture
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", self.furniture, '{0:02}'.format(self.index))
        print(self.furniture_path)
    def set_furniture(self, furniture):
        self.furniture = furniture
        self.furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", self.furniture, '{0:02}'.format(self.index))

    def load(self):
        image_path = os.path.join(self.furniture_path, "image.png");
        json_path = os.path.join(self.furniture_path, "description.json")
        with open(json_path) as file:
            json_file = json.load(file)
        #self.index +=1;
        image_path = os.path.join("/static/furnitures/", self.furniture, '{0:02}'.format(self.index), "image.png");
        return image_path, json_file
