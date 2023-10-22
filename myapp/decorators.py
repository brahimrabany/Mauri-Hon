from django.shortcuts import redirect
# from django.http import HttpResponse

def notLoggedUsers(view_func):
    def wrapper_func(request , *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        else:
            return view_func(request , *args,**kwargs)
    return wrapper_func



def forClient(view_func):
        def wrapper_func(request , *args,**kwargs):
            user = request.user
            if user.is_client:
                return view_func(request, *args, **kwargs)

            else:

                return redirect('b')

        return wrapper_func
def forPartenaire(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_partenaire:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('pro')

    return wrapper_func