# 面向对象设计原则

SOLID 是面向对象设计中的五个基本设计原则，这些原则旨在创建可维护、灵活和可扩展的软件系统。SOLID 是由罗伯特·马丁（Robert C. Martin）等人提出的一组设计原则的首字母缩写。

这五个原则分别是：



1. **单一职责原则（Single Responsibility Principle，SRP）：**

   - •一个类应该只有一个引起变化的原因。换句话说，一个类应该只有一个职责。这个原则强调类的职责应该保持单一，以提高代码的可维护性和复用性。

2. **开闭原则（Open/Closed Principle，OCP）：**

   - •软件实体（类、模块、函数等）应该对扩展是开放的，对修改是封闭的。这意味着系统的行为可以通过添加新的代码进行扩展，而不必修改现有代码。这鼓励使用抽象和接口来构建可扩展的系统。

3. **里氏替换原则（Liskov Substitution Principle，LSP）：**

   - •子类型必须能够替换它们的基类型，而不影响程序的正确性。子类应该保持对基类的兼容性，这是实现多态性的基础。
   - •可以接受父类对象必然要可以接受其子类对象，子类的方法要与父类保持一致

4. **接口隔离原则（Interface Segregation Principle，ISP）：**

   - •不应该强迫客户端依赖于它们不使用的接口。一个类不应该被迫实现它不使用的接口。这个原则鼓励创建精简的接口，避免过大而臃肿的接口。

5. **依赖反转原则（Dependency Inversion Principle，DIP）：**

   高层模块不应该依赖于底层模块，两者都应该依赖于抽象。抽象不应该依赖于具体实现，具体实现应该依赖于抽象。这个原则强调使用抽象和接口来减少模块之间的直接依赖，从而提高系统的灵活性和可维护性。

这些原则一起构成了一种设计思想，帮助开发者创建更加健壮、可扩展和可维护的面向对象软件系统。

---

# 设计模式分类

设计模式是软件设计中常见问题的通用解决方案，它们提供了在特定情境下解决问题的模板。设计模式可分为三大类：创建型模式、结构型模式和行为型模式。

1. 1.

   **创建型模式（Creational Patterns）：**

   - •

     这些模式关`注对象的创建机制，以确保系统可以灵活、高效地创建新`对象。创建型模式包括：

     - •

       单例模式（Singleton Pattern）

     - •

       工厂方法模式（Factory Method Pattern）

     - •

       抽象工厂模式（Abstract Factory Pattern）

     - •

       建造者模式（Builder Pattern）

     - •

       原型模式（Prototype Pattern）

2. 2.

   **结构型模式（Structural Patterns）：**

   - •

     结构型模式关注对象组合形成更大结构，以简化系统的设计。结构型模式包括：

     - •

       适配器模式（Adapter Pattern）

     - •

       装饰器模式（Decorator Pattern）

     - •

       代理模式（Proxy Pattern）

     - •

       外观模式（Facade Pattern）

     - •

       桥接模式（Bridge Pattern）

     - •

       组合模式（Composite Pattern）

     - •

       享元模式（Flyweight Pattern）

3. 3.

   **行为型模式（Behavioral Patterns）：**

   - •

     行为型模式关注对象之间的通信和职责分配。行为型模式包括：

     - •

       策略模式（Strategy Pattern）

     - •

       观察者模式（Observer Pattern）

     - •

       命令模式（Command Pattern）

     - •

       迭代器模式（Iterator Pattern）

     - •

       职责链模式（Chain of Responsibility Pattern）

     - •

       备忘录模式（Memento Pattern）

     - •

       状态模式（State Pattern）

     - •

       访问者模式（Visitor Pattern）

     - •

       模板方法模式（Template Method Pattern）

     - •

       解释器模式（Interpreter Pattern）

每种设计模式都有其特定的用途和场景，开发者在设计软件时可以根据问题的性质选择合适的设计模式，以提高代码的可重用性、可维护性和扩展性。设计模式并非一成不变的规定，而是一种经验丰富的开发者们在解决类似问题时总结出的最佳实践。

---

# 简单工厂模式

简单工厂模式（Simple Factory Pattern）是一种创建型设计模式，它提供了一种通过一个共同的接口来创建对象的方式，而无需暴露对象的创建逻辑。简单工厂模式包含一个工厂类，该类负责根据客户端的需求创建相应的对象。

简单工厂模式通常包含以下几个角色：

1. 1.

   **工厂类（Factory）：** 负责创建对象的类，提供一个静态方法或类方法用于根据客户端的需求创建不同类型的对象。

2. 2.

   **产品接口（Product Interface）：** 定义了被创建对象的接口，客户端通过该接口与具体产品进行交互。

3. 3.

   **具体产品类（Concrete Products）：** 实现了产品接口，是被工厂创建的对象。

下面是一个简单的例子，演示了简单工厂模式的基本结构：

```
from abc import ABCMeta, abstractmethod

# 产品接口
class Product(metaclass=ABCMeta):
	@abstractmethod
    def operation(self):
        pass

# 具体产品类A
class ConcreteProductA(Product):
    def operation(self):
        return "Operation from Product A"

# 具体产品类B
class ConcreteProductB(Product):
    def operation(self):
        return "Operation from Product B"

# 工厂类
class SimpleFactory:
    @staticmethod
    def create_product(product_type):
        if product_type == "A":
            return ConcreteProductA()
        elif product_type == "B":
            return ConcreteProductB()
        else:
            raise ValueError("Invalid product type")

# 客户端代码
def client_code(factory, product_type):
    product = factory.create_product(product_type)
    result = product.operation()
    print(result)

# 使用工厂创建不同类型的产品
factory = SimpleFactory()
client_code(factory, "A")  # 输出: Operation from Product A
client_code(factory, "B")  # 输出: Operation from Product B
```

在这个例子中，`SimpleFactory` 类负责根据客户端的需求创建不同类型的产品（ConcreteProductA 和 ConcreteProductB）。客户端通过调用工厂的方法来获取所需的产品，而无需直接实例化具体产品类。这种方式使得客户端与具体产品的创建过程解耦，同时提供了一种简单的方式来创建对象。

### 示例2

```
from abc import ABCMeta, abstractmethod


class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money) -> None:
        pass


class AlibabaPay(Payment):
    def __init__(self, huabei=''):
        self.huabei = huabei

    def pay(self, money) -> None:
        if self.huabei:
            print('花呗支付%d' % money)
        else:
            print('支付宝支付%d' % money)


class WeixinPay(Payment):
    def pay(self, money) -> None:
        print('微信支付%d' % money)


class PayFactory:
    def create_payment(self, payment_type):
        if payment_type == 'weixin':
            return WeixinPay()
        elif payment_type == 'alibaba':
            return AlibabaPay()
        elif payment_type == 'huabei':
            return AlibabaPay('huabei')
        else:
            raise TypeError('no such payment class')


pay_factory = PayFactory()
p = pay_factory.create_payment('huabei')
p = pay_factory.create_payment('weixin')
p.pay(100)
```

