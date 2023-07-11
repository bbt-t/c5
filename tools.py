class FileReader:
    """
    Read file. Implements an interface Reader.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> str:
        with open(self.file_path) as f:
            data = f.read()
        return data
