from sequence import *

class InOut:
    @classmethod
    def parsefasta(cls, file):
        """
        Cette fonction permet de lire un fichier au format FASTA et de récupérer les noms et les séquences qu'il contient.

        :param file: str
            Le nom du fichier FASTA à lire.

        :return data: list
            Une liste d'objet sequences contenant le nom et la séquence.
        """
        data = []  # Initialisation de la liste de dictionnaires des adaptateurs.
        nom = ""  # Initialisation de la variable nom qui contiendra le nom des adaptateurs.
        seq = ""  # Initialisation de la variable seq qui contiendra les séquences d'adaptateurs.
        with open(file, 'r', encoding="utf-8") as FileIn:  # Ouverture du fichier en lecture 'r'.
            allow_list = [">", "A", "T", "C", "G"]
            for ligne in FileIn:

                if ligne[0] in allow_list:
                    if ligne.startswith('>'):  # On prend les lignes qui débutent par '>'.
                        if nom and seq:  # On vérifie que nom et seq ne soient pas vides.
                            a = Sequence(nom, seq)
                            data.append(a)
                        nom = ligne.rstrip()
                        seq = ""  # On réinitialise la variable séquence.
                    else:
                        seq += ligne.rstrip()
                else:
                    raise ValueError("Le fichier donnée n'est pas au format fasta")

            if nom and seq:  # On vérifie que nom et seq ne soient pas vides, et on prend la dernière séquence.
                a = Sequence(nom, seq)
                data.append(a)
        return (data)

    @classmethod
    def parseconfig(cls, file):
        """
        Permet de récuperer les données de score issues d'un fichier de configuration.

        :param file: str nom du fichier score
        :return: Dictionnaire python
        """
        identity = None
        substitution = None
        indel = None

        # Ouverture et lecture du fichier ligne par ligne
        with open(file, 'r', encoding="utf-8") as FileIn:
            for line in FileIn:

                # Extraction du score d'identité
                if line.startswith('identity'):
                    identity = int(line.split(':')[1].rstrip())

                # Extraction du score de substitution
                elif line.startswith('substitution'):
                    substitution = int(line.split(':')[1].rstrip())

                # Extraction du score d'indel
                elif line.startswith('indel'):
                    indel = int(line.split(':')[1].rstrip())

        # Vérification que toutes les valeurs ont été trouvées
        if identity is None or substitution is None or indel is None:
            raise ValueError(
                "Le fichier de configuration doit contenir des lignes pour 'identity', 'substitution', et 'indel'.")

        # Création et renvoi du dictionnaire de configuration
        out = {
            "identity": identity,
            "substitution": substitution,
            "indel": indel
        }
        return out