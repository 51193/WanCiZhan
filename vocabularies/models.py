from django.db import models


# Create your models here.
# class VocabularyBookManager(models.Manager):
#   def create_book(self, book_name, code):
#       book = self.create(book_name=book_name, code=code)
#       return book


class VocabularyBook(models.Model):
    book_name = models.CharField(max_length=50, verbose_name="单词书名称")
    code = models.CharField(max_length=1, verbose_name="单词书对应代码")

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code'], name='code')
        ]

    def __str__(self):
        return "%s(编号为:%s)" % (self.book_name, self.code)


class Vocabulary(models.Model):
    vocabulary = models.CharField(max_length=50, verbose_name="单词")
    chinese = models.CharField(max_length=50, verbose_name="中文释义")
    sentence = models.CharField(max_length=100, verbose_name="例句")
    chinese_sentence = models.CharField(max_length=100, verbose_name="例句翻译")

    type = models.CharField(max_length=100, verbose_name="被哪些单词书包含")

    # 通过子字符串匹配判断该单词被包含在哪些单词书中，

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vocabulary'], name='vocabulary'),
        ]

    def __str__(self):
        return self.vocabulary


class PersonalVocabularyBook:
    client_number = models.ForeignKey('users.User', on_delete=models.CASCADE)
    vocabulary = models.ForeignKey('Vocabulary', on_delete=models.CASCADE)
    first_met_date = models.DateField(None, None, False, True)
    last_met_date = models.DateField(None, None, True, False)
    is_remembered=models.BooleanField()

    objects = models.Manager()
