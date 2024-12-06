from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.cache import cache
from django.shortcuts import render
from .forms import ContactForm

def get_client_ip(request):
    """Récupère l'adresse IP du client."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        # Récupérer l'adresse IP du client
        user_ip = get_client_ip(request)

        # Vérifier si l'utilisateur a déjà soumis récemment
        if cache.get(f"form_submit_{user_ip}"):
            # Afficher un message d'erreur si trop de soumissions
            return render(request, 'home.html', {
                'form': form,
                'error': "Vous avez déjà soumis un formulaire récemment. Veuillez patienter avant de réessayer."
            })

        if form.is_valid():
            # Récupération des données du formulaire
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            telephone = form.cleaned_data['telephone']
            email = form.cleaned_data['email']
            motif = form.cleaned_data['motif']
            contenu = form.cleaned_data['contenu']

            # Envoi de l'e-mail
            send_mail(
                subject=f"Nouveau message de {prenom} {nom} - {motif}",
                message=f"Téléphone : {telephone}\nEmail : {email}\n\nMessage :\n{contenu}",
                from_email='dav.chaussinand@gmail.com',  # Expéditeur
                recipient_list=['dav.chaussinand@gmail.com'],  # Destinataire
                fail_silently=False,
            )

            # Ajouter l'adresse IP au cache avec une expiration de 60 secondes
            cache.set(f"form_submit_{user_ip}", True, timeout=60)  # Timeout de 60 secondes

            return render(request, 'home.html', {'form': ContactForm(), 'success': True})

    else:
        form = ContactForm()

    return render(request, 'home.html', {'form': form})


def send_test_email(request):
    send_mail(
        'Test Email',  # Sujet
        'Ceci est un e-mail de test envoyé depuis Django.',  # Message
        'dav.chaussinand@gmail.com',  # Expéditeur
        ['destinataire@example.com'],  # Remplacez par une adresse e-mail réelle
        fail_silently=False,
    )
    return HttpResponse("E-mail envoyé avec succès.")
