# -*- coding: utf-8 -*-
'''
Created on 2009-12-31

@author: vls
'''

OFFSET = 0x1E130 # C5+ 台服与国服的偏移

class ADDR:
    #section 1
    MOUSE_BUSY = 0xB4D6A0 + OFFSET                  #鼠标是否为漏斗状  #B6B7D0
    TAB_OBJTYPE = MOUSE_BUSY + 0x9c - 0x78          #TAB对象类型
    TAB_ID = TAB_OBJTYPE + 0xA0 - 0x9c              #TAB对象ID
    
    SCENE_CHANGE = 0xB4e170 + OFFSET                #切换场景
    
    QUICK_KEY = 0xB4E8E8 + OFFSET + 0x1440          #快捷键
    #PC_STATE = 0xB6F97C				# =1 ==正常？ 还有断线
    
    
    
    
    #section 2
    
    HP = 0xB6FAF0                       #行动力
    
    PC_NAME = HP - 0xD8                 #玩家名称
    PC_ID = HP - 0xCC                   #玩家ID
    SHIP_STATE = HP - 0XBC              #船只状态
    
    MAXHP = HP + 4                      #最大行动力
    MONEY = HP + 8                      #金钱
    #SAILOR = 0xB6FAFC									#当前水手
    FATIGUE = HP + 0x10                 #疲劳 > 300吃，（显示值的10倍）
    FOOD = HP + 0x12                    #食品
    WATER = HP + 0x14                   #水
    BOMB = HP + 0x16                    #炮弹
    WOOD = HP + 0x18                    #木头
    
    SHIP_HP = HP + 0x3A - 0x20          #船耐久
    #SHIP_MAXHP = 0xB6FE60               #船最大耐久
    PC_X = 0xB6FB3C                     #人物X坐标 （陆地和海洋）
    PC_Y = PC_X + 8                     #玩家Y坐标
    
    PC_COS = PC_X + 0x10                #玩家方向COS（陆地和海洋）
    PC_SIN = PC_COS + 8                 #玩家SIN     
    
    #SECTION 3
    LAND_FOLLOW = 0xB51D9C + OFFSET + 4 #陆地跟随
    
    
    
    AUTO_SAIL = 0xB51DC0 + OFFSET + 4   #自动航行
    
    SEA_FOLLOW = 0xB6FF40               #海洋跟随
    
    TAB_PCBASE = SEA_FOLLOW + 0xCC - 0x68   #TAB 选择人物及NPC对象基址
    
    TAB_STATIC = SEA_FOLLOW + 0xEC - 0x68   #TAB 选择静物对象基址
    
    LOCATION = SEA_FOLLOW + 0xb0c -0xa68    #所在地方（包括港口，室内，海域）
    
    PARTY_BASE = SEA_FOLLOW + 0xb78 - 0xa68    #队伍基址 [[ADDR]+C]
    
    TAB_STATIC2 = TAB_STATIC + 0x690    #静物对象2级
    
    #section 4
    BOOL_CUSTOM = 0xb536c8 + OFFSET + 0x40
    
    
    
    #section 5
    WEATHER = 0xB538D5 + OFFSET + 0x60 #验证 2010/1/1
    SAIL_DAY = WEATHER + 3
    
    @staticmethod
    def getIntList():
        return [ADDR.HP, ADDR.MAXHP, ADDR.MONEY, ADDR.PC_ID,  ADDR.SHIP_HP]
    
    @staticmethod
    def getIntStr():
        return ['HP = %d', 'MaxHP = %d', 'Money = %d', '人物ID = %d', '船只耐久 = %d']
    
    @staticmethod
    def getShortList():
        return [ADDR.FATIGUE, ADDR.FOOD, ADDR.WATER, ADDR.WOOD, ADDR.BOMB]
    
    @staticmethod
    def getShortStr():
        return ['疲劳 = %d', '食物  = %d', '水 = %d', '木 = %d', '炮弹 = %d']
    


QuickKey = {
        0x0  : '未登录',  
        0x10 : "自定义栏",
        0x11 : '感情表现',
        0x12 : '人物信息',
        0x13 : '技能',
        0x14 : '装备物',
        0x15 : '持有物品一览',
        0x16 : '船只信息',
        0x17 : '船只配件',
        0x18 : '装载',
        0x19 : '入港许可',
        0x20 : '商会名单',
        0x21 : '聊天室',
        0x22 : '邮件',
        0x23 : '状态设置',
        0x24 : 'GM帮助',
        0x25 : '系统设置',
        0x26 : '自定义栏登录',
        0x27 : '快捷键登录',
        0x28 : '登出',
        0x48 : '副官信息',
        0x49 : '副官负责内容变更',
        0x50 : '宠物信息',
        0x0E : '使用技能',
        0x0F : '使用道具',
        0x1A : '任务',
        0x1B : '发现物',
        0x1C : '事件记录',
        0x1D : '露天市场',
        0x1E : '检索',
        0x1F : '好友一览',
        0x4A : '巡航并登出',
        0x4B : '卡片组合',
        0x4C : '沉船',
        0x4D : '班级名单',
        0x4F : '输入序列号' }


ShipState = {
 0x100000 : '不安',
 0x20 : '触礁',
 0x400 : '磁场混乱',
 0x2000000 : '大混乱',
 0x800000 : '大火灾',
 0x1000000 : '大漏水',
 0x4000 : '大鲨鱼',
 0x2000 : '大章鱼',
 0x1000 : '海怪',
 0x8000 : '海鸥',
 0x800 : '海妖歌声',
 0x200 : '海藻',
 1 : '坏血病',
 0x10000 : '甲板脏',
 4 : '叛乱',
 0x40000 : '失眠',
 8 : '鼠患',
 0x80000 : '思乡严重',
 2 : '瘟疫',
 0x80 : '小混乱',
 0x10 : '小火灾',
 0x40 : '小漏水',
 0x100 : '烟雾',
 0x20000 : '营养不良',
 0x200000 : '欲求不满',
 0x400000 : '争吵' }
    
    
#SKILL_BASE = 0xBD8388		#ADDR+0x20+0x38 = 技能数目
#  ADDR + 0x20 + 0xC #技能1ID
#ADDR + 0x20 + 0x14 #技能2ID
#ADDR + 0x20 + 0x1C #技能3ID

#