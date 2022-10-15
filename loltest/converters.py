class EUNEorEUWConverter:
    regex = 'eune|euw'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return '%s' % value