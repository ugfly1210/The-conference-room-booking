from django.db import models

# Create your models here.



class UserInfo(models.Model):
    '''用户信息表'''
    username = models.CharField(max_length=16,verbose_name='用户名')
    password = models.CharField(max_length=64,verbose_name='密码')

    def __str__(self):
        return self.username

class MeetingRoom(models.Model):
    '''会议室表'''
    title = models.CharField(verbose_name='会议室名称',max_length=32)
    num = models.IntegerField(verbose_name='可容纳人数',null=True)
    def __str__(self):
        return self.title

'''
一间会议室在同一天的同一时间段只能被订一次
用户和时间是一对多,一个用户可以定多个时间段

'''

class Book(models.Model):
    '''预定表'''
    book_date = models.DateField(verbose_name='预定日期')
    time_choices = (
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
    )
    book_time = models.IntegerField(verbose_name='预定时间',choices=time_choices)

    userinfo = models.ForeignKey(to='UserInfo',verbose_name='用户',on_delete=True)
    meetingroom = models.ForeignKey(to='MeetingRoom',verbose_name='会议室',on_delete=True)
    def __str__(self):
        return str(self.book_date)

    class Meta:
        '''
        联合唯一,同一天同一时间段同一间会议室只能被订一次
        '''
        unique_together = (
            'book_date','book_time','meetingroom'
        )