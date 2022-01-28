<<<<<<< HEAD
# week5 assignment

## 要求三：SQL CRUD
- insert into member (name,username,password)values('test','test','test');
insert into member 
![Screenshots](screenshot/3-1.jpg)
- select * from member;
![Screenshots](screenshot/3-2.jpg)
- select * from member order by time desc;
![Screenshots](screenshot/3-3.jpg)
- select * from member order by time desc limit 1,3;
![Screenshots](screenshot/3-4.jpg)
- select * from member where username='test';
![Screenshots](screenshot/3-5.jpg)
- select * from member where username='test' and password='test';
![Screenshots](screenshot/3-6.jpg)
- update member set name='test2' where username='test';
![Screenshots](screenshot/3-7.jpg)

## 要求四：SQL Aggregate Functions
- select count(id) from member;
![Screenshots](screenshot/4-1.jpg)
- select sum(follower_count) from member;
![Screenshots](screenshot/4-2.jpg)
- select avg(follower_count) from member;
![Screenshots](screenshot/4-3.jpg)

## 要求五：SQL JOIN (Optional)
- select content,username from member join message on member.id=message.member_id;
![Screenshots](screenshot/5-1.jpg)
- select content,username from member join message on member.id=message.member_id where username='test';
![Screenshots](screenshot/5-2.jpg)
=======
## 要求三：SQL CRUD
```
insert into member (name,username,password)values('test','test','test');
```
![Screenshots](screenshot/3-1.jpg)
```
 select * from member;
 ```
![Screenshots](screenshot/3-2.jpg)
```
select * from member order by time desc;
```
![Screenshots](screenshot/3-3.jpg)
```
select * from member order by time desc limit 1,3;
```
![Screenshots](screenshot/3-4.jpg)
```
select * from member where username='test';
```
![Screenshots](screenshot/3-5.jpg)
```
select * from member where username='test' and password='test';
```
![Screenshots](screenshot/3-6.jpg)
```
update member set name='test2' where username='test';
```
![Screenshots](screenshot/3-7.jpg)

## 要求四：SQL Aggregate Functions
```
select count(id) from member;
```
![Screenshots](screenshot/4-1.jpg)
```
select sum(follower_count) from member;
```
![Screenshots](screenshot/4-2.jpg)
```
select avg(follower_count) from member;
```
![Screenshots](screenshot/4-3.jpg)

## 要求五：SQL JOIN (Optional)
```
select content,username from member join message on member.id=message.member_id;
```
![Screenshots](screenshot/5-1.jpg)
```
select content,username from member join message on member.id=message.member_id where username='test';
```
![Screenshots](screenshot/5-2.jpg)
>>>>>>> 10ba2f2a30c5d6ed73b9e1f6a725a1533b853b03
