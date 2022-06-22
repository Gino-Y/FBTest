import datetime
import json
import math
import random
import time
from decimal import Decimal

import uvicorn
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import final_back_postmodel
import final_back_sqlmodel
import zhenzismsclient as smslicent

app = FastAPI(title="毕业设计接口")
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/sendcode", tags=['app', '用户/app'], summary="验证码发送/app")
async def sendcode(tele):
    nums = math.floor(1e5 * random.random())
    client = smslicent.ZhenziSmsClient('https://sms_developer.zhenzikj.com',
                                       "108024",
                                       "3874ba7b-fe47-46bd-b362-b18f6ef92b2d")
    params = {'number': tele,
              'templateId': '3612',
              'templateParams': [str(nums)]}
    data = final_back_sqlmodel.session.query(final_back_sqlmodel.Code).filter(
        final_back_sqlmodel.Code.tele == tele).all()
    final_back_sqlmodel.session.commit()
    result = json.loads(client.send(params))
    if result['code'] != 0:
        return result
    if result['code'] == 0:
        if len(data) == 0:
            final_back_sqlmodel.session.add(final_back_sqlmodel.Code(tele=tele, code=[str(nums)]))
            final_back_sqlmodel.session.commit()
        else:
            final_back_sqlmodel.session.query(final_back_sqlmodel.Code).filter(
                final_back_sqlmodel.Code.tele == tele).update({final_back_sqlmodel.Code.code: [str(nums)]})
            final_back_sqlmodel.session.commit()
        return result


@app.get("/codelogin", tags=['app', '用户/app'], summary="验证码登录/app")
async def codelogin(tele: int, code: str):
    a = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.UserLive.user_tele == tele).all()
    b = final_back_sqlmodel.session.query(final_back_sqlmodel.Code).filter(
        final_back_sqlmodel.Code.tele == tele).all()
    final_back_sqlmodel.session.commit()
    if len(a) == 0:
        return json.loads('{"msg":"此账号未注册"}')
    else:
        if a[0].user_statue == 0:
            return json.loads('{"msg":"此账号正在审核中"}')
        if a[0].user_statue == 1:
            if code == b[0].code:
                return json.loads('{"msg":"登陆成功"}')
            else:
                return json.loads('{"msg":"验证码错误，登陆失败"}')
        if a[0].user_statue == 2:
            return json.loads('{"msg":"此账号审核未通过"}')


@app.get("/liverlogin", tags=['app', '用户/app'], summary="用户密码登录/app")
async def userlogin(username: int, pwd: str):
    a = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.UserLive.user_tele == username).all()
    final_back_sqlmodel.session.commit()
    if len(a) == 0:
        return json.loads('{"msg":"此账号未注册"}')
    else:
        if a[0].user_statue == 0:
            return json.loads('{"msg":"此账号正在审核中"}')
        if a[0].user_statue == 1:
            if pwd == a[0].user_pwd:
                return json.loads('{"msg":"登陆成功"}')
            else:
                return json.loads('{"msg":"密码错误，登陆失败"}')
        if a[0].user_statue == 2:
            return json.loads('{"msg":"此账号审核未通过"}')


@app.get("/pclogin", tags=['PC', '用户/app'], summary="后台管理员登录/PC")
async def pclogin(username: str, password: str):
    data = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLogin).filter(
        final_back_sqlmodel.UserLogin.username == username).all()
    final_back_sqlmodel.session.commit()
    if len(data) == 0:
        return json.loads('{"code":2,"msg":"无此账号信息"}')
    else:
        if data[0].password == password:
            return json.loads('{"code":0,"msg":"登陆成功"}')
        else:
            return json.loads('{"code":1,"msg":"密码错误"}')


@app.post("/addliver", tags=['app', '用户/app'], summary="用户注册/app")
async def addliver(args: final_back_postmodel.UserLive):
    try:
        final_back_sqlmodel.session.add(final_back_sqlmodel.UserLive(user_name=args.uname,
                                                                     user_tele=args.utele,
                                                                     user_time=args.utime,
                                                                     user_build=args.ubuild,
                                                                     user_measure=args.umeasure,
                                                                     user_pwd=args.upwd,
                                                                     user_statue=0
                                                                     ))
        final_back_sqlmodel.session.commit()
        return json.loads('{"code":1,"msg":"加入成功,我们将尽快为您审核"}')
    except:
        final_back_sqlmodel.session.rollback()
        return json.loads('{"code":0,"msg":"手机号已经被注册"}')


@app.post("/delliver", tags=["用户", 'PC', '用户/PC'], summary="删除用户/PC")
async def delliver(item: final_back_postmodel.UserLive):
    final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.UserLive.user_tele == item.utele).delete()
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"删除成功"}')


@app.post("/updliver", tags=['PC', '用户/PC'], summary="修改用户/PC")
async def updliver(item: final_back_postmodel.UserLive):
    final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.UserLive.user_tele == item.utele).update(
        {final_back_sqlmodel.UserLive.user_name: item.uname,
         final_back_sqlmodel.UserLive.user_tele: item.utele,
         final_back_sqlmodel.UserLive.user_time: item.utime,
         final_back_sqlmodel.UserLive.user_measure: item.umeasure,
         final_back_sqlmodel.UserLive.user_build: item.ubuild,
         final_back_sqlmodel.UserLive.user_statue: item.ustatue
         })
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"修改成功"}')


