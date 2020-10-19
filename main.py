import jieba
import jieba.posseg as pseg
import nltk

# possible prefix for terms, do not modify
all_possible_prefix = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', '第一', '第二', '第三', '第四', '第五', '第六', '第七', '第八', '第九', '第十' ]
phrase_index = {} # a dictionary that stores all phrases' starting index

def is_substring(text, result, index, text_tp):
	'''
	:param text: string to check if it is a substring
	:param result: list of string that are terms
	:param index: starting index of text, use in range to check if is subtring
	:text_tp: language of text

	return true if text with given index is a substring of any string in result (at same position/index), false otherwise
	'''
	if phrase_index == {}:
		# empty dictionary -> first check, always not a substring
		return False
	else:
		for i in result:
			if text in i:
				indices = phrase_index.get(i) # this is a list of index, the index represent terms in words that contain temp
				if (indices == None):
					# should never happen
					print("key"+text+"with no value")
					return False

				# iuse the generator to check word length (since the generator has own way to split word)
				length_of_term = len(getWords(text, text_tp))

				for j in indices:
					# if the index is in range of the (starting index of any obtained term) to (the end of any obtained term)
					# then it is a substring and return true
					if index in range(j, j+length_of_term):
						#print(text+ "with index "+ str(index) +" is a substring of the string at index "+str(j))
						return True
	return False


def getWords(text, text_tp):
	'''
	:param text: paragraph to be dealed with
	:param text_tp: text type, either EN or CN
	:return: result after spliting words

	* NOTE: may wanna add extra feature based on usage, i.e. ignoring punctuation marks
	'''
	if text_tp == 'CN':
		# text type = chinese
		words = pseg.cut(text) # words is a generator that allows user to use for to obtain values
		return [(i,j) for i,j in words]
	else:
		# text type = english
		w_list = nltk.word_tokenize(text)  
		tagged = nltk.pos_tag(w_list) 
	return tagged


def is_term(text, term_lib):
	'''
	:param text: text to be checked according to the given terms
	:return: boolean value of it text exists in terms
	'''
	return text.strip() in term_lib # strip in case contains extra spaces


def split_words_to_list(text, text_type):
	'''
	return a list that contains words splited by the function getWords
	(getWords returns a list of tuple, this function converts to list of string)
	'''
	if (text_type == 'cn'):
		# for cases that cn is not capitalized
		words = getWords(text, "CN")
	else:
		words = getWords(text, text_type)

	all_words_in_text = [] # a list to store all words in the text, obtained from result of getWords

	for i in words:
		all_words_in_text.append(i[0])
	return all_words_in_text


def get_phrase_index_length(list_of_words, i, n, text_type):
	'''
	get phrase at index i, with length n, if i out of range, return ''
	
	>>> list_of_words = ['a','b','c']
	>>> get_word_index_length(list_of_words, 1, 2)
	>>> 'b c'

	if text_type == 'cn', the function will ignore the spaces in between
	'''
	if (i >= len(list_of_words)):
		return ''
	elif (i+n > len(list_of_words)):
		return ''
	result = ' '.join(list_of_words[i:i+n])
	if (text_type == 'cn' or text_type == 'CN'):
		result = result.replace(' ','')
	return result


def check_prefix(words, i):
	'''
	: param text : list of words
	: param i : index of the starting word of phrase (i.e. ['a', 'b', 'c'], if we want find the prefix of b, then i = 1)
	: param type: text type
	
	return the prefix of text if exists
	'''
	temp = ''
	if (i-1<0):
		# english, one word (first, second)
		pass
	else:
		temp = words[i-1]

	#check if temp is an accepatable prefix
	if (temp in all_possible_prefix):
		return temp
	return ''

def get_prefix(words, i , text_type, text):
	'''
	:param words: list of words
	:param i : index of text
	:param text_type: 'cn'/'en'
	:param text: text to be updated with prefix

	:return: a string that contains possible prefix like first or "第一"

	'''
	# check for possible prefix
	prefix = check_prefix(words, i)
	# combine prefix with the term
	if (type == 'cn' or type == 'CN'):
		temp = prefix.strip() + text.strip()
		temp = temp.replace(' ','') # replace the spaces between words caused when concatenated
	else:
		temp = prefix.strip() + text.strip()
		#since english, no need to remove middle spaces

	temp = temp.strip() #remove extra space
	return temp



