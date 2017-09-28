
file=open('test.txt','a+')

for i in range(20):
    if i in file.readlines():
        file.write('')
    else:
        file.write(str(i))

for item in file.readlines():
    print(1)

# file_read=open('test.txt','r')
# print(file_read.readlines())
