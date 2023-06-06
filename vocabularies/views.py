import json
import random
import requests

from django.shortcuts import render, redirect
from django.urls import reverse
from vocabularies.models import *
from users.models import *


# Create your views here.

def all_vocabularies():
    return Vocabulary.objects.values()


def display_all_vocabularies():
    print('正在输出所有单词')
    vocabulary = all_vocabularies()
    for i in range(vocabulary.count()):
        print(vocabulary[i])


def all_vocabulary_books():
    return VocabularyBook.objects.values()


def display_all_vocabulary_books():
    print('正在输出所有单词书')
    vocabulary_book = all_vocabulary_books()
    for i in range(vocabulary_book.count()):
        print(vocabulary_book[i])


def vocabularies_in_book(book_name):
    return Vocabulary.objects.filter(
        type__contains=VocabularyBook.objects.filter(book_name=book_name).values()[0]['code']).values()


def display_vocabularies_in_book(book_name):
    print('正在输出《' + book_name + '》中的所有单词')
    vocabulary = vocabularies_in_book(book_name)
    for i in range(vocabulary.count()):
        print(vocabulary[i])


def personal_vocabularies(client_number):
    return PersonalVocabularyBook.objects.filter(client_number=client_number).values()


def display_personal_vocabularies(client_number):
    print('正在输出client_number为:' + str(client_number) + ' 用户的单词本')
    personal_vocabulary = personal_vocabularies(client_number)
    for i in range(personal_vocabulary.count()):
        print(personal_vocabulary[i])


def staring_vocabularies(client_number):
    return PersonalVocabularyBook.objects.filter(client_number=client_number).filter(is_staring=True).values()


def display_staring_vocabularies(client_number):
    print('正在输出client_number为:' + str(client_number) + ' 用户的收藏单词')
    staring_vocabulary = staring_vocabularies(client_number)
    for i in range(staring_vocabulary.count()):
        print(staring_vocabulary[i])


def add_vocabulary(vocabulary, translation, sentence, sentence_translation):
    vocabulary = Vocabulary(
        vocabulary=vocabulary,
        chinese=translation,
        sentence=sentence,
        chinese_sentence=sentence_translation,
        type='')
    vocabulary.save()


def add_vocabulary_book(book_name, code):
    if VocabularyBook.objects.filter(book_name=book_name).exists() or VocabularyBook.objects.filter(code=code).exists():
        print("当前书名或代号已存在\n")
    else:
        vocabulary_book = VocabularyBook(
            book_name=book_name,
            code=code
        )
        vocabulary_book.save()


def distribute_vocabulary(vocabulary, vocabulary_book):
    if Vocabulary.objects.filter(vocabulary=vocabulary).exists() and VocabularyBook.objects.filter(
            book_name=vocabulary_book).exists():
        Vocabulary.objects.filter(vocabulary=vocabulary).update(
            type=
            Vocabulary.objects.filter(
                vocabulary=vocabulary).values()[0]['type'] +
            VocabularyBook.objects.filter(
                book_name=vocabulary_book).values()[0]['code'])
    else:
        print("目标单词或单词书不存在\n")


def handle_vocabulary(client_number, vocabulary, is_remembered):
    if PersonalVocabularyBook.objects.filter(client_number=client_number).filter(vocabulary=vocabulary).exists():

        p1 = PersonalVocabularyBook.objects.filter(client_number=client_number).filter(vocabulary=vocabulary)
        p2 = p1.first()
        p2.is_remembered = is_remembered
        p2.save()

    else:
        p = PersonalVocabularyBook(
            client_number=client_number,
            vocabulary=vocabulary,
            is_remembered=is_remembered
        )
        p.save()


def star_vocabulary(client_number, vocabulary, is_star):
    if PersonalVocabularyBook.objects.filter(client_number=client_number).filter(vocabulary=vocabulary).exists():

        PersonalVocabularyBook.objects.filter(client_number=client_number).filter(vocabulary=vocabulary).update(
            is_staring=is_star)

    else:
        p = PersonalVocabularyBook(
            client_number=client_number,
            vocabulary=vocabulary,
            is_remembered=False,
            is_staring=is_star
        )
        p.save()


def today_new_vocabularies(client_number, book_name, today_new_count):
    client = personal_vocabularies(client_number)
    client_list = []
    for i in client:
        client_list.append(i['vocabulary'])

    book = vocabularies_in_book(book_name)
    book_list = []
    for i in book:
        book_list.append(i['vocabulary'])

    v_list = list(set(book_list) - set(client_list))

    if len(v_list) <= today_new_count:
        return v_list

    else:
        return random.sample(v_list, today_new_count)


