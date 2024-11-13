class Sequence:
    def __init__(self, id, sequence):
        self.__id = id
        self.__sequence = sequence

    def id(self):
        """
        getter
        :return:
        """
        return self.__id[1:]

    def __len__(self):
        """
        Modification de la fonction len pour les objets sequences.
        :return: int
        """
        return len(self.__sequence)

    def getSequence(self):
        """
        getter
        :return:
        """
        return self.__sequence
