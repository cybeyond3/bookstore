from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page  # 将首页加入redis缓存而导包

from books.models import Books
from books.enums import *
from django.urls import reverse
from django.core.paginator import Paginator


# 为 index_list() 函数抽取基类
def base(type, sort):
	'''index_list() 函数的基类'''
	if sort == 1:
		sort_value = 'new'
		limit = 3
	else:
		sort_value = 'hot'
		limit = 4
	return Books.objects.get_books_by_type(type, limit, sort_value)


# 抽 index 和 list 基类
def index_list():
	'''为 index 和 list 抽取基类'''

	# 查询每个种类的三个新品信息和四个销量最好的商品信息
	python_new = base(PYTHON, 1)
	python_hot = base(PYTHON, 2)
	javascript_new = base(JAVASCRIPT, 1)
	javascript_hot = base(JAVASCRIPT, 2)
	algorithms_new = base(ALGORITHMS, 1)
	algorithms_hot = base(ALGORITHMS, 2)
	machinelearning_new = base(MACHINELEARNING, 1)
	machinelearning_hot = base(MACHINELEARNING, 2)
	operatingsystem_new = base(OPERATINGSYSTEM, 1)
	operatingsystem_hot = base(OPERATINGSYSTEM, 2)
	database_new = base(DATABASE, 1)
	database_hot = base(DATABASE, 2)
	# 定义模板上下文
	context = {
		'item': [
			['Python', python_new, python_hot, 'images/banner01.jpg', 1, "python"],
			['Javascript', javascript_new, javascript_hot, 'images/banner02.jpg', 2, "javascript"],
			['数据结构与算法', algorithms_new, algorithms_hot, 'images/banner03.jpg', 3, "algorithms"],
			['机器学习', machinelearning_new, machinelearning_hot, 'images/banner04.jpg', 4, "machinelearning"],
			['操作系统', operatingsystem_new, operatingsystem_hot, 'images/banner05.jpg', 5, "operatingsystem"],
			['数据库', database_new, database_hot, 'images/banner06.jpg', 6, "database"],
		]
	}
	return context


# Create your views here.
@cache_page(30)  # 将index页面添加至redis缓存中，并设置过期时间为30s，这样以提高访问的响应速度
def index(request):
	"""显示首页"""
	context = index_list()
	# 使用模板
	return render(request, 'books/index.html', context)


def detail(request, books_id):
	"""显示商品的详情页面"""
	# 获取商品的详情信息
	books = Books.objects.get_books_by_id(books_id=books_id)
	if books is None:
		# 如果商品不存在，跳转到首页
		return redirect(reverse('books:index'))
	# 新品推荐
	books_li = Books.objects.get_books_by_type(type_id=books.type_id, limit=2, sort='new')
	# 定义上下文
	context = {
		'books': books,
		'books_li': books_li,
		'item': index_list()['item']
	}
	# 使用模板
	return render(request, 'books/detail.html', context)


# 商品种类 页码 排序方式
# /list/(种类id)/(页码)/?sort=排序方式
def list(request, type_id, page):
	"""商品列表页面"""
	# 获取排序方式
	sort = request.GET.get('sort', 'default')
	# 判断type_id是否合法
	if int(type_id) not in BOOKS_TYPE.keys():
		# 如果不合法
		return redirect(reverse('books:index'))
	# 根据商品种类id和排序方式查询数据
	books_li = Books.objects.get_books_by_type(type_id=type_id, sort=sort)
	# 分页
	paginator = Paginator(books_li, 10)
	# 获取分页之后的总页数
	num_pages = paginator.num_pages
	# 取第page页的数据
	if page == "" or int(page) > num_pages:
		page = 1
	else:
		page = int(page)
	# 返回值是一个Page类的实例对象
	books_li = paginator.page(page)
	# 进行页码控制
	# 1. 当前页码<5， 显示所有页码
	# 2. 当前页是前3页， 显示前5页
	# 3. 当前页是后3页， 显示后5页
	# 4. 其他情况， 显示当前页前2页、 后2页、 当前页
	if num_pages < 5:
		pages = range(1, num_pages)
	elif int(page) <= 3:
		pages = range(1, 6)
	elif num_pages - int(page) < 3:
		pages = range(num_pages-4, num_pages+1)
	else:
		pages = range(int(page)-2, int(page)+3)
	# 新品推荐
	books_new = Books.objects.get_books_by_type(type_id=type_id, limit=2, sort='new')
	# 定义上下文
	type_title = BOOKS_TYPE[int(type_id)]
	context = {
		'books_li': books_li,
		'books_new': books_new,
		'type_id': type_id,
		'sort': sort,
		'type_title': type_title,
		'pages': pages,
		# 下面的 item 自己添加的，用来在 list 页面的下拉菜单中，可以直接跳转到别的类型的 list 页面
		'item': index_list()['item']
	}
	# 使用模板
	return render(request, 'books/list.html', context)
