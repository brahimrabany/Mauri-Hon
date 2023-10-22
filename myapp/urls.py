from django.urls import path 
from . import views

urlpatterns = [
    path('afficherNotif/<int:idn>/<int:idp>/', views.afficherNotif, name='afficherNotif'),
    path('notifier/<int:receiver>/<int:idp>', views.notifier, name='notifier'),
    path('notifi/', views.listnotification, name='notifi'),
    path('notifi2/', views.listnotification2, name='notifi2'),
    path('accepter/<int:dmd>/<int:p>/<int:idp>', views.accepter, name='accepter'),
    path('reffuser/<int:dmd>/<int:p>/<int:idp>', views.reffuser, name='reffuser'),

    path('entrepots', views.etr,name='b'),
    path('create/' ,views.create, name="create"),
    path('update/<str:pk>' ,views.update, name="update"),
    path('delete/<str:pk>' ,views.delete, name="delete"),
    path('list_de_Produits/', views.list_de_Produits, name='pr'),
    path('createProduit/', views.createProduit, name="create"),
    path('updateProduit/<str:pk>', views.updateProduit, name="updateProduit"),
    path('deleteProduit/<str:pk>', views.deleteProduit, name="deleteProduit"),
    path('list_de_cat/', views.cat, name='cat'),
    path('createcat/', views.createcat, name="createcat"),
    path('updatecat/<str:pk>', views.updatecat, name="updatecat"),
    path('deletecat/<str:pk>', views.deletecat, name="deletecat"),
    path('entre/<int:pk_test>/', views.entre, name="entre"),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('produit/', views.produit, name='pro'),
    path('show/<int:idp>/<int:ide>/', views.aff, name='show'),
     path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/',views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),


    path('register/',views.registerCli.as_view(), name="register"),
    path('register1/',views.registerPar.as_view(), name="register1"),

]