### 简单工厂模式具有一些优点，特别适用于一些简单的场景和对象的创建过程相对固定的情况：

1. 1.

   **封装对象创建过程：** 简单工厂模式封装了对象的创建过程，客户端不需要了解对象的创建细节，只需通过工厂类请求所需的对象即可。

2. 2.

   **减少耦合：** 客户端代码与具体产品类的实例化过程解耦，不直接依赖具体产品类，降低了客户端与产品类之间的耦合度。

3. 3.

   **集中控制：** 由工厂类集中控制和管理对象的创建，可以对对象的创建逻辑进行集中管理和修改，便于维护和扩展。

4. 4.

   **简化客户端代码：** 客户端只需关注请求工厂类创建对象的接口，而无需关心具体对象的实例化细节，使客户端代码更加简洁。

5. 5.

   **适用于简单场景：** 当对象的创建逻辑相对简单，且不需要频繁变更时，简单工厂模式是一个简单而有效的选择。

需要注意的是，简单工厂模式并不是适用于所有情况的通用解决方案。它有一些局限性，例如当具体产品类的种类非常多或者产品创建逻辑非常复杂时，可能会导致工厂类变得臃肿。在这种情况下，其他创建型模式如工厂方法模式或抽象工厂模式可能更加合适。选择适当的设计模式取决于具体问题的复杂性和需求。

---

# 工厂模式

工厂模式是一种创建型设计模式，它提供了一种创建对象的接口，但允许子类决定实例化哪个类。工厂模式使得一个类的实例化延迟到其子类。

工厂模式的主要目标是封装对象的创建过程，使客户端代码与具体类的实例化过程解耦。通过引入一个抽象的工厂接口和多个实现该接口的具体工厂类，客户端代码可以通过工厂接口请求对象的创建，而无需关心实际创建的具体类。

工厂模式通常包括以下几个角色：

1. 1.

   **抽象产品接口（Product Interface）：** 定义了产品的通用接口，客户端通过这个接口与产品进行交互。

2. 2.

   **具体产品类（Concrete Products）：** 实现了抽象产品接口的具体类。

3. 3.

   **抽象工厂接口（Factory Interface）：** 定义了创建产品的方法，客户端通过这个接口请求创建产品。

4. 4.

   **具体工厂类（Concrete Factories）：** 实现了抽象工厂接口，负责具体产品的创建。

工厂模式主要分为两种类型：

- •

  **工厂方法模式（Factory Method Pattern）：** 定义一个用于创建对象的接口，但由子类决定实例化哪个类。工厂方法使得一个类的实例化延迟到其子类。

- •

  **抽象工厂模式（Abstract Factory Pattern）：** 提供一个接口，用于创建一系列相关或依赖对象的家族，而不需要指定具体类。抽象工厂模式使用多个工厂接口，每个接口对应一个产品家族。

下面是一个简单的工厂方法模式的示例：

```
from abc import ABCMeta, abstractmethod


# 抽象产品接口
class Product(metaclass=ABCMeta):
	@abstractmethod
    def operation(self):
        pass

# 具体产品类A
class ConcreteProductA(Product):
    def operation(self):
        return "Operation from Product A"

# 具体产品类B
class ConcreteProductB(Product):
    def operation(self):
        return "Operation from Product B"

# 抽象工厂接口
class Factory(metaclass=ABCMeta):
	@abstractmethod
    def create_product(self):
        pass

# 具体工厂类A
class ConcreteFactoryA(Factory):
    def create_product(self):
        return ConcreteProductA()

# 具体工厂类B
class ConcreteFactoryB(Factory):
    def create_product(self):
        return ConcreteProductB()

# 客户端代码
def client_code(factory):
    product = factory.create_product()
    result = product.operation()
    print(result)

# 使用具体工厂创建具体产品
factory_A = ConcreteFactoryA()
client_code(factory_A)  # 输出: Operation from Product A

factory_B = ConcreteFactoryB()
client_code(factory_B)  # 输出: Operation from Product B
```

在上述例子中，`Factory` 是抽象工厂接口，`ConcreteFactoryA` 和 `ConcreteFactoryB` 是具体工厂类，分别创建 `ConcreteProductA` 和 `ConcreteProductB` 两个具体产品。客户端通过工厂接口请求创建产品，而不直接与具体产品类交互，从而实现了解耦。

针对每一个具体的产品类都要有对应的工厂类，实现单一原则与开闭原则（只做insert，不做update）

### 工厂模式的实际应用场景：

**场景：创建不同类型的数据库连接对象**

假设有一个应用程序需要与不同类型的数据库进行交互，包括 MySQL、PostgreSQL 和 MongoDB。在这种情况下，工厂模式可以被用来创建不同类型的数据库连接对象。

```
# 工厂接口
class DatabaseConnectionFactory:
    def create_connection(self):
        pass

# 具体工厂类
class MySqlConnectionFactory(DatabaseConnectionFactory):
    def create_connection(self):
        return MySqlConnection()

class PostgreSqlConnectionFactory(DatabaseConnectionFactory):
    def create_connection(self):
        return PostgreSqlConnection()

class MongoDBConnectionFactory(DatabaseConnectionFactory):
    def create_connection(self):
        return MongoDBConnection()

# 产品接口
class DatabaseConnection:
    def connect(self):
        pass

# 具体产品类
class MySqlConnection(DatabaseConnection):
    def connect(self):
        print("Connected to MySQL database")

class PostgreSqlConnection(DatabaseConnection):
    def connect(self):
        print("Connected to PostgreSQL database")

class MongoDBConnection(DatabaseConnection):
    def connect(self):
        print("Connected to MongoDB database")

# 客户端代码
def use_database_connection(factory):
    connection = factory.create_connection()
    connection.connect()

# 使用工厂模式
mysql_factory = MySqlConnectionFactory()
postgre_factory = PostgreSqlConnectionFactory()
mongo_factory = MongoDBConnectionFactory()

use_database_connection(mysql_factory)  # 输出：Connected to MySQL database
use_database_connection(postgre_factory)  # 输出：Connected to PostgreSQL database
use_database_connection(mongo_factory)  # 输出：Connected to MongoD
```

------

# 抽象工厂

抽象工厂是一种设计模式，属于创建型模式之一。它提供了一种将一组相关或相互依赖的对象创建操作封装到一个工厂接口中的方式，而不是直接指定它们的具体类。抽象工厂模式的目标是提供一个接口，用于创建一系列相关或相互依赖的对象，而无需指定它们的具体类。

