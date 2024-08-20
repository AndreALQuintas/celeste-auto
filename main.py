import _io
import os.path
import time
import threading
from Macro import Macro
from Translate_Keys import Translate_Keys
from pynput.keyboard import Listener, Controller

current_macros: list[Macro] = []
all_macros: list[Macro] = []
macro_file: _io.TextIOWrapper
listener: Listener
play_thread: threading.Thread
first_time: float

run = True

"""
IDEIAS

em vez de esperar pelo proximo timer, fazer um sleep desde o start do num1 até ao start do num 2 por exemplo etc...
"""

def on_press(key):
    try:
        if key.char == 'z':
            print("STOP!")
            listener.stop()
            return
    except:
        pass
    for macro in current_macros:
        if macro.action == key:
            return
    new_macro = Macro(start=time.time() - first_time, action=key)
    current_macros.append(new_macro)
    all_macros.append(new_macro)
    print('{0} pressed'.format(key))


def on_release(key):
    print('{0} release'.format(key))
    for macro in current_macros:
        if macro.action == key:
            current_macros.remove(macro)
            macro.set_end(time.time() - first_time)

def send_to_file(macro: Macro):
    macro_file.write(str(macro))


def sort_macro_list(macro_list: list[Macro]):
    print("Sorting macro...")
    pass
    print("Sorting macro... Success")

def record_menu():
    macro_name = input("Input macro name: ")
    macro_name += ".macr"
    if os.path.exists(f"./macros/{macro_name}"):
        print("File already exists!")
    global macro_file, listener, first_time
    macro_file = open(f"./macros/{macro_name}", "w")
    print(f"Starting recording for '{macro_name}' in 5 seconds...")
    time.sleep(5)
    print("Started recording...")

    first_time = time.time()

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

    print("Sending to file...")
    for macro in all_macros:
        send_to_file(macro)
    print("Success")
    macro_file.close()


def hold_key(action, duration: float, line: int):
    keyboard: Controller = Controller()
    try:
        keyboard.press(action)
        print(f"{action}, line - {line}")
        time.sleep(duration)
        keyboard.release(action)
    except:
        print(f"Error - Unknown action - '{action}')'")
        time.sleep(duration)


def main_play_loop(macros: tuple):
    run = True
    first_time = time.time()
    macros = list(macros)
    line = 0
    while run:

        line += 1
        current_macro: Macro = macros[0]
        next_macro = None
        if len(macros) > 1:
            next_macro: Macro = macros[1]

        duration = current_macro.end - current_macro.start
        action = current_macro.action
        thread = threading.Thread(target=hold_key, args=(action, duration, line))
        thread.start()
        macros.pop(0)

        if next_macro is not None:
            time.sleep(next_macro.start - current_macro.start)

        if len(macros) == 0:
            print("Finished Macro!")
            run = False
            return


def play_macro(filename: str):
    global macro_file
    macro_file = open(f"./macros/{filename}", "r")
    macros: list[Macro] = []
    for macro_line in macro_file.readlines():
        macro_line_split = macro_line.split(" - ")

        action: str = macro_line_split[2][:-1]
        if action.__contains__("'"):
            action = action[1:-1]
        elif action.__contains__("Key"):
            action = Translate_Keys[action[4:]]

        new_macro = Macro(start=float(macro_line_split[0]), end=float(macro_line_split[1]), action=action)

        macros.append(new_macro)

    macro_file.close()
    global play_thread
    play_thread = threading.Thread(target=main_play_loop, args=(macros,))
    play_thread.start()


def play_menu():
    macro_files = os.listdir("./macros")
    if len(macro_files) == 0:
        print("No macros recorded...\n\n")
        main()
    else:
        print("\nAll macros:")
        for i, macro in enumerate(macro_files):
            print(f"\t{i+1} - {macro}")
        print("\n")
        opc = int(input("Select a macro: "))
        macro = macro_files[opc-1]
        print(f"Starting '{macro}' in 5 seconds...")
        time.sleep(5)
        print(f"Started playing...")
        play_macro(macro)

def main():
    opc = input("1 - Record macro\n2 - Play macro\nAns: ")
    if opc == '1':
        record_menu()
    elif opc == '2':
        play_menu()

main()