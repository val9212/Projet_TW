import threading
import matplotlib
matplotlib.use('Agg')

import random
from Alignement import *
import matplotlib.pyplot as plt
import time
import os

class Significance:
    @classmethod
    def count_acgt(cls, seq):
        """
        compte le nombre de nucleotide a,c,g,t.

        :param seq: str séquence
        :return: a = int, c = int, g = int, t = int
        """
        a = 0
        c = 0
        t = 0
        g = 0

        for letter in seq: # Parcourt chaque nucléotide dans la séquence et incrémente le compteur correspondant
            if letter == 'A':
                a += 1
            elif letter == 'C':
                c += 1
            elif letter == 'T':
                t += 1
            elif letter == 'G':
                g += 1

        return a, t, c, g

    @classmethod
    def significance(cls, seq_1, seq_2, s, n, cost):
        """
        Permet de faire une liste de score et de fréquence à partir d'un nombre n de sequence aleatoire de meme compostion que seq_2.

        :param seq_1: str séquence
        :param seq_2: str séquence
        :param s: score minimal int
        :param n: nombre de copies aleatoire int
        :param cost: objt
        :return: Liste des scores
        """
        i = 0
        score_list = [[],[]]
        a, t, c, g = cls.count_acgt(seq_2)

        n_seq = 'A' * a + 'T' * t + 'C' * c + 'G' * g
        l_n_seq = list(n_seq)

        while i < n: # Génère et évalue 'n' séquences aléatoires
            random.shuffle(l_n_seq)
            random_seq = ''.join(l_n_seq)

            scores = cls.DPmatrix_v2(seq_1, random_seq, cost) # Calcule le score en utilisant la méthode DPmatrix_v2

            score, _, _ = scores

            if score >= s: # Si le score est supérieur ou égal à 's' (le score minimal), met à jour la liste des scores
                if score not in score_list[0]:
                    score_list[0].append(score)
                    score_list[1].append(1)
                else:
                    index = score_list[0].index(score)
                    score_list[1][index] += 1
            i += 1


        sorted_score_list = sorted(zip(*score_list), key=lambda x: x[0]) # Trie la liste des scores et fréquences par score
        sorted_score_list = [list(t) for t in zip(*sorted_score_list)]

        return sorted_score_list

    @classmethod
    def modes(cls, score_liste):
        """
        Permet de trouver et de noter la postions des modes dans la liste des scores.

        :param score_liste: liste de score
        :return: les scores max et leurs positions dans la liste
        """
        maxi = max(score_liste[1]) # Trouve la fréquence la plus élevée dans la liste des fréquences
        position = []

        for i in range(len(score_liste[1])): # Recherche toutes les positions où cette fréquence apparaît
            if score_liste[1][i] == maxi:
                position.append(i)

        return maxi, position

    @classmethod
    def DisplayDist(cls, seq_1, seq_2, s, n, cost, eqs_size):
        """
        Affiche la distribution des scores pour des séquences aléatoires par rapport au score d'une séquence de référence.

        :param seq_1: str séquence
        :param seq_2: str séquence
        :param s: score minimal int
        :param n: nombre de copies aleatoire int
        :param cost: Obj
        :param eqs_size: Le nombre d'égales.
        """
        score_list = cls.significance(seq_1.getSequence(), seq_2.getSequence(), s, n, cost)

        original_score, _, _ = cls.DPmatrix_v2(seq_1.getSequence(), seq_2.getSequence(), cost)

        if s > original_score: # Vérifie que le score minimal est inférieur au score original
            raise ValueError(f"Parametre '-m' trop elevé, le score minimum doit être inférieure a {original_score}")

        original_score_percentage = (score_list[1][score_list[0].index(original_score)] / n) * 100 if original_score in score_list[0] else 0 # Calcule le pourcentage de séquences ayant le score original

        max_frequency, mode_positions = cls.modes(score_list)

        #print(f"\nSignificance of the score ({original_score}): {original_score_percentage:.1f}% ({n} sequences)")
        #print(f"score\t#")

        #i = s
        #while i < score_list[0][0]: # Affiche la distribution des scores, en commençant par le score minimal
            #print(f"\t{i}\t0:")
         #   i += 1

        #for score, freq in zip(score_list[0], score_list[1]): # Affiche chaque score et sa fréquence
          #  marker = "*" if score == original_score else " "
           # eqs = "=" * (freq * eqs_size // max_frequency)
            #print(f"{marker}\t{score}\t{freq}:{eqs}")

        plots_dir = 'media'
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)

        filename = f'media/distribution_{int(time.time())}.svg'
        cls.plot_distribution(seq_1, seq_2, s, n, cost, eqs_size, filename)

        threading.Thread(target=cls.delete_file_after_delay, args=(filename, 600)).start()

        return {
            'score': original_score,
            'pourcentage': original_score_percentage,
            'filename': filename,
        }


    @classmethod
    def DPmatrix_v2(cls, seq1, seq2, cost):
        """
           Calcule le score d'alignement maximal entre deux séquences d'ADN en utilisant la programmation dynamique.

           :param seq1: str séquence
           :param seq2: str séquence
           :param cost: obj
           :return: un tuple contenant le score maximal et leurs positions dans les séquences.
        """
        prev_ligne = [0] * (len(seq2) + 1)


        max_score = 0
        max_i = 0
        max_j = 0

        for i in range(1, len(seq1) + 1):
            ligne = [0]
            prev_data = 0

            for j in range(1, len(seq2) + 1):
                # match/missmatch
                match = prev_data + cost(seq1[i - 1], seq2[j - 1])
                # indel
                delete = ligne[-1] + cost.get_indel()
                # indel
                insert = prev_ligne[j] + cost.get_indel()

                # Le score est le maximum entre 0, match, delete et insert.
                data = max(0, match, delete, insert)

                ligne.append(data)

                if data > max_score: # Mise à jour du score maximal et de sa position
                    max_score = data
                    max_i = i
                    max_j = j

                prev_data = prev_ligne[j]

            prev_ligne = ligne

        return max_score, max_i, max_j



    @classmethod
    def plot_distribution(cls, seq_1, seq_2, s, n, cost, eqs_size, filename):
        """
        Affiche un graphique de la distribution des scores pour des séquences aléatoires par rapport au score d'une séquence de référence.

        :param seq_1: str séquence
        :param seq_2: str séquence
        :param s: score minimal int
        :param n: nombre de copies aleatoire int
        :param cost: Obj
        :param eqs_size: Le nombre d'égales.
        """
        score_list = cls.significance(seq_1.getSequence(), seq_2.getSequence(), s, n, cost)

        original_score, _, _ = cls.DPmatrix_v2(seq_1.getSequence(), seq_2.getSequence(), cost)

        if s > original_score:
            raise ValueError(f"Parametre '-m' trop elevé, le score minimum doit être inférieure a {original_score}")

        original_score_percentage = (score_list[1][score_list[0].index(original_score)] / n) * 100 if original_score in score_list[0] else 0

        max_frequency, mode_positions = cls.modes(score_list)

        # Création du graphique
        plt.figure(figsize=(10, 6))
        plt.bar(score_list[0], score_list[1], color='blue', label='Fréquence des scores')

        # Marquer le score original
        if original_score in score_list[0]:
            original_freq = score_list[1][score_list[0].index(original_score)]
            plt.bar(original_score, original_freq, color='red', label='Score Original')

        plt.title('Distribution des Scores')
        plt.xlabel('Scores')
        plt.ylabel('Fréquence')
        plt.axhline(y=max_frequency, color='gray', linestyle='--', label='Max Fréquence')
        plt.legend()
        plt.grid(axis='y')

        plt.savefig(filename, format='svg')
        plt.close()

    @classmethod
    def delete_file_after_delay(cls, filepath, delay=600):
        """
        Supprime un fichier après un certain délai.
        :param filepath: Chemin vers le fichier à supprimer.
        :param delay: Temps à attendre en secondes avant de supprimer le fichier.
        """
        time.sleep(delay)
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(f"Fichier supprimé : {filepath}")