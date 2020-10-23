class Step:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        durationS = kwargs.get("durationS")
        self.durationS = durationS + 1 if durationS != None else None
        self.displayPath = kwargs.get("displayPath")