import requests
import time

class requestHandler:
    def __init__(self):
        self.url = "http://127.0.0.1:5000/shape"
    def getShapes(self):
        while True:
            try:
                response = requests.get(self.url)
                data = response.json()
                if response.status_code == 200 and data['player_shape'] != "":
                    print("Got Shapes")
                    return data['bot_shape'], data['player_shape'], data['current_turn']
                print("Waiting for player to select shape")
            except Exception as e:
                print(f"failed to get shape: {e}")
            time.sleep(2)
            
    def resetShapes(self):
        while True:
            try:
                response = requests.delete(self.url)
            except Exception as e:
                print(f"failed to delete shape: {e}")