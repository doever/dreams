## 字符串编码

字符：

字节：

字节流：

转义序列：

unicode序列：

### python2：





### python3：

---

## 导包

**在入口程序中将项目所在的根目录添加到sys.path中**

```python
import sys
import os

# 将项目的根目录添加到sys.path中
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    
sys.path.append(BASE_DIR)

# 导入包或模块
from db.mysql.my_connect import connect
```

项目结构：

/src/common

​							\_\_init\_\_.py

​							tools.py

/src/compare

​							compare.py

在compare.py中引用tools.py

​							





---

## 注释规范

### python开头注释

```python
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                              ${NAME}.py                                     #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                #
#     This script .                                                           #
#                                                                             #
# Author     : cl                                                             #
# Version    : v1.0                                                           #
# CreateTime : ${DATE} ${TIME}                                                #
# Copyright (c) 2024 by cl                                                    #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
```



![image-20240407142148861](D:\cl\dreams\static\pic\image-20240407142148861.png)

1. #!/usr/bin/env [python](https://so.csdn.net/so/search?q=python&spm=1001.2101.3001.7020) 与 #!/usr/bin/python 的区别

**这些注释并不仅仅是写给读者看的注释，它也写给操作系统看的，这些注释决定了系统将如何运行这些文件。**

\#!/usr/bin/python 注释的问题在于，Linux只系统默认的py解释器（也就是自带的那个）来运行文件。这样用户就无法使用自己的python版本了，不同的py版本之间语法有些差异，尤其是变动比较大的py2和py3，这些差异会使得整个程序无法正常运行。而#!/usr/bin/env python 的出现可则让用户可以自行选择python版本，用户可以在**环境变量**中配置自己的py解释器（ps：用户安装的版本默认定位在linux的local文件夹中）。#!/usr/bin/env python 这行注释，会使linux在解析文件时，知道要去使用环境变量中的py解释器而非系统自带的那个。

所以如果你要使用该注释，推荐使用#!/usr/bin/env python 的注释，而非 #!/usr/bin/python。

### 函数注释（函数、方法、生成器）

一个函数必须要有文档字符串，除非满足以下条件：

1. 外部不可见
2. 非常短小
3. 简单明了

文档字符串应该：

1. 包含函数做什么，而不是怎么做的。
2. 让使用者不需要看一行代码，只需要看文档就可以
3. 包含输入和输出的详细描述
4. 对于复杂的代码可以在代码旁边加注释
5. 覆盖基类的方法可以加：See base class

在文档字符串中，应该根据不同的内容进行分组。文档字符串常用的分组：

- Args:

  

  列出每个参数的名字, 并在名字后使用一个冒号和一个空格, 分隔对该参数的描述.如果描述太长超过了单行80字符,使用2或者4个空格的悬挂缩进(与文件其他部分保持一致). 描述应该包括所需的类型和含义. 如果一个函数接受*foo(可变长度参数列表)或者**bar (任意关键字参数), 应该详细列出`*foo`和`**bar`.

- Returns:

   

  (或者 Yields: 用于生成器)

  

  描述返回值的类型和语义. 如果函数返回None, 这一部分可以省略.

- Raises:

  

  列出与接口有关的所有异常.

  示例

  ```python
  def fetch_smalltable_rows(table_handle: smalltable.Table,
                          keys: Sequence[Union[bytes, str]],
                          require_all_keys: bool = False,
  ) -> Mapping[bytes, Tuple[str]]:
      """Fetches rows from a Smalltable.
  
      Retrieves rows pertaining to the given keys from the Table instance
      represented by table_handle.  String keys will be UTF-8 encoded.
  
      Args:
          table_handle: An open smalltable.Table instance.
          keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
          require_all_keys: Optional; If require_all_keys is True only
          rows with values set for all keys will be returned.
  
      Returns:
          A dict mapping keys to the corresponding table row data
          fetched. Each row is represented as a tuple of strings. For
          example:
  
          {b'Serak': ('Rigel VII', 'Preparer'),
          b'Zim': ('Irk', 'Invader'),
          b'Lrrr': ('Omicron Persei 8', 'Emperor')}
  
          Returned keys are always bytes.  If a key from the keys argument is
          missing from the dictionary, then that row was not found in the
          table (and require_all_keys must have been False).
  
      Raises:
          IOError: An error occurred accessing the smalltable.
      """
  ```

### 类注释

类应该在其定义下有一个用于描述该类的文档字符串. 如果有公共属性(Attributes), 那么文档中应该有一个属性(Attributes)段. 并且应该和函数参数的格式相同。

```
class SampleClass(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""
```

### 块注释和行注释

如果代码在代码审查的时候，可能需要再次思索该代码意义，那么就应该写注释。

需要注意以下两点：

1. 行注释，应离开代码最少两个空格。
2. 不要描述代码，阅读代码的时候，一般不是看不懂，而不是不认识。

示例：

```
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:        # True if i is 0 or a power of 2.
```

---

##  魔术方法

在Python中，`__getitem__`是一个特殊方法，用于实现对象的索引访问。当你使用索引操作符`[]`来访问对象的元素时，解释器会调用该对象的`__getitem__`方法。这个方法接受一个参数，通常是索引，然后返回相应位置的值。