@app.get("/condliver", tags=['PC', '用户/PC'], summary="条件查询用户/PC")
async def condliver(page_index: int, uname: str = Query(None, min_length=0), utele: str = Query(None, min_length=0),
                    utime: str = Query(None, min_length=0), ustatue: str = Query(None, min_length=0)):
    json = []
    jsondata2 = {}
    thiscon = ["user_name", "user_tele", "user_time", "user_statue"]
    condition = [uname, utele, utime, ustatue]
    fil = ""
    for item in condition:
        if item != None:
            if len(item) != 0:
                fil = fil + thiscon[condition.index(item)] + "=" + '"' + str(item) + '"' + " and "
    fil = fil.strip(" and ")
    jsondata2['count'] = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.text(fil)).count()
    final_back_sqlmodel.session.commit()
    thisdata = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive.user_name,
                                                 final_back_sqlmodel.UserLive.user_tele,
                                                 final_back_sqlmodel.UserLive.user_time,
                                                 final_back_sqlmodel.UserLive.user_build,
                                                 final_back_sqlmodel.UserLive.user_measure,
                                                 final_back_sqlmodel.UserLive.user_statue).filter(
        final_back_sqlmodel.text(fil)).limit(2).offset((page_index - 1) * 2).all()
    for item in thisdata:
        jsondata = {}
        jsondata['name'] = item[0]
        jsondata['tele'] = item[1]
        jsondata['date'] = item[2]
        jsondata['build'] = item[3]
        jsondata['measure'] = item[4]
        jsondata['statue'] = item[5]
        json.append(jsondata)
    jsondata2['rows'] = json
    final_back_sqlmodel.session.commit()
    return jsondata2


@app.post("/addwaterfee", tags=['PC', '水费操作/PC'], summary="录入水费（pc端）")
async def addwaterfee(args: final_back_postmodel.WaFree, ard: final_back_postmodel.UserLive):
    a = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.UserLive.user_tele == ard.utele).all()
    final_back_sqlmodel.session.commit()
    if len(a) == 0:
        return json.loads('{"code":"1","msg":"此账号未注册"}')
    else:
        if a[0].user_statue == 0:
            return json.loads('{"code":"1","msg":"此账号正在审核中"}')
        if a[0].user_statue == 1:
            b = final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees).filter(
                final_back_sqlmodel.WaterFees.wa_user_id == ard.utele,
                final_back_sqlmodel.WaterFees.wa_date == args.wfdate).all()
            final_back_sqlmodel.session.commit()
            if len(b) == 0:
                final_back_sqlmodel.session.add(
                    final_back_sqlmodel.WaterFees(wa_user_id=ard.utele, wa_date=args.wfdate, wa_num=args.wfnum,
                                                  wa_pay=0))
                final_back_sqlmodel.session.commit()
                return json.loads('{"code":"0","msg":"数据添加成功"}')
            else:
                return json.loads('{"code":"1","msg":"相同月份数据已经录入"}')
        if a[0].user_statue == 2:
            return json.loads('{"code":"1","msg":"此账号审核未通过"}')


@app.post("/updwafee", tags=['PC', '水费操作/PC'], summary="修改水费（pc端）")
async def updwafee(args: final_back_postmodel.WaFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees).filter(
        final_back_sqlmodel.WaterFees.wa_id == args.wfid).update({final_back_sqlmodel.WaterFees.wa_num: args.wfnum})
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"修改成功"}')


@app.get("/condwafee", tags=['PC', '水费操作/PC'], summary="查询水费（pc端）")
async def condwafee(page_index: int, utele: str = Query(None, min_length=0), wdate: str = Query(None, min_length=0),
                    wpay: str = Query(None, min_length=0)):
    json = []
    jsondata2 = {}
    thiscon = ["live_user.user_tele", "water_fees.wa_date", "water_fees.wa_pay"]
    condition = [utele, wdate, wpay]
    fil = " and "
    for item in condition:
        if item != None:
            if item != "":
                fil = fil + thiscon[condition.index(item)] + "=" + '"' + str(item) + '"' + " and "
    fil = fil.strip(" and ")
    jsondata2['count'] = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive,
                                                           final_back_sqlmodel.WaterFees).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.WaterFees.wa_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "水费", final_back_sqlmodel.text(fil)).count()
    thisdata = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive.user_name,
                                                 final_back_sqlmodel.UserLive.user_tele,
                                                 final_back_sqlmodel.WaterFees.wa_num,
                                                 final_back_sqlmodel.WaterFees.wa_date,
                                                 final_back_sqlmodel.WaterFees.wa_num * final_back_sqlmodel.ChargingStandard.cs_standard,
                                                 final_back_sqlmodel.WaterFees.wa_pay,
                                                 final_back_sqlmodel.WaterFees.wa_id,
                                                 final_back_sqlmodel.WaterFees.wa_hadpay,
                                                 final_back_sqlmodel.WaterFees.wa_payday
                                                 ).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.WaterFees.wa_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "水费", final_back_sqlmodel.text(fil)).order_by(
        final_back_sqlmodel.desc(final_back_sqlmodel.WaterFees.wa_id)).limit(6).offset((page_index - 1) * 6).all()
    for item in thisdata:
        jsondata = {}
        jsondata['name'] = item[0]
        jsondata['tele'] = item[1]
        jsondata['num'] = item[2]
        jsondata['date'] = item[3]
        jsondata['money'] = item[4]
        jsondata['ispay'] = item[5]
        jsondata['id'] = item[6]
        jsondata["hadpay"] = item[7]
        jsondata["payday"] = item[8]
        json.append(jsondata)
    jsondata2['rows'] = json
    final_back_sqlmodel.session.commit()
    return jsondata2


