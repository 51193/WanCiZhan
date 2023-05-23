from django.db import models


# Create your models here.

class VocabularyBooks(models.Model):
    book_name = models.CharField(max_length=50, verbose_name="单词书名称")
    code = models.CharField(max_length=1, verbose_name="单词书对应代码")

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vocabulary'], name='vocabulary'),
        ]

    def __str__(self):
        return self.vocabulary
