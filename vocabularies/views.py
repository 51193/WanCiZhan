import random
from pprint import pprint

from django.forms import model_to_dict
from django.shortcuts import render
from vocabularies.models import *


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

    v_list = []

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
        if (i['last_met_date'] - i['first_met_date']).days <= day_count:
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
