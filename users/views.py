from django.shortcuts import render, HttpResponse, reverse, redirect

from constants import INVALID_KIND
from users.forms import UserLoginForm, AdminLoginForm
from users.models import Admin, User


# Create your views here.
def back(request):
    return render(request, "background.html")


def home(request):
    return render(request, "login_home.html")


def login(request, *args, **kwargs):
    if not kwargs or "kind" not in kwargs or kwargs["kind"] not in ["Admin", "User"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]

    if request.method == 'POST':
        if kind == "Admin":
            form = AdminLoginForm(data=request.POST)
        else:
            form = UserLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if len(uid) != 10:
                form.add_error("uid", "账号长度必须为10")
            else:
                if kind == "Admin":
                    number = uid
                    object_set = Admin.objects.filter(admin_number=number)
                else:
                    number = uid
                    object_set = User.objects.filter(client_number=number)
                if object_set.count() == 0:
                    form.add_error("uid", "该账号未注册.")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.password:
                        form.add_error("password", "密码不正确.")
                    else:
                        # request.session['kind'] = kind
                        # request.session['user'] = uid
                        # request.session['id'] = user.id
                        # successful login
                        # to_url = reverse("course", kwargs={'kind': kind})
                        # return redirect(to_url)
                        return HttpResponse(user.nick_name + "登录成功");

            return render(request, 'login_detail.html', {'form': form, 'kind': kind})
    else:
        context = {'kind': kind}
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            if kind == "Admin":
                form = AdminLoginForm({"uid": uid, 'password': '12345678'})
            else:
                form = UserLoginForm({"uid": uid, 'password': '12345678'})
        else:
            if kind == "Admin":
                form = AdminLoginForm()
            else:
                form = UserLoginForm()
        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')

        return render(request, 'login_detail.html', context)


def register(request):
    return HttpResponse("注册页面")
