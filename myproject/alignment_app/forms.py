from operator import truediv

from django import forms
from scipy.ndimage import label


class AlignmentForm(forms.Form):
    sequence_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, label="Séquences au format Fasta", initial="> seq 1\nATCG\n> seq 2\nATTG")
    sequence_file = forms.FileField(required=False, label="Fichier de séquences")

    align = forms.BooleanField(required=False, initial=True, label="Activer Alignement")
    indel = forms.IntegerField(required=True, initial=-2, label="coup d'une insertion / deletion.")
    substitution = forms.IntegerField(required=True, initial=-1, label="coup d'une substitution")
    identity = forms.IntegerField(required=True, initial=+2, label="coup d'une identity")

    significance = forms.BooleanField(required=False, initial=False, label="Activer Significance")
    length = forms.IntegerField(required=False, initial=50, label="Longueur d'alignement")
    random_size = forms.IntegerField(required=False, initial=100, label="Nombre de séquences aléatoires")

    def clean(self):
        cleaned_data = super().clean()
        align = cleaned_data.get("align")
        significance = cleaned_data.get("significance")
        sequence_file = cleaned_data.get("sequence_file")
        sequence_text = cleaned_data.get("sequence_text")

        if not sequence_file and not sequence_text:
            raise forms.ValidationError("Vous devez fournir un fichier ou du texte.")

        #desactiver cette verification pour accéder à la page cachée)
        if not align and not significance:
            raise forms.ValidationError("vous devez selectionner une methode d'analyse")

        return cleaned_data