@app.post("/delwafee", tags=['PC', '水费操作/PC'], summary="删除水费（pc端）")
async def delwafee(arg: final_back_postmodel.WaFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees).filter(
        final_back_sqlmodel.WaterFees.wa_id == arg.wfid).delete()
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"删除成功"}')


@app.post("/paywafee", tags=['app', '水费操作/app'], summary="交纳水费（app端）")
async def paywafee(arg: final_back_postmodel.WaFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees).filter(
        final_back_sqlmodel.WaterFees.wa_id == arg.wfid).update(
        {final_back_sqlmodel.WaterFees.wa_pay: 1, final_back_sqlmodel.WaterFees.wa_hadpay: arg.wfhadpay,
         final_back_sqlmodel.WaterFees.wa_payday: datetime.datetime.now().strftime('%Y-%m-%d')})
    final_back_sqlmodel.session.commit()
    return json.loads('{"msg":"交费成功"}')


@app.get("/condelfee", tags=['PC', '电费操作/PC'], summary="查询电费（pc端）")
async def condelfee(page_index: int, utele: str = Query(None, min_length=0), edate: str = Query(None, min_length=0),
                    wpay: str = Query(None, min_length=0)):
    json = []
    jsondata2 = {}
    thiscon = ["live_user.user_tele", "electricity_fees.ef_date", "electricity_fees.ef_pay"]
    condition = [utele, edate, wpay]
    print(condition)
    fil = " and "
    for item in condition:
        if item != None:
            if len(item) != 0:
                fil = fil + thiscon[condition.index(item)] + "=" + '"' + str(item) + '"' + " and "
    fil = fil.strip(" and ")
    jsondata2['count'] = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive,
                                                           final_back_sqlmodel.ElectricityFees).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.ElectricityFees.ef_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "电费", final_back_sqlmodel.text(fil)).count()
    thisdata = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive.user_name,
                                                 final_back_sqlmodel.UserLive.user_tele,
                                                 final_back_sqlmodel.ElectricityFees.ef_num,
                                                 final_back_sqlmodel.ElectricityFees.ef_date,
                                                 final_back_sqlmodel.ElectricityFees.ef_num * final_back_sqlmodel.ChargingStandard.cs_standard,
                                                 final_back_sqlmodel.ElectricityFees.ef_pay,
                                                 final_back_sqlmodel.ElectricityFees.ef_id,
                                                 final_back_sqlmodel.ElectricityFees.ef_hadpay,
                                                 final_back_sqlmodel.ElectricityFees.ef_payday
                                                 ).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.ElectricityFees.ef_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "电费", final_back_sqlmodel.text(fil)).order_by(
        final_back_sqlmodel.desc(final_back_sqlmodel.ElectricityFees.ef_id)).limit(6).offset((page_index - 1) * 6).all()
    for item in thisdata:
        jsondata = {}
        jsondata['name'] = item[0]
        jsondata['tele'] = item[1]
        jsondata['num'] = item[2]
        jsondata['date'] = item[3]
        jsondata['money'] = item[4]
        jsondata['ispay'] = item[5]
        jsondata['id'] = item[6]
        jsondata["hadpay"] = item[7]
        jsondata["payday"] = item[8]
        json.append(jsondata)
    jsondata2['rows'] = json
    final_back_sqlmodel.session.commit()
    return jsondata2


@app.post("/addelfee", tags=['PC', '电费操作/PC'], summary="录入电费（pc端）")
async def addelfee(ard: final_back_postmodel.UserLive, args: final_back_postmodel.EleFree):
    a = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.UserLive.user_tele == ard.utele).all()
    final_back_sqlmodel.session.commit()
    if len(a) == 0:
        return json.loads('{"code":"1","msg":"此账号未注册"}')
    else:
        if a[0].user_statue == 0:
            return json.loads('{"code":"1","msg":"此账号正在审核中"}')
        if a[0].user_statue == 1:
            b = final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees).filter(
                final_back_sqlmodel.ElectricityFees.ef_user_id == ard.utele,
                final_back_sqlmodel.ElectricityFees.ef_date == args.efdate).all()
            final_back_sqlmodel.session.commit()
            if len(b) == 0:
                final_back_sqlmodel.session.add(
                    final_back_sqlmodel.ElectricityFees(ef_user_id=ard.utele, ef_date=args.efdate, ef_num=args.efnum,
                                                        ef_pay=0))
                final_back_sqlmodel.session.commit()
                return json.loads('{"code":"0","msg":"数据添加成功"}')
            else:
                return json.loads('{"code":"1","msg":"相同月份数据已经录入"}')
        if a[0].user_statue == 2:
            return json.loads('{"code":"1","msg":"此账号审核未通过"}')


@app.post("/updelfee", tags=['PC', '电费操作/PC'], summary="修改电费（pc端）")
async def updelfee(args: final_back_postmodel.EleFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees).filter(
        final_back_sqlmodel.ElectricityFees.ef_id == args.efid).update(
        {final_back_sqlmodel.ElectricityFees.ef_num: args.efnum})
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"修改成功"}')


