# -*- coding: utf-8 -*-
import os,sys,pygame
from pygame.locals import *
import objects,config

DEBUG = False

""" 这个模块也包括了Squish游戏的主要游戏逻辑"""

class State:
    """
    范型游戏状态类，可以处理事件并在给定的表面上显示自身
    """
    def handle(self,event):
        """
        只处理退出事件的默认事件处理
        """
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
    def firstDisplay(self,screen):
        """
        用于第一次的显示状态，使用北京色填充屏幕
        """
        screen.fill(config.background_color)
        
        #记得要调用flip，让更改可见
        pygame.display.flip()
        #开头音乐

    def display(self,screen):
        """
        用于在已经显示过一次状态后再次显示。默认的行为是什么都不做
        """
        pass


class Level(State):
    """
    游戏等级，用于计算已经下落多少火团，移动子图形以及其他和游戏逻辑相关的任务
    """
    def __init__(self,number=1):
        self.number = number
        #本关内容还要下落多少火团？
        self.remaining = config.weights_per_level

        speed = config.drop_speed
        #为每个大于1的等级都增加一个speed_increase
        speed += (self.number-1) * config.speed_increase
        #创建人和火团
        self.weight = objects.Weight(speed)
        self.people = objects.People()
        both = self.weight,self.people   #这个能包含更多的精灵对象Sprite
        self.sprites = pygame.sprite.RenderUpdates(both)

    def  update(self,game):
        """
        从前一帧更新游戏状态
        """
        #更新所有的子图形
        self.sprites.update()
        #如果人碰到了火团，那么告诉游戏切换到GameOver状态
        if self.people.touches(self.weight):
            #config.pause_image = config.shuai_image
            game.nextState = GameOver()
        #否则在火团落地时将其复位
        #如果本关内的所有火团都落下了，则让游戏切换到LevelCleared的状态
        elif self.weight.landed:
            self.weight.reset()
            self.remaining -= 1
            if self.remaining == 0:
                game.nextState = LevelCleared(self.number)

    def display(self,screen):
        """
        在第一次显示（只清空屏幕）后显示状态。与firstDisplay不同，这个方法使用pygame.display.update
        对self.sprites.draw提供的、需要更新的矩形进行更新
        """
        screen.fill(config.background_color)
        updates = self.sprites.draw(screen)
        pygame.display.update(updates)

class Paused(State):
    """
    简单的游戏暂停状态，按下键盘上任意键或者点击鼠标都会结束这个状态
    """
    finished = 0 #用户结束暂停了么
    image = config.pause_image #这个可以设定图片
    text = "Pause"#设置提示性文本

    def handle(self,event):
        """
        通过对State进行委托(一般处理退出事件)以及对按键和鼠标点击做出反应来处理事件
        如果键被按下或者鼠标被点击，将self.finished设为真
        """
        State.handle(self,event)
        if event.type in [MOUSEBUTTONDOWN,KEYDOWN]:
            self.finished = 1
    def update(self,game):
        """
        更新等级。如果按键被按下或者鼠标被编辑(比如self.finished为真)，
        那么告诉游戏切换到下一个有self.nextState()表示的状态(应该由子类实现)
        """
        if self.finished:
            '''
            game,nextState = self.nextState()#这里会抛出异常，iteration over non-sequence,原因是在下一步程序nextState()中的for循
            # 环迭代器在访问空的序列或者可迭代对象，这里的nextState是null
          '''
            try:
                game.nextState = self.nextState()
            except Exception,e:
                print "捕捉到了异常 ",Exception,":",e
                pygame.quit()
                sys.exit()
            #print game,nextState

        
    def firstDisplay(self,screen):
        """
        暂停状态第一次出现时，绘制图像并生成文本
        """
        #首先使用填充背景色的方式清空屏幕：
        screen.fill(config.background_color)

        #使用默认的外观和指定的大小创建Font对象
        font = pygame.font.Font(None,config.font_size)

        #获取self.text中的文本行，忽略开头和结尾的空行
        lines = self.text.strip().splitlines()

        #计算文本的高度(使用font.get_linesize())以获取每行文本的高度
        height = len(lines) * font.get_linesize()

        #计算文本的放置位置（屏幕中心）
        center,top = screen.get_rect().center
        top -= height // 2   #????
        #如果有图片要显示的话。。。
        if self.image:
            #载入图片
            image = pygame.image.load(self.image).convert()

            #去掉黑色，在网上搜索的方法
            
            image.set_colorkey((0,0,0))
            #获取它的rect
            r = image.get_rect()
            #将图像向下移动其高度的一半的距离
            top += r.height // 2
            #将图片放置在文本上方20像素处
            r.midbottom = center,top - 20
            #将图像移动到屏幕上
            screen.blit(image,r)  # 需要再看一下
        antialias = 1#Smooth the text
        black = 0,0,0 #render it as black

        #生成的所有行从计算过的top开始，并且对于每一行向下移动font.get_linesize()像素
        for line in lines:
            text = font.render(line.strip(),antialias,black)
            r = text.get_rect()
            r.midtop = center,top
            screen.blit(text,r)
            top += font.get_linesize()
        #显示所有的更改

        pygame.display.flip()



