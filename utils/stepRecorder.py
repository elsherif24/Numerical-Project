class Step:
    def __init__(self, stepNumber, operation, description, **data):
        self.stepNumber = stepNumber
        self.operation = operation
        self.description = description
        self.data = data


class StepRecorder:
    def __init__(self, enabled=True):
        self.steps = []
        self.enabled = enabled

    def isEnabled(self):
        return self.enabled

    def record(self, operation, description, **data):
        if self.enabled:
            step = Step(len(self.steps) + 1, operation, description, **data)
            self.steps.append(step)

    def getSteps(self):
        return self.steps


def copyMatrix(matrix):
    return [[elem for elem in row] for row in matrix]


def copyVector(vector):
    return [elem for elem in vector]


def createAugmentedMatrix(a, b):
    n = len(b)
    augmented = []
    for i in range(n):
        row = a[i] + [b[i]]
        augmented.append(row)
    return augmented
