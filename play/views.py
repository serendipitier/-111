from django.shortcuts import render
from django.http import StreamingHttpResponse, FileResponse, HttpResponse
from gmssl import sm2
from index.models import *
from user.models import MyUser


def playView(request, id):
    if request.user.username:
        uname = request.user.username
        this_user = MyUser.objects.get(username=uname).is_secert
    else:
        this_user = 0

    sec = Document.objects.values('Classification').get(id=id)['Classification']
    if sec > this_user:
        return HttpResponse("非法参数，已报告管理员并记录日志")
    if this_user:
        # 热搜公文
        searchs = Dynamic.objects.select_related('document__label').order_by('-search').all()[:6]
        # 相关公文推荐
        type = Document.objects.values('type').get(id=id)['type']
        relevant = Dynamic.objects.select_related('document').filter(document__type=type).order_by('-plays').all()[:6]
    else:
        searchs = Dynamic.objects.select_related('document__label').filter(document_id__Classification=this_user).order_by('-search').all()[:6]
        type = Document.objects.values('type').get(id=id)['type']
        relevant = Dynamic.objects.select_related('document').filter(document__type=type).filter(document_id__Classification=this_user).order_by('-plays').all()[:6]
    # 公文信息
    documents = Document.objects.get(id=int(id))
    # 观看列表
    play_list = request.session.get('play_list', [])
    exist = False
    if play_list:
        for i in play_list:
            if int(id) == i['id']:
                exist = True
    if exist == False:
        play_list.append({'id': int(id), 'singer': documents.person, 'name': documents.name})
    request.session['play_list'] = play_list
    # 摘要

    if documents.lyrics != '暂无摘要':
        lyrics = str(documents.lyrics.url)[1::]
        with open(lyrics, 'r', encoding='utf-8') as f:
            lyrics = f.read()
    # 添加播放次数
    # 功能扩展：可使用Session实现每天只添加一次播放次数
    p = Dynamic.objects.filter(document_id=int(id)).first()
    plays = p.plays + 1 if p else 1
    Dynamic.objects.update_or_create(document_id=id, defaults={'plays': plays})

    documents = Document.objects.get(id=int(id))
    if documents.key:
        key_b = documents.key
        SM2_PRIVATE_KEY = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
        SM2_PUBLIC_KEY = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
        sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)

        str1_sm2de = sm2_crypt.decrypt(key_b)
        str1_m = str(str1_sm2de, encoding="utf8")
        print(str1_m)

    return render(request, 'play.html', locals())


def downloadView(request, id):
    # 添加下载次数
    p = Dynamic.objects.filter(document_id=int(id)).first()
    download = p.download + 1 if p else 1
    Dynamic.objects.update_or_create(document_id=id, defaults={'download': download})
    # 读取文件内容
    # 根据id查找公文信息
    documents = Document.objects.get(id=int(id))
    file = documents.file.url[1::]
    name = documents.name

    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    # 将文件内容写入StreamingHttpResponse对象
    # 并以字节流方式返回给用户，实现文件下载
    f = name + '.pdf'
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s"' %(f)
    return response


def downloadr(request, id):
    documents = Document.objects.get(id=int(id))
    file = documents.file.url[1::]
    try:
        f = open(file, 'rb')
        # as_attachment为T则可以下载到本机，为F则不可以下载只能浏览
        r = FileResponse(f, as_attachment=False)  # 只支持文件输出
        return r
    except Exception:
        return render(request, '404.html')