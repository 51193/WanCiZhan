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


def vocabulary_books():
    return VocabularyBook.objects.values()


def display_all_vocabulary_books():
    print('正在输出所有单词书')
    vocabulary_book = vocabulary_books()
    for i in range(vocabulary_book.count()):
        print(vocabulary_book[i])


def vocabularies_in_book(book_name):
    return Vocabulary.objects.filter(
        type__contains=VocabularyBook.objects.filter(book_name=book_name).values()[0]['code'])


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
        PersonalVocabularyBook.objects.filter(client_number=client_number).filter(vocabulary=vocabulary).update(
            is_remembered=is_remembered)

    else:
        p = PersonalVocabularyBook(
            client_number=client_number,
            vocabulary=vocabulary,
            is_remembered=is_remembered
        )
        p.save()


def today_vocabularies(client_number, book_name, today_number):
    # 明天继续写
    return 0
