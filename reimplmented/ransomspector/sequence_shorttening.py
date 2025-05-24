class FSequence:
    __slots__ = ("seq")

    def __init__(self):
        self.seq: list = []

    def push(self, x):
        if self.seq and self.seq[-1] == x:
            return False

        if len(self.seq) >= 3:
            last2 = (self.seq[-1], x)
            prev2 = tuple(self.seq[-3:-1])
            if last2 == prev2:
                del self.seq[-1]
                return False

        if len(self.seq) >= 5:
            last3 = (self.seq[-2], self.seq[-1], x)
            prev3 = tuple(self.seq[-5:-2])
            if last3 == prev3:
                del self.seq[-1]
                del self.seq[-2]
                return False

        self.seq.append(x)
        return True

    def __iter__(self):
        return iter(self.seq)

    def __repr__(self):
        return f"{self.seq}"