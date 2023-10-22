from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from .decorators import forClient,forPartenaire

from django.contrib.auth.decorators import login_required

from rest_framework.parsers import JSONParser

from  .forms import ClientSignUpForm,PartenaireSignUpForm
from  .serializers import MessageSerializer


#new

def login_request(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method=='POST':
             if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_client:
                    request.session['user'] = user.username
                    login(request,user)
                    return redirect('pro')
                elif user is not None and user.is_partenaire:
                    request.session['user'] = user.username
                    login(request, user)
                    return redirect('b')
                else:
                    msg = "Invalid username or password"
             else:
                    msg = "Erreur l'or de validation de form "
    context ={  'msg':msg, 'form': form }
    return render(request, '../templates/chat/login.html',context)
class registerCli(CreateView):
    model = User_App
    form_class = ClientSignUpForm
    template_name = '../templates/UserPartenaire/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('/')
    # ------------------------------------------------------------------------------------------------------------#
    # ------------------------------------------------------------------------------------------------------------#

class registerPar(CreateView):
    model = User_App
    form_class = PartenaireSignUpForm
    template_name = '../templates/UserPartenaire/register1.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('/')

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('b')

    if request.method == "GET":
        return render(request, 'chat/chat.html',{'users':  User_App.objects.exclude(username=request.user.username),
   })

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('b')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users':    User_App.objects.exclude(username=request.user.username),
                       'receiver': User_App.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})

def logout_view(request):
    logout(request)
    return redirect('login')
@forClient

def produit(request):
    u = Produit.objects.all()

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,).order_by('-timestamp').values()
    nbre = Notification.objects.filter(receiver_id=conn.id,).count()

    context = {'u':u,'nbre': nbre, 'list': list, }

    return render(request, 'UserClient/Produit.html', context)
def aff(request,idp,ide):
       p = Produit.objects.get(id=idp)
       e = Entrepot.objects.get(id=ide)
       u= User_App.objects.get(id=ide)
       con = request.user
       conn = User_App.objects.get(username=con)
       list = Notification.objects.filter(receiver_id=conn.id, ).order_by('-timestamp').values()
       nbre = Notification.objects.filter(receiver_id=conn.id, ).count()
       context = {'u':u, 'p':p,'e':e,'list':list,'nbre':nbre,}
       return render(request, 'UserClient/show.html', context)
@forPartenaire
def afficherNotif(request,idn,idp):
    n = Notification.objects.get(id=idn)
    p = Produit.objects.get(id=idp)
    s = User_App.objects.get(id=idp)
    st = n.status
    con  = request.user
    conn  = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False ).order_by('-timestamp').values()
    nbre = Notification.objects.filter(receiver_id=conn.id,status=False ).count()
    context = {'n': n,'p':p,'s':s, 'st':st,'nbre':nbre,'list':list}
    return render(request, 'UserPartenaire/afficherNotification.html', context)
def notifier(request,receiver,idp):
    r = User_App.objects.get(id=receiver)
    p= Produit.objects.get(id=idp)
    a = request.user
    b = User_App.objects.get(username=a)
    c = request.user.username
    l="Demande du client : "+c
    notif = Notification(status=False,sender_id=b.id, sujet=l, description="",receiver_id=receiver,idProduit_id=idp)
    notif.save()
    return render(request, 'Demande envoyée avec succès')
def accepter(request,dmd,p,idp):
    r = Notification.objects.get(id=dmd)
    r.status = True
    r.save()
    a = request.user
    b = User_App.objects.get(username=a)
    notif = Notification( status = True,sender_id=b.id, sujet="Demande accepte ", description="produit",receiver_id=p ,idProduit_id=idp )
    notif.save()
    return redirect('notifi')
def reffuser(request,dmd,p,idp):
    r = Notification.objects.get(id=dmd)
    r.status = True
    r.save()
    a = request.user
    b = User_App.objects.get(username=a)
    notif = Notification(status=False, sender_id=b.id, sujet="Demande Refuse ", description="produit", receiver_id=p,idProduit_id=idp)
    notif.save()
    return redirect('notifi')
def listnotification(request):
        if not request.user.is_authenticated:
            return redirect('register')
        else:

          con = request.user
          conn = User_App.objects.get(username=con)
          list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()
          list2 = Notification.objects.filter(receiver_id=conn.id ).order_by('-timestamp').values()
          nbre=  Notification.objects.filter(receiver_id=conn.id,status=False).count()

          context = { 'nbre': nbre, 'list': list, 'list2': list2,}
        return render(request, 'UserPartenaire/tousnotif.html', context)


def listnotification2(request):
    if not request.user.is_authenticated:
        return redirect('register')
    else:
        a = request.user
        b = User_App.objects.get(username=a)
        list2 = Notification.objects.filter(receiver_id=b.id).order_by('-timestamp').values()

        nbr2= Notification.objects.filter(receiver_id=b.id,status=False).count()

        context = {'nbr2': nbr2, 'list2': list2, }
    return render(request, 'UserPartenaire/nt.html', context)

