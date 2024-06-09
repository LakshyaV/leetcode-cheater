import random
import subprocess
import time

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
            # Simulate typing an invalid character
            characters = "abcdefghijklmnopqrstuvwxyz"
            chosen = random.choice(characters)
            self.run_applescript(f'keystroke "{chosen}"')
            self.simulate_key("backspace")  # Simulate backspace to correct the error
        elif key == "backspace":
            self.run_applescript('key code 51')
        elif key == "\n":
            self.run_applescript('key code 36')
        elif key == "\t":
            self.run_applescript('keystroke tab')
        else:
            self.run_applescript(f'keystroke "{key}"')

    def run_applescript(self, command):
        # Use a single subprocess call to run the AppleScript
        script = f'tell application "System Events" to {command}'
        subprocess.run(['osascript', '-e', script])

    def handle_toggle(self):
        self.enabled = not self.enabled
        print("Toggle ", "on" if self.enabled else "off")

        if self.enabled:
            # Prepare the AppleScript command to type all characters
            script_commands = []
            for c in self.text:
                if random.random() < 0.1:  # Introduce occasional errors
                    script_commands.append(self.create_keystroke_command("error"))
                script_commands.append(self.create_keystroke_command(c))
            # Join all commands into a single AppleScript
            full_script = ' '.join(script_commands)
            subprocess.run(['osascript', '-e', f'tell application "System Events" to {full_script}'])
            self.enabled = False  # Disable the simulation after typing the text

    def create_keystroke_command(self, key):
        if key == "error":
            characters = "abcdefghijklmnopqrstuvwxyz"
            chosen = random.choice(characters)
            return f'keystroke "{chosen}" & key code 51'  # Include backspace in the same command
        elif key == "backspace":
            return 'key code 51'
        elif key == "\n":
            return 'key code 36'
        elif key == "\t":
            return 'keystroke tab'
        else:
            return f'keystroke "{key}"'

    def handle_exit(self):
        exit()

s = '''def twoSum(nums, target):
    hash_map = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[nums[i]] = i'''
solver = AutoSolver(s)
solver.start()

# Add a loop to keep the script running
while True:
    time.sleep(1)
