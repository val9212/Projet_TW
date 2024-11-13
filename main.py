from Alignement import *
from Significance import *
from inout import *
from Cost import *
import argparse

def parse():
    """
    Programme permettant de faire une ligne de commande avec option.
    """
    parser = argparse.ArgumentParser(description="Programme permettant de calculer l'alignement et significance entre deux séquences")
    parser.add_argument('-s', '--fasta', dest="sequences", required=True,
                        help="Le fichier Fasta avec vos deux sequences.")
    parser.add_argument('-c', '--score', dest="score", required=True,
                        help="Le fichier score.")
    parser.add_argument('-l', '--length', dest="length", required=False, default=50, type=int,
                        help="La longueur d'affichage de l'alignement et du nombre de '=' pour significance. (Default : 50) ")
    parser.add_argument('-a', '--alignement', dest="align", required=False, default=True, type= bool,
                        help="Activer le calcul de l'alignement. (Default : True) ")
    parser.add_argument('-p', '--significance', dest="sign", required=False, default=True, type= bool,
                        help="Activer le calcul de significance. (Default : True) ")
    parser.add_argument('-r', '--random', dest="random_size", required=False, default=100, type=int,
                        help="Nombre de sequence aleatoire créée pour le calcule de la significance. (Default : 100)")
    parser.add_argument('-m', '--minimal', dest="minimal_score", required=False, default=0, type=int,
                        help="Le score minimal pour l'affichage de significance. (Default : 0)")
    return parser.parse_args()


#Programe Principale :
if __name__ == "__main__":
    OPTIONS = parse()
    fasta = OPTIONS.sequences
    score = OPTIONS.score
    align = OPTIONS.align
    significance = OPTIONS.sign
    length = OPTIONS.length
    minimal = OPTIONS.minimal_score
    random_size = OPTIONS.random_size

    data = InOut.parsefasta(fasta)
    cost = Cost(InOut.parseconfig(score), 'ACGT')

    if align:
        SequenceAlignment.Align(data[0], data[1], cost, length)

    if significance:
        Significance.DisplayDist(data[0], data[1], minimal, random_size, cost, length)