class Info(Paused):
    """
    简单的暂停状态，显示游戏相关的信息。在level状态后显示(第一级)
    """

    nextState = Level
    #print nextState
    text = '''
    In this game you are a people,
    trying to survive a course in self-
    defense against fire,where the participants
    will "defend" themselves
    against you with a fire.'''


class StartUp(Paused):
    """
    显示展开图片和欢迎信息的暂停状态。在Info状态后显示。
    """

    nextState = Info
    image = config.splash_image


    text = '''
    Welcome to Squish,
    the game of Fruit Self-Defense'''

class LevelCleared(Paused):
    """
    提示用户过关的暂停状态。在next level状态后显示。
    """
    def __init__(self,number):
        self.number = number
        self.text = '''Level %i cleared
        Click to start next level''' % self.number
    def nextState(self):
        return Level(self.number+1)
class GameOver(Paused):#都是继承Paused、State
    """
    提示用户输掉游戏的状态。在first level后显示
    """
    nextState = Level #??
    text = '''
    Game Over
    Click to Restart ,Esc to Quit'''


class Game:
    '''
    负责主事件循环的游戏对象，任务包括不同状态间的切换
    '''

    def __init__(self,*args):
        #获取游戏和图像放置的目录(这样图片文件可以在随后打开)
        path = os.path.abspath(args[0])#获得当前文件的绝对路径H:\Python\Game\newone\squish.py
        dir = os.path.split(path)[0]#获取当前文件所在的路径H:\Python\Game\newone
        #移动那个目录(这样图片文件可以在随后打开)
        os.chdir(dir) #调用系统的dir函数将当前的路径转到指定的路径
        #无状态方式启动
        self.state = None
        #在第一个事件循环迭代中移动到StartUp
        self.nextState = StartUp()
    def run(self):
        """
        这个方法动态设定变量。进行一些重要的初始化工作，并且进入主事件循环。
        """
        pygame.init()#初始化所有的pygame模块
        #决定以后以窗口模式还是全屏模式显示游戏
        pygame.mixer.music.load(config.begin_music)
        pygame.mixer.music.play(-1)
        flag = 0#默认窗口

        if config.full_screen:
            flag = FULLSCREEN   #全屏模式
        screen_size = config.screen_size
        screen = pygame.display.set_mode(screen_size,flag,32)
        pygame.display.set_caption('Fruit Self Defense')
        pygame.mouse.set_visible(False)

        #主循环
        while True:
            #(1)如果nextState被修改了，那么移动到新状态，并且显示它(第一次)
            if self.state != self.nextState:
                self.state = self.nextState
                self.state.firstDisplay(screen)
            #(2)代理当前状态的事件处理
            for event in pygame.event.get():
                self.state.handle(event)
            #(3)更新当前状态
            self.state.update(self)
            #(4)显示当前状态
            self.state.display(screen)
           # print "循环了一次"


    
            




if __name__=='__main__':
    if DEBUG:
        import pdb
        pdb.set_trace()
    game = Game(*sys.argv)
    game.run()
