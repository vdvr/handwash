class Step:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.durationS = kwargs.get("durationS", 0) + 1
        self.displayPath = kwargs.get("displayPath")