import requests
import time
class requestHandler:
    def __init__(self):
        # URL of the server which is localhost in this case
        self.url = "http://127.0.0.1:5000"
    # Method which sends a GET request to the server to get the shapes selected by the player
    def getShapes(self):
        while True:
            try:
                # Send a GET request to the server
                response = requests.get(f"{self.url}/shape")
                # Get the response in JSON format
                data = response.json()
                # Check if the response is successful and the player has selected a shape
                if response.status_code == 200 and data['player_shape'] != "":
                    print("Got Shapes")
                    return data['bot_shape'], data['player_shape'], data['current_turn']
                # If the player has not selected a shape, wait for 2 seconds and try again
                print("Waiting for player to select shape")
            except Exception as e:
                print(f"failed to get shape: {e}")
            time.sleep(2)
    # Method which sends a DELETE request to the server to reset the shapes when the game ends
    def resetShapes(self):
        try:
            # Send a DELETE request to the server
            response = requests.delete(f"{self.url}/shape")
        except Exception as e:
            print(f"failed to delete shape: {e}")
    # Method which sends a GET request to the server to get the last played shape
    def getLastPlayed(self):
        while True:
            try:
                # Send a GET request to the server
                response = requests.get(f"{self.url}/last-played")
                # Get the response in JSON format
                data = response.json()
                return data['last_played']
            except Exception as e:
                print(f"failed to get last played: {e}")
            time.sleep(2)