关键特点和组成部分：

1. 1.

   **抽象工厂接口（Abstract Factory）：** 定义了创建一组相关对象的方法，但不指定具体类别。

2. 2.

   **具体工厂类（Concrete Factory）：** 实现了抽象工厂接口，负责创建一组相关对象的具体实例。

3. 3.

   **抽象产品接口（Abstract Product）：** 定义了一类产品的创建方法。

4. 4.

   **具体产品类（Concrete Product）：** 实现了抽象产品接口，是具体工厂创建的对象。

抽象工厂模式的优势在于它使得客户端代码与具体类的实现解耦。客户端通过抽象工厂接口创建产品，而不需要关心具体产品的实现。这使得在系统中更容易替换一组相关对象而不影响客户端代码。

一个简单的抽象工厂模式的例子可以是 GUI 工具包的设计。假设有一个抽象工厂接口 `GUIFactory`，定义了创建按钮和窗口的方法。具体工厂类 `WinFactory` 和 `MacFactory` 实现了这个接口，并分别用于创建 Windows 风格和 Mac 风格的按钮和窗口。抽象产品接口可以是 `Button` 和 `Window`，而具体产品类则为 `WinButton`、`MacButton`、`WinWindow`、`MacWindow` 等。

示例代码（简化）：

```
from abc import ABCMeta, abstractmethod


# 产品接口A
class Shell(metaclass=ABCMeta):
    @abstractmethod
    def show_shell(self):
        pass


# 产品接口B
class Cpu(metaclass=ABCMeta):
    @abstractmethod
    def show_cpu(self):
        pass


# 产品接口C
class Os(metaclass=ABCMeta):
    @abstractmethod
    def show_os(self):
        pass


# 具体产品A1
class BigShell(Shell):
    def show_shell(self):
        print('大手机壳')


# 具体产品A2
class SmallShell(Shell):
    def show_shell(self):
        print('小手机壳')


# 具体产品B1
class ArmCpu(Cpu):
    def show_cpu(self):
        print('Arm cpu')


# 具体产品B2
class X86Cpu(Cpu):
    def show_cpu(self):
        print('X86 Cpu')


# 具体产品C1
class IosOs(Os):
    def show_os(self):
        print('IosOs os')


# 具体产品C2
class AndroidOs(Os):
    def show_os(self):
        print('Android os')


# 抽象工厂(创建一系列相关，相依赖的对象)
class PhoneFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_shell(self):
        pass

    @abstractmethod
    def create_os(self):
        pass

    @abstractmethod
    def create_cpu(self):
        pass


# 具体工厂A
class WindowsPhoneFactory(PhoneFactory):
    def create_shell(self):
        return BigShell()

    def create_os(self):
        return AndroidOs()

    def create_cpu(self):
        return X86Cpu()


class ApplePhoneFactory(PhoneFactory):
    def create_shell(self):
        return SmallShell()

    def create_os(self):
        return IosOs()

    def create_cpu(self):
        return ArmCpu()


def client_code(factory):
    shell = factory.create_shell()
    os = factory.create_os()
    cpu = factory.create_cpu()
    shell.show_shell()
    os.show_os()
    cpu.show_cpu()
    # return factory.create_shell()


iphone = ApplePhoneFactory()
client_code(iphone)

win_phone = WindowsPhoneFactory()
client_code(win_phone)
```

这段代码是一个实现了抽象工厂模式的例子。抽象工厂模式的目的是提供一个接口，用于创建一系列相关或相互依赖的对象，而无需指定它们的具体类。在这个例子中，通过抽象工厂模式创建了手机的一组相关组件，如手机壳（`Shell`）、CPU（`Cpu`）和操作系统（`Os`）。

主要组成部分：

1. 1.

   **产品接口：** 定义了一组产品接口，包括手机壳（`Shell`）、CPU（`Cpu`）和操作系统（`Os`）。

2. 2.

   **具体产品类：** 实现了产品接口的具体产品类，例如大手机壳（`BigShell`）、小手机壳（`SmallShell`）、Arm CPU（`ArmCpu`）、X86 CPU（`X86Cpu`）、iOS OS（`IosOs`）和 Android OS（`AndroidOs`）。

3. 3.

   **抽象工厂：** 定义了一个抽象工厂接口（`PhoneFactory`），包括创建手机壳、CPU 和操作系统的方法。

4. 4.

   **具体工厂：** 实现了抽象工厂接口的具体工厂类，包括 `WindowsPhoneFactory` 和 `ApplePhoneFactory`，分别用于创建 Windows Phone 和 Apple Phone 相关的产品。

5. 5.

   **客户端代码：** 使用工厂创建一组相关的产品，并调用其方法展示。

在客户端代码中，通过创建不同的具体工厂对象（`WindowsPhoneFactory` 和 `ApplePhoneFactory`），可以得到不同手机系列的产品组合。这个例子中展示了创建了一个 Apple Phone 和一个 Windows Phone，分别包括了不同的手机壳、CPU 和操作系统。

------

# 建造者模式

建造者模式是一种创建型设计模式，旨在通过将构建复杂对象的过程拆分为多个简单的步骤，以便于更灵活、更清晰地构建复杂对象。该模式允许客户端代码指定要构建的对象类型和构建步骤，同时隐藏了实际构建的细节。

关键组成部分：

1. 1.

   **产品（Product）：** 被构建的复杂对象。它通常包含多个组成部分，这些部分的构建过程由具体的建造者负责。

2. 2.

   **抽象建造者（Builder）：** 定义了构建产品的抽象接口，包括构建产品的各个部分的方法。具体的建造者类将实现这个接口以构建具体的产品。

3. 3.

   **具体建造者（Concrete Builder）：** 实现了抽象建造者接口，负责实际构建产品的各个部分。具体建造者通常包含一个持有产品的实例，以便逐步构建它。

4. 4.

   **指挥者（Director）：** 负责调用具体建造者的方法来构建产品。指挥者知道构建的步骤和顺序，但不知道具体的产品。

5. 5.

   **客户端（Client）：** 使用建造者模式的客户端，通过指挥者构建复杂对象。

建造者模式的主要优势在于它能够构建不同类型的产品，而且客户端代码可以指定构建的过程，从而得到不同的表示。这种模式特别适用于构建复杂对象，其中对象的构建过程较为稳定，但不同的构建步骤可能导致不同的表示。

以下是一个简化的 Python 示例：

