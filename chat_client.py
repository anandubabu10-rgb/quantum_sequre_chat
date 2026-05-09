import tkinter as tk
import threading
import time
import requests

from quantum import (
    quantum_key_distribution,
    enable_attack,
    disable_attack
)

from encryption import (
    encrypt_message,
    decrypt_message
)

from qber_visualizer import (
    record_qber,
    show_graph
)

# CHANGE THIS AFTER DEPLOYMENT
# SERVER_URL = "http://127.0.0.1:5000"
SERVER_URL = "https://quantum-sequre-chat.onrender.com"

username = input(
    "Enter your username: "
)

partner = input(
    "Enter receiver username: "
)

current_key = None

attack_active = False


def generate_key():

    global current_key

    key, qber, attack = quantum_key_distribution()

    current_key = key
    record_qber(qber)

    qber_label.config(
        text=f"QBER: {qber}%"
    )

    if attack:

        status_label.config(
            text="⚠ Eavesdropping Detected"
        )

    else:

        status_label.config(
            text="✅ Secure Channel Established"
        )


def simulate_attack():

    global attack_active

    attack_active = True

    enable_attack()

    key, qber, attack = quantum_key_distribution()
    record_qber(qber)

    qber_label.config(
        text=f"QBER: {qber}%"
    )

    status_label.config(
        text="⚠ Eve Attack Simulated"
    )


def stop_attack():

    global attack_active

    attack_active = False

    disable_attack()

    status_label.config(
        text="✅ Secure Channel Restored"
    )


def send_message():

    global current_key

    if current_key is None:

        status_label.config(
            text="Generate key first"
        )

        return

    message = entry.get()

    entry.delete(0, tk.END)

    encrypted = encrypt_message(
        message,
        current_key
    )

    data = {

        "from": username,

        "to": partner,

        "message": encrypted,

        "key": current_key.hex(),

        "attack": attack_active
    }

    requests.post(
        SERVER_URL + "/send",
        json=data
    )

    add_chat(
        f"You: {message}",
        "right"
    )


def receive_messages():

    while True:

        try:

            res = requests.get(
                SERVER_URL +
                f"/receive/{username}"
            ).json()

            if res["message"]:

                if res["attack"]:

                    qber_label.config(
                        text="QBER: 31%"
                    )

                    add_chat(
                        "⚠ Eavesdropping Detected",
                        "left"
                    )

                    status_label.config(
                        text="⚠ Attack Detected"
                    )

                    continue

                key = bytes.fromhex(
                    res["key"]
                )

                decrypted = decrypt_message(
                    res["message"],
                    key
                )

                add_chat(
                    f'{res["from"]}: {decrypted}',
                    "left"
                )

                qber_label.config(
                    text="QBER: 2.1%"
                )

                status_label.config(
                    text="✅ Secure Communication"
                )

        except Exception as e:

            print(e)

        time.sleep(2)


def add_chat(message, side):

    frame = tk.Frame(
        chat_area,
        bg="white"
    )

    color = (
        "#DCF8C6"
        if side == "right"
        else "#FFFFFF"
    )

    bubble = tk.Label(
        frame,
        text=message,
        bg=color,
        relief="solid",
        padx=10,
        pady=5,
        wraplength=250
    )

    bubble.pack(
        anchor="e"
        if side == "right"
        else "w",
        padx=10,
        pady=2
    )

    frame.pack(fill="both")


root = tk.Tk()

root.title(
    f"Quantum Chat - {username}"
)

root.geometry("500x650")

root.configure(bg="white")


chat_area = tk.Frame(
    root,
    bg="white"
)

chat_area.pack(
    fill="both",
    expand=True
)


bottom = tk.Frame(root)

bottom.pack(fill="x")


entry = tk.Entry(bottom)

entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5,
    pady=5
)


send_btn = tk.Button(
    bottom,
    text="Send",
    command=send_message,
    bg="lightgreen"
)

send_btn.pack(side="right")


generate_btn = tk.Button(
    root,
    text="Generate Quantum Key",
    command=generate_key,
    bg="lightblue"
)

generate_btn.pack(pady=5)


attack_btn = tk.Button(
    root,
    text="Simulate Eve Attack",
    command=simulate_attack,
    bg="red"
)

attack_btn.pack(pady=5)


restore_btn = tk.Button(
    root,
    text="Restore Secure Channel",
    command=stop_attack,
    bg="orange"
)

restore_btn.pack(pady=5)


qber_label = tk.Label(
    root,
    text="QBER: -"
)

qber_label.pack()


status_label = tk.Label(
    root,
    text="Waiting"
)

status_label.pack()


threading.Thread(
    target=receive_messages,
    daemon=True
).start()

graph_btn = tk.Button(
    root,
    text="Show QBER Graph",
    command=show_graph,
    bg="violet"
)

graph_btn.pack(pady=5)

root.mainloop()