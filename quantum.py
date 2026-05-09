import hashlib
import random

attack_mode = False

def quantum_key_distribution():

    global attack_mode

    key_string = str(random.random())

    key = hashlib.sha256(
        key_string.encode()
    ).digest()

    # Normal QBER
    if not attack_mode:

        qber = round(
            random.uniform(1, 5),
            2
        )

    # Attack QBER
    else:

        qber = round(
            random.uniform(25, 40),
            2
        )

    attack = qber > 25

    return key, qber, attack


def enable_attack():

    global attack_mode

    attack_mode = True


def disable_attack():

    global attack_mode

    attack_mode = False