```
# 产品类
class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None

    def display_info(self):
        print(f"CPU: {self.cpu}, Memory: {self.memory}, Storage: {self.storage}")

# 抽象建造者接口
class ComputerBuilder:
    def build_cpu(self):
        pass

    def build_memory(self):
        pass

    def build_storage(self):
        pass

    def get_computer(self):
        pass

# 具体建造者
class CheapComputerBuilder(ComputerBuilder):
    def __init__(self):
        self.computer = Computer()

    def build_cpu(self):
        self.computer.cpu = "Intel Core i3"

    def build_memory(self):
        self.computer.memory = "4GB DDR3"

    def build_storage(self):
        self.computer.storage = "500GB HDD"

    def get_computer(self):
        return self.computer

# 具体建造者
class HighEndComputerBuilder(ComputerBuilder):
    def __init__(self):
        self.computer = Computer()

    def build_cpu(self):
        self.computer.cpu = "Intel Core i7"

    def build_memory(self):
        self.computer.memory = "16GB DDR4"

    def build_storage(self):
        self.computer.storage = "1TB SSD"

    def get_computer(self):
        return self.computer

# 指挥者
class Director:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.build_cpu()
        self.builder.build_memory()
        self.builder.build_storage()

# 客户端
cheap_computer_builder = CheapComputerBuilder()
director = Director(cheap_computer_builder)
director.construct()
cheap_computer = cheap_computer_builder.get_computer()
cheap_computer.display_info()

high_end_computer_builder = HighEndComputerBuilder()
director = Director(high_end_computer_builder)
director.construct()
high_end_computer = high_end_computer_builder.get_computer()
high_end_computer.display_info()
```

在这个示例中，`Computer` 是产品类，`ComputerBuilder` 是抽象建造者接口，`CheapComputerBuilder` 和 `HighEndComputerBuilder` 是具体建造者，`Director` 是指挥者，而客户端则通过指挥者构建具体产品。

------

# 单例模式

单例模式是一种设计模式，其主要目的是确保一个类只有一个实例，并提供一个全局访问点供程序使用。这种模式通常用于控制对资源的访问，例如数据库连接、文件管理器或配置对象等。单例模式的实现方式有多种，其中最常见的是懒汉式和饿汉式。

### 懒汉式单例模式：

懒汉式是指在第一次使用时才创建对象实例。

```
class Singleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# 使用示例
obj1 = Singleton()
obj2 = Singleton()

print(obj1 is obj2)  # 输出: True
```

### 饿汉式单例模式：

饿汉式是指在类加载时就创建对象实例。

```
class Singleton:
    _instance = Singleton()

    def __new__(cls):
        return cls._instance

# 使用示例
obj1 = Singleton()
obj2 = Singleton()

print(obj1 is obj2)  # 输出: True
```

### 运用场景：

1. 1.

   **数据库连接池：** 在需要频繁访问数据库的场景中，使用单例模式可以确保只有一个数据库连接池实例，节省资源并提高性能。

2. 2.

   **日志对象：** 在记录日志的应用中，使用单例模式可以确保只有一个日志对象，方便集中管理和控制日志输出。

3. 3.

   **配置管理器：** 在需要管理应用程序配置的场景中，使用单例模式可以确保只有一个配置管理器对象，方便统一管理配置信息。

4. 4.

   **线程池：** 在需要使用线程池的场景中，使用单例模式可以确保只有一个线程池实例，提高线程池的复用性。

5. 5.

   **GUI应用程序中的窗口管理器：** 在GUI应用程序中，使用单例模式可以确保只有一个窗口管理器实例，方便统一管理和控制窗口的打开和关闭。

需要注意的是，在多线程环境中，单例模式的实现需要考虑线程安全性，可以使用加锁等方式来保证单例对象的创建是线程安全的。

###  单例跟简单工厂的结合

```
class Fruit(object):
    def __init__(self):
        pass

    def print_color(self):
        pass

class Apple(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("apple is in red")

class Orange(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("orange is in orange")


class FruitFactory(object):
    fruits = {"apple": Apple, "orange": Orange}

    def __new__(cls, name):
        if name in cls.fruits.keys():
            return cls.fruits[name]()
        else:
            return Fruit()


fruit1 = FruitFactory("apple")
fruit2 = FruitFactory("orange")
fruit1.print_color()
fruit2.print_color()
```

------

# 适配器模式

适配器模式（Adapter Pattern）是一种结构型设计模式，它允许将一个类的接口转换成客户端期望的另一个接口。适配器模式使得原本由于接口不兼容而不能一起工作的类能够协同工作。

适配器模式主要涉及三个角色：

1. 1.

   **目标接口（Target Interface）：** 客户端所期望的接口，适配器通过实现这个接口，使得被适配者（Adaptee）能够与客户端一起工作。

2. 2.

   **适配器（Adapter）：** 适配器是一个类，它实现了目标接口，同时包含一个对被适配者的引用。适配器的主要任务是将客户端的请求转发给被适配者。

3. 3.

   **被适配者（Adaptee）：** 被适配者是原本无法与客户端兼容的类，适配器通过对被适配者的引用，使得它能够适应客户端的期望接口。

适配器模式通常有两种实现方式：类适配器和对象适配器。

- •

  **类适配器：** 适配器继承自被适配者，并实现目标接口。这样适配器既具有被适配者的行为，又符合客户端的接口期望。

- •

  **对象适配器：** 适配器包含一个对被适配者的引用，通过组合的方式实现目标接口。适配器将客户端的请求转发给被适配者。

以下是一个简单的类适配器模式的示例，假设有一个英国插座（被适配者），而我们的设备（客户端）使用的是中国插头，我们需要一个适配器：

```
# 被适配者（英国插座）
class UKSocket:
    def provide_power(self):
        return "UK power supply"

# 目标接口（中国插头）
class ChinaPlug:
    def provide_power(self):
        return "China power supply"

# 适配器（类适配器）
class UKToChinaAdapter(UKSocket, ChinaPlug):
    def provide_power(self):
        # 转换逻辑：调用被适配者的方法，将英国插座的电源转换为中国插头的电源
        uk_power = super().provide_power()
		# uk_power = super(UKSocket, self).provide_power()   （一个有趣的小问题，这里的super(UKSocket, self) 实际上不是指UKSocket ，而是此类的在MRO查找（C3算法）后的下一个类ChinaPlug）
        return f"Converted: {uk_power} to China plug"

# 客户端代码
def client_code(plug):
    print(plug.provide_power())

# 在客户端中，使用适配器将英国插座适配为中国插头
uk_socket_adapter = UKToChinaAdapter()
client_code(uk_socket_adapter)
```

适配器模式在软件设计中常用于整合已有的系统、类库或组件，以确保它们能够与新的系统或客户端协同工作，从而提高代码的可复用性和灵活性。

#### 示例2