def entre(request, pk_test):
    entre = Entrepot.objects.get(id=pk_test)
    e = Entrepot.objects.get(id=pk_test)
    produit = Produit.objects.filter(entrepot_id=entre)
    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notificatio.htmln.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'produit':produit,'e':e, 'list':list, 'nbre':nbre,}
    return render(request, 'UserPartenaire/entrepotDetaille.html', context)

def cat(request):
    # return HttpResponse('about page')
    cat = Domaine.objects.all()
    return render(request, 'UserPartenaire/categorie.html', {'cat': cat})
    # pass


def createcat(request):
    form = DomaineForm()
    if request.method == 'POST':
        form = DomaineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')


    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'form': form,'list': list,'nbre': nbre}
    return render(request, 'UserPartenaire/creeEntrepot.html', context)

def updatecat(request, pk):
    cat = Domaine.objects.get(id=pk)
    form = DomaineForm(instance=cat)
    if request.method == 'POST':
        form = DomaineForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('/')

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'form': form,'list': list,'nbre': nbre}
    return render(request, 'UserPartenaire/creeEntrepot.html', context)


def deletecat(request, pk):
    cat = Domaine.objects.get(id=pk)

    if request.method == 'POST':
        cat.delete()
        return redirect('/')

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'cat': cat,'list': list,'nbre': nbre}

    return render(request, 'UserPartenaire/eleteCategorie.html', context)


def list_de_Produits(request):
    # return HttpResponse('about page')
    userr = request.user
    id_user = User_App.objects.get(username=userr)
    entrepot = Entrepot.objects.filter(user_id=id_user.id)

    p = Produit.objects.filter(entrepot=id_user.id)

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    return render(request, 'UserPartenaire/liste_de_produits.html', {'p': p,'list': list,'nbre': nbre})

def createProduit(request):
    form = ProduitForm()
    if request.method == 'POST':
        form = ProduitForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'form': form,'list': list,'nbre': nbre}

    return render(request, 'UserPartenaire/AjouterProduit.html', context)


def updateProduit(request, pk):
    produit = Produit.objects.get(id=pk)
    form = ProduitForm(instance=produit)

    if request.method == 'POST':

        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('pr')

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'form': form,'list': list,'nbre': nbre}

    return render(request, 'UserPartenaire/AjouterProduit.html', context)


def deleteProduit(request, pk):
    p = Produit.objects.get(id=pk)

    if request.method == 'POST':
        p.delete()
        return redirect('/')
        # print(request.POST)

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'p': p,'list': list,'nbre': nbre}

    return render(request, 'UserPartenaire/deleteProduit.html', context)
@login_required(login_url='login')
def etr(request):
    if not request.user.is_authenticated:
        return redirect('register')
    else:
        userr = request.user
        id_user = User_App.objects.get(username=userr)
        entrepot = Entrepot.objects.filter(user_id=id_user.id)
        list = Notification.objects.filter(receiver_id= id_user.id,status=False).order_by('-timestamp').values()
        nbre = Notification.objects.filter(receiver_id= id_user.id,status=False).count()

    return render(request,'UserPartenaire/entrepo.html',{'entrepot':entrepot,'nbre':nbre,'list':list, })

def create(request):
    form=EntrepotForm()
    if request.method == 'POST':
       form = EntrepotForm(request.POST)
       id = request.POST['nom']
       if form.is_valid():
           form.save()
           userr = request.user
           id_user = User_App.objects.get(username=userr)
           entrepo = Entrepot.objects.get(nom=id)
           entrepo.user_id = id_user.id
           entrepo.save()
           return redirect('/')

    con = request.user
    conn = User_App.objects.get(username=con)
    list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

    nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

    context = {'form':form,'list': list,'nbre': nbre}

    return render(request , 'UserPartenaire/creeEntrepot.html', context )


def update(request,pk):
   entrepot=Entrepot.objects.get(id=pk)
   form=EntrepotForm(instance=entrepot)

   if request.method == 'POST':

      form = EntrepotForm(request.POST,instance=entrepot)
      if form.is_valid():
         form.save()
         return redirect('/')

   con = request.user
   conn = User_App.objects.get(username=con)
   list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

   nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()



   context = {'form':form,'list': list,'nbre': nbre}

   return render(request , 'UserPartenaire/creeEntrepot.html', context )


def delete(request,pk):
   entrepot=Entrepot.objects.get(id=pk)

   if request.method == 'POST':
      entrepot.delete()
      return redirect('/')
       # print(request.POST)

   con = request.user
   conn = User_App.objects.get(username=con)
   list = Notification.objects.filter(receiver_id=conn.id,status=False).order_by('-timestamp').values()

   nbre = Notification.objects.filter(receiver_id=conn.id,status=False).count()

   context = {'entrepot':entrepot,'list': list,'nbre': nbre}

   return render(request , 'UserPartenaire/deletef.html', context )