@app.post("/deelfee", tags=['PC', '电费操作/PC'], summary="删除电费（pc端）")
async def delelfee(arg: final_back_postmodel.EleFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees).filter(
        final_back_sqlmodel.ElectricityFees.ef_id == arg.efid).delete()
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"删除成功"}')


@app.get("/appcondwafee", tags=['app', '水费操作/app'], summary="查询水费（app端）")
async def appcondwafee(utele: str, wpay: str = None):
    json = []
    jsondata2 = {}
    thiscon = ["live_user.user_tele", "water_fees.wa_pay"]
    condition = [utele, wpay]
    fil = " and "
    for item in condition:
        if item != None:
            fil = fil + thiscon[condition.index(item)] + " in" + '(' + str(item) + ')' + " and "
    fil = fil.strip(" and ")
    jsondata2['count'] = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive,
                                                           final_back_sqlmodel.WaterFees).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.WaterFees.wa_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "水费", final_back_sqlmodel.text(fil)).count()
    thisdata = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive.user_name,
                                                 final_back_sqlmodel.UserLive.user_tele,
                                                 final_back_sqlmodel.WaterFees.wa_num,
                                                 final_back_sqlmodel.WaterFees.wa_date,
                                                 final_back_sqlmodel.WaterFees.wa_num * final_back_sqlmodel.ChargingStandard.cs_standard,
                                                 final_back_sqlmodel.WaterFees.wa_pay,
                                                 final_back_sqlmodel.WaterFees.wa_id,
                                                 final_back_sqlmodel.WaterFees.wa_hadpay,
                                                 final_back_sqlmodel.WaterFees.wa_payday
                                                 ).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.WaterFees.wa_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "水费", final_back_sqlmodel.text(fil)).all()
    for item in thisdata:
        jsondata = {}
        jsondata['name'] = item[0]
        jsondata['tele'] = item[1]
        jsondata['num'] = item[2]
        jsondata['date'] = item[3]
        jsondata['money'] = item[4]
        jsondata['ispay'] = item[5]
        jsondata['id'] = item[6]
        jsondata["hadpay"] = item[7]
        jsondata["payday"] = item[8]
        json.append(jsondata)
    jsondata2['rows'] = json
    final_back_sqlmodel.session.commit()
    return jsondata2


@app.get("/appcondelfee", tags=['app', '水费操作/app'], summary="查询电费（app端）")
async def appcondelfee(utele: str, wpay: str = None):
    json = []
    jsondata2 = {}
    thiscon = ["live_user.user_tele", "electricity_fees.ef_pay"]
    condition = [utele, wpay]
    fil = " and "
    for item in condition:
        if item != None:
            fil = fil + thiscon[condition.index(item)] + " in" + '(' + str(item) + ')' + " and "
    fil = fil.strip(" and ")
    jsondata2['count'] = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive,
                                                           final_back_sqlmodel.ElectricityFees).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.ElectricityFees.ef_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "电费", final_back_sqlmodel.text(fil)).count()
    thisdata = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive.user_name,
                                                 final_back_sqlmodel.UserLive.user_tele,
                                                 final_back_sqlmodel.ElectricityFees.ef_num,
                                                 final_back_sqlmodel.ElectricityFees.ef_date,
                                                 final_back_sqlmodel.ElectricityFees.ef_num * final_back_sqlmodel.ChargingStandard.cs_standard,
                                                 final_back_sqlmodel.ElectricityFees.ef_pay,
                                                 final_back_sqlmodel.ElectricityFees.ef_id,
                                                 final_back_sqlmodel.ElectricityFees.ef_hadpay,
                                                 final_back_sqlmodel.ElectricityFees.ef_payday
                                                 ).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.ElectricityFees.ef_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "水费", final_back_sqlmodel.text(fil)).all()
    for item in thisdata:
        jsondata = {}
        jsondata['name'] = item[0]
        jsondata['tele'] = item[1]
        jsondata['num'] = item[2]
        jsondata['date'] = item[3]
        jsondata['money'] = item[4]
        jsondata['ispay'] = item[5]
        jsondata['id'] = item[6]
        jsondata["hadpay"] = item[7]
        jsondata["payday"] = item[8]
        json.append(jsondata)
    jsondata2['rows'] = json
    final_back_sqlmodel.session.commit()
    return jsondata2


@app.post("/payelfee", tags=['app', '水费操作/app'], summary="交纳电费（app端）")
async def payelfee(arg: final_back_postmodel.EleFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees).filter(
        final_back_sqlmodel.ElectricityFees.ef_id == arg.efid).update(
        {final_back_sqlmodel.ElectricityFees.ef_pay: 1, final_back_sqlmodel.ElectricityFees.ef_hadpay: arg.efhadpay,
         final_back_sqlmodel.ElectricityFees.ef_payday: datetime.datetime.now().strftime('%Y-%m-%d')})
    final_back_sqlmodel.session.commit()
    return json.loads('{"msg":"交费成功"}')


