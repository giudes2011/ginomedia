from django.shortcuts import render, redirect, get_object_or_404
from .models import profile, post
from django.contrib import messages
from .forms import Postform, signupform, profilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
def home(request):
    if request.user.is_authenticated:
        form = Postform(request.POST or None)  
        if request.method == "POST":
            if form.is_valid():
                poste = form.save(commit=False)
                poste.user = request.user
                poste.save()
                messages.success(request, "Post creato con successo.")
                return redirect('home')
        posts = post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts": posts, "form": form})
    else:
        posts = post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts": posts})
def profilelist(request):
    if request.user.is_authenticated:
        profiles = profile.objects.exclude(user=request.user)
        return render(request, 'profili.html', {'profiles':profiles})
    else:
        messages.success(request, ("Per entrare in questa pagina, bisogna accedere ad un account."))
        return redirect('home')
def userprofile(request, pk):
    if request.user.is_authenticated:
        profilo = profile.objects.get(user_id=pk)
        posts = post.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == 'POST':
            currentuserprofile = request.user.profile
            action = request.POST.get('follow')
            if action == 'unfollow':
                currentuserprofile.follows.remove(profilo)
            elif action == 'follow':
                currentuserprofile.follows.add(profilo)
            currentuserprofile.save()
        return render(request, "profile.html", {"profile": profilo, "posts": posts})
    else:
        messages.success(request, ("Per entrare in questa pagina, bisogna accedere ad un account."))
        return redirect('home')
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Accesso/Login effettuato con successo."))
            return redirect('home')
        else:
            messages.success(request, ("Un errore è successo durante l'accesso, per favore riprovate."))
            return redirect('login')
    else:
        return render(request, "login.html", {})
def logoutuser(request):
    logout(request)
    messages.success(request, ("Disconnessione effettuata con successo."))
    return redirect('home')
def registeruser(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            print("User saved")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            messages.success(request, ("Registrazione effettuata con successo."))
            return redirect('login')
    else:
        form = signupform()
    return render(request, "register.html", {'form': form})
def updateuser(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = profile.objects.get(user__id=request.user.id)
		user_form = signupform(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = profilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			login(request, current_user)
			messages.success(request, ("Profilo aggiornato con successo."))
			return redirect('home')
		return render(request, "updateuserpage.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("Per entrare in questa pagina, bisogna accedere ad un account."))
		return redirect('home')
def postlike(request, pk):
    if request.user.is_authenticated:
        likepost = get_object_or_404(post, id=pk)
        if likepost.likes.filter(id=request.user.id):
            likepost.likes.remove(request.user)
        else:
            likepost.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("Per entrare in questa pagina, bisogna accedere ad un account."))
        return redirect('home')
def postshare(request, pk):
    sharepost = get_object_or_404(post, id=pk)
    if sharepost:
        return render(request, "sharepost.html", {'post': sharepost})
    else:
        messages.success(request, ("Questo post non esiste o è stato eliminato."))
        return redirect('home')
def postdelete(request, pk):
    if request.user.is_authenticated:
        deletepost = get_object_or_404(post, id=pk)
        if request.user.username == deletepost.user.username:
            deletepost.delete()
            messages.success(request, ("Post eliminato con successo."))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("Impossibile eliminare un post che non è tuo."))
            return redirect('home')
    else:
        messages.success(request, ("Per entrare in questa pagina, bisogna accedere ad un account."))
        return redirect('home')
def postedit(request, pk):
    if request.user.is_authenticated:
        Post = get_object_or_404(post, id=pk)
        if request.user.username == Post.user.username:
            Form = Postform(request.POST or None, instance=Post)
            if request.method == "POST":
                if Form.is_valid():
                    ps = Form.save(commit=False)
                    ps.user = request.user
                    ps.save()
                    messages.success(request, ("Post modificato con successo."))
                    return redirect('home')
            else:
                return render(request, "postedit.html", {'form': Form, 'post': Post})
        else:
            messages.success(request, ("Impossibile modificare un post che non è tuo."))
            return redirect('home')
    else:
        messages.success(request, ("Per entrare in questa pagina, bisogna accedere ad un account."))
        return redirect('home')
def searchpost(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        found = post.objects.filter(body__contains=search)
        return render(request, 'cercapost.html', {'search':search, 'found':found})
    else:
        return render(request, 'cercapost.html', {})
def searchuser(request):
    if request.method == 'POST':
            search = request.POST.get('search')
            found = User.objects.filter(username__contains=search)
            return render(request, 'cercautente.html', {'search':search, 'found':found})
    else:
        return render(request, 'cercautente.html', {})