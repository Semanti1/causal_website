import os
import json
import random

class FurnitureLoader():
    def __init__(self, furniture=None):
        self.index = 1;
        self.furniture_list = ["lamp", "flashlight", "kerosene_lamp", "candle"]
        self.electric_based_list = ["lamp", "flashlight", "wall_lamp"]
        self.heat_based_list = ["kerosene_lamp", "candle", "oil_lamp"]
        if furniture is None:
            self.furniture="table"
        else:
            self.furniture = furniture
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", self.furniture, '{0:02}'.format(self.index))
        print(self.furniture_path)
    def set_furniture(self, furniture, index=1):
        self.furniture = furniture
        self.index = index;
        self.furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", self.furniture, '{0:02}'.format(self.index))
    def load(self):
        image_path = os.path.join(self.furniture_path, "image.png");
        json_path = os.path.join(self.furniture_path, "description.json")
        with open(json_path) as file:
            json_file = json.load(file)
        #self.index +=1;
        image_path = os.path.join("/static/furnitures/", self.furniture, '{0:02}'.format(self.index), "image.png");
        return [image_path], [json_file]

    def load_all(self):
        image_path_list = []
        json_file_list = []
        self.furniture_path = os.path.join(self.APP_ROOT, "static/causal_graph/");
        for furniture in self.furniture_list:
            furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", furniture, "01")
            image_path = os.path.join("/static/furnitures/", furniture, "01", "image.png")
            json_path = os.path.join(furniture_path, "description.json")
            with open(json_path) as file:
                json_file = json.load(file)
            image_path_list.append(image_path)
            json_file_list.append(json_file)
        return image_path_list, json_file_list

    def load_all2(self):
        rand_indx_1 = random.randint(0, len(self.heat_based_list)-1)
        display_object_1 = self.heat_based_list[rand_indx_1]
        index_list = list(range(0, len(self.heat_based_list)))
        del index_list[rand_indx_1]
        plan_rand_indx_1 = random.choice(index_list)
        plan_object_1 = self.heat_based_list[plan_rand_indx_1]

        rand_index_2 =random.randint(0, len(self.electric_based_list)-1)
        display_object_2 = self.electric_based_list[rand_index_2]
        index_list = list(range(0, len(self.electric_based_list)))
        del index_list[rand_index_2]
        plan_rand_indx_2 = random.choice(index_list)
        plan_object_2 = self.electric_based_list[plan_rand_indx_2]
        image_path_list = []
        json_file_list = []
        plan_image_path_list = []
        plan_json_file_list = []
        plan_object_list = list([plan_object_1, plan_object_2])
        for furniture in list([display_object_1 , display_object_2]):
            furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", furniture, "01")
            image_path = os.path.join("/static/furnitures/", furniture, "01", "image.png")
            json_path = os.path.join(furniture_path, "description.json")
            with open(json_path) as file:
                json_file = json.load(file)
            image_path_list.append(image_path)
            json_file_list.append(json_file)

        for furniture in list([plan_object_1, plan_object_2]):
            furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", furniture, "01")
            image_path = os.path.join("/static/furnitures/", furniture, "01", "image.png")
            json_path = os.path.join(furniture_path, "description.json")
            with open(json_path) as file:
                json_file = json.load(file)
            plan_image_path_list.append(image_path)
            plan_json_file_list.append(json_file)

        return image_path_list, json_file_list, plan_image_path_list, plan_json_file_list, plan_object_list


    def load_category(self, category_list):
        image_path_list = []
        json_file_list = []
        self.furniture_path = os.path.join(self.APP_ROOT, "static/causal_graph/");
        for furniture in category_list:
            furniture_path = os.path.join(self.APP_ROOT, "static/furnitures/", furniture, "01")
            image_path = os.path.join("/static/furnitures/", furniture, "01", "image.png")
            json_path = os.path.join(furniture_path, "description.json")
            with open(json_path) as file:
                json_file = json.load(file)
            image_path_list.append(image_path)
            json_file_list.append(json_file)
        return image_path_list, json_file_list


