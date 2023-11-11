from django.views.generic import TemplateView, ListView
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Appointment
from django.template.loader import get_template
from project import settings
import datetime

class HomeTemplateView(TemplateView):
    template_name = "index.html"

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        email_message = EmailMessage(
            subject=f"{name} vous a envoyé un message via le Dr JONAS",
            body=f"Ce message vient de {name}.\n\nVoici le contenu du message : {message}",
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )

        email_message.send()
        return HttpResponse(f"Email envoyé avec succès. Veuillez vérifier votre email {name} pour consulter votre message.")

class AppTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        message = request.POST.get('message')
        
        appointment = Appointment(
            first_name=nom,
            last_name=prenom, 
            email=email,
            phone_number=contact,
            request=message,
        )
        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Merci de votre confiance, {nom} {prenom}. Votre message a été envoyé avec succès.")
        return HttpResponseRedirect(request.path)

class ManageTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3

    def post(self, request, *args, **kwargs):
        appointment_id = request.POST.get('appointment-id')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.accepted = True
            appointment.accepted_date = datetime.datetime.now()
            appointment.save()

            data = {
                "first_name": appointment.first_name,
                "date": appointment.accepted_date,    
            }

            message = get_template('email.html').render(data)
            email = EmailMessage( 
                "À propos de votre rendez-vous",
                message,
                settings.EMAIL_HOST_USER,
                [appointment.email]
            )
            email.content_subtype = 'html'
            email.send()

            messages.add_message(request, messages.SUCCESS, f"Merci de votre confiance. {appointment.first_name} est pris en considération.")
        except Appointment.DoesNotExist:
            messages.add_message(request, messages.ERROR, "la date est reservé pour un autre patient,Veuillez choisir une autre.")

        return HttpResponseRedirect(request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Gestion RDV - Dr JONAS",
        })
        return context
