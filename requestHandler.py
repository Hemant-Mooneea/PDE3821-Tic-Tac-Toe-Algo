import requests
import time

class requestHandler:
    def __init__(self):
        self.url = "http://127.0.0.1:5000"
    def getShapes(self):
        while True:
            try:
                response = requests.get(f"{self.url}/shape")
                data = response.json()
                if response.status_code == 200 and data['player_shape'] != "":
                    print("Got Shapes")
                    return data['bot_shape'], data['player_shape'], data['current_turn']
                print("Waiting for player to select shape")
            except Exception as e:
                print(f"failed to get shape: {e}")
            time.sleep(2)
            
    def resetShapes(self):
        try:
            response = requests.delete(f"{self.url}/shape")
        except Exception as e:
            print(f"failed to delete shape: {e}")
    
    def getLastPlayed(self):
        while True:
            try:
                response = requests.get(f"{self.url}/last-played")
                data = response.json()
                return data['last_played']
            except Exception as e:
                print(f"failed to get last played: {e}")
            time.sleep(2)