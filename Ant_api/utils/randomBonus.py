import random
from django.conf import settings
import sys

def getRandomBonus():
    bonus = open(str(settings.BASE_DIR)+"/utils/bonus.txt","r",encoding="utf-8")
    bonusList = bonus.read().split()
    bonus.close()
    rd_bonus = random.choices(bonusList)
    return rd_bonus[0]

if __name__ == "__main__":
    getRandomBonus()