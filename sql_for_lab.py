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

# 通过软件名查找
exist_software_by_name = lambda tgt: f'''
SELECT * FROM Software
WHERE sName in ({tgt})
'''
# 获取最大当天id已有软件(计算当天已有的软件数)
max_software = f'''
SELECT max(CONVERT(INT,SUBSTRING(id,11,21))) FROM SoftWare WHERE id LIKE 's'+(CONVERT(varchar(8),GETDATE(),112))+'/%'
'''

# 查找登记的实验室
exist_lab = f'''
SELECT * FROM Laboratory
ORDER BY id
'''
# 删除已有实验室
delete_lab = lambda tgt: f'''
DELETE FROM Laboratory
WHERE id = {tgt}
'''
# 统计当天入库电脑
max_computer = f'''
SELECT max(CONVERT(INT,SUBSTRING(id,11,21))) FROM Computer WHERE id LIKE 'c'+(CONVERT(varchar(8),GETDATE(),112))+'/%'
'''
# 注销电脑位置
remove_computer_from = lambda tgt:f'''
UPDATE Computer
SET lId=NULL
WHERE lId='{tgt}'
'''
# 查找已有计算机种类
exist_computer = f'''
SELECT DISTINCT cName FROM Computer
'''
# 删除软件,可多条记录tgt为类似'xiaoming','daming'的字符串
delete_software=lambda tgt: f'''
DELETE FROM Software
WHERE id = {tgt}
'''
# 原本设置了外键关联软件表和安装表，但是存在安装了软件后，软件版权出库的情况，所以，这里把外键删除了
# 所以如果需要检查，则需要在设计网站时自行加入对应的逻辑

# 查找目标实验室中有这软件的所有电脑id
have_software_of = lambda sId,labId:f'''
SELECT Computer.id,cName,producer,Computer.aId 
FROM InstallList,Computer
WHERE sId IN ({sId})  AND Computer.lId = '{labId}'
AND Computer.id = InstallList.cId
'''

# 查找目标实验室中没有这软件的所有电脑id
not_have_software_of = lambda sId,labId:f'''
SELECT id,cName,producer,aId From Computer
WHERE lId='{labId}'
EXCEPT
SELECT Computer.id,cName,producer,Computer.aId 
FROM InstallList,Computer
WHERE  Computer.lId = '{labId}'
AND Computer.id = InstallList.cId AND sId IN ({sId})
'''

# 查看闲置电脑
avil_computer='''
SELECT * FROM Computer
WHERE lId IS NULL
'''
# 查看实验室已有电脑
lab_computer_of=lambda tgt: f'''
SELECT * FROM Computer
WHERE lId='{tgt}'
'''
# 查看实验室已有电脑数
count_lab_computer_of=lambda tgt: f'''
SELECT COUNT(id) FROM Computer
WHERE lId='{tgt}'
'''
# 注销电脑
export_computer=lambda cId: f'''
UPDATE Computer
SET lId=NULL
WHERE id='{cId}'
'''


# 登记电脑到指定实验室电脑
import_computer=lambda cId,labId: f'''
UPDATE Computer
SET lId='{labId}'
WHERE id='{cId}'

'''
# 统计当天安装软件数
max_today_install=f'''
SELECT max(CONVERT(INT,SUBSTRING(id,11,21))) FROM InstallList WHERE id LIKE 'i'+(CONVERT(varchar(8),GETDATE(),112))+'/%'
'''
# 登记安装
install = lambda  sId,cId,aId,num: f'''
INSERT INTO InstallList
VALUES('i'+(CONVERT(varchar(8),GETDATE(),112))+'/{num}',
        '{aId}',
        '{cId}',
        '{sId}'
        )
'''
# 删除安装
uninstall = lambda sId,cId: f'''
DELETE FROM InstallList
WHERE sId = '{sId}' AND cId='{cId}'
'''


