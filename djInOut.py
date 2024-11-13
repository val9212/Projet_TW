from sequence import *

class InOut:

    @classmethod
    def parse_fasta(cls, fasta_string):
        """
        Cette fonction permet de lire une chaîne de caractères au format FASTA
        et de récupérer les noms et les séquences qu'elle contient.

        :param fasta_string: str
            La chaîne de caractères représentant les séquences au format FASTA.

        :return data: list
            Une liste d'objets Sequence contenant le nom et la séquence.
        """
        data = []  # Initialisation de la liste d'objets Sequence.
        nom = ""  # Initialisation de la variable nom qui contiendra le nom des séquences.
        seq = ""  # Initialisation de la variable seq qui contiendra les séquences.

        allow_list = [">", "A", "T", "C", "G"]
        for ligne in fasta_string.splitlines():  # Itérer sur chaque ligne
            ligne = ligne.strip()  # Supprimer les espaces inutiles

            if ligne and ligne[0] in allow_list:  # Vérifier que la ligne n'est pas vide
                if ligne.startswith('>'):  # Lignes qui débutent par '>'.
                    if nom and seq:  # Vérifier que nom et seq ne soient pas vides.
                        a = Sequence(nom, seq)
                        data.append(a)
                    nom = ligne.rstrip()  # Enregistrer le nom de la séquence.
                    seq = ""  # Réinitialiser la séquence.
                else:
                    seq += ligne.rstrip()  # Ajouter à la séquence en cours.
            else:
                raise ValueError("Le texte donné n'est pas au format FASTA")

        # Ajouter la dernière séquence si elle existe
        if nom and seq:
            a = Sequence(nom, seq)
            data.append(a)

        return data

    @classmethod
    def parseconfig(cls, file):
        """
        Permet de récupérer les données de score issues d'un fichier de configuration.

        :param file: InMemoryUploadedFile
            L'objet fichier score à lire.

        :return: Dictionnaire python
        """
        identity = None
        substitution = None
        indel = None

        # Lire le contenu du fichier directement
        content = file.read().decode('utf-8')  # Lire et décoder le contenu en UTF-8

        # Itérer sur chaque ligne du contenu
        for line in content.splitlines():
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
