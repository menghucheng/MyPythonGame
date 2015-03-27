# -*- coding: cp936 -*-
import pygame,config,os
from random import randrange

#���ģ���������Ϸ�����еĶ���
class SquishSprite(pygame.sprite.Sprite):
    """
    ���������Ϸ��������ĳ��ࡣ���캯����������ͼ��������ͼ�ε�rect��area����
    ������������ָ���������ڽ����ƶ���area����Ļ�Ĵ�С�Ϳհ׾���
    
    """
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)#��ִ�и���Ĺ��췽��
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey((0,0,0))#ȥ����������ĺ�ɫ
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()#�ڵ���flip��blit֮ǰ����һ��surface����
        shrink = -config.margin * 2#����
        self.area = screen.get_rect().inflate(shrink,shrink)
        #inflate�������ø�����������Ϊˮƽ�ʹ�ֱ�����ϵĴ�С���޸�(����)���Σ�
        #��������������˵ı߽磬�����˺ͻ�����ײǰ�ص��Ĳ��ֱ���ʾ


class Weight(SquishSprite):
    '''
        ���µĻ���ʹ����SquishSprite�Ĺ��캯����������ͼ�񣬲��һ��Ը���
        ���ٶ���Ϊ���캯���Ĳ���������������ٶ�
    '''
    def __init__(self,speed):
        SquishSprite.__init__(self,config.Fire_image)
        self.speed = speed
        self.reset()
    def reset(self):
        """
        �����ƶ�����Ļ�Ķ���(������)������������ˮƽλ��
        """
        x = randrange(self.area.left,self.area.right)
        self.rect.midbottom = x,0
    def update(self):
        """
        ���������ٶ��뽫��ֱ�ƶ�(����)һ�ξ��롣���Ҹ������Ƿ񴥼���Ļ�׶�������landed����
        """
        self.rect.top += self.speed
        self.landed = self.rect.top >= self.area.bottom  #��landed���ò���ֵ
class People(SquishSprite):
    """
    �������ˡ���ʹ��SquishSprite���캯�������˵�ͼ�񣬲��һ�ͣ������Ļ�׶ˡ�����ˮƽλ���ɵ�ǰ�����λ�þ���
    """
    def __init__(self):
        SquishSprite.__init__(self,config.People_image)
        self.rect.bottom = self.area.bottom
        #��û���˵Ĳ��ֽ�����䣬����䡣�������ƶ�����Щ�����򲻻ᱻ��䣬���ж�Ϊ��ײ
        self.pad_top = config.people_pad_top;
        self.pad_side = config.people_pad_side
    def update(self):
        """
            ��banana���ĵ�ĺ������趨Ϊ��ǰ���ָ��ĺ����꣬����ʹ��rect��clamp����ȷ��Bananaͣ��������ķ�Χ��
        """
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect = self.rect.clamp(self.area)
    def touches(self,other):
        """
        ȷ�����Ƿ��������������ͼ�Σ�����𣩣�����ʹ��rect��colliderect�������⣬����Ҫ����һ��������
        ��ͼ�񶥶˺Ͳ�ߡ������򡱵��¾��Σ�ʹ��rect��inflate�����춥�˺Ͳ�߽�����䣩
        """
        #ʹ���ʵ��������С�߽�
        bounds = self.rect.inflate(-self.pad_side,-self.pad_top)
        #�ƶ��߽磬�����Ƿ��õ�Banana�ĵײ�
        bounds.bottom = self.rect.bottom
        #���߽��Ƿ�����������rect����
        return bounds.colliderect(other.rect)
        
    
