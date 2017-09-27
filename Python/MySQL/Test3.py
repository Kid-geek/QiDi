import pymysql

# 连接数据库
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='anhui',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()

# 插入数据
cursor = connect.cursor()
sql = "INSERT INTO 行政许可 (行政相对人名称, 书文号, 项目名称, 审批类别, 许可内容, 组织机构代码) VALUES ( '%s', '%s', '%s', '%s', '%s', %s)"

data = ('1', '1', '1', '1', '1', '1')
cursor.execute(sql % data)
connect.commit()
print('成功插入', cursor.rowcount, '条数据')