@app.get("/appcondprfee", tags=['app', '物业费操作/app'], summary="查询物业费（app端）")
async def appcondprfee(utele: str, wpay: str = None):
    json = []
    jsondata2 = {}
    thiscon = ["live_user.user_tele", "property_fees.pr_pay"]
    condition = [utele, wpay]
    fil = " and "
    for item in condition:
        if item != None:
            fil = fil + thiscon[condition.index(item)] + " in" + '(' + str(item) + ')' + " and "
    fil = fil.strip(" and ")
    jsondata2['count'] = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive,
                                                           final_back_sqlmodel.PropertyFees).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.PropertyFees.pr_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "物业费", final_back_sqlmodel.text(fil)).count()
    thisdata = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive.user_name,
                                                 final_back_sqlmodel.UserLive.user_tele,
                                                 final_back_sqlmodel.PropertyFees.pr_date,
                                                 final_back_sqlmodel.UserLive.user_measure,
                                                 final_back_sqlmodel.UserLive.user_measure * final_back_sqlmodel.ChargingStandard.cs_standard,
                                                 final_back_sqlmodel.PropertyFees.pr_pay,
                                                 final_back_sqlmodel.PropertyFees.pr_id,
                                                 final_back_sqlmodel.PropertyFees.pr_hadpay,
                                                 final_back_sqlmodel.PropertyFees.pr_payday
                                                 ).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.PropertyFees.pr_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "物业费", final_back_sqlmodel.text(fil)).all()
    for item in thisdata:
        jsondata = {}
        jsondata['name'] = item[0]
        jsondata['tele'] = item[1]
        jsondata['date'] = item[2]
        jsondata['measure'] = item[3]
        jsondata['money'] = item[4]
        jsondata['ispay'] = item[5]
        jsondata['id'] = item[6]
        jsondata["hadpay"] = item[7]
        jsondata["payday"] = item[8]
        json.append(jsondata)
    jsondata2['rows'] = json
    final_back_sqlmodel.session.commit()
    return jsondata2


@app.get("/condprfee", tags=['PC', '物业费操作/PC'], summary="查询物业费（pc端）")
async def condprfee(page_index: int, utele: str = Query(None, min_length=0), pdate: str = Query(None, min_length=0),
                    wpay: str = Query(None, min_length=0)):
    json = []
    jsondata2 = {}
    thiscon = ["live_user.user_tele", "property_fees.pr_date", "property_fees.pr_pay"]
    condition = [utele, pdate, wpay]
    fil = " and "
    for item in condition:
        if item != None:
            if item != "":
                fil = fil + thiscon[condition.index(item)] + "=" + '"' + str(item) + '"' + " and "
    fil = fil.strip(" and ")
    jsondata2['count'] = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive,
                                                           final_back_sqlmodel.PropertyFees).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.PropertyFees.pr_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "物业费", final_back_sqlmodel.text(fil)).count()
    thisdata = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive.user_name,
                                                 final_back_sqlmodel.UserLive.user_tele,
                                                 final_back_sqlmodel.PropertyFees.pr_date,
                                                 final_back_sqlmodel.UserLive.user_measure,
                                                 final_back_sqlmodel.UserLive.user_measure * final_back_sqlmodel.ChargingStandard.cs_standard,
                                                 final_back_sqlmodel.PropertyFees.pr_pay,
                                                 final_back_sqlmodel.PropertyFees.pr_id,
                                                 final_back_sqlmodel.PropertyFees.pr_hadpay,
                                                 final_back_sqlmodel.PropertyFees.pr_payday
                                                 ).filter(
        final_back_sqlmodel.UserLive.user_tele == final_back_sqlmodel.PropertyFees.pr_user_id,
        final_back_sqlmodel.ChargingStandard.cs_kind == "物业费", final_back_sqlmodel.text(fil)).order_by(
        final_back_sqlmodel.desc(final_back_sqlmodel.PropertyFees.pr_id)).limit(6).offset(
        (page_index - 1) * 6).all()
    print(len(thisdata))
    for item in thisdata:
        jsondata = {}
        jsondata['name'] = item[0]
        jsondata['tele'] = item[1]
        jsondata['date'] = item[2]
        jsondata['measure'] = item[3]
        jsondata['money'] = item[4]
        jsondata['ispay'] = item[5]
        jsondata['id'] = item[6]
        jsondata["hadpay"] = item[7]
        jsondata["payday"] = item[8]
        json.append(jsondata)
    jsondata2['rows'] = json
    final_back_sqlmodel.session.commit()
    return jsondata2


@app.post("/addprfee", tags=['PC', '物业费操作/PC'], summary="录入物业费（pc端）")
async def addprfee(args: final_back_postmodel.PrFree, ard: final_back_postmodel.UserLive):
    a = final_back_sqlmodel.session.query(final_back_sqlmodel.UserLive).filter(
        final_back_sqlmodel.UserLive.user_tele == ard.utele).all()
    final_back_sqlmodel.session.commit()
    if len(a) == 0:
        return json.loads('{"code":"1","msg":"此账号未注册"}')
    else:
        if a[0].user_statue == 0:
            return json.loads('{"code":"1","msg":"此账号正在审核中"}')
        if a[0].user_statue == 1:
            b = final_back_sqlmodel.session.query(final_back_sqlmodel.PropertyFees).filter(
                final_back_sqlmodel.PropertyFees.pr_user_id == ard.utele,
                final_back_sqlmodel.PropertyFees.pr_date == args.pfdate).all()
            final_back_sqlmodel.session.commit()
            if len(b) == 0:
                final_back_sqlmodel.session.add(
                    final_back_sqlmodel.PropertyFees(pr_user_id=ard.utele, pr_date=args.pfdate, pr_pay=0))
                final_back_sqlmodel.session.commit()
                return json.loads('{"code":"0","msg":"数据添加成功"}')
            else:
                return json.loads('{"code":"1","msg":"相同月份数据已经录入"}')
        if a[0].user_statue == 2:
            return json.loads('{"code":"1","msg":"此账号审核未通过"}')


