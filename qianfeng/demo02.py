print("Dear Sir,")
print('  Please click the link to active the user account!')
money =  9.9
print(money,type(money))
# 命名方式：驼峰式、下划线式

import keyword
print(keyword.kwlist) # keyword

age = 18
print("age is %s" % age)
print("age is " + str(age))
print("age is %d" % age)
print(int(19.99)) # 取整舍尾

year = 2021
print("%02d" % year)

dog = 89.1234567890
print("%.2f" % dog) # 四舍五入小数点后几位小数

message='{}-{}'.format(year,age)
print(message)
print(id(message))  # 内存地址
