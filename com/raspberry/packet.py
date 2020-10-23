class Packet:
    def __init__(self, cmd, args):
        self.cmd = cmd
        self.args = args

    def serialize(self):
        return f'\x02{self.cmd}\x00{self.args}\x03'

    def pp(self):
        print(f'[Command: {self.cmd} , Arguments: {self.args}]')