```python
from abc import ABCMeta, abstractmethod

class Payment:
    __metaclass__ = ABCMeta
    @abstractmethod
    def pay(self, money):
        pass

class Alipay(Payment):
    def pay(self, money):
        print('Alipay %d' % money)


class Weixinpay(Payment):
    def pay(self, money):
        print('Weixinpay %d' % money)


class ApplePay:
    def cost(self, money):
        print('ApplePay %d' % money)


# 类适配器（无法适用于多个类的情况）
class NewApplePay(Payment, ApplePay):
    def pay(self, money):
        ApplePay().cost(money)


# client code
pay = NewApplePay()
pay.pay(100)


# 对象适配器
class PaymentAdapter():
    def __init__(self, pay_obj):
        self.pay_obj = pay_obj

    def pay(self, money):
        self.pay_obj.cost(money)


# client code
apply_pay = ApplePay()
pay2 = PaymentAdapter(apply_pay)
pay2.pay(100)
```

# 桥模式

桥模式（Bridge Pattern）是一种结构型设计模式，用于将抽象部分与实现部分分离，使它们可以独立变化而互不影响。桥模式通过将一个系统分成多个抽象类和实现类，然后通过一个桥接（Bridge）连接它们，从而达到解耦的目的。

桥模式主要包括以下几个关键角色：

1. 1.

   **抽象类（Abstraction）：** 定义了系统的抽象部分，并维护一个指向实现类的引用，它可能包含一些与实现相关的业务方法。

2. 2.

   **扩充抽象类（Refined Abstraction）：** 继承自抽象类，对抽象类进行扩展，通常包含更多的业务方法。

3. 3.

   **实现类接口（Implementor）：** 定义了实现类的接口，可以包含一些基本的操作。

4. 4.

   **具体实现类（Concrete Implementor）：** 实现了实现类接口，提供了具体的实现。

5. 5.

   **桥接（Bridge）：** 将抽象部分与实现部分连接起来，充当桥梁的角色。

桥模式的核心思想是将抽象和实现分离，使得它们可以独立变化。这种解耦使得系统更灵活，可以方便地对抽象部分和实现部分进行扩展和修改，而不影响彼此。桥模式常用于以下场景：

1. 1.

   **当一个系统需要在多个维度上进行独立变化时，可以使用桥模式将各个维度的变化分离**。

2. 2.

   当一个抽象的实现可以有多个具体的实现时，可以使用桥模式进行解耦。

3. 3.

   当需要通过组合的方式来实现不同的功能时，桥模式也是一个有效的选择。

***一句话秒懂：将m\*n个实现类转换为m+n个实现类***

假设有一个这样的场景，一个画图软件，有一个图形接口类，用于绘制图形例如圆形，长方形... ，  图形需要有颜色，如果通过继承可能会写红色的圆形，红色的长方形，绿色的长方形，绿色的圆形，添加一种颜色就需要实现所有的图形，需要m*n个类实现；通过桥接模式，将在图形类里面添加一个颜色的对象引用，就可以实现将两个维度的类组合到一起，从而只需要m+n个类

```
from abc import ABC, abstractmethod, ABCMeta


class Shape(metaclass=ABCMeta):
    def __init__(self, color):   # 引用颜色对象，从而组合在一起，可以自由的使用所有颜色，不需要一个个去实现
        self.color = color

    @abstractmethod
    def draw(self):
        pass


class Circle(Shape):
    name = '圆形'

    def draw(self):
        print('返回圆形的区域')
        self.color.give_color(self)


class Rectangle(Shape):
    name = '长方形'

    def draw(self):
        print('返回长方形形的区域')
		self.color.give_color(self)


class Color(metaclass=ABCMeta):
    @abstractmethod
    def give_color(self, shape):
        pass


class Red(Color):
    def give_color(self, shape):
        print("给%s涂上红色" % shape.name)


class Green(Color):
    def give_color(self, shape):
        print("给%s涂上绿色" % shape.name)


shape1 = Circle(Red())
shape1.draw()
```

------

# 组合模式

组合模式（Composite Pattern）是一种结构型设计模式，它允许客户端以统一的方式处理单个对象和对象组合，即将对象组织成树形结构以表示"整体-部分"的层次关系。

组合模式主要包括以下几个角色：

1. 1.

   **组件（Component）：** 定义了组合中所有对象的通用接口，可以是抽象类或接口。在组合中，叶子节点和容器节点都实现了这个接口。

2. 2.

   **叶子（Leaf）：** 表示组合中的叶子节点，叶子节点没有子节点，实现了组件接口。

3. 3.

   **容器（Composite）：** 表示组合中的容器节点，容器节点可以包含叶子节点或其他容器节点，也实现了组件接口。容器节点的主要责任是管理其子节点。

在组合模式中，客户端可以一致地处理单个对象和对象组合，无需关心处理的是叶子节点还是容器节点。这种模式使得客户端代码更加简洁和灵活。

以下是一个使用组合模式的简单示例，假设我们要 表示一个文件系统的层次结构：

```
from abc import ABC, abstractmethod

# 组件接口
class FileSystemComponent(ABC):
    @abstractmethod
    def display(self):
        pass

# 叶子节点
class File(FileSystemComponent):
    def __init__(self, name):
        self.name = name

    def display(self):
        print(f"File: {self.name}")

# 容器节点
class Directory(FileSystemComponent):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def display(self):
        print(f"Directory: {self.name}")
        for child in self.children:
            child.display()

# 客户端代码
file1 = File("file1.txt")
file2 = File("file2.txt")
file3 = File("file3.txt")

dir1 = Directory("Folder 1")
dir1.add(file1)
dir1.add(file2)

dir2 = Directory("Folder 2")
dir2.add(file3)

root = Directory("Root")
root.add(dir1)
root.add(dir2)

# 客户端可以一致地处理文件和文件夹
root.display()
```

在这个例子中，`FileSystemComponent` 是组件接口，`File` 是叶子节点，`Directory` 是容器节点。客户端代码可以一致地处理文件和文件夹，而不需要知道具体是哪种类型的节点。这使得组合模式非常适用于需要处理树状结构的场景，如图形界面中的UI组件、文件系统、组织结构等。

### 示例2

```
from abc import ABCMeta, abstractmethod


class Graphics(metaclass=ABCMeta):
    @abstractmethod
    def draw(self):
        pass


class Point(Graphics):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        print(f"画了点({self.x}, {self.y})")

    def __str__(self):
        return f"({self.x}, {self.y})"


class Line(Graphics):
    def __init__(self,p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self):
        print(f"画了线（{self.p1}）（{self.p2}）")

    def __str__(self):
        return f"({self.p1}) - ({self.p2})"


class Picture(Graphics):
    def __init__(self, elements):
        self.childrens = []
        for element in elements:
            self.add(element)

    def add(self, graphic):
        self.childrens.append(graphic)

    def remove(self, graphic):
        self.childrens.remove(graphic)

    def draw(self):
        for children in self.childrens:
            children.draw()


p1 = Point(1, 2)
p2 = Point(3, 4)
l1 = Line(p1, p2)
pic1 = Picture([p1, p2, l1])
# pic1.draw()

p3 = Point(6, 7)
p4 = Point(8, 9)
l2 = Line(p3, p4)
pic2 = Picture([p3, p4, l2])
l3 = Line(p1, p3)
pic2.add(l3)
# pic2.draw()

pic = Picture([pic1, pic2])
pic.draw()
```