@app.post("/updprfee", tags=['PC', '物业费操作/PC'], summary="修改物业费（pc端）")
async def upprfee(arg: final_back_postmodel.PrFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.PropertyFees).filter(
        final_back_sqlmodel.PropertyFees.pr_id == arg.pfid).delete()
    final_back_sqlmodel.session.commit()


@app.post("/payprfee", tags=['app', '物业费操作/app'], summary="交纳物业费（app端）")
async def payprfee(arg: final_back_postmodel.PrFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.PropertyFees).filter(
        final_back_sqlmodel.PropertyFees.pr_id == arg.pfid).update(
        {final_back_sqlmodel.PropertyFees.pr_pay: 1, final_back_sqlmodel.PropertyFees.pr_hadpay: arg.pfhadpay,
         final_back_sqlmodel.PropertyFees.pr_payday: datetime.datetime.now().strftime('%Y-%m-%d')})
    final_back_sqlmodel.session.commit()
    return json.loads('{"msg":"交费成功"}')


@app.post("/delprfee", tags=['PC', '物业费操作/PC'], summary="删除物业费（pc端）")
async def delprfee(arg: final_back_postmodel.PrFree):
    final_back_sqlmodel.session.query(final_back_sqlmodel.PropertyFees).filter(
        final_back_sqlmodel.PropertyFees.pr_id == arg.pfid).delete()
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"删除成功"}')


@app.get("/selectnouse", tags=['PC', '停车位操作/PC'], summary="查询未用车位")
async def selectnouse(page_index: int):
    num = final_back_sqlmodel.session.query(final_back_sqlmodel.Parking).filter(
        final_back_sqlmodel.Parking.is_used == 0).order_by(
        final_back_sqlmodel.desc(final_back_sqlmodel.Parking.pa_id)).limit(6).offset((page_index - 1) * 6).all()
    datacount = final_back_sqlmodel.session.query(final_back_sqlmodel.Parking).filter(
        final_back_sqlmodel.Parking.is_used == 0).count()
    jsondata = {}
    jsondata['datacount'] = datacount
    jsondata['num'] = num
    return jsondata


@app.get("/selectaluse", tags=['PC', '停车位操作/PC'], summary="查询已用车位")
async def selectaluse(page_index: int):
    datanum = []
    num = final_back_sqlmodel.session.query(final_back_sqlmodel.Parking.pa_id, final_back_sqlmodel.Parking.pa_fooler,
                                            final_back_sqlmodel.ParkingFees.pf_id,
                                            final_back_sqlmodel.ParkingFees.pf_user_tele,
                                            final_back_sqlmodel.ParkingFees.pf_user_carnum,
                                            final_back_sqlmodel.ParkingFees.pf_starttime).filter(
        final_back_sqlmodel.Parking.pa_id == final_back_sqlmodel.ParkingFees.pa_id,
        final_back_sqlmodel.Parking.is_used == 1, final_back_sqlmodel.ParkingFees.pf_money == None).limit(6).offset(
        (page_index - 1) * 6).all()
    datacount = final_back_sqlmodel.session.query(final_back_sqlmodel.Parking, final_back_sqlmodel.ParkingFees).filter(
        final_back_sqlmodel.Parking.pa_id == final_back_sqlmodel.ParkingFees.pa_id,
        final_back_sqlmodel.Parking.is_used == 1).count()
    final_back_sqlmodel.session.commit()
    for item in num:
        numdata = {}
        numdata['pa_id'] = item[0]
        numdata['pa_floor'] = item[1]
        numdata['pf_id'] = item[2]
        numdata['tele'] = item[3]
        numdata['carnum'] = item[4]
        numdata['starttime'] = str(item[5])
        datanum.append(numdata)
    jsondata = {}
    jsondata['datacount'] = datacount
    jsondata['datanum'] = datanum
    print(jsondata)
    return jsondata


@app.get("/selectchange", tags=['PC', '停车位操作/PC'], summary="查询停车位单价")
async def selectchange():
    data = final_back_sqlmodel.session.query(final_back_sqlmodel.ChargingStandard.cs_standard).filter(
        final_back_sqlmodel.ChargingStandard.cs_kind == "停车费").all()
    final_back_sqlmodel.session.commit()
    return data


@app.get("/selecthistory", tags=['PC', '停车位操作/PC'], summary="查询停车位历史")
async def selectchange(page_index: int):
    data = final_back_sqlmodel.session.query(final_back_sqlmodel.ParkingFees).filter(
        final_back_sqlmodel.ParkingFees.pf_money.isnot(None)).limit(6).offset((page_index - 1) * 6).all()
    datacount = final_back_sqlmodel.session.query(final_back_sqlmodel.ParkingFees).filter(
        final_back_sqlmodel.ParkingFees.pf_money.isnot(None)).count()
    jsondata = {}
    jsondata['datacount'] = datacount
    jsondata['datanum'] = data
    return jsondata


