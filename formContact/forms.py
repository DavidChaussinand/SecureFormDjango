from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
import re

class ContactForm(forms.Form):
    MOTIF_CHOICES = [
        ('devis', 'Devis Tattoo'),
        ('reclamation', 'Réclamation'),
        ('autres', 'Autres'),
    ]

    # Validateur pour nom et prénom (lettres uniquement)
    def validate_letters_only(value):
        if not re.match(r'^[a-zA-Z\s-]*$', value):
            raise ValidationError(
                "Ce champ ne peut contenir que des lettres, des espaces et des tirets."
            )
        
    # Validateur personnalisé pour email
    def validate_email_custom(value):
        if "@" not in value:
            raise ValidationError("L'adresse email doit contenir le symbole '@'.")
        if value.endswith("@example.com"):
            raise ValidationError("Les adresses email avec le domaine 'example.com' ne sont pas autorisées.")

    # Validateur pour téléphone (chiffres uniquement)
    def validate_digits_only(value):
        if not value.isdigit():
            raise ValidationError(
                "Ce champ ne peut contenir que des chiffres."
            )

    # Validateur pour alphanumérique (lettres, chiffres, espaces)
    def validate_alphanumeric(value):
        if not re.match(r'^[a-zA-Z0-9\s]*$', value):
            raise ValidationError(
                "Ce champ ne peut contenir que des lettres, des chiffres et des espaces."
            )

    nom = forms.CharField(
        max_length=50,
        label="Nom :",  # Label personnalisé
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_letters_only],
    )
    prenom = forms.CharField(
        max_length=50,
        label="Prénom :",  # Label personnalisé
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_letters_only],
    )
    telephone = forms.CharField(
        max_length=15,
        label="Téléphone :",  # Label personnalisé
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_digits_only],
    )
    email = forms.EmailField(
        label="Email :",  # Label personnalisé
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': "Veuillez entrer une adresse email valide.",
        },
        validators=[validate_email_custom],  # Ajout du validateur personnalisé
    )
    motif = forms.ChoiceField(
        choices=MOTIF_CHOICES,
        label="Motif de la demande :",  # Label personnalisé
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    contenu = forms.CharField(
        label="Contenu :",  # Label personnalisé
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        validators=[validate_alphanumeric],
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'class': 'mt-3'}
        )
    )
