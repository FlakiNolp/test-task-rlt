from dataclasses import dataclass


@dataclass
class OutputJSON:
    dataset: list[int]
    labels: list[str]

    def __dict__(self):
        return {"dataset": self.dataset, "labels": self.labels}