def today_review_vocabularies(client_number, book_name, today_review_count):
    client1 = PersonalVocabularyBook.objects.filter(client_number=client_number).filter(is_remembered=False).values()
    client_list = []
    for i in client1:
        client_list.append(i['vocabulary'])

    client2 = PersonalVocabularyBook.objects.filter(client_number=client_number).filter(is_remembered=True).values()
    client_additional_list = []
    for i in client2:
        client_additional_list.append(i['vocabulary'])

    book = vocabularies_in_book(book_name)
    book_list = []
    for i in book:
        book_list.append(i['vocabulary'])

    v_list1 = list(set(book_list) & set(client_list))
    v_list2 = list(set(book_list) & set(client_additional_list))

    if len(v_list1) < today_review_count:
        if len(v_list1) + len(v_list2) <= today_review_count:
            v_list = v_list1 + v_list2
        else:
            v_list = v_list1 + random.sample(v_list2, today_review_count - len(v_list1))

    else:
        v_list = random.sample(v_list1, today_review_count)

    random.shuffle(v_list)
    return v_list


def remember_line(client_number, day_count):
    client = personal_vocabularies(client_number)

    client_total = [0] * day_count
    client_remembered = [0] * day_count

    for i in client:
        if (i['last_met_date'] - i['first_met_date']).days < day_count:
            client_total[(i['last_met_date'] - i['first_met_date']).days] += 1
            if i['is_remembered']:
                client_remembered[(i['last_met_date'] - i['first_met_date']).days] += 1

    r_line = [0.0] * day_count
    for i in range(day_count):
        if client_total[i] != 0:
            r_line[i] = client_remembered[i] / client_total[i]
        else:
            r_line[i] = 0.0

    r_line[0] = 1.0

    return r_line


def recite_home(request):
    book = VocabularyBook.objects.filter(code=request.POST.get('book')).values('book_name')[0]['book_name']
    request.session['book_name'] = book
    review = request.POST.get('review')
    new = request.POST.get('new')
    r_list = today_review_vocabularies(int(request.session['id']), str(book), int(review))
    n_list = today_new_vocabularies(int(request.session['id']), str(book), int(new))
    t_list = r_list + n_list
    random.shuffle(t_list)
    json_str = json.dumps(t_list)
    request.session['recite_list'] = json_str
    dummy = ['CheChang']
    emt = json.dumps(dummy)
    request.session['not_remember'] = emt
    return redirect(reverse('begin_recite'))


def recite(request):
    return redirect(reverse('vocabulary'))


def recite_vocabulary(request):
    t_list = json.loads(request.session['recite_list'])
    if t_list:
        v = t_list.pop()
        json_str = json.dumps(t_list)
        request.session['recite_list'] = json_str
        request.session['vocabulary'] = v
        return render(request, 'vocabulary.html',
                      {'vocabulary': v})
    else:
        return redirect(reverse('finish_recite'))


def recite_detail(request, is_remembered):
    if is_remembered == 'True':
        is_remembered = True
    else:
        is_remembered = False
    v = request.session['vocabulary']
    n = json.loads(request.session['not_remember'])
    if v in n:
        if not is_remembered:
            l = json.loads(request.session['recite_list'])
            l.append(v)
            random.shuffle(l)
            request.session['recite_list'] = json.dumps(l)
    else:
        handle_vocabulary(int(request.session['id']), v, is_remembered)
        if not is_remembered:
            n.append(v)
            request.session['not_remember'] = json.dumps(n)
            l = json.loads(request.session['recite_list'])
            l.append(v)
            random.shuffle(l)
            request.session['recite_list'] = json.dumps(l)

    return render(request, 'vocabulary_detail.html',
                  {'vocabulary': v,
                   'Chinese': translate(v),
                   'sentence': Vocabulary.objects.filter(vocabulary=v).values('sentence')[0]['sentence'],
                   'Chinese_sentence': Vocabulary.objects.filter(vocabulary=v).values('chinese_sentence')[0][
                       'chinese_sentence'],
                   'is_staring': PersonalVocabularyBook.objects.filter(
                       client_number=int(request.session['id'])).filter(vocabulary=v).values(
                       'is_staring')[0]['is_staring']
                   })


def finish_recite(request):
    book = request.session['book_name']
    t_count = len(vocabularies_in_book(book))
    vocabulary1 = vocabularies_in_book(book)
    l1 = []
    for i in range(vocabulary1.count()):
        l1.append(vocabulary1[i]['vocabulary'])

    vocabulary2 = personal_vocabularies(int(request.session['id']))
    l2 = []
    for i in range(vocabulary2.count()):
        l2.append(vocabulary2[i]['vocabulary'])

    p_count = len(list(set(l1) & (set(l2))))
    return render(request, 'finish_recite.html',
                  {'book': book,
                   't_count': t_count,
                   'p_count': p_count
                   })


def display_book(request):
    book = VocabularyBook.objects.filter(code=request.POST.get('book')).values('book_name')[0]['book_name']
    vocabulary = vocabularies_in_book(book)

    return render(request, 'display_book.html', {'list': vocabulary})


def display_personal(request):
    client = int(request.session['id'])
    vocabulary = personal_vocabularies(client)

    return render(request, 'display_personal.html', {'list': vocabulary})