@app.post("/usepaking", tags=['PC', '停车位操作/PC'], summary="使用车位")
async def usepaking(ard: final_back_postmodel.Pakingfee):
    final_back_sqlmodel.session.query(final_back_sqlmodel.Parking).filter(
        final_back_sqlmodel.Parking.pa_id == ard.paid).update({final_back_sqlmodel.Parking.is_used: 1})
    final_back_sqlmodel.session.add(
        final_back_sqlmodel.ParkingFees(pa_id=ard.paid, pf_user_tele=ard.pftele, pf_user_carnum=ard.pfcarnum,
                                        pf_starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        pf_stoptime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"停车位使用成功"}')


@app.post("/addpaking", tags=['PC', '停车位操作/PC'], summary="添加车位")
async def addpaking(ard: final_back_postmodel.Paking):
    final_back_sqlmodel.session.add(final_back_sqlmodel.Parking(pa_fooler=ard.pa_fooler, is_used=0))
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"停车位使用成功"}')


@app.post("/stopparking", tags=['PC', '停车位操作/PC'], summary="结束用车位")
async def stopparking(ard: final_back_postmodel.Pakingfee):
    final_back_sqlmodel.session.query(final_back_sqlmodel.Parking).filter(
        final_back_sqlmodel.Parking.pa_id == ard.paid).update({final_back_sqlmodel.Parking.is_used: 0})
    final_back_sqlmodel.session.query(final_back_sqlmodel.ParkingFees).filter(
        final_back_sqlmodel.ParkingFees.pf_id == ard.pfid).update(
        {final_back_sqlmodel.ParkingFees.pf_money: ard.pfmoney, final_back_sqlmodel.ParkingFees.pf_hour: ard.pfhour,
         final_back_sqlmodel.ParkingFees.pf_stoptime: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"缴费成功"}')


@app.get("/pushfee", tags=['PC', '杂项数据/PC'], summary="催缴费用")
async def pushfee(fid: str, tele: int, feekind: str, money: str):
    client = smslicent.ZhenziSmsClient('https://sms_developer.zhenzikj.com', "108024",
                                       "3874ba7b-fe47-46bd-b362-b18f6ef92b2d")
    params = {'number': tele, 'templateId': '3526', 'templateParams': [feekind, str(money)]}
    result = json.loads(client.send(params))
    if result['code'] != 0:
        return result
    if result['code'] == 0:
        if feekind == "电":
            final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees).filter(
                final_back_sqlmodel.ElectricityFees.ef_id == fid).update(
                {final_back_sqlmodel.ElectricityFees.ef_pay: 2})
            final_back_sqlmodel.session.commit()
        if feekind == "水":
            final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees).filter(
                final_back_sqlmodel.WaterFees.wa_id == fid).update({final_back_sqlmodel.WaterFees.wa_pay: 2})
            final_back_sqlmodel.session.commit()
        return json.loads('{"code":"0","msg":"催缴费用成功"}')


@app.get("/carddata", tags=['PC', '杂项数据/PC'], summary="卡片数据展示")
async def carddata():
    elfee_pass = final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees).filter(
        final_back_sqlmodel.ElectricityFees.ef_pay == "1").count()
    elfee = final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees).count()
    wafee_pass = final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees).filter(
        final_back_sqlmodel.WaterFees.wa_pay == "1").count()
    wafee = final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees).count()
    prfee_pass = final_back_sqlmodel.session.query(final_back_sqlmodel.PropertyFees).filter(
        final_back_sqlmodel.PropertyFees.pr_pay == "1").count()
    prfee = final_back_sqlmodel.session.query(final_back_sqlmodel.PropertyFees).count()
    paking_use = final_back_sqlmodel.session.query(final_back_sqlmodel.Parking).filter(
        final_back_sqlmodel.Parking.is_used == 1).count()
    paking = final_back_sqlmodel.session.query(final_back_sqlmodel.Parking).count()
    final_back_sqlmodel.session.commit()
    jsondata = [{}, {}, {}, {}]
    jsondata[0]["pass"] = elfee_pass
    jsondata[0]["total"] = elfee
    jsondata[0]["percent"] = Decimal(elfee_pass / elfee).quantize(Decimal("0.00")) * 100
    jsondata[0]["code"] = "电"
    jsondata[1]["pass"] = wafee_pass
    jsondata[1]["total"] = wafee
    jsondata[1]["percent"] = Decimal(wafee_pass / wafee).quantize(Decimal("0.00")) * 100
    jsondata[1]["code"] = "水"
    jsondata[2]["pass"] = prfee_pass
    jsondata[2]["total"] = prfee
    jsondata[2]["percent"] = Decimal(prfee_pass / prfee).quantize(Decimal("0.00")) * 100
    jsondata[2]["code"] = "物业"
    jsondata[3]["pass"] = paking_use
    jsondata[3]["total"] = paking
    jsondata[3]["percent"] = Decimal(paking_use / paking).quantize(Decimal("0.00")) * 100
    jsondata[3]["code"] = "停车场"
    return jsondata


