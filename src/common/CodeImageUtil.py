
#coding: utf-8
import random

from PIL import Image,ImageFont,ImageDraw,ImageFilter

class CodeImageGen:

    count = 4

    def __init__(self):
        self.width = 100
        self.height = 32
        self.imgName = 'idencode.png'
        self.curCode = '****'
        self.font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\SIMLI.TTF', 26)  # 验证码的字体和字体大小


    def random_txt(self):
        s = ''
        for index in range(4):
            if index == 0:
                s += ' '
            s += str(random.randint(0, 9))
            s += ' '
        return s

    def gen_img(self, width = 100, height = 32):
        self.width = width
        self.height = height
        image = Image.new('RGBA', (width, height), (255,255,255))  # 创建图片
        draw = ImageDraw.Draw(image)  # 创建画笔
        self.curCode = self.random_txt()  # 生成字符串
        font_width, font_height = self.font.getsize(self.curCode)
        draw.text(((width-font_width-15) / self.count, (height-font_height+15) / self.count), self.curCode,
                  font=self.font, fill=(0,0,255))  # 填充字符串
        self.draw_line(draw)
        #image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
        #image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        image.save(self.imgName)  # 保存验证码图片

    def draw_line(self, draw):

        fil = (255, 0, 0)
        for x in range(25):
            begin = (random.randint(0, self.width), random.randint(0, self.height))
            end = (random.randint(0, self.width), random.randint(0, self.height))
            draw.line([begin, end], fill=fil)


#gen = CodeImageGen()
#gen.gen_img()
#图片增强

# img = Image.open("E:\\workspace_vme\\ui\\bg1.jpg")
# im = img.filter(ImageFilter.DETAIL)
# im.save("E:\\workspace_vme\\ui\\bg2.jpg")
# print(im)