def display_star(request):
    client = int(request.session['id'])
    vocabulary = staring_vocabularies(client)

    return render(request, 'display_star.html', {'list': vocabulary})


def star(request):
    star_vocabulary(int(request.session['id']), request.session['vocabulary'],
                    not PersonalVocabularyBook.objects.filter(
                        client_number=int(request.session['id'])).filter(
                        vocabulary=request.session['vocabulary']).values(
                        'is_staring')[0]['is_staring'])
    return redirect(reverse('vocabulary_detail'))


def recite_detail_noarg(request):
    v = request.session['vocabulary']

    return render(request, 'vocabulary_detail.html',
                  {'vocabulary': v,
                   'Chinese': translate(v),
                   'sentence': Vocabulary.objects.filter(vocabulary=v).values('sentence')[0]['sentence'],
                   'Chinese_sentence': Vocabulary.objects.filter(vocabulary=v).values('chinese_sentence')[0][
                       'chinese_sentence'],
                   'is_staring': PersonalVocabularyBook.objects.filter(
                       client_number=int(request.session['id'])).filter(vocabulary=v).values(
                       'is_staring')[0]['is_staring']
                   })


def display_r_line(request):
    count = request.POST.get('count')
    r_list = remember_line(int(request.session['id']), int(count))
    l = []
    for i in r_list:
        l.append(int(i * 100))
    return render(request, 'display_r_line.html', {'list': l})


def translate(word):
    post_url = 'https://fanyi.baidu.com/sug'
    # UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'

    }
    # post请求参数处理（同get请求一致）
    data = {
        'kw': word
    }
    # 发起请求
    response = requests.post(url=post_url, data=data, headers=headers)
    # 获取响应数据:json方法返回的是obj(对象)（如果确认响应数据是json类型，才可以使用json()）
    dic_obj = response.json()
    return dic_obj['data'][0]['v']


def test(request):
    count = int(request.POST.get('count'))
    r_list = personal_vocabularies(int(request.session['id']))
    l = []
    for i in range(r_list.count()):
        l.append(r_list[i]['vocabulary'])
    t_list = []
    if count < len(l):
        t_list = random.sample(l, count)
    else:
        t_list = l
    random.shuffle(t_list)
    json_str = json.dumps(t_list)
    request.session['test_list'] = json_str
    request.session['test_total'] = count
    request.session['test_correct'] = 0
    return redirect(reverse('begin_test'))


def begin_test_noarg(request):
    v = json.loads(request.session['test_list'])
    if not v:
        return redirect(reverse('finish_test'))
    r_list = personal_vocabularies(int(request.session['id']))
    l = []
    for i in range(r_list.count()):
        l.append(r_list[i]['vocabulary'])
    random.shuffle(l)

    e = v.pop()
    request.session['test_list'] = json.dumps(v)
    correct = Vocabulary.objects.filter(vocabulary=e).values()[0]['chinese']
    l.remove(e)
    f1 = Vocabulary.objects.filter(vocabulary=l.pop()).values()[0]['chinese']
    f2 = Vocabulary.objects.filter(vocabulary=l.pop()).values()[0]['chinese']
    f3 = Vocabulary.objects.filter(vocabulary=l.pop()).values()[0]['chinese']
    return render(request, 'test.html',
                  {'rand1': bool(random.getrandbits(1)),
                   'rand2': bool(random.getrandbits(1)),
                   'vocabulary': e,
                   'correct': correct,
                   'f1': f1,
                   'f2': f2,
                   'f3': f3
                   })


def begin_test(request, is_correct):

    if is_correct == "True":
        request.session['test_correct'] += 1

    v = json.loads(request.session['test_list'])
    if not v:
        return redirect(reverse('finish_test'))

    r_list = personal_vocabularies(int(request.session['id']))
    l = []
    for i in range(r_list.count()):
        l.append(r_list[i]['vocabulary'])
    random.shuffle(l)

    e = v.pop()
    request.session['test_list'] = json.dumps(v)
    correct = Vocabulary.objects.filter(vocabulary=e).values()[0]['chinese']
    l.remove(e)
    f1 = Vocabulary.objects.filter(vocabulary=l.pop()).values()[0]['chinese']
    f2 = Vocabulary.objects.filter(vocabulary=l.pop()).values()[0]['chinese']
    f3 = Vocabulary.objects.filter(vocabulary=l.pop()).values()[0]['chinese']
    return render(request, 'test.html',
                  {'rand1': bool(random.getrandbits(1)),
                   'rand2': bool(random.getrandbits(1)),
                   'vocabulary': e,
                   'correct': correct,
                   'f1': f1,
                   'f2': f2,
                   'f3': f3
                   })


def finish_test(request):
    total = request.session['test_total']
    correct = request.session['test_correct']
    return render(request, 'finish_test.html', {'total': total, 'correct': correct})