------

# 外观模式

外观模式（Facade Pattern）是一种结构型设计模式，它提供了一个简化的接口，用于访问系统中的一组接口，从而隐藏系统的复杂性，并为客户端提供一个更加简单和统一的入口点。

外观模式的主要目的是通过创建一个包装类（外观类），将系统中一系列复杂的子系统接口整合在一起，为客户端提供一个更高层次的接口，使得客户端不需要直接与底层复杂的子系统接口交互。

外观模式的关键角色包括：

1. 1.

   **外观类（Facade）：** 提供了一个简化的接口，封装了系统中一组复杂的子系统接口。客户端通过调用外观类的方法来访问系统。

2. 2.

   **子系统类（Subsystem）：** 实际执行系统功能的类，外观类将客户端的请求委派给这些子系统类来完成具体的工作。

以下是一个简单的外观模式的示例，假设有一个电脑系统，包括CPU、内存和硬盘等子系统：

```
# 子系统类
class CPU:
    def start(self):
        print("CPU is starting")

    def shutdown(self):
        print("CPU is shutting down")

class Memory:
    def load(self):
        print("Memory is loading data")

    def unload(self):
        print("Memory is unloading data")

class HardDrive:
    def read(self):
        print("Hard Drive is reading data")

    def write(self):
        print("Hard Drive is writing data")

# 外观类
class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()

    def start(self):
        self.cpu.start()
        self.memory.load()
        self.hard_drive.read()
        print("Computer is starting")

    def shutdown(self):
        self.cpu.shutdown()
        self.memory.unload()
        self.hard_drive.write()
        print("Computer is shutting down")

# 客户端代码
computer = ComputerFacade()
computer.start()
print("--------")
computer.shutdown()
```

在这个例子中，`ComputerFacade` 是外观类，封装了启动和关闭电脑的一系列操作。客户端通过调用外观类的方法来启动和关闭电脑，而无需直接与 CPU、内存和硬盘等子系统类交互。外观模式有助于降低系统的复杂性，提供了一个简单的接口给客户端使用。

------

# 代理模式

代理模式（Proxy Pattern）是一种结构型设计模式，它提供了一个代理类，用于控制对另一个对象的访问。代理模式允许通过引入一个代理类来间接访问目标对象，以在访问时添加额外的功能或控制访问的方式。

代理模式的主要角色包括：

1. 1.

   **抽象实体（Subject）：** 定义了目标对象和代理对象的共同接口，这样在任何使用目标对象的地方都可以使用代理对象。

2. 2.

   **真实实体（Real Subject）：** 实现了抽象主题接口，是代理模式中所关注的具体业务类，代理模式的目标对象。

3. 3.

   **代理（Proxy）：** 实现了抽象主题接口，同时持有一个真实主题的引用。在代理类中可以控制对真实主题的访问，并在访问时添加额外的功能。

代理模式常见的应用场景包括：

- •

  **远程代理：** 用于在不同地址空间中代表对象，使得这些对象可以在不同的进程或计算机上运行。

- •

  **虚拟代理：** 用于控制访问目标对象的时机，延迟加载目标对象，以提高系统的性能。

- •

  **保护代理：** 用于控制对目标对象的访问权限，限制某些用户对目标对象的操作。

- •

  **缓存代理：** 用于为某些昂贵操作的结果提供缓存，避免重复执行相同操作。

以下是一个简单的代理模式的示例，假设有一个图片加载的场景：（延迟加载案例）

```
from abc import ABC, abstractmethod

# 抽象主题
class Image(ABC):
    @abstractmethod
    def display(self):
        pass

# 真实主题
class RealImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self.load_image()            # 此时已经加载

    def load_image(self):
        print(f"Loading image: {self.filename}")

    def display(self):
        print(f"Displaying image: {self.filename}")

# 代理
class ProxyImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None

    def display(self):            # 只有调用此方法才会真的去加载
        if self.real_image is None:
            self.real_image = RealImage(self.filename)
        self.real_image.display()

# 客户端代码
image1 = ProxyImage("image1.jpg")
image1.display()  # 此时真实主题被加载和显示

image2 = ProxyImage("image2.jpg")
# 此时不会立即加载和显示真实主题，直到调用display方法时才加载和显示
image2.display()
```

在这个例子中，`Image` 是抽象主题，`RealImage` 是真实主题，`ProxyImage` 是代理。当客户端调用代理的 `display` 方法时，代理会在需要时创建并调用真实主题的 `display` 方法。代理模式使得客户端无需直接访问真实主题，而通过代理来间接访问，从而在访问时添加了一些控制或额外的功能。

------

# 装饰器模式

装饰器模式（Decorator Pattern）是一种结构型设计模式，它允许向一个对象动态地添加新功能，通过创建一个包装类，将新功能封装在这个包装类中，然后通过将原始对象传递给包装类的方式来实现功能的叠加。

在装饰器模式中，有几个主要的角色：

1. 1.

   **组件（Component）：** 定义了一个抽象接口，可以是具体组件和装饰器都实现的接口。通常是一个抽象类或接口。

2. 2.

   **具体组件（Concrete Component）：** 实现了组件的具体实现，是被装饰的对象。

3. 3.

   **装饰器（Decorator）：** 也是组件，但是它持有一个对其他组件的引用，并通过该引用添加或覆盖组件的功能。装饰器具有与组件相同的接口。

4. 4.

   **具体装饰器（Concrete Decorator）：** 实现了装饰器的具体实现，向组件添加新的功能。

装饰器模式的核心思想是通过层层包装，将新功能一层一层地叠加到原始对象上，而客户端可以根据需要选择是否应用这些额外的功能。

以下是一个简单的装饰器模式的示例，假设有一个简单的咖啡订单系统：

```
from abc import ABC, abstractmethod

# 抽象组件
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

# 具体组件
class SimpleCoffee(Coffee):
    def cost(self):
        return 5  # 简单咖啡的价格为5元

# 装饰器
class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    @abstractmethod
    def cost(self):
        pass

# 具体装饰器
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 2  # 加牛奶的价格为2元

# 具体装饰器
class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 1  # 加糖的价格为1元

# 客户端代码
simple_coffee = SimpleCoffee()
print("Cost of simple coffee:", simple_coffee.cost())

milk_coffee = MilkDecorator(simple_coffee)
print("Cost of milk coffee:", milk_coffee.cost())

sugar_milk_coffee = SugarDecorator(milk_coffee)
print("Cost of sugar milk coffee:", sugar_milk_coffee.cost())
```

