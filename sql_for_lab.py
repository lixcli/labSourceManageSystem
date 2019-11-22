# 查找已有的目标实验室已有的电脑
computers_of = lambda tgt:f'''
SELECT id, cName,producer 
FROM Computer
WHERE lId={tgt} 
ORDER BY cName
'''

# 查找已有软件
# orm重构
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
# orm重构
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
SELECT  Computer.id,Computer.cpu,Computer.mm,cName,producer,Computer.aId,Computer.lId,Computer.normal 
FROM InstallList,Computer
WHERE sId IN ({sId})  AND Computer.lId = '{labId}'
AND Computer.id = InstallList.cId
'''

# 查找目标实验室中没有这软件的所有电脑iad
not_have_software_of = lambda sId,labId:f'''
SELECT Computer.id,Computer.cpu,Computer.mm,cName,producer,Computer.aId,Computer.lId,Computer.normal  From Computer
WHERE lId='{labId}'
EXCEPT
SELECT Computer.id,Computer.cpu,Computer.mm,cName,producer,Computer.aId,Computer.lId,Computer.normal 
FROM InstallList,Computer
WHERE  Computer.lId = '{labId}'
AND Computer.id = InstallList.cId AND sId IN ({sId})
'''

# 查看闲置电脑
# orm 重构
avil_computer=lambda page,limit: '''
SELECT TOP {0} *
FROM Computer
WHERE lId IS NULL AND  id not in (
        select top {1}  id 
        from Computer
        )
'''.format(limit,(page-1)*limit)
# 闲置电脑个数
count_avil_computer=f'''
SELECT COUNT(id)
FROM Computer
WHERE lId IS NULL
'''
# orm重构
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
install = lambda  sId,cId,aId,sys,num: f'''
INSERT INTO InstallList
VALUES('i'+(CONVERT(varchar(8),GETDATE(),112))+'/{num}',
        '{aId}',
        '{cId}',
        '{sId}',
        '{sys}'
        )
'''
# 删除安装
uninstall = lambda sId,cId: f'''
DELETE FROM InstallList
WHERE sId = '{sId}' AND cId='{cId}'
'''

# 当天最大需求id号
max_today_demand=f'''
SELECT max(CONVERT(INT,SUBSTRING(id,11,21))) FROM Demand WHERE id LIKE 'd'+(CONVERT(varchar(8),GETDATE(),112))+'/%'
'''

# 老师查看未完成的需求
open_teacher_demand=lambda tId: f'''
SELECT * FROM Demand
WHERE tId='{tId}' AND closeDate is NULL
'''

# 老师查看完成的需求
# orm重构
close_teacher_demand=lambda tId: f'''
SELECT * FROM Demand
WHERE tId='{tId}' AND closeDate IS NOT NULL
'''

# 查看所有未解决需求
# orm 重构
all_open_demand=f'''
SELECT * FROM Demand
WHERE closeDate is NULL
'''
# 查看所有我受理但是未解决的需求
# orm重构
all_m_accepted_demand=lambda aId: f'''
SELECT * FROM Demand
WHERE aId='{aId}' AND closeDate is NULL
'''

# 查看所有我受理解决的需求
# orm重构
all_m_close_demand=lambda aId: f'''
SELECT * FROM Demand
WHERE aId='{aId}' AND closeDate is NOT NULL
'''

# 受理需求
set_demand_accept=lambda dId,aId: f'''
UPDATE Demand
SET aId='{aId}'
WHERE id='{dId}'
'''

# 取消受理需求
cancel_demand_accept=lambda dId,aId: f'''
UPDATE Demand
SET aId=NULL
WHERE id='{dId}'
'''

close_accepted_demand=lambda dId: f'''
UPDATE Demand
SET closeDate=GETDATE()
WHERE id='{dId}'
'''

set_demand_response=lambda dId,res: f'''
UPDATE Demand
SET response='{res}'
WHERE id='{dId}'
'''

# 修改管理员密码
set_admin_passwd=lambda id,pwd: f'''
UPDATE Adminitrator
SET pwd='{pwd}'
WHERE id='{id}'
'''
# 修改用户密码
set_teacher_passwd=lambda id,pwd: f'''
UPDATE Teacher
SET pwd='{pwd}'
WHERE id='{id}'
'''
# 删除用户
delete_user=lambda id: f'''
DELETE FROM Demand
WHERE tId='{id}'

DELETE FROM Teacher
WHERE id='{id}' 
'''

# 重置用户密码
reset_user_pwd=lambda id: f'''
UPDATE Teacher
SET pwd='pbkdf2:sha256:150000$qImwjNTC$efc8b17a0ec47f711e8cacc216d6a506e601cf92e741eb8bdbf1ec2618b36e01'
WHERE id='{id}'
'''

# 删除电脑
delete_computer=lambda id: f'''
DELETE FROM InstallList
WHERE id in( 
SELECT id FROM Computer
WHERE id='{id}' AND lId is NULL
)
DELETE FROM ComputerSys
WHERE cId in( 
SELECT id FROM Computer
WHERE id='{id}'
)

DELETE FROM Computer
WHERE id='{id}'
'''

# 根据电脑id获取其所有已有系统
get_sys_by_cId=lambda id: f'''
SELECT sys FROM ComputerSys
WHERE cId='{id}'
'''

# 根据电脑id获取已有的软件(所有电脑都有的软件)
get_lab_software_by_id=lambda lId: f'''
SELECT Software.id,Software.sName,Software.sys 
FROM Software
WHERE id IN (
        SELECT sId FROM Installist
        WHERE cId IN (
                SELECT Computer.id From Computer
                WHERE Computer.id = '{lId}'
        )
)
'''