class XMLFormatError(Exception):
    """
    Import Exception for issues with XML formatting
    :param Exeception:
    :return:
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg