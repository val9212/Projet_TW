class SequenceAlignment:

    @classmethod
    def DPmatrix(cls, seq_1, seq_2, cost):
        """
        Permet de calculer la matrice d'alignement entre deux sequences avec les scores de l'objet cost.

        :param seq_1: DNA sequence str
        :param seq_2: DNA sequence str
        :param cost: COST obj
        :return: liste
        """
        matrix = [[0] * (len(seq_2) + 1) for _ in range(len(seq_1) + 1)]

        for i in range(1, len(seq_1) + 1):
            for j in range(1, len(seq_2) + 1):
                # match/missmatch
                match = matrix[i - 1][j - 1] + cost(seq_2[j - 1], seq_1[i - 1])
                # indel
                delete = matrix[i - 1][j] + cost.get_indel()
                # indel
                insert = matrix[i][j - 1] + cost.get_indel()

                # Choix du score le plus élevé pour la cellule actuelle de la matrice.
                matrix[i][j] = max(match, delete, insert, 0)
        return matrix

    @classmethod
    def SimilarityScore(cls, matrix):
        """
        Permet de retourner le plus gros score et sa position dans la matrice d'alignement.

        :param matrix: liste
        :return: max score, pos max_i, pos max_j
        """
        max_score = 0
        max_i, max_j = 0, 0

        for i in range(len(matrix)): # Parcours de la matrice pour trouver le score le plus élevé et sa position.
            for j in range(len(matrix[0])):
                # Mise à jour du score maximal si un score plus élevé est trouvé.
                if matrix[i][j] > max_score:
                    max_score = matrix[i][j]
                    max_i, max_j = i, j

        return max_score, max_i, max_j

    @classmethod
    def Align(cls, seq1, seq2, cost, length):
        """
        Print l'alignement des deux sequences selon les scores de l'objet cost.

        :param seq_1: DNA sequence obj
        :param seq_2: DNA sequence obj
        :param cost: COST objt
        """
        seq_1 = seq1.getSequence()
        seq_2 = seq2.getSequence()

        matrix = cls.DPmatrix(seq_1, seq_2, cost)
        max_score, max_i, max_j = cls.SimilarityScore(matrix)
        aligned_seq1, aligned_seq2, match_aligned = "", "", ""

        i, j = max_i, max_j

        count1 = 0
        count2 = 0

        while i > 0 and j > 0 and matrix[i][j] > 0:

            if matrix[i][j] == matrix[i - 1][j - 1] + cost.get_identity() and seq_1[i - 1] == seq_2[j - 1]:
                # Match (Identity)
                aligned_seq1 = seq_1[i - 1] + aligned_seq1
                aligned_seq2 = seq_2[j - 1] + aligned_seq2
                match_aligned = "|" + match_aligned
                i -= 1
                j -= 1
            elif matrix[i][j] == matrix[i - 1][j - 1] + cost.get_substitution():
                # Mismatch (Substitution)
                aligned_seq1 = seq_1[i - 1] + aligned_seq1
                aligned_seq2 = seq_2[j - 1] + aligned_seq2
                match_aligned = " " + match_aligned
                i -= 1
                j -= 1
            elif i > 0 and matrix[i][j] == matrix[i - 1][j] + cost.get_indel():
                # Insertion (Indel) sequence 2
                aligned_seq1 = seq_1[i - 1] + aligned_seq1
                aligned_seq2 = "-" + aligned_seq2
                match_aligned = " " + match_aligned
                count2 += 1
                i -= 1
            elif j > 0 and matrix[i][j] == matrix[i][j - 1] + cost.get_indel():
                # Insertion (Indel) sequence 1
                aligned_seq1 = "-" + aligned_seq1
                aligned_seq2 = seq_2[j - 1] + aligned_seq2
                match_aligned = " " + match_aligned
                count1 += 1
                j -= 1

        start_index_seq1 = max_i - len(aligned_seq1) + 1 + count1
        start_index_seq2 = max_j - len(aligned_seq2) + 1 + count2

        # Appelle la méthode d'affichage formaté
        formatted_alignment = cls.__print_formatted_alignment__(seq1, seq2, aligned_seq1, aligned_seq2, match_aligned, start_index_seq1, start_index_seq2, length)
        return {
            'seq1_id': seq1.id(),
            'seq1_original': seq1.getSequence(),
            'seq2_id': seq2.id(),
            'seq2_original': seq2.getSequence(),
            'alignment': formatted_alignment,
            'score': max_score,
        }

    @classmethod
    def __print_formatted_alignment__(cls,seq1, seq2, aligned_seq1, aligned_seq2, match_aligned, start_index_seq1, start_index_seq2, line_length):
        """
        Imprime l'alignement formaté avec des retours à la ligne tous les 'line_length' caractères.

        :param aligned_seq1: str, séquence alignée 1
        :param aligned_seq2: str, séquence alignée 2
        :param match_aligned: str, ligne de correspondance
        :param start_index_seq1: int, index de départ de la séquence 1
        :param start_index_seq2: int, index de départ de la séquence 2
        :param line_length: int, nombre de caractères par ligne
        """
        formatted_lines = []

        for i in range(0, len(aligned_seq1), line_length):
            end_i = i + line_length
            chunk_seq1 = aligned_seq1[i:end_i]
            chunk_seq2 = aligned_seq2[i:end_i]
            chunk_match = match_aligned[i:end_i]

            # Calcule l'index de fin pour l'affichage, qui peut ne pas être 50 caractères de long pour la dernière ligne
            end_index_seq1 = start_index_seq1 + chunk_seq1.replace('-', '').__len__() - 1  # -1 car l'indice de début est inclus
            end_index_seq2 = start_index_seq2 + chunk_seq2.replace('-', '').__len__() - 1  # -1 car l'indice de début est inclus

            formatted_lines.append(f"{seq1.id()}\t{start_index_seq1}\t{chunk_seq1}\t{end_index_seq1}")
            formatted_lines.append(f"\t\t\t{chunk_match}")
            formatted_lines.append(f"{seq2.id()}\t{start_index_seq2}\t{chunk_seq2}\t{end_index_seq2}\n")

            start_index_seq1 += chunk_seq1.replace('-', '').__len__()
            start_index_seq2 += chunk_seq2.replace('-', '').__len__()


        return formatted_lines


