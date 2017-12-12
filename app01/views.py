import datetime,json
from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.
def login(req):
    if req.method == 'GET':
        return render(req,'login.html')
    else:
        username = req.POST.get('username')
        password = req.POST.get('password')
        obj = models.UserInfo.objects.filter(username=username,password=password).first()
        if not obj :
            return render(req,'login.html',{'error':'username or password is error !'})
        else:
            # 如果登录成功,把用户信息写进session中.
            req.session['user'] =  {'id':obj.id,'username':username}
            return redirect('/index/')
# def index(req):
#     '''这个使用模版渲染了,逼格没有ajax高,换!'''
#     time_choices = models.Book.time_choices
#     room_list = models.MeetingRoom.objects.all()
#     return render(req,'index.html',{'time_choices':time_choices,'room_list':room_list})
def index(req):
    if req.method == 'GET':
        time_choices = models.Book.time_choices
        return render(req,'index.html',{'time_choices':time_choices})

def booking(request):
    ret = {'status':True,'msg':None,'data':None}
    if request.method == 'GET':
        # print('==================',type(request.session['user']))
        try :
            fetch_date = request.GET.get('date')
            fetch_date = datetime.datetime.strptime(fetch_date,'%Y-%m-%d').date()
            current_date = datetime.datetime.now().date()
            # models.Book.objects.create(book_date=current_time,book_time=7,userinfo_id=1,meetingroom_id=1)
            book_list = models.Book.objects.filter(book_date=fetch_date).select_related('userinfo','meetingroom').order_by('book_time')
            if fetch_date < current_date:
                raise Exception('莫回头,白了少年头!')


            else:
                #######   获取预定信息          ##########
                book_dict = {}
                for b_obj in book_list:
                    '''拿到当前日期的所有预订表对象'''
                    if b_obj.meetingroom_id not in book_dict:
                        book_dict[b_obj.meetingroom_id] = {b_obj.book_time:{'user':b_obj.userinfo.username,'id':b_obj.userinfo.id}}
                    else:
                        if b_obj.book_time not in book_dict[b_obj.meetingroom_id]:
                            book_dict[b_obj.meetingroom_id][b_obj.book_time] = {'user':b_obj.userinfo.username,'id':b_obj.userinfo_id}


    # {
    #     room_id(会议室1) : {
    #         time(时间段1) : {user : username(用户),userid : userid(3)},
    #         time(时间段2) : {user : username(用户),userid : userid(3)},
    #         time(时间段3) : {user : username(用户),userid : userid(3)},
    #               }
    # }
                ###          生成会议室信息         ###
            book_list = []
            room_list = models.MeetingRoom.objects.all()
            for room in room_list:
                '''
                办公室名称1 1 2 3 4 5 6 7 8
                办公室名称2 1 2 3 4 5 6 7 8
                '''
                '''先打印一遍,再进行循环'''
                td_list = [{'title':room.title,'attrs':{}}]
                for time_choices in models.Book.time_choices:

                    '''当房间ID和时间段都存在的话,说明该会议室已经被预定了'''
                    if room.id in book_dict and time_choices[0] in book_dict[room.id]:
                        '''拿到book_dict表中的对应的用户信息'''
                        userinfo = book_dict[room.id][time_choices[0]]  # 用户信息等于 字典里面 会议室id对应的值得时间段id对应的值
                        uid = request.session['user']['id']
                        if userinfo['id'] == uid :
                            # 如果存在,说明是自己的预定,可以删除和修改的
                            td_list.append({'title':'雷机gay','attrs':{'class':'chosen','room_id':room.id,'book_time':time_choices[0]},})
                        else: # 如果不是自己的预定,在属性里面会加一个fuck  这个为了区分,如果是当前登录用户的预定,他是可以对自己的预定做操作的
                            td_list.append({'title':userinfo['user'],'attrs':{'class':'chosen_gun','room_id':room.id,'book_time':time_choices[0],'fuck':'true'}})

                    else: # 如果是没预定的我们要怎么显示它呢?
                        td_list.append({'title':'🎃','attrs':{'room_id':room.id,'book_time':time_choices[0]}})
                book_list.append(td_list)
            ret['data'] = book_list
        except Exception as e :
            ret['msg'] = str(e)
            ret['status'] = False
    # print(ret)
    # [[{'title': '啊', 'attrs': {}}, {'title': '', 'attrs': {'room_id': 1, 'book_time': 1}},
    #   {'title': '', 'attrs': {'room_id': 1, 'book_time': 2}}, {'title': '', 'attrs': {'room_id': 1, 'book_time': 3}},
    #   {'title': '', 'attrs': {'room_id': 1, 'book_time': 4}},
    #   {'title': '雷机gay', 'attrs': {'class': 'chosen', 'room_id': 1, 'book_time': 5}},
    #   {'title': '', 'attrs': {'room_id': 1, 'book_time': 6}},
    #   {'title': '雷机gay', 'attrs': {'class': 'chosen', 'room_id': 1, 'book_time': 7}},
    #   {'title': '雷机gay', 'attrs': {'class': 'chosen', 'room_id': 1, 'book_time': 8}},
    #   {'title': '', 'attrs': {'room_id': 1, 'book_time': 9}}, {'title': '', 'attrs': {'room_id': 1, 'book_time': 10}},
    #   {'title': '', 'attrs': {'room_id': 1, 'book_time': 11}}, {'title': '', 'attrs': {'room_id': 1, 'book_time': 12}}],
    #  [{'title': '喔', 'attrs': {}},
    #   {'title': 'ww', 'attrs': {'class': 'chosen', 'room_id': 2, 'book_time': 1, 'fuck': 'true'}},
    #   {'title': '雷机gay', 'attrs': {'class': 'chosen', 'room_id': 2, 'book_time': 2}},
    #   {'title': '', 'attrs': {'room_id': 2, 'book_time': 3}}, {'title': '', 'attrs': {'room_id': 2, 'book_time': 4}},
    #   {'title': '', 'attrs': {'room_id': 2, 'book_time': 5}}, {'title': '', 'attrs': {'room_id': 2, 'book_time': 6}},
    #   {'title': '', 'attrs': {'room_id': 2, 'book_time': 7}}, {'title': '', 'attrs': {'room_id': 2, 'book_time': 8}},
    #   {'title': '', 'attrs': {'room_id': 2, 'book_time': 9}}, {'title': '', 'attrs': {'room_id': 2, 'book_time': 10}},
    #   {'title': '', 'attrs': {'room_id': 2, 'book_time': 11}}, {'title': '', 'attrs': {'room_id': 2, 'book_time': 12}}],
    #  [{'title': '额', 'attrs': {}}, {'title': '', 'attrs': {'room_id': 3, 'book_time': 1}},
    #   {'title': '', 'attrs': {'room_id': 3, 'book_time': 2}}, {'title': '', 'attrs': {'room_id': 3, 'book_time': 3}},
    #   {'title': '', 'attrs': {'room_id': 3, 'book_time': 4}}, {'title': '', 'attrs': {'room_id': 3, 'book_time': 5}},
    #   {'title': 'ww', 'attrs': {'class': 'chosen', 'room_id': 3, 'book_time': 6, 'fuck': 'true'}},
    #   {'title': '', 'attrs': {'room_id': 3, 'book_time': 7}}, {'title': '', 'attrs': {'room_id': 3, 'book_time': 8}},
    #   {'title': '', 'attrs': {'room_id': 3, 'book_time': 9}}, {'title': '', 'attrs': {'room_id': 3, 'book_time': 10}},
    #   {'title': '', 'attrs': {'room_id': 3, 'book_time': 11}},
    #   {'title': '', 'attrs': {'room_id': 3, 'book_time': 12}}]]}

    return HttpResponse(json.dumps(ret))

# ret  :   [{"title": "agay", "attrs": {"class": "chosen", "room_id": 2, "book_time": 2}},{"title":'未预定',"attrs":{'room_id':2,'book_time':6}}]