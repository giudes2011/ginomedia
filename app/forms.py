from django import forms
from .models import post, profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class profilePicForm(forms.ModelForm):
    immagine_profilo = forms.ImageField(label="Immagine Profilo")
    profile_bio = forms.CharField(label='Biografia Profilo', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Inserisci la tua biografia (se vuoi, massimo 500 caratteri).'}))
    # links to different social media platforms, cuz why not???
    facebook = forms.CharField(label='Link Facebook', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il tuo profilo Facebook (se vuoi).'}))
    youtube = forms.CharField(label='Link YouTube', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il tuo profilo YouTube (se vuoi).'}))
    instagram = forms.CharField(label='Link Instagram', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il tuo profilo Instagram (se vuoi).'}))
    tiktok = forms.CharField(label='Link TikTok', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il tuo profilo TikTok (se vuoi).'}))
    class Meta:
        model = profile
        fields = ('immagine_profilo', 'profile_bio', 'facebook', 'youtube', 'instagram', 'tiktok',)
class Postform(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder":"Che cosa vuoi dire? (Massimo 40000 caratteri)", "class":"form-control",}), label="")
    class Meta:
        model = post
        exclude = ("user", "likes",)
class signupform(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci la tua e-mail.'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il tuo nome.'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il tuo cognome.'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        def __init__(self, *args, **kwargs):
            super(signupform, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'User Name'
            self.fields['username'].label = ''
            self.fields['username'].help_text = '<span class="form-text text-muted"><small>Richiesto. 150 caratteri o meno. Solo lettere, cifre e @/./+/-/_.</small></span>'
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>La password non può essere troppo simile alle altre informazioni personali.</li><li>La password deve contenere almeno 8 caratteri.</li><li>La password non può essere una password comunemente utilizzata.</li><li>La password non può essere interamente numerica.</li></ul>'
            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Coferma Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Inserire la stessa password di prima, per verificazione.</small></span>'