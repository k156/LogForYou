
-- 과 테이블(Departments)
-- 과 번호
-- 과명
-- 과 코드

drop table if exists Departments;
create table Departments(
	id int auto_increment comment '진료과번호',
    name varchar(128) comment '진료과명',
    primary key(id)
)charset='utf8';



-- 의사 테이블(Doctors)
-- Id
-- 의사명
-- 과번호
-- 이메일
-- 패스워드 

drop table if exists Doctors;
create table Doctors(
	id int auto_increment comment '의사번호',
    name varchar(128) comment '의사이름',
    departmentId int comment '담당진료과',
    email varchar(128),
    password varchar(128),
    primary key(id)
)charset='utf8';


-- 환자 테이블(Patients)
-- 환자번호
-- 환자명
-- 이메일
-- 패스워드
-- 성별
-- 생년월일

drop table if exists Patients;
create table Patients(
	id int auto_increment comment '환자번호',
    name varchar(128) comment '환자이름',
    email varchar(128),
    password varchar(128),
    birth varchar(128),
    gender tinyint,
    primary key(id)
)charset='utf8';


-- 나의 환자 테이블(MyPatients)
-- 의사번호
-- 환자번호
-- label???


drop table if exists MyPatients;
create table MyPatients(
	id int auto_increment,
    doctorId int comment '의사번호',
    patientId int comment '환자번호',
    label varchar(128) comment '의사가 분류하는 환자그룹명',
    primary key(id)
)charset='utf8';

desc logforyoudb.UsercolMaster ;
select *
  from UsercolMaster;

desc Doctors;
desc Patients;
select *
  from Doctors;
select *
  from Departments;
desc Departments;
select * 
  from Patients;
desc Patients;
insert into Patients(name, email, password) value('a', 'a@com', sha2('a', 256));
insert into Doctors(name, email, password) value('da', 'da@com', sha2('da', 256));
update Doctors set departmentId = 1 where id = 1;

select *
  from DisCode;
desc DisCode;

select *
  from Pat_Usercol;
select *
  from UsercolMaster; 
## 1 2 11 12 18 19 int, str.
desc UsercolMaster;
select *
  from DisCode;
## 311

select * 
  from Usercol_DisCode;
  
insert into Usercol_DisCode(usercol_id, discode_id) values(19, 311);
select *
  from Pat_Usercol;
select * from Usercol_DisCode where discode_id = 311;
insert into Pat_Usercol(pat_id, usercol_id) select 1, usercol_id from Usercol_DisCode;



select *
  from Patients;

 insert into UsercolMaster(col_name, min, max, col_desc) value('기상시간', null, null,'');
  
show grants for 'root'@'localhost';
SELECT @@GLOBAL.sql_mode; 
SET @@GLOBAL.sql_mode = 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
SELECT @@global.sql_mode;

21:14:44	SET @@GLOBAL.sql_mode = 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'	Error Code: 1227. Access denied; you need (at least one of) the SUPER privilege(s) for this operation	0.037 sec