@app.get("/chartdata", tags=['PC', '杂项数据/PC'], summary="折线统计图数据展示")
async def chartdata():
    INSPECT_MONTH = 6
    output = []

    def generate_months(t: datetime.datetime = None):
        t = t or datetime.datetime.now()
        ret = []
        for i in range(INSPECT_MONTH):
            ret.append((t - relativedelta(months=i)).strftime("%Y-%m"))
        return ret[::-1]

    def generate_efoutput(raw_data):
        months = generate_months()
        raw_data = dict(raw_data)
        print(raw_data)
        for month in months:
            output.append({'month': month, 'count': raw_data.get(month, 0), 'type': '电费'})

    def generate_waoutput(raw_data):
        months = generate_months()
        raw_data = dict(raw_data)
        print(raw_data)
        for month in months:
            output.append({'month': month, 'count': raw_data.get(month, 0), 'type': '水费'})

    def generate_proutput(raw_data):
        months = generate_months()
        raw_data = dict(raw_data)
        print(raw_data)
        for month in months:
            output.append({'month': month, 'count': raw_data.get(month, 0), 'type': '物业费'})

    efdata = final_back_sqlmodel.session.query(final_back_sqlmodel.ElectricityFees.ef_date,
                                               final_back_sqlmodel.func.sum(
                                                   final_back_sqlmodel.ElectricityFees.ef_hadpay)).filter(
        final_back_sqlmodel.ElectricityFees.ef_date.in_(generate_months()),
        final_back_sqlmodel.ElectricityFees.ef_pay == 1).group_by(final_back_sqlmodel.ElectricityFees.ef_date).all()
    wadata = final_back_sqlmodel.session.query(final_back_sqlmodel.WaterFees.wa_date, final_back_sqlmodel.func.sum(
        final_back_sqlmodel.WaterFees.wa_hadpay)).filter(final_back_sqlmodel.WaterFees.wa_date.in_(generate_months()),
                                                         final_back_sqlmodel.WaterFees.wa_pay == 1).group_by(
        final_back_sqlmodel.WaterFees.wa_date).all()
    prdata = final_back_sqlmodel.session.query(final_back_sqlmodel.PropertyFees.pr_date, final_back_sqlmodel.func.sum(
        final_back_sqlmodel.PropertyFees.pr_hadpay)).filter(
        final_back_sqlmodel.PropertyFees.pr_date.in_(generate_months()),
        final_back_sqlmodel.PropertyFees.pr_pay == 1).group_by(final_back_sqlmodel.PropertyFees.pr_date).all()
    final_back_sqlmodel.session.commit()
    generate_efoutput(efdata)
    generate_waoutput(wadata)
    generate_proutput(prdata)
    return output


@app.get("/thatchart", tags=['PC', '杂项数据/PC'], summary="柱形统计图数据展示")
async def thatchart():
    waterall = final_back_sqlmodel.session.query(
        final_back_sqlmodel.func.sum(final_back_sqlmodel.WaterFees.wa_hadpay).label("count")).all()
    eleall = final_back_sqlmodel.session.query(
        final_back_sqlmodel.func.sum(final_back_sqlmodel.ElectricityFees.ef_hadpay).label("count")).all()
    prall = final_back_sqlmodel.session.query(
        final_back_sqlmodel.func.sum(final_back_sqlmodel.PropertyFees.pr_hadpay).label("count")).all()
    pakingall = final_back_sqlmodel.session.query(
        final_back_sqlmodel.func.sum(final_back_sqlmodel.ParkingFees.pf_money).label("count")).all()
    final_back_sqlmodel.session.commit()
    jsondata = [{}, {}, {}, {}]
    jsondata[0]['type'] = '水费'
    jsondata[0]['value'] = waterall[0][0]
    jsondata[1]['type'] = '电费'
    jsondata[1]['value'] = eleall[0][0]
    jsondata[2]['type'] = '物业费'
    jsondata[2]['value'] = prall[0][0]
    jsondata[3]['type'] = '停车费'
    jsondata[3]['value'] = pakingall[0][0]
    return jsondata


@app.get("/selectcs", tags=['PC', '系统设置/PC'], summary="查询数据单价")
async def selectcs():
    jsondata = final_back_sqlmodel.session.query(final_back_sqlmodel.ChargingStandard).all()
    return jsondata


@app.post("/insertcs", tags=['PC', '系统设置/PC'], summary="插入默认数据单价")
async def insertcs():
    TestData = ['水费', '电费', '物业费', '停车费']
    for item in TestData:
        final_back_sqlmodel.session.add(final_back_sqlmodel.ChargingStandard(cs_kind=item, cs_standard=0))
        final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"数据添加成功"}')


@app.get("/updatecs", tags=['PC', '系统设置/PC'], summary="修改默认数据单价")
async def updatecs(cswater: int, csele: int, cspr: int, csparking: int):
    TestData = ['水费', '电费', '物业费', '停车费']
    RealData = [cswater, csele, cspr, csparking]
    for item in TestData:
        final_back_sqlmodel.session.query(final_back_sqlmodel.ChargingStandard).filter(
            final_back_sqlmodel.ChargingStandard.cs_kind == item).update(
            {final_back_sqlmodel.ChargingStandard.cs_standard: RealData[TestData.index(item)]})
        final_back_sqlmodel.session.commit()
    return json.loads('{"code":"0","msg":"修改数据成功"}')


if __name__ == '__main__': uvicorn.run(app='final_back:app', host="127.0.0.1", port=8000, reload=True, debug=True)
