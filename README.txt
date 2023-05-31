新添加的函数：
	vocabularies\views.py中的
		all_vocabularies()		
		#返回全部单词，以QuerrySet{List[Dict]}的数据结构返回，可以直接通过List和Dict访问模式访问内部元素

		display_all_vocabularies	
		#以文本形式输出所有单词在数据库中的所有部分，其他display函数功能都相似，不再在文档里叙述

		all_vocabulary_books()
		#返回全部单词书，与all_vocabularies的返回格式相同

		vocabularies_in_book(book_name)
		#返回在名为:'book_name'的单词书中包含的所有单词，返回格式同上

		personal_vocabularies(client_number)
		#返回用户client_number学过的所有单词，返回格式同上，注：只要是学过的都会显示，并不只是收藏的

		staring_vocabularies(client_number)
		#返回用户client_number收藏的所有单词，返回格式同上

		add_vocabulary(vocabulary, translation, sentence, sentence_translation)
		#新增单词，参数名称即为需要填的内容，请注意：不要添加数据库中已存在的vocabulary；新增的单词不属于任何单词书，需要通过其他函数分配

		add_vocabulary_book(book_name, code)
		#新增单词书，请注意：不要填写数据库中已存在的book_name或code；新增的单词书为空，需要通过其他函数分配

		distribute_vocabulary(vocabulary, vocabulary_book)
		#分配单词给单词书，将vocabulary分配给vocabulary_book，一个vocabulary可以被分配给多个vocabulary_book

		handle_vocabulary(client_number, vocabulary, is_remembered)
		#处理vocabulary，当用户client_number每次遇到vocabulary时，无论是否记住，都要调用一次该函数；is_remembered填写布尔值，代表是否记住；该函数中包装了许多功能，包括为遗忘曲线和生成需要背诵的单词表打下的基础，直接调用就好

		star_vocabulary(client_number, vocabulary, is_star)
		#用户client_number收藏或取消收藏vocabulary；is_star填写布尔值，True代表收藏，False代表取消收藏

		today_new_vocabularies(client_number, book_name, today_new_count)
		#返回为用户client_number在book_name单词书中今日需要背的新单词；today_new_count代表今日需要背的新单词的数量；返回值为List类型

		today_review_vocabularies(client_number, book_name, today_review_count)
		#返回为用户client_number在book_name单词书中今日需要复习的旧单词；today_review_count代表今日需要复习的旧单词的数量；返回值为List类型

		remember_line(client_number, day_count)
		#返回用户client_number在day_count天内的遗忘曲线；返回值为长度为day_count的List，数组下标代表日期，所有数字都在0-1之间，代表记住的单词占全部单词的比例，day0锁定为1