import numpy as np
import matplotlib.pyplot as plt


class TColors:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def process_fig(df, processes, name):

    fig, axis = plt.subplots(figsize=(30, len(processes) * 0.8))

    axis.set_ylim(9, 10 * (len(processes) + 1))
    axis.set_xlim(0, df["Finish"].max() + 1)

    axis.set_xlabel("Time", fontsize=16)
    axis.set_ylabel("Processor", fontsize=16)

    axis.set_yticks(np.arange(15, 11 * len(processes), 10))
    axis.set_yticklabels([p for i, p in enumerate(processes)], fontsize=14)

    axis.grid(True)
    for i, value in enumerate(df.values):
        if value[3] == "Arrival":
            axis.broken_barh(
                [(value[1], value[5])],
                (10 * value[4], 9),
                facecolors=("tab:blue"),
                label="Arrival",
            )
        elif value[3] == "CPU":
            axis.broken_barh(
                [(value[1], value[5])],
                (10 * value[4], 9),
                facecolors=("tab:green"),
                label="CPU",
            )
        elif value[3] == "Overload":
            axis.broken_barh(
                [(value[1], value[5])],
                (10 * value[4], 9),
                facecolors=("tab:red"),
                label="Overload",
            )
        elif value[3] == "Deadline":
            axis.broken_barh(
                [(value[1], value[5])],
                (10 * value[4], 9),
                facecolors=("black"),
                label="Deadline",
            )
        elif value[3] == "Paging":
            axis.broken_barh(
                [(value[1], value[5])],
                (10 * value[4], 9),
                facecolors=("orange"),
                label="Paging",
            )
    start, end = axis.get_xlim()
    axis.xaxis.set_ticks(np.arange(start, end, 5))
    axis.set_xticklabels(np.arange(start, end, 5, dtype=int), fontsize=14)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), fontsize=12, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{name}.jpeg", dpi=300)
