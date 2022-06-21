from pydantic import BaseModel


class UserLive(BaseModel):
    uname: str = None
    utele: int = None
    utime: str = None
    umeasure: int = None
    ubuild: str = None
    upwd: str = None
    ustatue: int = None


class EleFree(BaseModel):
    efid: int = None
    efuserid: int = None
    efdate: str = None
    efnum: int = None
    efpay: int = None
    efpush: int = None
    efhadpay: int = None
    efpayday: int = None


class WaFree(BaseModel):
    wfid: int = None
    wfuserid: int = None
    wfdate: str = None
    wfnum: int = None
    wfpay: int = None
    wfpush: int = None
    wfhadpay: int = None
    wfpayday: str = None


class PrFree(BaseModel):
    pfid: int = None
    pfuserid: int = None
    pfdate: str = None
    pfpay: int = None
    pfpush: int = None
    pfhadpay: int = None
    pfpayday: int = None


class Paking(BaseModel):
    paid: int = None
    pa_fooler: str = None
    is_used: int = None


class Pakingfee(BaseModel):
    pfid: int = None
    paid: int = None
    pftele: int = None
    pfcarnum: str = None
    pfstarttime: str = None
    pfstoptime: str = None
    pfhour: str = None
    pfmoney: str = None
