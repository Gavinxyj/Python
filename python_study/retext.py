import re

content = '''Although we have taken every care to ensure the accuracy of our content, mistakes do happen. If you find a mistake in one of our books—maybe a mistake in the text or
the code—we would be grateful if you could report this to us. By doing so, you can
save other readers from frustration and help us improve subsequent versions of this
book. If you find any errata, please report them by visiting http://www.packtpub.com/submit-errata,'''

# literal 匹配字符串的值
pattern = re.compile(r'find', re.S)

# 使用findall函数，该函数返回一个列表
items = re.findall(pattern, content)
print('findall() 返回一个列表: %s' % items)
print('*'*100)
# 使用finditer函数，该函数返回一个迭代器,迭代器是一个match对象，需要用match对象的group()函数取值
items = re.finditer(pattern, content)
print('finditer()返回一个迭代器:%s' % items)
for index, item in enumerate(items):
	print('item[%d] = %s, item-value = %s' % (index, item, item.group()))
print('*'*100)

# 使用match函数, 该函数返回一个match对象, 该函数只返回一个匹配的对象，切记！切记！
# 这个函数只检查正则表达式是不是在string的开始位置匹配,所以下面的表达式返回的是None
items = re.match(pattern, content)
print(items)
print('*'*100)

# 使用search, 该函数返回表达式模式pattern的第一次出现, 同时该函数返回一个match对象
item = re.search(pattern, content)
print('item = %s, item-value = %s' % (item, item.group()))
print('*'*100)

# sub替换字符串中pattern匹配的地方, 下面是将字符串中的find替换成hello
item = re.sub(pattern, 'hello', content)
print(item)
print('*'*100)


# |表示或的意思，x|y|z|...表示匹配x或y或z或者其它
pattern = re.compile(r'find|we', re.S)
# 使用findall函数，该函数返回一个列表
items = re.findall(pattern, content)
print('findall() 返回一个列表: %s' % items)
print('*'*100)

# .匹配任何字符除换行符外, 
pattern = re.compile(r'f..d', re.S) #匹配f,d之间包含两个任意字符的字符串结果
items = re.findall(pattern, content)
print(items)
print('*'*100)

# ^匹配字符串的开始
pattern = re.compile(r'^Although', re.S) # 匹配以Although开始的字符串
items= re.findall(pattern, content)
print(items)
print('*'*100)

# $匹配字符串结尾
pattern = re.compile(r'submit-errata,$', re.S)
items= re.findall(pattern, content)
print(items)
print('*'*100)

# 匹配以字符串Although，并且以字符串submit-errata,结尾的字符串
pattern = re.compile(r'^Although.*?submit-errata,$', re.S)
items= re.findall(pattern, content)
print(items)
print('*'*100)

# split() 分割字符串
pattern = re.compile(r' ', re.S)
items= re.split(pattern, content)
print(items)
print('*'*100)

# \b匹配单词边界 \bAlthough表示匹配以单词Although开头的字符串，Although\b表示以Although的单词
pattern = re.compile(r'\bAlthough\b', re.S) #精确匹配单词Although
items= re.findall(pattern, content)
print(items)
print('*'*100)

# 查找字符串中的url
pattern = re.compile(r'\w{3}\.\w+\.\w{3}', re.S) #精确匹配单词Although
items= re.findall(pattern, content)
print(items)
print('*'*100)

# 查找字符串中的url
pattern = re.compile(r'[a-zA-z]+://[^\s]*', re.S) #精确匹配单词Although
items= re.findall(pattern, content)
print(items)
print('*'*100)