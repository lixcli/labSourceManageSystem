# 问题收集

## 网页异步通讯
[ajax load方法](https://www.runoob.com/jquery/jquery-ajax-load.html) 

## mssql check约束
[ms文档](https://docs.microsoft.com/zh-cn/sql/relational-databases/tables/create-check-constraints?view=sql-server-ver15)  

## sqlalchemy执行sql
想使用 sql 需要这样操作：
db.session.execute(sql)  
返回的结果是一个列表，获取后通过循环解析出来  
即便结果是单条记录，也需要按照列表进行解析  

## mssql字符串拼接
```sql
'c'+(CONVERT(varchar(8),GETDATE(),112))+'/'+cast(@i AS VARCHAR)
```
## sqlalchemy commit回滚
```python
 try:
    user_db = User(email=self.email, nickname=self.nickname, password=self.password)
    db.session.add(user_db)
    #所有的数据处理准备好之后，执行commit才会提交到数据库！
    db.session.commit()
except Exception as e:
    #加入数据库commit提交失败，必须回滚！！！
    db.session.rollback()
    raise e

```

## flask后台发送信息到html的方法
[flask后台发送信息到html的方法](https://blog.csdn.net/shuibuzhaodeshiren/article/details/86770144)  


