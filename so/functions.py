import numpy as np
import pandas as pd
import random
from hardware import Process


def turnaround(processes):
    turnaround_sum = 0
    for p in processes:
        turnaround_sum += p.endtime - p.arrival
    return turnaround_sum / len(processes)


def process_generator(tam):
    return [
        Process(
            arrival=random.randint(0, 10),
            duration=random.randint(8, 20),
            pid=i + 1,
            deadline=random.randint(30, 90),
            n_pages=random.randint(4, 10),
        )
        for i in range(tam)
    ]


def processes_df(processes):
    times = []
    for p in processes:
        for value in p.running_time:
            times.append(
                dict(
                    Task=p.__str__(),
                    Start=value,
                    Finish=value + 1,
                    Resource=f"CPU",
                    Id=p.id,
                )
            )
        for value in p.overload_time:
            times.append(
                dict(
                    Task=p.__str__(),
                    Start=value,
                    Finish=value + 1,
                    Resource=f"Overload",
                    Id=p.id,
                )
            )
        for value in p.paging_time:
            times.append(
                dict(
                    Task=p.__str__(),
                    Start=value,
                    Finish=value + 1,
                    Resource=f"Paging",
                    Id=p.id,
                )
            )
        times.append(
            dict(
                Task=p.__str__(),
                Start=p.arrival,
                Finish=p.arrival + 0.3,
                Resource="Arrival",
                Id=p.id,
            )
        )
        times.append(
            dict(
                Task=p.__str__(),
                Start=p.deadline,
                Finish=p.deadline + 0.3,
                Resource="Deadline",
                Id=p.id,
            )
        )
    df = pd.DataFrame(times)
    df["delta"] = df["Finish"] - df["Start"]
    df.sort_values(by="Start", inplace=True)
    return df
