# -*- coding: cp936 -*-
import pygame,config,os
from random import randrange

#这个模块包含了游戏的所有的对象
class SquishSprite(pygame.sprite.Sprite):
    """
    这个类是游戏中所有类的超类。构造函数负责载入图像，设置子图形的rect和area属性
    并且允许它在指定的区域内进行移动。area由屏幕的大小和空白决定
    
    """
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)#先执行父类的构造方法
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey((0,0,0))#去除背景后面的黑色
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()#在调用flip或blit之前返回一个surface对象
        shrink = -config.margin * 2#收缩
        self.area = screen.get_rect().inflate(shrink,shrink)
        #inflate方法会用给定的像素作为水平和垂直方向上的大小来修改(扩大)矩形，
        #这个方法来所见人的边界，允许人和火在碰撞前重叠的部分被显示


class Weight(SquishSprite):
    '''
        落下的火，它使用了SquishSprite的构造函数设置他的图像，并且会以给定
        的速度作为构造函数的参数来设置下落的速度
    '''
    def __init__(self,speed):
        SquishSprite.__init__(self,config.Fire_image)
        self.speed = speed
        self.reset()
    def reset(self):
        """
        将火移动到屏幕的顶端(视线外)，放置在任意水平位置
        """
        x = randrange(self.area.left,self.area.right)
        self.rect.midbottom = x,0
    def update(self):
        """
        根据他的速度与将火垂直移动(下落)一段距离。并且根据他是否触及屏幕底端来设置landed属性
        """
        self.rect.top += self.speed
        self.landed = self.rect.top >= self.area.bottom  #给landed设置布尔值
class People(SquishSprite):
    """
    绝望的人。它使用SquishSprite构造函数设置人的图像，并且会停留在屏幕底端。它的水平位置由当前的鼠标位置决定
    """
    def __init__(self):
        SquishSprite.__init__(self,config.People_image)
        self.rect.bottom = self.area.bottom
        #在没有人的部分进行填充，被填充。若果火被移动到这些区域则不会被填充，被判定为碰撞
        self.pad_top = config.people_pad_top;
        self.pad_side = config.people_pad_side
    def update(self):
        """
            将banana中心点的横坐标设定为当前鼠标指针的横坐标，并且使用rect的clamp方法确保Banana停留在允许的范围内
        """
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect = self.rect.clamp(self.area)
    def touches(self,other):
        """
        确定人是否碰触到另外的子图形（比如火），出了使用rect的colliderect方法以外，首先要计算一个不包括
        人图像顶端和侧边“空区域”的新矩形（使用rect的inflate方法遂顶端和侧边进行填充）
        """
        #使用适当的填充缩小边界
        bounds = self.rect.inflate(-self.pad_side,-self.pad_top)
        #移动边界，将它们放置到Banana的底部
        bounds.bottom = self.rect.bottom
        #检查边界是否和其他对象的rect交叉
        return bounds.colliderect(other.rect)
        
    
