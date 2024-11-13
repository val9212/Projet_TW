import sys
import os

# Ajouter le répertoire parent à sys.path pour que Python puisse trouver les modules Alignement, Significance, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from django.shortcuts import render
from .forms import AlignmentForm
from Alignement import SequenceAlignment
from Significance import Significance
from djInOut import InOut
from Cost import Cost

def alignment_view(request):
    if request.method == 'POST':
        form = AlignmentForm(request.POST, request.FILES)  # Récupérer les fichiers depuis request.FILES
        if form.is_valid():
            # Récupération des fichiers
            sequence_file = form.cleaned_data.get('sequence_file')
            sequence_text = form.cleaned_data.get('sequence_text')
            indel = form.cleaned_data.get('indel')
            substitution = form.cleaned_data.get('substitution')
            identity = form.cleaned_data.get('identity')

            score = {
                'indel' : indel,
                'substitution' : substitution,
                'identity' : identity
            }

            align = form.cleaned_data['align']
            significance = form.cleaned_data['significance']
            length = form.cleaned_data['length']
            minimal = form.cleaned_data['minimal_score']
            random_size = form.cleaned_data['random_size']

            # Charger les séquences à partir du contenu du fichier FASTA
            if sequence_file:
                file_content = sequence_file.read().decode('utf-8')
                data = InOut.parse_fasta(file_content)  # Traitez le contenu du fichier
            elif sequence_text:
                data = InOut.parse_fasta(sequence_text)

            # Charger la configuration des coûts à partir du contenu du fichier de score
            cost = Cost(score, 'ACGT')

            # Calculer l'alignement
            if align and significance:
                align_result = SequenceAlignment.Align(data[0], data[1], cost, length)

                context_align = {
                    'seq1_id': align_result['seq1_id'],
                    'seq1_original': align_result['seq1_original'],
                    'seq2_id': align_result['seq2_id'],
                    'seq2_original': align_result['seq2_original'],
                    'alignment': align_result['alignment'],
                    'score': align_result['score'],
                }

                significance_result = Significance.DisplayDist(data[0], data[1], minimal, random_size, cost, length)

                context_significance = {
                    'filename': significance_result['filename'],
                    'score' : significance_result['score'],
                    'pourcentage': significance_result['pourcentage'],
                }

                context_show = {
                    'alignment': "block",
                    'significance': "block",
                }
                return render(request, 'result.html',{'align_result': context_align, 'significance_result': context_significance, 'show': context_show })

            if align:
                align_result = SequenceAlignment.Align(data[0], data[1], cost, length)

                context = {
                    'seq1_id': align_result['seq1_id'],
                    'seq1_original': align_result['seq1_original'],
                    'seq2_id': align_result['seq2_id'],
                    'seq2_original': align_result['seq2_original'],
                    'alignment': align_result['alignment'],
                    'score': align_result['score'],
                }

                context_show = {
                    'alignment': "block",
                    'significance': "none",
                }
                return render(request, 'result.html',
                              {'align_result': context, 'show': context_show })

            # Calculer la significance
            if significance:
                significance_result = Significance.DisplayDist(data[0], data[1], minimal, random_size, cost, length)

                context_significance = {
                    'filename': significance_result['filename'],
                    'score' : significance_result['score'],
                    'pourcentage': significance_result['pourcentage'],
                }

                context_show = {
                    'alignment': "none",
                    'significance': "block",
                }
                return render(request, 'result.html', {'significance_result': context_significance, 'show': context_show})

            if not align and not significance:
                return render(request, 'formulaire_W.html')


    else:
        form = AlignmentForm()

    return render(request, 'alignment_form.html', {'form': form})

