
from django.db import IntegrityError
from django.db.models import Q

from django.http import HttpResponse
from django.shortcuts import render, redirect

from users.models import User, Admin
from constants import INVALID_KIND

from vocabularies.forms import WordForm, WordForm, ButtonDeleteForm, ButtonDeleteAllForm

from vocabularies.function import TranslateWord
from vocabularies.models import Word, VocabularyBooks


def get_user(request, kind):
    if request.session.get('kind', '') != kind or kind not in {"User", "Admin"}:
        return None

    if len(request.session.get('user', '')) != 10:
        return None

    uid = request.session.get('user')

    if kind == "User":
        number = uid
        User_set = User.objects.filter(client_number=number)
        if User_set.count() == 0:
            return None
        return User_set[0]
    else:
        number = uid
        Admin_set = Admin.objects.filter(admin_number=number)
        if Admin_set.count() == 0:
            return None
        return Admin_set[0]


def home(request, kind):
    if kind == "Admin":
        return Admin_home(request)
    elif kind == "User":
        return User_home(request)
    return HttpResponse(INVALID_KIND)


def Admin_home(request):
    kind = "Admin"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.nick_name,
        "kind": kind
    }

    context = {
        "info": info
    }

    return render(request, 'nav.html', context)


def User_home(request):
    kind = "User"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.nick_name,
        "kind": kind
    }

    chinese_to_english_form = WordForm()
    english_to_chinese_form = WordForm()
    english_meaning = None
    chinese_meaning = None

    if request.method == 'POST':
        if 'chinese_to_english' in request.POST:
            form = WordForm(request.POST)
            if form.is_valid():
                chinese_meaning = form.cleaned_data['word']
                # 翻译并按行拆分
                s = TranslateWord(chinese_meaning)
                lst = s.splitlines()
                # 获取：后的部分
                s = lst[0]
                lst = s.split("：")
                english_meaning = lst[1]
                # 将单词保存进历史记录里面
                word = chinese_meaning
                language = "Chinese"
                translation = english_meaning
                # 放入code=0的历史记录里面
                book, created = VocabularyBooks.objects.get_or_create(user=user, code="0",
                                                                      defaults={"book_name": "历史记录"})
                new_word = Word(word=word, language=language, book=book, translation=translation)
                try:
                    new_word.save()
                except IntegrityError as e:
                    # 如果违反了唯一约束，则记录日志或执行其他操作
                    print("IntegrityError occurred: ", str(e))

                # 保存到word里
                request.session["word"] = word
                request.session["language"] = language
                request.session["translation"] = translation
        elif 'english_to_chinese' in request.POST:
            form = WordForm(request.POST)
            if form.is_valid():
                english_meaning = form.cleaned_data['word']
                # 翻译并按行拆分
                s = TranslateWord(english_meaning)
                lst = s.splitlines()
                # 获取：后的部分
                s = lst[0]
                lst = s.split("：")
                chinese_meaning = lst[1]
                # 将单词保存进历史记录里面
                word = english_meaning
                language = "Chinese"
                translation = chinese_meaning
                # 放入code=0的历史记录里面
                book, created = VocabularyBooks.objects.get_or_create(user=user, code="0",
                                                                      defaults={"book_name": "历史记录"})
                new_word = Word(word=word, translation=translation, language=language, book=book)
                try:
                    new_word.save()
                except IntegrityError as e:
                    # 如果违反了唯一约束，则记录日志或执行其他操作
                    print("IntegrityError occurred: ", str(e))

                # 保存到word里
                request.session["word"] = word
                request.session["language"] = language
                request.session["translation"] = translation

        elif 'word' in request.POST:
            word = request.session.get("word")
            language = request.session.get("language")
            translation = request.session.get("translation")
            # 放入code=1的收藏里面
            book, created = VocabularyBooks.objects.get_or_create(user=user, code="1",
                                                                  defaults={"book_name": "收藏单词"})
            new_word = Word(word=word, translation=translation, language=language, book=book)
            try:
                new_word.save()
            except IntegrityError as e:
                # 如果违反了唯一约束，则记录日志或执行其他操作
                print("IntegrityError occurred: ", str(e))

    context = {
        "info": info,
        'chinese_to_english_form': chinese_to_english_form,
        'english_to_chinese_form': english_to_chinese_form,
        'english_meaning': english_meaning,
        'chinese_meaning': chinese_meaning
    }

    return render(request, 'home.html', context)


def history(request, *args, **kwargs):
    kind = "User"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.nick_name,
        "kind": kind
    }

    delete_form = None
    delete_all_form = None
    if request.method == 'POST':
        if "button_clicked" in request.POST:
            delete_form = ButtonDeleteForm(request.POST)
            if delete_form.is_valid():
                # 删除对应id的单词
                clicked_id = delete_form.cleaned_data['button_clicked']
                clicked_word = Word.objects.get(id=clicked_id)
                clicked_word.delete()
        if "delete_all_history" in request.POST:
            delete_all_form = ButtonDeleteAllForm(request.POST)
            if delete_all_form.is_valid():
                # 删除所有单词
                book = VocabularyBooks.objects.get(user=user, code="0")
                clicked_word = Word.objects.filter(book=book)
                clicked_word.delete()
            else:
                # 返回错误消息
                print(123)
    else:
        delete_form = ButtonDeleteForm()
        delete_all_form = ButtonDeleteAllForm()

    # 查询用户的历史记录
    q = Q(user=user, code="0")
    book = VocabularyBooks.objects.get(q)
    search_list = Word.objects.filter(book=book).order_by('save_day')

    search = {
        "info": info,
        "delete_form": delete_form,
        "delete_all_form": delete_all_form,
        "search_list": search_list
    }
    return render(request, "history.html", search)


def collections(request, *args, **kwargs):
    kind = "User"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.nick_name,
        "kind": kind
    }

    form = None
    if request.method == 'POST':
        if "button_clicked" in request.POST:
            form = ButtonDeleteForm(request.POST)
            if form.is_valid():
                # 删除对应id的单词
                clicked_id = form.cleaned_data['button_clicked']
                clicked_word = Word.objects.get(id=clicked_id)
                clicked_word.delete()
        if "delete_all_history" in request.POST:
            form = ButtonDeleteForm(request.POST)
            if form.is_valid():
                # 删除所有单词
                book = VocabularyBooks.objects.get(user=user, code="1")
                clicked_word = Word.objects.filter(book=book)
                clicked_word.delete()
    else:
        form = ButtonDeleteForm()

    # 查询用户的收藏表
    q = Q(user=user, code="1")
    book = VocabularyBooks.objects.get(q)
    collection_list = Word.objects.filter(book=book).order_by('last_day')

    collection = {
        "info": info,
        "form": form,
        "collection_list": collection_list
    }
    return render(request, "collections.html", collection)


def vocabularyTest(request, *args, **kwargs):
    return HttpResponse("单词测试")
