import random
from django.conf import settings
import sys

def getRegisterNameAvatarlist_male():
    fadj = open(str(settings.BASE_DIR)+"/utils/adjectivelist.text","r",encoding="utf-8")
    fname = open(str(settings.BASE_DIR)+"/utils/nametext.text","r",encoding="utf-8")
    fadjlist = fadj.read().split()
    fnamelist = fname.read().split()
    fadj.close()
    fname.close()
    rd_fadj = random.choices(fadjlist)
    rd_fname = random.choices(fnamelist)
    name = rd_fadj[0]+"的"+rd_fname[0]
    avatarUrl="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar_male.png"
    return name,avatarUrl

def getRegisterNameAvatarlist_female():
    fadj = open(str(settings.BASE_DIR)+"/utils/adjectivelist.text","r",encoding="utf-8")
    fname = open(str(settings.BASE_DIR)+"/utils/nametext.text","r",encoding="utf-8")
    fadjlist = fadj.read().split()
    fnamelist = fname.read().split()
    fadj.close()
    fname.close()
    rd_fadj = random.choices(fadjlist)
    rd_fname = random.choices(fnamelist)
    name = rd_fadj[0]+"的"+rd_fname[0]
    avatarUrl="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar_female.png"
    return name,avatarUrl

def getRegisterNameAvatarlist():
    fadj = open(str(settings.BASE_DIR)+"/utils/adjectivelist.text","r",encoding="utf-8")
    fname = open(str(settings.BASE_DIR)+"/utils/nametext.text","r",encoding="utf-8")
    fadjlist = fadj.read().split()
    fnamelist = fname.read().split()
    fadj.close()
    fname.close()
    rd_fadj = random.choices(fadjlist)
    rd_fname = random.choices(fnamelist)
    name = rd_fadj[0]+"的"+rd_fname[0]
    avatarUrl= ["https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar_female.png",
                "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar_male.png"]
    return name,avatarUrl[0]

def getNameAvatarlist():
    fadj = open(str(settings.BASE_DIR)+"/utils/adjectivelist.text","r",encoding="utf-8")
    fname = open(str(settings.BASE_DIR)+"/utils/nametext.text","r",encoding="utf-8")
    fadjlist = fadj.read().split()
    fnamelist = fname.read().split()
    fadj.close()
    fname.close()
    rd_fadj = random.choices(fadjlist)
    rd_fname = random.choices(fnamelist)
    name = rd_fadj[0]+"的"+rd_fname[0]
    avatarUrl=[
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar1.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar2.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar3.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar4.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar5.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar6.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar7.png",
    ]
    avatarUrl = random.choices(avatarUrl)
    return name,avatarUrl[0]

def getRandomName():
    fadj = open(str(settings.BASE_DIR)+"/utils/adjectivelist.text","r",encoding="utf-8")
    fname = open(str(settings.BASE_DIR)+"/utils/nametext.text","r",encoding="utf-8")
    fadjlist = fadj.read().split()
    fnamelist = fname.read().split()
    fadj.close()
    fname.close()
    rd_fadj = random.choices(fadjlist)
    rd_fname = random.choices(fnamelist)
    name = rd_fadj[0]+"的"+rd_fname[0]
    return name

def getRandomAvatar():
    avatarUrl = [
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar1.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar2.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar3.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar4.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar5.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar6.png",
        "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar7.png",
    ]
    avatarUrl = random.choices(avatarUrl)
    return avatarUrl[0]

def getRegisterAvatar_male():
    avatarUrl="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar_male.png"
    return avatarUrl

def getRegisterAvatar_female():
    avatarUrl="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/avatar/simple_avatar_female.png"
    return avatarUrl

def getMosaic():
    avatarUrl = "https://mini-1257058751.cos.ap-chengdu.myqcloud.com/static/mosaic.jpg"
    return avatarUrl

if __name__ == "__main__":
    getNameAvatarlist()