import os
import json

class FurnitureLoader():
    def __init__(self):
        self.index = 1;
        self.furniture = "lamp"
        self.furniture_path = "./static/furnitures/"
    def load(self):
        image_path = os.path.join(self.furniture_path, self.furniture, '{0:02}'.format(self.index), "image.png");
        json_path = os.path.join(self.furniture_path, self.furniture, '{0:02}'.format(self.index), "description.json")
        with open(json_path) as file:
            json_file = json.load(file)
        #self.index +=1;
        image_path = image_path[1:]
        return image_path, json_file
