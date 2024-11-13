class Cost:
    def __init__(self, score, allowed_letters):
        self.__indel = score['indel']
        self.__substitution = score['substitution']
        self.__identity = score['identity']
        self.__alphabet = allowed_letters

    def get_indel(self):
        """ Renvoie le score pour un indel. """
        return self.__indel

    def get_substitution(self):
        """ Renvoie le score pour une substitution. """
        return self.__substitution

    def get_identity(self):
        """ Renvoie le score pour une identité. """
        return self.__identity
    def __compare(self, letter1 , letter2):
        """
        Compare la lettre 1 et 2 et retourne le score d'un match si ce sont les meme et le score d'une substitution si elles ne sont pas les memes.
        :param letter1: str
        :param letter2: str
        :return: int
        """
        if letter1 == letter2:  # Si les lettres sont identiques, le score d'identité est renvoyé.
            return self.__identity
        else: # Si les lettres diffèrent, le score de substitution est renvoyé.
            return self.__substitution

    def __call__(self, letter1, letter2):
        """
        Permet d'appeler la methode compare d'un objet cost.
        :param letter1: str
        :param letter2: str
        :return: int
        """
        if (letter1 == "" or letter2 == "") or (letter1 in self.__alphabet and letter2 in self.__alphabet):
            if letter1 == "" or letter2 == "": # Retourne le score d'indel si l'une des lettres est vide, indiquant une insertion ou suppression.
                return self.__indel
            else: # Si les deux lettres sont présentes, compare les lettres pour renvoyer le score correspondant.
                return self.__compare(letter1, letter2)
        else: # Si une lettre n'est pas dans l'alphabet autorisé, une erreur est levée.
            raise ValueError("Operation invalide pour ces caractères")