在这个例子中，`Coffee` 是抽象组件，`SimpleCoffee` 是具体组件。`CoffeeDecorator` 是装饰器，`MilkDecorator` 和 `SugarDecorator` 是具体装饰器。通过不断地叠加具体装饰器，可以在不修改原始组件的情况下为咖啡添加额外的功能，如加牛奶或加糖。客户端可以根据需要选择叠加的装饰器，实现了动态地添加新功能的效果。

------

# 责任链模式

责任链模式（Chain of Responsibility Pattern）是一种行为型设计模式，它允许你构建一个对象链，每个对象都包含了对请求的处理，同时还持有对下一个处理者的引用。通过这种方式，请求沿着链传递，直到有一个对象处理它为止。

在责任链模式中，有几个主要的角色：

1. 1.

   **处理者（Handler）：** 定义了一个处理请求的接口，并包含了对下一个处理者的引用。

2. 2.

   **具体处理者（Concrete Handler）：** 实现了处理请求的具体逻辑，如果能够处理请求，则进行处理；如果不能处理，则将请求传递给下一个处理者。

3. 3.

   **客户端（Client）：** 创建一个处理链，并向链的第一个处理者发送请求。

责任链模式的核心思想是将请求沿着处理链传递，直到有一个处理者能够处理它。这样可以动态地改变处理链的结构，增加或删除处理者，而不影响客户端。

以下是一个简单的责任链模式的示例，假设有一个请假申请的场景：

```
from abc import ABC, abstractmethod

# 处理者接口
class Approver(ABC):
    @abstractmethod
    def process_request(self, amount):
        pass

# 具体处理者
class Manager(Approver):
    def process_request(self, amount):
        if amount <= 1000:
            print(f"Manager approves the request for {amount} dollars.")
        elif self.next is not None:                          # self.next用于绑定下一个处理对象，可以在客户端绑定，也可以在底层代码的__init__里面初始化好
            self.next.process_request(amount)

# 具体处理者
class Director(Approver):
    def process_request(self, amount):
        if amount <= 5000:
            print(f"Director approves the request for {amount} dollars.")
        elif self.next is not None:
            self.next.process_request(amount)

# 具体处理者
class VicePresident(Approver):
    def process_request(self, amount):
        if amount <= 10000:
            print(f"Vice President approves the request for {amount} dollars.")
        elif self.next is not None:
            self.next.process_request(amount)

# 具体处理者
class President(Approver):
    def process_request(self, amount):
        if amount <= 20000:
            print(f"President approves the request for {amount} dollars.")
        elif self.next is not None:
            self.next.process_request(amount)

# 客户端代码
manager = Manager()
director = Director()
vp = VicePresident()
president = President()

# 构建处理链
manager.next = director
director.next = vp
vp.next = president

# 客户端发送请求
manager.process_request(8000)
```

在这个例子中，`Approver` 是处理者的抽象接口，`Manager`、`Director`、`VicePresident` 和 `President` 是具体处理者。客户端通过构建处理链，并将请求发送给链的第一个处理者，请求会沿着链传递，直到有一个处理者能够处理它。责任链模式使得请求的发送者和接收者解耦，可以灵活地调整处理链的结构。

------

# 观察者模式

**观察者模式**是一种行为型设计模式，其中一个对象（称为主题）维护其依赖项列表（称为观察者），并在对象状态变化时通知所有观察者，使得它们能够自动更新。

### 主要角色：

1. 1.

   **主题（Subject）：** 维护一组观察者对象，提供注册和移除观察者的方法，并在状态变化时通知观察者。

2. 2.

   **观察者（Observer）：** 定义一个更新接口，用于接收主题的通知并进行相应的处理。

3. 3.

   **具体主题（Concrete Subject）：** 继承自主题，实现具体的业务逻辑，当状态变化时通知观察者。

4. 4.

   **具体观察者（Concrete Observer）：** 继承自观察者，实现具体的更新逻辑。

### 优点：

1. 1.

   **松耦合：** 主题和观察者之间是松耦合的，主题不需要知道观察者的具体细节，只需要知道观察者实现了更新接口即可。

2. 2.

   **可扩展：** 可以动态地添加和删除观察者，使系统更易于扩展。

3. 3.

   **解耦：** 观察者模式可以使主题和观察者之间的关系解耦，使得它们可以独立变化。

### 缺点：

1. 1.

   **可能引起性能问题：** 如果观察者太多或者更新操作较为复杂，可能会影响性能。

2. 2.

   **可能引起循环依赖：** 如果观察者之间存在相互依赖，可能导致循环依赖的问题。

### 应用场景：

1. 1.

   **事件处理系统：** 当一个事件发生时，多个对象需要作出响应，例如图形界面中的按钮点击事件。

2. 2.

   **消息通知系统：** 当系统中的某个状态发生变化时，需要通知多个订阅者。

3. 3.

   **分布式系统：** 在分布式系统中，一个节点的状态变化可能需要通知其他节点进行相应处理。

4. 4.

   **股票市场：** 股票价格变化时，多个投资者需要及时得知并作出相应决策。

观察者模式适用于当一个对象的状态变化会影响其他对象，并且希望实现低耦合、可扩展的系统时。

Certainly! Here's a simple Python example of the Observer pattern:

```
# Subject (Observable)
class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)


# Observer (Observer)
class Observer:
    def update(self, message):
        pass


# Concrete Subject (Concrete Observable)
class NewsAgency(Subject):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._news = ""

    def set_news(self, news):
        self._news = news
        self.notify_observers(f"{self._name} News: {self._news}")


# Concrete Observer (Concrete Observer)
class NewsReader(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, message):
        print(f"{self._name} received news: {message}")


# Client code
if __name__ == "__main__":
    # Create subjects and observers
    bbc_news = NewsAgency("BBC News")
    cnn_news = NewsAgency("CNN News")

    reader1 = NewsReader("Reader 1")
    reader2 = NewsReader("Reader 2")

    # Attach observers to subjects
    bbc_news.add_observer(reader1)
    bbc_news.add_observer(reader2)
    cnn_news.add_observer(reader1)

    # Set news for subjects
    bbc_news.set_news("Breaking: Python is awesome!")
    cnn_news.set_news("Tech giants announce new collaboration")

    # Output:
    # Reader 1 received news: BBC News News: Breaking: Python is awesome!
    # Reader 2 received news: BBC News News: Breaking: Python is awesome!
    # Reader 1 received news: CNN News News: Tech giants announce new collaboration
```