例如，如果你有一个自定义的类，并在该类中实现了`__getitem__`方法，你就可以使用索引来访问该类的实例。下面是一个简单的示例：

```
class MyList:
    def __init__(self, elements):
        self.elements = elements

    def __getitem__(self, index):
        return self.elements[index]

# 创建一个MyList实例
my_list = MyList([1, 2, 3, 4, 5])

# 使用索引访问元素
print(my_list[2])  # 输出: 3
```

在这个例子中，`MyList`类实现了`__getitem__`方法，使得类的实例可以像列表一样使用索引来访问元素。这使得你的自定义类可以表现得像内置的序列类型，如列表或元组。

此外，通过实现`__getitem__`方法，你还可以使你的对象支持切片操作。如果`__getitem__`方法中的索引参数是一个切片对象，你可以根据需要返回切片的结果。这可以进一步提高对象的灵活性。

示例2，如何使用魔术方法实现一个可切片对象：

```python
class MyGroup:
    def __init__(self, company_name, group_name, staffs):
        self.company_name = company_name
        self.group = group_name
        self.staffs = staffs

    def __getitem__(self, item):
        if isinstance(item, slice):
            cls = self.__class__
            return cls(self.company_name, self.group, self.staffs[item])
        if isinstance(item, int):
            cls = self.__class__
            return cls(self.company_name, self.group, [self.staffs[item]])

    # def __iter__(self):
    #     pass

    def __len__(self):
        pass

    def __contains__(self, item):
        pass

    def __str__(self):
        return f"{self.staffs}"


grp = MyGroup('abc', 'g1', ['a', 'b', 'c'])
print(grp[1])
print(grp[1].company_name)
print(grp[:2])
print(type(grp[:2]))
for i in grp[0:2]:
    print(i)
```

------

##  __new__ **方法跟 __**init__ 方法

- •

  `__new__` 是一个类方法，而 `__init__` 是一个实例方法。

- •

  `__new__` 负责创建实例，它的返回值通常是一个新的实例。

- •

  `__init__` 负责初始化实例，它不返回值，但通常会修改实例的属性等。

在一般情况下，你不需要显式地调用 `__new__` 方法，因为它在实例创建的过程中会被自动调用。而 `__init__` 方法会在实例创建后，通过调用类实例时自动调用。

