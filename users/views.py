# 导入响应
from django.shortcuts import render, HttpResponse, reverse, redirect
# 导入常量
from constants import INVALID_KIND
# 导入格式
from users.forms import UserLoginForm, AdminLoginForm, UserRegisterForm
# 导入模型
from users.models import Admin, User
# 导入视图函数
from django.views.generic import CreateView
from vocabularies.views import all_vocabulary_books


# Create your views here.

def all_users():
    return User.objects.all().values()


def display_all_users():
    print("正在输出所有用户")
    user = all_users()
    for i in range(user.count()):
        print(user[i])


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
                        request.session['kind'] = kind
                        if request.session['kind'] == 'User':
                            request.session['id'] = user.client_number
                        else:
                            request.session['id'] = user.admin_number
                        # successful login
                        # to_url = reverse("course", kwargs={'kind': kind})
                        # return redirect(to_url)
                        return redirect(reverse('main_page'))

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


def logout(request):
    if request.session.get("kind", ""):
        del request.session["kind"]
    if request.session.get("id", ""):
        del request.session["id"]
    return redirect(reverse("login"))


class CreateUserView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "register.html"
    success_url = "login"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)

    def form_valid(self, form):
        # order_by默认升序排列，number前的负号表示降序排列
        user_set = User.objects.filter().order_by("-client_number")
        if user_set.count() > 0:
            last_user = user_set[0]
            new_client_number = str(int(last_user.client_number) + 1)
            for i in range(10 - len(new_client_number)):
                new_client_number = "0" + new_client_number
        else:
            new_client_number = "0000000001"

        # Create, but don't save the new user instance.
        new_user = form.save(commit=False)
        # Modify the student
        new_user.client_number = new_client_number
        # Save the new instance.
        new_user.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_user

        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'User'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (new_client_number, from_url))


def register(request, kind):
    func = None
    if kind == "User":
        func = CreateUserView.as_view()

    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)


def users_home(request):
    books = all_vocabulary_books()
    if request.session['kind'] == "Admin":
        return render(request, 'admin.html', {'books': books})
    else:
        return render(request, 'home.html', {
            'books': books,
            "id": User.objects.filter(client_number=request.session['id']).values('nick_name')[0]['nick_name']})


def delete_user(request):
    client_number = request.POST.get('client_number')
    if User.objects.filter(client_number=client_number).exists():
        User.objects.filter(client_number=client_number).delete()
    return redirect(reverse('main_page'))


def reset_password(request):
    client_number = request.POST.get('client_number')
    if User.objects.filter(client_number=client_number).exists():
        User.objects.filter(client_number=client_number).update(password='000000')
    return redirect(reverse('main_page'))


def change_password(request):
    password = request.POST.get('password')
    User.objects.filter(client_number=request.session['id']).update(password=password)
    return redirect(reverse('login'))


def change_nick_name(request):
    nick_name = request.POST.get('nick_name')
    User.objects.filter(client_number=request.session['id']).update(nick_name=nick_name)
    return redirect(reverse('main_page'))


def display_user(request):
    return render(request, 'display_user.html', {'user': all_users()})