### 示例2

```
from abc import ABCMeta, abstractmethod


# 观察者接口
class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, content):
        pass


# 发布者接口
class Notice:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)


# 具体发布者
class CompanyNotice(Notice):
    def __init__(self):
        super().__init__()
        self.__info = []

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, into):
        self.__info.append(into)
        self.notify()


# 具体观察者
class StaffObserver(Observer):
    def __init__(self, name=None):
        self.info = None
        self.name = name

    def update(self, notice_obj):
        self.info = notice_obj.info

    def __str__(self):
        return f'{self.name}'


staff1 = StaffObserver(name='cl')
staff2 = StaffObserver(name='opp')
notice = CompanyNotice()
notice.attach(staff1)
notice.attach(staff2)

notice.info = '公司开业啦!!!'
print(staff1.info)
print(staff2.info)

notice.info = '上班啦'
print(staff1.info)
print(staff2.info)

notice.info = '下班啦'
print(staff1.info)
print(staff2.info)
```

------

# 策略模式

**策略模式**是一种行为型设计模式，它定义了一系列算法，将每个算法封装成一个类，并使它们可互换。策略模式使得算法的变化独立于使用算法的客户端。

### 主要角色：

1. 1.

   **环境类（Context）：** 维护一个对策略对象的引用，可以动态切换策略对象。

2. 2.

   **策略接口（Strategy）：** 定义所有支持的算法的公共接口，具体策略类实现这个接口。

3. 3.

   **具体策略类（Concrete Strategy）：** 实现了策略接口的具体算法。

### 优点：

1. 1.

   **简化算法替换：** 策略模式将每个算法封装成一个类，使得新增、替换算法更加灵活，不影响其他部分的代码。

2. 2.

   **减少条件语句：** 避免了大量的条件语句，提高代码可读性。

3. 3.

   **提高扩展性：** 新增策略只需要增加新的策略类，而不需要修改环境类。

### 缺点：

1. 1.

   **客户端需要了解所有的策略类：** 客户端必须了解所有可用的策略类，并选择合适的策略。这可能会增加客户端的复杂性。

### 应用场景：

1. 1.

   **算法需要经常变化：** 当一个系统的算法经常变化，而且不希望客户端依赖具体的算法实现时，可以使用策略模式。

2. 2.

   **避免使用大量条件语句：** 当一个类有多个相关的条件语句，并且每个条件都会执行不同的操作时，可以考虑使用策略模式。

3. 3.

   **对算法进行扩展：** 当需要对算法进行扩展，增加新的算法时，可以使用策略模式，避免修改原有代码。

### 示例代码：

```
# 策略接口
class PaymentStrategy:
    def pay(self, amount):
        pass

# 具体策略类 - 支付宝支付
class AlipayPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} via Alipay")

# 具体策略类 - 微信支付
class WeChatPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} via WeChat Pay")

# 环境类 - 支付上下文
class PaymentContext:
    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def set_payment_strategy(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def perform_payment(self, amount):
        self.payment_strategy.pay(amount)

# 客户端代码
if __name__ == "__main__":
    alipay = AlipayPayment()
    wechat_pay = WeChatPayment()

    context = PaymentContext(alipay)
    context.perform_payment(100)

    context.set_payment_strategy(wechat_pay)
    context.perform_payment(150)

# 输出:
# Paid 100 via Alipay
# Paid 150 via WeChat Pay
```

在这个例子中，`PaymentStrategy` 是策略接口，`AlipayPayment` 和 `WeChatPayment` 是具体策略类，而 `PaymentContext` 是环境类，负责维护策略对象的引用，并在运行时切换不同的支付策略。

------

# 模板方法模式

**模板方法模式**是一种行为型设计模式，它定义了一个算法的骨架，将算法中一些步骤的实现延迟到子类中。模板方法模式使得子类可以在不改变算法结构的情况下，重新定义算法的某些步骤。

### 主要角色：

1. 1.

   **抽象类（Abstract Class）：** 定义了算法的骨架，包含一个或多个抽象方法，这些方法由子类实现。

2. 2.

   **具体类（Concrete Class）：** 实现了抽象类中的抽象方法，提供算法的具体实现。

### 优点：

1. 1.

   **代码复用：** 将相同的算法步骤放在抽象类中，避免代码重复。

2. 2.

   **扩展性：** 允许子类在不改变算法结构的情况下，重新定义或扩展算法的某些步骤。

3. 3.

   **封装不变部分：** 将算法的不变部分封装在抽象类中，提高了代码的封装性。

### 缺点：

1. 1.

   **逻辑复杂性：** 模板方法模式可能导致算法的逻辑复杂，难以理解。

### 应用场景：

1. 1.

   **多个子类共享相同的算法：** 当多个子类有相同的行为，但具体实现有差异时，可以使用模板方法模式。

2. 2.

   **固定算法骨架：** 当一个算法有固定的执行步骤，但某些步骤的具体实现可能不同，可以考虑使用模板方法模式。

### 示例代码：

```
# 抽象类 - 煮饭
class CookTemplate:
    def cook(self):
        self.boil_water()
        self.add_ingredients()
        self.cook_food()
        self.serve_dish()

    def boil_water(self):
        print("Boiling water")

    def serve_dish(self):
        print("Serving the dish")

    # 抽象方法 - 加食材
    def add_ingredients(self):
        pass

    # 抽象方法 - 烹饪食物
    def cook_food(self):
        pass

# 具体类 - 红烧肉
class BraisedPork(CookTemplate):
    def add_ingredients(self):
        print("Adding pork and soy sauce")

    def cook_food(self):
        print("Simmering the pork")

# 具体类 - 清蒸鱼
class SteamedFish(CookTemplate):
    def add_ingredients(self):
        print("Adding fish and ginger")

    def cook_food(self):
        print("Steaming the fish")

# 客户端代码
if __name__ == "__main__":
    braised_pork = BraisedPork()
    braised_pork.cook()

    print("\n")

    steamed_fish = SteamedFish()
    steamed_fish.cook()

# 输出:
# Boiling water
# Adding pork and soy sauce
# Simmering the pork
# Serving the dish
#
# Boiling water
# Adding fish and ginger
# Steaming the fish
# Serving the dish
```

在这个例子中，`CookTemplate` 是抽象类，定义了煮饭的算法骨架，包含了一些共同的步骤。`BraisedPork` 和 `SteamedFish` 是具体类，分别实现了抽象类中的抽象方法，提供了煮红烧肉和清蒸鱼的具体实现。客户端可以使用这些具体类来调用模板方法 `cook()`，而不需要关心具体步骤的实现。