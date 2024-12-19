from django import forms
from django.utils.safestring import mark_safe

import djInOut
import re


class AlignmentForm(forms.Form):
    sequence_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, label="Séquences au format Fasta", initial="> seq 1\nATCGACCT\n> seq 2\nATTGGTTC")
    sequence_file = forms.FileField(required=False, label="Fichier de séquences")

    align = forms.BooleanField(required=False, initial=True, label="Activer Alignement")
    indel = forms.IntegerField(required=True, initial=-2, label="coup d'une insertion / deletion.")
    substitution = forms.IntegerField(required=True, initial=-1, label="coup d'une substitution")
    identity = forms.IntegerField(required=True, initial=+2, label="coup d'une identity")

    significance = forms.BooleanField(required=False, initial=False, label="Activer Significance")
    length = forms.IntegerField(required=True, initial=50, min_value=10, label="Longueur d'alignement")
    random_size = forms.IntegerField(required=True, initial=100, min_value=1, max_value=500, label="Nombre de séquences aléatoires")

    def clean(self):
        cleaned_data = super().clean()
        align = cleaned_data.get("align")
        significance = cleaned_data.get("significance")
        sequence_file = cleaned_data.get("sequence_file")
        sequence_text = cleaned_data.get("sequence_text")

        if not sequence_file and not sequence_text:
            raise forms.ValidationError(mark_safe("Vous devez fournir un fichier ou du texte."))

        if not align and not significance:
            raise forms.ValidationError(mark_safe("vous devez selectionner une methode d'analyse"))

        if sequence_file:
            sequence_content = sequence_file.read().decode('utf-8')
            sequence_file.seek(0)

            try:
                x = djInOut.InOut.parse_fasta(sequence_content)
                for seq in x:
                    if not re.fullmatch(r'[ACGT]+', seq.getSequence()):
                        raise TypeError
            except:
                raise forms.ValidationError(mark_safe("<strong>Fichier de séquences:</strong> Le fichier fournis n'est pas compatible: caractere autorisé dans les sequences : ACGT"))

        else:

            try:
                x = djInOut.InOut.parse_fasta(sequence_text)
                for seq in x:
                    if not re.fullmatch(r'[ACGT]+', seq.getSequence()):
                        raise TypeError
            except:
                raise forms.ValidationError(mark_safe("<strong>Séquences au format Fasta:</strong> Le texte n'est pas compatible: caractere autorisé dans les sequences : ACGT"))

        return cleaned_data
