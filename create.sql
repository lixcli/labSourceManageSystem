USE DB_laboratory

CREATE TABLE ComputerSys(
    cId CHAR(16) NOT NULL,
    sys CHAR(16) NOT NULL,
    FOREIGN KEY(cId) REFERENCES Computer(id),
    PRIMARY KEY(cId,sys),
    CHECK (sys='win7' or sys='ubuntu16.04' or sys='centos7')
)
-- drop TABLE ComputerSys