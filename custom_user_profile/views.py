from django.shortcuts import render
from forms import UserProfileForm, ExtendedUserCreationForm
from models import UserProfile
from django.views.generic.edit import CreateView,View
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from custom_user_profile import signals
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response

class RegistrationView(View):

    extended_user_creation_form = ExtendedUserCreationForm
    user_profile_form = UserProfileForm
    template_name = 'qb_registration/registration_form.html'

    def get(self, request, *args, **kwargs):
        form1 = self.extended_user_creation_form()
        form2 = self.user_profile_form()
        return render(request, self.template_name, {'form1': form1, 'form2': form2})

    def post(self, request, *args, **kwargs):
        form1 = self.extended_user_creation_form(request.POST)
        form2 = self.user_profile_form(request.POST)

        if all((form1.is_valid(), form2.is_valid())):
            UserProfile.objects.create_inactive_user(form1.cleaned_data,  form2.cleaned_data)
            '''
                self.user = form1.save()
                self.user.is_active = False
                self.user = form1.save()
                self.user_profile = form2.save(commit=False)
                self.user_profile.user = self.user
                self.user_profile.save()
                print id(form1)
                print id(form2)
            '''
            return HttpResponseRedirect(reverse('registration_complete'))
        return render(request, self.template_name, {'form1': form1, 'form2': form2 })


class ProfileView(TemplateView):
    template_name = 'qb_registration/profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


def ActivationView(request, activation_key):

    activated_user = UserProfile.objects.activate_user(activation_key)

    return render_to_response('qb_registration/activate.html', {"account": activated_user })





'''
    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            signals.user_activated.send(sender=self.__class__, user=activated_user, request=request)
            success_url = self.get_success_url(request, activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, request, activation_key):
        activated_user = UserProfile.objects.activate_user(activation_key)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user

    def get_success_url(self, request, user):

        return ('registration_activation_complete', (), {})

'''