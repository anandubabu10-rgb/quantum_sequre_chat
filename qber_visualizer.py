import matplotlib.pyplot as plt

qber_values = []

def record_qber(qber):

    qber_values.append(qber)

def show_graph():

    if len(qber_values) == 0:
        return

    plt.figure(figsize=(8, 5))

    plt.plot(
        range(1, len(qber_values) + 1),
        qber_values,
        marker='o'
    )

    plt.axhline(
        y=25,
        color='r',
        linestyle='--',
        label='Attack Threshold'
    )

    plt.xlabel("Communication Session")

    plt.ylabel("QBER (%)")

    plt.title("QBER Monitoring Graph")

    plt.legend()

    plt.grid(True)

    plt.show()