__new__方法主要是当你继承一些不可变的class时(比如int, str, tuple)， 提供给你一个自定义这些类的实例化过程的途径。还有就是实现自定义的[metaclass](http://www.cnblogs.com/wancy86/p/python_meteclass.html)。

假如我们需要一个永远都是正数的整数类型，通过集成int，我们可能会写出这样的代码

```
class PositiveInteger(int):

    def __init__(self, value):
        super().__init__(self, abs(value))

i = PositiveInteger(-3)
print(i)
# # TypeError: object.__init__() takes no parameters


class PositiveInteger(int):

    def __new__(cls, value):
        return super(PositiveInteger, cls).__new__(cls, abs(value))
i = PositiveInteger(-3)
print(i)
# 3
class IntClass(object):
    def __new__(cls, *args, **kwargs):
        a = super().__new__(cls)
        a.value = 11
        # a.__str__ = lambda self: str(self.value+1)
        print(type(a))   #<class '__main__.IntClass'> a就是初始化的实例对象
        print(a)  # 会调用 __str__方法
        return a  # 返回创建的实例

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
        # return '123'
```

## __name__ 与 __main__

**python的main是什么，为什么打印类的时候会出现main.类名**

`__main__` 是 Python 中一个特殊的模块名称，用于表示当前执行的脚本或程序。当一个 Python 脚本被直接运行时，该脚本的命名空间将被指定为 `__main__`。这意味着在这个脚本中定义的变量、函数和类都属于 `__main__` 模块。

当你在脚本中定义了一个类，例如：

```
class MyClass:
    pass

print(MyClass)
```

在这个脚本中执行时，`MyClass` 类的输出可能会显示为 `<class '__main__.MyClass'>`。这里的 `__main__` 表示该类是在当前模块（即当前执行的脚本）中定义的。

这样的输出形式 `<class '__main__.MyClass'>` 中的 `__main__` 指示了类的定义是在主程序中，而不是在其他模块中。如果这个类是在一个单独的模块中定义的，那么输出可能为 `<class '模块名.MyClass'>`。  --简单来说就是命名空间

需要注意的是，如果这个类是在交互式环境（如 Python 解释器的交互式终端或 Jupyter Notebook）中定义的，那么输出中可能没有 `__main__`，而直接显示为 `<class '__main__.MyClass'>`。这是因为在交互式环境中，代码的执行方式与脚本稍有不同。

**这个main 跟python的 if 'name' == 'main'是一样的吗，为什么python的入口要这么写**

`__main__` 和 `if __name__ == "__main__"` 是相关的概念，但不完全相同。

1. 1.

   `**__main__**`**:** 在 Python 中，`__main__` 是一个特殊的模块名称，用于表示当前执行的脚本或程序。当一个 Python 脚本被直接运行时，该脚本的命名空间将被指定为 `__main__`。这使得脚本中定义的变量、函数和类都属于 `__main__` 模块。

2. 2.

   `**if __name__ == "__main__":**`**:** 这是一个惯用的写法，用于判断当前模块是被直接运行还是被导入到其他模块中。当一个 Python 模块被直接运行时，`__name__` 的值会被设置为 `"__main__"`。因此，通过 `if __name__ == "__main__":` 来判断可以使得一些特定的代码块只在模块被直接执行时执行，而在被导入时不执行。

```
# 示例脚本：my_script.py

def my_function():
    print("Function in my_script")

if __name__ == "__main__":
    print("This is executed when the script is run directly.")
    my_function()
```

如果你运行这个脚本，你会看到输出中包含 `"This is executed when the script is run directly."`。但如果你在其他脚本中导入 `my_script.py`，那么这个输出就不会被执行。

结合起来，`if __name__ == "__main__":` 常常和 `__main__` 模块一起使用，以确保某些代码块只在脚本直接运行时执行，而在被导入时不执行。这样的设计模式在编写可重用模块时很有用。

**__name__还有哪些值**

`__name__` 是一个特殊的内置变量，在不同的上下文中它可以取不同的值。以下是几种常见的情况：

1. 1.`**__name__ == "__main__"**`**：** 当一个 Python 脚本被直接执行时，`__name__` 的值为 `"__main__"`。这是常用于判断模块是被直接运行还是被导入到其他模块中的条件。

   ```
if __name__ == "__main__":
       # 这里的代码块只在脚本直接执行时执行
   ```
   
2. 2.**在模块中的其他情况：** 如果一个模块被导入到其他模块中，`__name__` 的值为模块的名称。

   ```
e# 如果 my_module.py 被导入到其他模块，__name__ 的值为 "my_module"
   ```
   
3. 3.**在交互式环境中的情况：** 在交互式环境中，`__name__` 的值为 `"__main__"`，与直接执行脚本时的情况相同。这样可以使得在交互环境中定义的函数或变量与脚本中的行为一致。

   ```
   
   ```

在交互式环境中

   >>> __name__
   '__main__'
   
   ```
   
   ```

4. 4.**在 Python 脚本中运行的模块的情况：** 如果一个 Python 脚本中的代码块（而非被导入的模块）被执行，`__name__` 的值为 `"__main__"`。

   ```
   
   ```

在运行的 Python 脚本中

   >>> __name__
   '__main__'
   
   ```
   
   ```

总体来说，`__name__` 在不同的执行环境中扮演不同的角色，提供了一种机制来判断代码是在何种上下文中运行的。

------

## 元类 Metaclass


在 Python 中，元类（metaclass）是一种高级的编程概念，用于定义类的创建方式。元类是类的类，它控制着类的创建和初始化过程。在 Python 中，类本身也是对象，而元类就是用来创建这些类对象的。

元类的作用主要体现在以下几个方面：

1. 1.

   **控制类的创建过程：** 元类可以拦截类的创建过程，可以在类被创建时执行一些特殊操作。这使得你可以自定义类的创建逻辑。

2. 2.

   **修改类的属性和方法：** 元类可以在类被创建后，动态地修改类的属性和方法。这使得你可以在运行时改变类的行为。

3. 3.

   **约束类的结构：** 元类可以用来强制某些规范，确保类的结构符合特定的要求。

4. 4.

   **自动化代码生成：** 元类可以用来自动生成代码，减少重复工作。这在一些框架和库中很常见。

使用元类的场景相对较少，一般来说，普通的面向对象编程并不需要使用元类。但在一些特殊的情况下，元类提供了强大的工具，用于实现一些高级的编程技巧。

以下是一些可能需要使用元类的情况：

- •

  **框架和库的开发：** 元类可以用于创建具有特定结构和行为的类，例如 Django ORM 中的模型类。

- •

  **代码检查和规范：** 元类可以用于强制执行编码规范，确保类的结构满足预定义的标准。

- •

  **自动化代码生成：** 元类可以用于自动生成重复性的代码，提高开发效率。

需要注意的是，使用元类是一种高级特性，不是每个项目都需要。在大多数情况下，普通的类和继承关系足以满足需求。

自定义类的的目的，我总结了一下就是拦截类的创建，然后修改一些特性，然后返回该类。是不是有点熟悉？没错，就是感觉是装饰器干的事情，只是装饰器是修饰一个函数，同样是一个东西进去，然后被额外加了一些东西，最后被返回。

其实除了上面谈到的制定一个__metaclass__并不需要赋值给它的不一定要是正式类，是一个函数也可以。要创建一个使所有模块级别都是用这个元类创建类的话，在模块级别设定__metaclass__就可以了。先写一个来试试看，我还是延用stackoverflow上面那个哥们的例子，将所有的属性都改为大写的。🤗

来看这个例子：

```
input:
def upper_attr(class_name, class_parents, class_attr):
    """
    返回一个对象,将属性都改为大写的形式
    :param class_name:  类的名称
    :param class_parents: 类的父类tuple
    :param class_attr: 类的参数
    :return: 返回类
    """
    # 生成了一个generator
    attrs = ((name, value) for name, value in class_attr.items() if not name.startswith('__'))
    uppercase_attrs = dict((name.upper(), value) for name, value in attrs)
    return type(class_name, class_parents, uppercase_attrs)

__metaclass__ = upper_attr

pw = upper_attr('Trick', (), {'bar': 0})
print hasattr(pw, 'bar')
print hasattr(pw, 'BAR')
print pw.BAR

output:
False
True
0
```

可以从上面看到，我实现了一个元类(metaclass)， 然后指定了模块使用这个元类来创建类，所以当我下面使用type进行类创建的时候，可以发现小写的bar参数被替换成了大写的BAR参数，并且在最后我调用了这个类属性并，打印了它。

上面我们使用了函数做元类传递给类，下面我们使用一个正式类来作为元类传递给__metaclass__

```
class UpperAttrMetaClass(type):
    def __new__(mcs, class_name, class_parents, class_attr):
        attrs = ((name, value) for name, value in class_attr.items() if not name.startswith('__'))
        uppercase_attrs = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaClass, mcs).__new__(mcs, class_name, class_parents, uppercase_attrs)


class Trick(object):
    __metaclass__ = UpperAttrMetaClass
    bar = 12
    money = 'unlimited'

print Trick.BAR
print Trick.MONEY
```

---

## 上下文管理器

使用上下文管理器来管理数据库连接是一种常见的做法，它确保在代码块执行完毕后正确地关闭数据库连接，即便发生异常也能正确处理。在 Python 中，你可以使用 `with` 语句和上下文管理器来实现这个目的。

下面是一个简单的示例，展示如何使用上下文管理器来处理数据库连接：

```
import sqlite3
from contextlib import contextmanager

# 定义数据库连接上下文管理器
@contextmanager
def database_connection(db_file):
    # 建立数据库连接
    connection = sqlite3.connect(db_file)

    try:
        # 提供连接对象，使其可用于 with 语句块中的代码
        yield connection
    finally:
        # 确保在退出 with 语句块时关闭数据库连接
        connection.close()

# 使用上下文管理器来执行数据库操作
db_file = 'my_database.db'

# 在 with 语句中使用数据库连接
with database_connection(db_file) as coqqnn:
    cursor = conn.cursor()

    # 执行数据库操作
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('John Doe', 30))
    conn.commit()

    # 查询数据
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
```

在上述例子中，`database_connection` 函数是一个上下文管理器，它使用了 `@contextmanager` 装饰器。在 `with` 语句块内，建立数据库连接并将连接对象传递给 `yield`，使得在 `with` 语句块中可以使用这个连接对象执行数据库操作。无论代码块执行是否出现异常，`finally` 语句都会确保在退出时关闭数据库连接。

示例2：

```
@contextmanager
def my_context_manager():
    # 在进入上下文之前的代码，相当于 __enter__ 方法
    print("Entering the context")
    f = open('app.py', 'r')
    # 返回一个值，该值将被赋给与 as 关键字关联的变量
    yield f
    # 在退出上下文之后的代码，相当于 __exit__ 方法
    print("Exiting the context")
    f.close()


# 使用 with 语句调用上下文管理器
with my_context_manager() as message:
    for line in message:
        print(line)
```

------

##  解包语法

当你需要将一个可迭代对象中的元素传递给一个函数或方法，或者在赋值时需要将元组中的值解包为独立的变量时，使用解包语法是非常方便的。以下是一个类似的解包例子：

```
# 一个简单的函数，接受两个参数并返回它们的和
def add_numbers(a, b):
    return a + b

# 一个元组，包含两个数字
numbers_tuple = (3, 7)

# 不使用解包，将整个元组传递给函数
result_without_unpacking = add_numbers(numbers_tuple)
# 上述代码会导致 TypeError，因为 add_numbers 函数期望接收两个参数，但只收到一个元组参数

# 使用解包，将元组中的元素作为独立的参数传递给函数, 相当于 add_numbers(3, 7)，得到结果 10
result_with_unpacking = add_numbers(*numbers_tuple)

# 使用字典解包，将元组中的元素作为独立的参数传递给函数
result = add_numbers(**{'a':1, 'b':2})

print("Result without unpacking:", result_without_unpacking)
print("Result with unpacking:", result_with_unpacking)
```

在这个例子中，`add_numbers(*numbers_tuple)` 使用解包语法，将元组 `(3, 7)` 中的元素解包为两个独立的参数，传递给 `add_numbers` 函数。这样就避免了使用整个元组作为单一参数，确保函数的参数数量和类型正确匹配。

如何使用字典解包呢？

在 Python 中，使用 `**`（双星号）可以进行字典解包，将字典中的键值对作为关键字参数传递给一个函数。这在函数调用时特别有用，允许你通过字典的方式传递参数，而不必一个一个地列举参数名。以下是一个使用字典解包传参的简单示例：

```
# 一个简单的函数，接受两个参数并返回它们的和
def add_numbers(a, b):
    return a + b

# 一个字典，包含两个键值对
numbers_dict = {'a': 3, 'b': 7}

# 使用字典解包，将键值对作为关键字参数传递给函数
result = add_numbers(**numbers_dict)
# 上述代码相当于 add_numbers(a=3, b=7)，得到结果 10

print("Result with dictionary unpacking:", result)
```

在这个例子中，`add_numbers(**numbers_dict)` 使用字典解包语法，将字典 `{'a': 3, 'b': 7}` 中的键值对解包为两个关键字参数，传递给 `add_numbers` 函数。这样就避免了一个一个地列举参数名，使得代码更加清晰和灵活。

需要注意的是，字典中的键必须与函数的参数名匹配，否则会引发 `TypeError`。字典解包的语法可以在函数调用中方便地使用键值对，特别适用于具有多个参数的函数。

------

## 闭包

闭包（Closure）是指在某个作用域内定义的函数，它可以访问该作用域内的变量，并且在函数被返回后，仍然能够保持对这些变量的引用。换句话说，闭包是一个函数对象，它记住了在创建时存在的环境信息。

要理解闭包，首先需要了解一下嵌套函数。在一个函数内部定义了另一个函数时，内部函数就被称为嵌套函数。当内部函数引用了外部函数的变量时，就形成了一个闭包。

下面是一个简单的 Python 示例，演示了闭包的概念：

```
def outer_function(x):
    # 内部函数是嵌套在外部函数内部的
    def inner_function(y):
        return x + y
    # 返回内部函数，形成闭包
    return inner_function

# 创建一个闭包
closure_example = outer_function(10)

# 调用闭包
result = closure_example(5)
print(result)  # 输出: 15
```

在这个例子中，`outer_function` 是外部函数，它接受一个参数 `x`。在外部函数内部，定义了一个内部函数 `inner_function`，它引用了外部函数的参数 `x`。当 `outer_function` 被调用时，它返回了内部函数 `inner_function`，形成了一个闭包。

在后续的调用中，`closure_example` 就是这个闭包的引用。当我们调用 `closure_example(5)` 时，它实际上是调用了内部函数 `inner_function`，并且 `x` 的值仍然是 10，因为闭包保持了对外部环境的引用。

闭包在很多编程语言中都是一种重要的编程概念，它可以用于实现一些高级的编程模式和技术，例如函数式编程中的柯里化（Currying）等。

使用闭包的好处：

闭包在编程中具有多种作用，其中一些主要的作用包括：

1. 1.

   **封装变量：** 闭包允许将函数与其引用的环境（包括局部变量）绑定在一起。这样，函数可以访问和操作其创建时的上下文中的变量，形成了一个封闭的作用域。

2. 2.

   **保持状态：** 由于闭包可以捕获外部函数的局部变量，并在函数返回后保留对它们的引用，因此闭包可以用于在多次调用之间保持状态。这对于实现记忆化（Memoization）和缓存等场景非常有用。

3. 3.

   **实现柯里化：** 闭包可以用于实现柯里化，即将接受多个参数的函数转化为一系列接受单个参数的函数链。这可以提高函数的复用性和灵活性。

4. 4.

   **实现回调函数：** 闭包常常用于实现回调函数，将函数作为参数传递给其他函数。由于闭包能够捕获其创建时的上下文，因此可以在回调函数中使用外部作用域的变量。

5. 5.

   **模块化设计：** 通过使用闭包，可以创建具有私有状态和行为的模块化组件。这种方式有助于降低全局命名空间的污染，提高代码的封装性。

下面是一个简单的例子，演示了闭包的保持状态和封装变量的作用：

```
def counter():
    count = 0

    def increment():
        nonlocal count  # 使用 nonlocal 声明以修改外部作用域的变量
        count += 1
        return count

    return increment

# 创建一个计数器闭包
counter1 = counter()

# 每次调用闭包都会增加计数
print(counter1())  # 输出: 1
print(counter1())  # 输出: 2
print(counter1())  # 输出: 3
```

在这个例子中，`counter` 函数返回了一个闭包 `increment`，它保持了对外部作用域中 `count` 变量的引用，使得在每次调用 `counter1()` 时，`count` 的值得以保留和增加。

示例2：

注意到返回的函数在其定义内部引用了局部变量args，所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。

另一个需要注意的问题是，返回的函数并没有立刻执行，而是直到调用了f()才执行。我们来看一个例子：

```
def count():
	fs = [] 
	for i in range(1, 4):
		def f(): 
			return i*i 
		fs.append(f) 
	return fs 
f1, f2, f3 = count()
>>> f1() 
9 
>>> f2()
9 
>>> f3()
9
```

在上面的例子中，每次循环，都创建了一个新的函数，然后，把创建的3个函数都返回了。

你可能认为调用f1()，f2()和f3()结果应该是1，4，9，但实际结果是：

全部都是9！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。

 返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。

------

## **__builtins**__ 与 eval 与namespace

```python
tuple_new = tuple.__new__
_dict, _tuple, _len, _map, _zip = dict, tuple, len, map, zip
namespace = {
    '_tuple_new': tuple_new,
    '__builtins__': {},
    '__name__': f'namedtuple_{typename}',
}
code = f'lambda _cls, {arg_list}: _tuple_new(_cls, ({arg_list}))'
__new__ = eval(code, namespace)
__new__.__name__ = '__new__'
__new__.__doc__ = f'Create new instance of {typename}({arg_list})'
```

这段代码看起来是在动态生成一个 `__new__` 函数，该函数被用于创建一个新的实例。这个实例似乎是一个命名元组（namedtuple），其类型是通过 `typename` 和 `arg_list` 动态生成的。

具体来说，代码做了以下事情：

1. 1.

   定义了一个名为 `namespace` 的字典，包含了三个键值对：

   - •

     `_tuple_new`: 对象 `tuple_new` 的引用（在代码中并未提供 `tuple_new` 的定义）。

   - •

     `__builtins__`: 一个空字典，用于限制 `eval` 中对内置命名空间的访问。

   - •

     `__name__`: 一个字符串，其值是以 `'namedtuple_'` 为前缀，后接 `typename` 的结果。

2. 2.

   构建了一个字符串 `code`，其中包含了一个 `lambda` 表达式的定义。这个表达式接受 `_cls` 和其他参数，并调用 `_tuple_new` 函数来创建一个新的元组。

3. 3.

   使用 `eval` 函数执行了字符串 `code`，将其转换为一个可调用对象（函数），并将其赋值给变量 `__new__`。

4. 4.

   修改了 `__new__` 函数的属性，包括将其名称设为 `'__new__'` 和添加文档字符串。

需要注意的是，代码中涉及到的 `tuple_new` 对象并没有在提供的代码中定义。这个对象可能是在其他部分的代码中定义的，或者是通过某种方式动态生成的。

整体而言，这段代码看起来是为了创建一个用于生成命名元组实例的 `__new__` 函数，并通过一些动态生成的命名空间和字符串来实现。

_builtins__是干嘛的?

在 Python 中，`__builtins__` 是一个模块，包含了 Python 解释器中内置的所有函数、异常和对象。这个模块在 Python 解释器启动时自动导入，允许用户直接访问内置的函数和对象。

`__builtins__` 模块是一个字典，包含了 Python 内置的全局命名空间。通过它，你可以直接访问内置的函数和对象，而不需要显式导入。例如，你可以直接使用 `len()`、`range()`、`int()` 等函数，而无需导入任何模块。

在上述提到的代码中，将 `__builtins__` 设置为一个空字典的目的可能是为了限制 `eval` 函数在字符串 `code` 的执行中对内置命名空间的访问。通过将 `__builtins__` 设置为空字典，可以防止在 `eval` 中执行的代码访问和修改内置的函数或对象，从而提高安全性。

例如，如果在 `eval` 中可以访问 `__builtins__`，那么可能允许执行一些危险的操作，例如修改内置的函数行为，这可能导致安全风险。在某些情况下，限制对 `__builtins__` 的访问可以帮助防止一些潜在的安全问题。

eval的namespace有什么用

在 `eval` 函数中，`namespace` 参数用于指定执行字符串时的命名空间（namespace）。这个参数是一个字典，它包含了在执行字符串时可用的全局和局部变量。

在Python中，`eval` 函数允许你执行包含 Python 表达式的字符串。通过提供 `namespace` 参数，你可以控制在执行字符串时所使用的变量。这样，你可以在执行期间指定哪些变量是全局可见的，哪些是局部的。

举例说明：

```python
# 定义一个全局变量
global_var = 10

# 定义一个包含表达式的字符串
expression = "x + global_var"

# 定义一个包含变量 x 的命名空间
namespace = {"x": 5}

# 使用 eval 执行表达式，通过 namespace 传递变量
result = eval(expression, namespace)

print(result)  # 输出: 15
```

在上述例子中，通过在 `namespace` 中定义变量 `x`，我们可以在执行字符串表达式时将其传递给 `eval` 函数，从而影响执行结果。`global_var` 是一个全局变量，也可在 `eval` 中访问。

在你提供的代码示例中，`namespace` 被用于限制 `eval` 中对内置命名空间的访问，通过设置 `__builtins__` 为一个空字典，防止执行的字符串能够直接访问和修改内置的函数或对象。这是一种提高代码安全性的做法，防止 `eval` 中的代码执行可能的危险操作。

他是怎么做到 通过设置 `__builtins__` 为一个空字典，防止执行的字符串能够直接访问和修改内置的函数或对象的？

在 Python 中，`__builtins__` 是一个包含内置命名的模块。通过在 `eval` 函数中设置 `__builtins__` 为一个空字典，可以限制执行的字符串对内置命名空间的直接访问。

这样做的原理是，在执行字符串时，`eval` 函数首先在提供的 `namespace` 中查找变量，然后才在全局命名空间中查找。如果 `__builtins__` 被设置为一个空字典，那么在字符串中不能直接访问内置的函数和对象，因为它们在 `__builtins__` 中。

例如，考虑下面的示例：

```
# 定义一个包含表达式的字符串
expression = "__builtins__.print('Hello, world!')"

# 定义一个包含变量 x 的命名空间
namespace = {"x": 5, "__builtins__": {}}

# 使用 eval 执行字符串表达式，通过 namespace 传递变量
result = eval(expression, namespace)
```

在这个示例中，尽管字符串中包含了 `__builtins__.print`，但由于 `__builtins__` 在 `namespace` 中被设置为空字典，所以在执行期间无法直接访问内置的 `print` 函数，从而避免了直接对内置函数的访问。

这种做法主要用于增加对 `eval` 执行的代码的控制，以防止可能的安全问题。然而，需要注意的是，对 `eval` 的使用本身就需要非常小心，因为它可能导致代码注入和其他潜在的安全风险。在实际应用中，通常应该避免直接使用 `eval`，除非绝对有必要，而且能够确保输入是安全的。

------

## 反射

### **反射是什么？**

反射的概念是由 Smith 在 1982 年首次提出的，主要是指程序可以访问、检测和修改它本身状态或行为的一种能力。通俗地讲，一提到反射，我们就可以想到镜子。镜子可以明明白白地照出我是谁，还可以照出别人是谁。反映到程序中，反射就是用来让开发者知道这个类中有什么成员，以及别的类中有什么成员。

### **为什么要有反射**

有的同学可能会疑惑，Java 已经有了封装为什么还要有反射呢？反射看起来像是破坏了封装性。甚至让私有变量都可以被外部访问到，使得类变得不那么安全了。我们来看一下 Oracle 官方文档中对反射的描述：

从 Oracle 官方文档中可以看出，反射主要应用在以下几方面：

- •

  反射让开发人员可以通过外部类的全路径名创建对象，并使用这些类，实现一些扩展的功能。

- •

  反射让开发人员可以枚举出类的全部成员，包括构造函数、属性、方法。以帮助开发者写出正确的代码。

- •

  测试时可以利用反射 API 访问类的私有成员，以保证测试代码覆盖率。

也就是说，Oracle 希望开发者将反射作为一个工具，用来帮助程序员实现本不可能实现的功能（perform operations which would otherwise be impossible）。正如《人月神话》一书中所言：软件工程没有银弹。很多程序架构，尤其是三方框架，无法保证自己的封装是完美的。如果没有反射，对于外部类的私有成员，我们将一筹莫展，所以我们有了反射这一后门，为程序设计提供了更大的灵活性。工具本身并没有错，关键在于如何正确地使用。

### FromGPT

反射（Reflection）是指在运行时（runtime）能够获取、检测和使用类（class）、对象（object）、接口（interface）等信息的一种机制。在反射中，程序可以动态地获取类的信息、调用方法、操作属性等，而不需要在编译时就确定这些信息。

反射通常包括以下几个方面的功能：

1. 1.

   **获取类的信息：** 可以获取类的名称、方法、属性等相关信息。

2. 2.

   **创建对象：** 可以在运行时创建类的实例。

3. 3.

   **调用方法：** 可以在运行时通过方法名调用类的方法。

4. 4.

   **操作属性：** 可以在运行时获取和设置类的属性值。

在许多面向对象的编程语言中，反射是一种强大而灵活的特性，它允许程序在运行时根据需要进行动态的操作。在 Python 中，反射机制由一些内置函数和模块提供，例如 `getattr()`、`setattr()`、`hasattr()`、`type()` 等。

下面是一个简单的 Python 反射的示例：

```
class MyClass:
    def __init__(self, x):
        self.x = x

    def display(self):
        print(f"Value of x: {self.x}")

# 创建对象
obj = MyClass(42)

# 获取类的信息
class_name = obj.__class__.__name__
print(f"Class name: {class_name}")

# 调用方法
if hasattr(obj, 'display'):
    method = getattr(obj, 'display')
    method()  # 输出：Value of x: 42

# 操作属性
if hasattr(obj, 'x'):
    print(f"Value of x: {getattr(obj, 'x')}")  # 输出：Value of x: 42
```

上述示例演示了如何通过反射获取类的信息、调用方法以及操作属性。反射在一些动态性较高的场景中非常有用，但过度使用反射也可能导致代码的可读性和维护性降低，因此需要根据具体情况权衡使用。

------

## 枚举

在 Python 中，枚举通过继承 `Enum` 类来实现。继承 `Enum` 类的好处在于它提供了一些有用的功能，使得枚举更加强大和灵活。以下是继承 `Enum` 类的一些好处：

1. 1.

   **唯一性：** 继承 `Enum` 类确保枚举中的每个常量都是唯一的，即每个常量都具有唯一的名称和值。这消除了可能出现重复常量的问题。

2. 2.

   **可迭代性：** 通过继承 `Enum` 类，枚举类型变得可迭代。这使得在循环中遍历枚举中的常量变得非常方便。

3. 3.

   **支持成员访问：** 继承 `Enum` 类后，枚举类型的常量可以通过名称或值进行访问，例如 `Color.RED` 或 `Color(1)`。

4. 4.

   **自动编号：** 使用 `auto()` 函数作为常量值，可以使枚举类型自动为每个常量分配唯一的值。这简化了枚举的定义过程。

5. 5.

   **字符串表示：** 继承 `Enum` 类的枚举类型具有默认的字符串表示形式，即 `EnumClassName.EnumMember`。这对于调试和输出信息很有帮助。

下面是一个简单的例子，演示了使用 `Enum` 类的好处：

```
from enum import Enum, auto

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

# 唯一性
print(Color.RED is Color.RED)  # 输出: True

# 可迭代性
for color in Color:
    print(color)
# 输出:
# Color.RED
# Color.GREEN
# Color.BLUE

# 支持成员访问
print(Color.RED)        # 输出: Color.RED
print(Color['RED'])     # 输出: Color.RED
print(Color(1))          # 输出: Color.GREEN

# 自动编号
print(Color.RED.value)   # 输出: 1
print(Color.GREEN.value) # 输出: 2
print(Color.BLUE.value)  # 输出: 3

# 字符串表示
print(repr(Color.RED))   # 输出: <Color.RED: 1>
```

通过继承 `Enum` 类，枚举类型变得更加强大和易于使用。这些功能使得枚举在代码中更加清晰、可读，同时也提供了一些方便的操作和查询方法。

------

##   _与__开头的变量

在Python中，有以下几种方式来定义变量：

- •

  xx：公有变量

- •

  _xx：前置单下划线，私有化属性或方法，一般来讲，变量名_xx被看作是“私有 的”，在模块或类外不可以使用。当变量是私有的时候，用_xx 来表示变量是很好的习惯。类对象和子类可以访问,这并不能完全做到真正的私有，只是约定俗成的而已，这样写表示不希望这个变量在外部被直接调用，实际上可以访问

- •

  __xx：前置双下划线，私有化属性或方法，无法在外部直接访问（名字重整所以访问不到,只能是允许这个类本身进行访问了。连子类也不可以）

- •

  __xx__：前后双下划线，系统定义名字（这就是在python中强大的魔法方法），因为变量名__xxx__对Python 来说有特殊含义，对于普通的变量应当避免这种命名风格。

- •

  xx_：后置单下划线，用于避免与Python关键词的冲突

  - •

    如以下例子所示，我在test类中定义了x，_x和 __x三个属性，并创建了test的类对象t，对这三个属性进行访问，__x不能被访问到

    ```
    class test(object):
     def __init__(self):
     	self.x = 10
     	self._x = 20
     	self.__x = 30
    t = test()
    print(t.x) # 10
    print(t._x) # 20
    # print(t.__x) # AttributeError: 'test' object has no attribute '__x'
    ```

    

    可以使用命令dir查看t中的属性和方法，__x的名字已经被重整为“_test__x”了，如果你非要通过外部访问，也是可以的，可以使用t._test__x对__x进行访问。
    python中没有真正的公有和私有变量，python只是对变量名称做了一个变化，还是可以在外部访问到的，是伪私有。

示例

```
class ParentC(object):
    sal = 3000
    _age = '18'
    __name = 'jack'

    def __init__(self):
        self.sal = 1000
        self._age = '88'
        self.__name = 'father'


class Child(ParentC):
    # def __init__(self):
    #     self.sal = 10000
    #     self._age = 100

    def get_father_name(self):
        print(self._ParentC__name)   # 通过父类名来访问


ch = Child()
# ch.get_father_name()
# print(ch.__name) # 无法访问
print(ch._ParentC__name)  # 可以访问
print(ch.sal)      # 子类对象优先在子类中找sal，其次在父类的实例对象找，最后在父类的类对象找
print(ch._age)

print(ParentC.sal)
print(ParentC._age)
# print(ParentC.__name)  # 无法访问，只能在类内部使用
print(ParentC._ParentC__name)  # 通过这种方式访问

pc = ParentC()
print(pc.sal)
print(pc._age)
# print(pc.__name)  # 无法访问
print(pc._ParentC__name)
```

### 单下划线（_）的使用

#### 1.命名约定

在Python中，单下划线作为命名约定，用于表示某个变量、方法或属性是内部使用的或具有特定含义，但不希望在外部直接访问。

代码示例：

```
class MyClass:
	def init (self):
		self._internal_var = 42
	def _internal_method(self):
		return "Internal method'
	def public_method(self):
		return self._internal_method()
```

在上面的例子中，变量_internal_var和方法_internal_method都以单下划线开头。这是一种约定，告诉其他开发人员这些成员是类内部使用的，不建议在类外部直接访问。公共方法public_method可以访问内部方法_internal_method。

#### 2.避免命名冲突

单下划线还可以用于避免命名冲突。当我们在导入模块时，可以使用单下划线作为前缀，以避免与当前命名空间中的其他标识符冲突。

代码示例：

```
from mymodule import my_function, _internal_function
```

在上面的例子中，通过使用单下划线前缀导入_internal_function函数，我们可以明确指定该函数是模块的内部使用，而不是公共接口。

#### 3.临时变量

在一些情况下，我们可能只需要临时使用某个变量，而不关心它的具体值。此时，可以使用单下划线作为变量名，表示它是一个无关紧要的临时变量。

代码示例：

```
for _ in range(3):
	print("hello world")
```

在上面的例子中，循环变量被命名为单下划线，这告诉其他开发人员循环变量的具体值并不重要，只需要执行循环体内的代码5次即可。

#### 4.引入未使用的变量

有时候，在编码过程中我们可能会定义一些变量，但在后续的代码中并没有使用它们。为了避免出现未使用变量的警告，可以使用单下划线作为变量名。

代码示例：

```
_, y, _ = (1, 2, 3)
```

在上面的例子中，我们使用单下划线占位符引入了一个未使用的变量。这样做可以告诉读者，我们在意识到该变量存在但并不关心它的具体值。