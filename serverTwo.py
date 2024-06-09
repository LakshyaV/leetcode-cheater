from flask import Flask, request, jsonify
from flask_cors import CORS
import prompt
import random
import time
import subprocess

app = Flask(__name__)
CORS(app)

class AutoSolver:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.enabled = False

    def start(self):
        print("[x] Starting keyboard")
        self.handle_toggle()  # Start with the keyboard simulation enabled

    def simulate_key(self, key):
        if key == "error":
            # Simulate typing an invalid character (here, "~")
            characters = "abcdefghijklmnopqrstuvwxyz"
            chosen = random.choice(characters)
            subprocess.run(['osascript', '-e', f'tell application "System Events" to keystroke "{chosen}"'])
            time.sleep(0.1)  # Pause for a moment to simulate correcting the error
            self.simulate_key("backspace")  # Simulate backspace to correct the error
        elif key == "backspace":
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 51'])
            time.sleep(0.001)  # Pause between each delete key press
        elif key == "\n":
            # Simulate pressing the Enter key
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 36'])
        elif key == "\t":  # Simulate typing a tab
            subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke tab'])
        else:
            subprocess.run(['osascript', '-e', f'tell application "System Events" to keystroke "{key}"'])

    def handle_toggle(self):
        self.enabled = not self.enabled
        print("Toggle ", "on" if self.enabled else "off")

        if self.enabled:
            for c in self.text:
                if random.random() < 0.065:  # Introduce occasional errors
                    self.simulate_key("error")
                self.simulate_key(c)
                # Introduce fluctuations in typing speed by randomly adjusting the sleep time
                if c == " ":
                    if random.random() < 0.78:
                        time.sleep(random.randint(1, 3))
                else:
                    time.sleep(random.uniform(0.000000000000001, 0.000000000000002))  # Reduce the range for faster typing
            self.enabled = False  # Disable the simulation after typing the random string{}

    def handle_exit(self):
        exit()

def indentation(text):
    indentation_level = 0
    lines = text.split('\n')

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces > indentation_level:
                solver = AutoSolver(line)
                solver.start()
                indentation_level = leading_spaces
            elif leading_spaces < indentation_level:
                self.simulate_key("backspace")
                solver = AutoSolver(line)
                solver.start()
                indentation_level = leading_spaces

@app.route('/solution', methods=['POST'])
def solution():
    list = ["first"]
    string = "Please code the following LeetCode question in Python and only output the code and absolutely nothing else: \n"
    data = request.json
    print(f"Received data: {data}")
    for key, value in data.items():
        string += f"{value} \n"
    result = prompt.get_response(string)
    if list[-1] == result:
        list.append(result)
    else:
        result = result.replace("    ", "")
        result = result.replace("```python", "")
        result = result.replace("```", "")
        print(result)

        # Initialize and start AutoSolver with the result
        solver = AutoSolver(result)
        solver.start()

    return jsonify({'message': 'Success'})

if __name__ == '__main__':
    app.run(debug=True, port=3000)

# Add a loop to keep the script running
while True:
    time.sleep(1)
