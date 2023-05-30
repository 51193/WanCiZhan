import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WanCiZhan.settings")

import django

django.setup()

# 必须要在 初始化django 之后导入 models
from vocabularies.models import Vocabulary
from vocabularies.views import *
from users.views import *

print(today_vocabularies(1, '测试用例', 0))

display_personal_vocabularies(1)

display_all_users()

display_all_vocabulary_books()
display_all_vocabularies()
display_vocabularies_in_book('测试用例')
