# 查找已有的目标实验室已有的电脑
computers_of = lambda tgt:f'''
SELECT id, cName,producer 
FROM Computer
WHERE lId={tgt} 
ORDER BY cName
'''

# 查找已有软件
exist_software = f'''
SELECT * FROM SoftWare
'''
# 统计已有软件(计算当天已有的软件数)
count_software = f'''
SELECT COUNT(*) FROM SoftWare WHERE id LIKE 's'+(CONVERT(varchar(8),GETDATE(),112))+'%'
'''

# 查找登记的实验室
exist_lab = f'''
SELECT id,lName FROM Laboratory
'''
# 统计当天入库电脑
count_computer = f'''
SELECT COUNT(*) FROM Computer WHERE id LIKE 'c'+(CONVERT(varchar(8),GETDATE(),112))+'%'
'''
# 注销电脑位置
remove_computer_from = lambda tgt:f'''
UPDATE Computer
SET lId=NULL
WHERE lId={tgt}
'''
# 查找已有计算机种类
exist_lab = f'''
SELECT DISTINCT cName FROM Computer
'''
# 删除软件,可多条记录tgt为类似'xiaoming','daming'的字符串
delete_software=lambda tgt: f'''
DELETE FROM Software
WHERE id = {tgt}
'''


# TODO 查找目标实验室中全部电脑都有的软件
software_of = lambda tgt:f'''

'''