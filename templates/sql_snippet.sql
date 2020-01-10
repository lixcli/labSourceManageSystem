-- 查看表名
USE DB_laboratory
-- Select Name FROM SysObjects Where XType='U' orDER BY Name

-- 查询指定表中的所有字段名和字段类型
-- select sc.name,st.name from syscolumns sc,systypes st where sc.xtype=st.xtype and sc.id in(select id from sysobjects where xtype='U' and name='Software');
-- DELETE FROM Software
-- WHERE id in ('s20191027/0')
-- 查看指定表
-- SELECT * FROM InstallList
-- DELETE FROM InstallList
-- WHERE id LIKE '%'

-- SELECT max(CONVERT(INT,SUBSTRING(id,11,21))) FROM InstallList WHERE id LIKE 'i'+(CONVERT(varchar(8),GETDATE(),112))+'/%'
-- 插入指定表
-- SELECT * FROM Teacher
-- INSERT INTO Teacher
-- VALUES('22920172204148','pbkdf2:sha256:150000$qImwjNTC$efc8b17a0ec47f711e8cacc216d6a506e601cf92e741eb8bdbf1ec2618b36e01','lxc','人工智能系','学生')

-- INSERT INTO Adminitrator
-- VALUES('22920172204148','pbkdf2:sha256:150000$qImwjNTC$efc8b17a0ec47f711e8cacc216d6a506e601cf92e741eb8bdbf1ec2618b36e01','lxc')

-- SELECT * FROM Teacher

-- 插入随机数据
-- 插入计算机
    -- 循环插入

-- DECLARE @i int  --声明i字段，字段类型
--  set @i=0  --设置i初始值
 
-- WHILE @i<40      --100为你要执行插入的次数
-- BEGIN
-- INSERT INTO Computer
-- VALUES('c'+(CONVERT(varchar(8),GETDATE(),112))+'/'+cast(@i AS VARCHAR),
-- '暗影精灵5','HP','22920172204148','301',1)    --循环插入SQL语句
-- SET @i=@i+1 --设置变量i的值
-- END




-- TEST area
-- SELECT id, cName,producer 
-- FROM Computer
-- WHERE lId='301' 
-- ORDER BY cName
-- 数组
-- create type stringArray as NVARCHAR(16) array[100] 
-- SELECT COUNT(*) FROM SoftWare WHERE id LIKE 's'+(CONVERT(varchar(8),GETDATE(),112))+'%'
-- SELECT COUNT(id) FROM Computer WHERE id LIKE 'c'+(CONVERT(varchar(8),GETDATE(),112))+'%'
-- DELETE FROM Computer
-- WHERE id LIKE 's%'
-- SELECT MAX(id) FROM InstallList
-- WHERE id LIKE 'i'+(CONVERT(varchar(8),GETDATE(),112))+'/%'
-- SELECT * FROM Computer
-- SELECT id,cName,producer,aId From Computer
-- WHERE lId='301'
-- SELECT Computer.id,cName,producer,Computer.aId 
-- FROM InstallList,Computer
-- WHERE  Computer.lId = '301'
-- AND Computer.id = InstallList.cId AND sId IN ('s20191030/1')

-- SELECT Computer.id,cName,producer,Computer.aId 
-- FROM InstallList,Computer
-- WHERE sId IN ('s20191030/1')  AND Computer.lId = '301'
-- AND Computer.id = InstallList.cId
-- SELECT max(CONVERT(INT,SUBSTRING(id,11,21))) FROM InstallList WHERE id LIKE 'i'+(CONVERT(varchar(8),GETDATE(),112))+'/%'
-- SELECT * FROM Demand

-- SELECT * FROM Demand
-- WHERE tId='22920172204148' AND closeDate IS  NULL

-- SELECT * FROM Adminitrator

-- DELETE FROM InstallList
-- WHERE id in( 
-- SELECT id FROM Computer
-- WHERE id='c20191111/1' AND lId is NULL
-- )



DELETE FROM Laboratory
WHERE id='301'



-- SELECT * 
-- FROM Software
-- WHERE id IN (
--         SELECT sId FROM InstallList
--         WHERE cId IN (
--                 SELECT Computer.id From Computer
--                 WHERE Computer.id = '301'
--         )
-- )

-- SELECT * FROM Demand