def processor(text, term_lib, length_of_maximum, text_type):
	'''
	:param text: a string of text to be processed
	:param term_lib: a list of all terms that can be matched up
	:param length_of_maximum: an integer of maximum length of term (also known as N as in the description)
	:return: list of all terms that has length <= length_of maximum that can be matched up in term_lib, serial number is also included
	
	>>> text = 'hello world, hello python, first hello'
	>>> term_lib = ['hello world', 'python', 'hello']
	>>> length_of_maximum = 5
	>>> text_type = "EN"
	>>> result = processor(text, term_lib, length_of_maximum, text_type)
	>>> result
	>>> ['hello world', 'python', 'hello', 'first hello']

	----------------

	>>> text = '世界第一高峰是珠穆朗玛峰'
	>>> term_lib = ['世界','高峰', '珠穆朗玛峰']
	>>> length_of_maximum = 1 
	>>> text_type = "CN"
	>>> result = processor(text, term_lib, length_of_maximum, text_type)
	>>> result
	>>> [‘珠穆朗玛峰’，‘世界’，‘第一高峰’]

	>>> term_lib = ['世界第一高峰','珠穆朗玛峰']
	>>> result = processor(text, term_lib, length_of_maximum, text_type)
	>>> result
	>>> ['珠穆朗玛峰’]

	>>>	length_of_maximum = 3
	>>> result = processor(text, term_lib, length_of_maximum, text_type)
	>>> result
	>>> ['世界第一高峰','珠穆朗玛峰’]
	'''

	# temp var for test, all term_lib -> temp_lib when testing
	# temp_lib = ['one', 'two', 'three', 'four', 'five', 'one word', '你好', '你','我']

	global phrase_index # call the dictionary so later on can update if needed
	#------------split words-----------------
	words = split_words_to_list(text, text_type) # split words into a list

	# init result
	result = []
	# long phrases first
	for n in range(length_of_maximum, 0, -1):
		# i represents length of words
		index = 0
		temp = get_phrase_index_length(words, index, n, text_type)
		while (temp != ''):
			#check if temp is a term
			if (is_term(temp, term_lib)):
				# check if temp is any obtained term's substring
				if (is_substring(temp, result, index,text_type)):
					temp = '' # ignore the substrings

				# if it is a substring then over
				if (temp == ''):
					pass
				else:
					temp = get_prefix(words, index, text_type, temp) # get word with prefix if exist

					# does not have a index like 'first' or '第一'
					if check_prefix(words, index) != '': 
						# in this case the index of the start of the phrase is the previous index
						index_of_phrase -= 1 # this is used to check if temp is a substring
					else:
						index_of_phrase = index
					# check if temp is already added, if not, append it, and add into dictionary with corresponding key
					if (temp not in result):
						result.append(temp)
						phrase_index.update({temp :[index_of_phrase]})
					# or just update the dictionary
					else:
						phrase_index.update({temp:phrase_index[temp] + [index_of_phrase]})
			#end of term check

			# move to next word
			index+=1
			temp = get_phrase_index_length(words, index, n,text_type)

	print('processor done\n')
	return result


def txt_to_dict(file_name):
	'''
	:param file_name: a string represents name of the file containing terms
	:param text_type: type of terms 术语本身的语言 'cn'/'en'
	:precondition: terms and meaning are seperated by tabs in txt file i.e. 术语名(tab\t)意思
	:return: a dictionary such that key is term, value is meaning
	'''
	with open(file_name,'r',encoding="utf8") as f:
		data = f.readlines()
	term_dict = {}
	# split based on tabs
	# term before tab, meaning after tab
	for i in data:
		index_of_space = i.find('\t')
		if (index_of_space == -1):
			continue
		else:
			term = i[0:index_of_space].strip() # from the first index to the space
			meaning = i[index_of_space+1::].strip() # from first occurence of space to end of string
			term_dict.update({term: meaning})
	# gathering data done
	return term_dict


def remove_redundant_data(terms):
	'''
	:param terms: list of terms that may have repeated string with upper case / lower case
	list of 术语 in english，可能存在大写term和小写term都在里面的问题

	:return: a list that contains no redundant data
	'''
	temp = terms
	for i in terms:
		if i.lower() in terms:
			temp.remove(i)
	return temp


def term_and_meaning(term, term_dict, text_tp):
	'''
	: param term: term to be looked up for meaning, might contain prefix
	: param term_dict: a dictionary which key is term and value is meaning
	: param text_tp: language of term

	return a string in such form "<term>         <meaning>"
								 "<a long term>  <meaning>"
	'''

	# check if term already exist in term_dict
	if term in term_dict.keys():
		# result formatted
		result = term + '\t' + term_dict[term] 

	else:
		#not in keys --> have prefix --> check based on language
		if (text_tp.lower() == 'cn'):
			# chinese --> first two char is prefix
			prefix = term[0:2]
			temp = term[2::].strip()
			meaning_of_prefix = all_possible_prefix[all_possible_prefix.index(prefix) - 10] 
			# global var defined at top of the code file, inner part respresents index of the meaning of the prefix
			# for example '第一' is at index 10, and we want 'first', which is at index 0
			result = term+'\t' + meaning_of_prefix + ' ' +term_dict[temp] # add space because english needs space to seperate
			#(original term language is cn --> meaning(result) language is en)
		else:
			# english
			first_space_index = term.find(' ')
			prefix = term[0: first_space_index]
			temp = term[first_space_index::].strip()
			# similar algorithm as above (cn)
			meaning_of_prefix = all_possible_prefix[all_possible_prefix.index(prefix) + 10]
			result = term+'\t' + meaning_of_prefix + term_dict[temp]

	return result





if __name__ == '__main__':
	filename = input("Enter the file name: ")
	# Open a file: filename
	file = open(filename,mode='r', encoding="utf8")
 
	# read all lines at once
	file_text = file.read()
 
	# close the file
	file.close()

	text_type = input("Enter language: ") # *******always remember to update text_type

	# get terms 
	lib_file_name = input("Enter term lib file name: ")
	term_lib_dict = txt_to_dict(lib_file_name)
	term_lib_list = term_lib_dict.keys()

	max_length = 5
	
	#run processor
	result = processor(file_text,term_lib_list,max_length,text_type)

	if (text_type.lower() != 'cn'):
		# not chinese, may have capitalization problem
		result = remove_redundant_data(result)

	target = open("result.txt", 'w+', encoding="utf8")
	# print result 
	for i in result:
		target.write(term_and_meaning(i, term_lib_dict, text_type)+'\n')
	
	target.close()
