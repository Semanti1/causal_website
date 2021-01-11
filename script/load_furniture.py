import os
import json

class FurnitureLoader():
    def __init__(self):
        self.index = 1;
        self.furniture = "table"
        self.furniture_path = os.path.join("./static/furnitures/", self.furniture, '{0:02}'.format(self.index))
    def load(self):
        image_path = os.path.join(self.furniture_path, "image.png");
        json_path = os.path.join(self.furniture_path, "description.json")
        with open(json_path) as file:
            json_file = json.load(file)
        #self.index +=1;
        image_path = image_path[1:]
        return image_path, json_file
