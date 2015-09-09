drop table if exists members;
drop table if exists status;
drop table if exists friends;
drop table if exists groups;
drop table if exists users;
create table users (userid char(10) unique, name char(20), birthdate date, joined date);
create table groups (groupid char(10) unique, name char(100));
create table friends (userid1 char(10) references users(userid), userid2 char(10) references users(userid));
create table status (userid char(10) references users(userid), status_time date, text char(60));
create table members (userid char(10) references users(userid), groupid char(10) references groups(groupid));
insert into users values ('user0', 'Anthony Roberts', to_date('1979-11-11', 'yyyy-mm-dd'), to_date('2004-01-25', 'yyyy-mm-dd'));
insert into users values ('user1', 'Barbara Rodriguez', to_date('1991-12-04', 'yyyy-mm-dd'), to_date('2003-08-19', 'yyyy-mm-dd'));
insert into users values ('user2', 'Betty Garcia', to_date('1994-06-04', 'yyyy-mm-dd'), to_date('2002-05-24', 'yyyy-mm-dd'));
insert into users values ('user3', 'Carol Jones', to_date('1971-05-13', 'yyyy-mm-dd'), to_date('2003-10-29', 'yyyy-mm-dd'));
insert into users values ('user4', 'Charles Gonzalez', to_date('1976-02-16', 'yyyy-mm-dd'), to_date('2005-06-09', 'yyyy-mm-dd'));
insert into users values ('user5', 'Charles Williams', to_date('1979-07-12', 'yyyy-mm-dd'), to_date('2006-07-27', 'yyyy-mm-dd'));
insert into users values ('user6', 'George Allen', to_date('1979-01-15', 'yyyy-mm-dd'), to_date('2002-05-22', 'yyyy-mm-dd'));
insert into users values ('user7', 'Helen Anderson', to_date('1971-01-06', 'yyyy-mm-dd'), to_date('2002-09-22', 'yyyy-mm-dd'));
insert into users values ('user8', 'James Walker', to_date('1998-09-11', 'yyyy-mm-dd'), to_date('2005-03-31', 'yyyy-mm-dd'));
insert into users values ('user9', 'Jason Taylor', to_date('1992-01-18', 'yyyy-mm-dd'), to_date('2003-07-17', 'yyyy-mm-dd'));
insert into users values ('user10', 'Karen Mitchell', to_date('1981-01-14', 'yyyy-mm-dd'), to_date('2003-07-02', 'yyyy-mm-dd'));
insert into users values ('user11', 'Margaret Smith', to_date('1974-09-22', 'yyyy-mm-dd'), to_date('2006-08-25', 'yyyy-mm-dd'));
insert into users values ('user12', 'Maria Johnson', to_date('1977-01-23', 'yyyy-mm-dd'), to_date('2003-01-19', 'yyyy-mm-dd'));
insert into users values ('user13', 'Maria King', to_date('1997-10-24', 'yyyy-mm-dd'), to_date('2002-09-09', 'yyyy-mm-dd'));
insert into users values ('user14', 'Michael Moore', to_date('1971-03-06', 'yyyy-mm-dd'), to_date('2004-07-20', 'yyyy-mm-dd'));
insert into users values ('user15', 'Sharon Taylor', to_date('1982-09-12', 'yyyy-mm-dd'), to_date('2002-07-12', 'yyyy-mm-dd'));
insert into users values ('user16', 'William Lee', to_date('1990-10-04', 'yyyy-mm-dd'), to_date('2004-02-07', 'yyyy-mm-dd'));
insert into users values ('user17', 'William Parker', to_date('1974-10-19', 'yyyy-mm-dd'), to_date('2005-01-13', 'yyyy-mm-dd'));
insert into groups values ('group0', 'Harvard University USA');
insert into groups values ('group1', 'University of Oxford UK');
insert into groups values ('group2', 'University of Cambridge UK');
insert into groups values ('group3', 'Stanford University USA');
insert into groups values ('group4', 'Massachusetts Institute of Technology USA');
insert into friends values ('user0', 'user1');
insert into friends values ('user1', 'user0');
insert into friends values ('user0', 'user2');
insert into friends values ('user2', 'user0');
insert into friends values ('user0', 'user3');
insert into friends values ('user3', 'user0');
insert into friends values ('user0', 'user4');
insert into friends values ('user4', 'user0');
insert into friends values ('user0', 'user5');
insert into friends values ('user5', 'user0');
insert into friends values ('user0', 'user7');
insert into friends values ('user7', 'user0');
insert into friends values ('user0', 'user8');
insert into friends values ('user8', 'user0');
insert into friends values ('user0', 'user9');
insert into friends values ('user9', 'user0');
insert into friends values ('user0', 'user10');
insert into friends values ('user10', 'user0');
insert into friends values ('user0', 'user17');
insert into friends values ('user17', 'user0');
insert into friends values ('user1', 'user2');
insert into friends values ('user2', 'user1');
insert into friends values ('user1', 'user3');
insert into friends values ('user3', 'user1');
insert into friends values ('user1', 'user4');
insert into friends values ('user4', 'user1');
insert into friends values ('user1', 'user6');
insert into friends values ('user6', 'user1');
insert into friends values ('user1', 'user11');
insert into friends values ('user11', 'user1');
insert into friends values ('user1', 'user12');
insert into friends values ('user12', 'user1');
insert into friends values ('user1', 'user14');
insert into friends values ('user14', 'user1');
insert into friends values ('user2', 'user4');
insert into friends values ('user4', 'user2');
insert into friends values ('user2', 'user7');
insert into friends values ('user7', 'user2');
insert into friends values ('user2', 'user9');
insert into friends values ('user9', 'user2');
insert into friends values ('user2', 'user12');
insert into friends values ('user12', 'user2');
insert into friends values ('user2', 'user13');
insert into friends values ('user13', 'user2');
insert into friends values ('user3', 'user7');
insert into friends values ('user7', 'user3');
insert into friends values ('user3', 'user10');
insert into friends values ('user10', 'user3');
insert into friends values ('user3', 'user14');
insert into friends values ('user14', 'user3');
insert into friends values ('user3', 'user16');
insert into friends values ('user16', 'user3');
insert into friends values ('user4', 'user5');
insert into friends values ('user5', 'user4');
insert into friends values ('user4', 'user6');
insert into friends values ('user6', 'user4');
insert into friends values ('user4', 'user15');
insert into friends values ('user15', 'user4');
insert into friends values ('user4', 'user16');
insert into friends values ('user16', 'user4');
insert into friends values ('user5', 'user6');
insert into friends values ('user6', 'user5');
insert into friends values ('user5', 'user8');
insert into friends values ('user8', 'user5');
insert into friends values ('user5', 'user9');
insert into friends values ('user9', 'user5');
insert into friends values ('user6', 'user15');
insert into friends values ('user15', 'user6');
insert into friends values ('user7', 'user8');
insert into friends values ('user8', 'user7');
insert into friends values ('user8', 'user12');
insert into friends values ('user12', 'user8');
insert into friends values ('user8', 'user13');
insert into friends values ('user13', 'user8');
insert into friends values ('user8', 'user14');
insert into friends values ('user14', 'user8');
insert into friends values ('user9', 'user16');
insert into friends values ('user16', 'user9');
insert into friends values ('user10', 'user11');
insert into friends values ('user11', 'user10');
insert into friends values ('user12', 'user17');
insert into friends values ('user17', 'user12');
insert into friends values ('user13', 'user15');
insert into friends values ('user15', 'user13');
insert into friends values ('user15', 'user17');
insert into friends values ('user17', 'user15');
insert into members values ('user0', 'group3');
insert into members values ('user0', 'group4');
insert into members values ('user1', 'group4');
insert into members values ('user2', 'group0');
insert into members values ('user2', 'group2');
insert into members values ('user2', 'group4');
insert into members values ('user3', 'group1');
insert into members values ('user3', 'group2');
insert into members values ('user4', 'group0');
insert into members values ('user4', 'group1');
insert into members values ('user4', 'group2');
insert into members values ('user5', 'group3');
insert into members values ('user5', 'group4');
insert into members values ('user6', 'group0');
insert into members values ('user6', 'group3');
insert into members values ('user6', 'group4');
insert into members values ('user7', 'group1');
insert into members values ('user7', 'group3');
insert into members values ('user8', 'group0');
insert into members values ('user8', 'group1');
insert into members values ('user8', 'group2');
insert into members values ('user8', 'group3');
insert into members values ('user8', 'group4');
insert into members values ('user9', 'group3');
insert into members values ('user10', 'group0');
insert into members values ('user10', 'group4');
insert into members values ('user11', 'group0');
insert into members values ('user11', 'group4');
insert into members values ('user12', 'group2');
insert into members values ('user12', 'group4');
insert into members values ('user13', 'group0');
insert into members values ('user13', 'group3');
insert into members values ('user14', 'group1');
insert into members values ('user14', 'group4');
insert into members values ('user15', 'group2');
insert into members values ('user15', 'group4');
insert into members values ('user16', 'group4');
insert into members values ('user17', 'group0');
insert into members values ('user17', 'group1');
insert into status values ('user0', to_date('2015-08-21 02:50:37', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user0');
insert into status values ('user0', to_date('2015-08-16 17:45:54', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user0');
insert into status values ('user1', to_date('2015-08-14 23:05:48', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user1');
insert into status values ('user1', to_date('2015-08-21 12:57:59', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user1');
insert into status values ('user1', to_date('2015-08-17 04:45:04', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 2 by user1');
insert into status values ('user2', to_date('2015-08-16 07:13:16', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user2');
insert into status values ('user3', to_date('2015-08-12 07:57:33', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user3');
insert into status values ('user5', to_date('2015-08-12 21:56:50', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user5');
insert into status values ('user5', to_date('2015-08-14 18:03:18', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user5');
insert into status values ('user5', to_date('2015-08-15 21:34:10', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 2 by user5');
insert into status values ('user5', to_date('2015-08-14 14:31:29', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 3 by user5');
insert into status values ('user6', to_date('2015-08-17 06:34:24', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user6');
insert into status values ('user6', to_date('2015-08-19 13:13:55', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user6');
insert into status values ('user7', to_date('2015-08-15 12:53:09', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user7');
insert into status values ('user7', to_date('2015-08-14 21:09:54', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user7');
insert into status values ('user7', to_date('2015-08-16 03:04:15', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 2 by user7');
insert into status values ('user8', to_date('2015-08-18 15:50:17', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user8');
insert into status values ('user8', to_date('2015-08-15 23:03:17', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user8');
insert into status values ('user9', to_date('2015-08-16 09:57:20', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user9');
insert into status values ('user9', to_date('2015-08-18 19:40:40', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user9');
insert into status values ('user11', to_date('2015-08-14 17:59:47', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user11');
insert into status values ('user11', to_date('2015-08-12 10:52:20', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user11');
insert into status values ('user12', to_date('2015-08-19 16:22:24', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user12');
insert into status values ('user12', to_date('2015-08-18 01:27:51', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user12');
insert into status values ('user12', to_date('2015-08-15 11:00:06', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 2 by user12');
insert into status values ('user12', to_date('2015-08-13 06:17:19', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 3 by user12');
insert into status values ('user13', to_date('2015-08-13 14:05:21', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user13');
insert into status values ('user13', to_date('2015-08-18 02:33:09', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user13');
insert into status values ('user15', to_date('2015-08-21 06:02:39', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user15');
insert into status values ('user15', to_date('2015-08-21 05:46:24', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 1 by user15');
insert into status values ('user15', to_date('2015-08-11 21:34:13', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 2 by user15');
insert into status values ('user15', to_date('2015-08-21 01:57:03', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 3 by user15');
insert into status values ('user17', to_date('2015-08-15 19:10:19', 'YYYY-MM-DD HH24:MI:SS'), 'This is status update number 0 by user17');
