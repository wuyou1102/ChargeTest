#-*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlwt


class ExcelStyle(object):
    @staticmethod
    def cell_style(vertical='c', horizontal='c', font_name='Arial', font_size=10, bold=False, border='thin',
                   font_color=0, background_color=1):
        flag = True
        style = xlwt.XFStyle()

        # alignment : horizontal  = 'l','c','r','d','f','j','g','cas'  [ l=LEFT,c=CENTER,r=RIGHT,d=DISTRIBUTED,
        #                                                       f=FILLED,j=JUSTIFIED,g=GENERAL, cas = CENTER_ACROSS_SEL]
        # alignment : vertical  = 't','c','b','d','j'  [ t=TOP,c=CENTER,b=BOTTOM,d=DISTRIBUTED,j=JUSTIFIED]
        # font_name :['Calibri', 'Arial',...]
        # font_size : int
        # bold = False,True
        # border = ['thick','thin','none']
        # font_color:see ColorDemo.xls
        # background_color:see ColorDemo.xls

        if horizontal not in ['l', 'c', 'r', 'd', 'f', 'j', 'g', 'cas']:
            print 'horizontal should in: \"l\",\"c\",\"r\",\"d\",\"f\",\"j\",\"g\",\"cas\",but was \"%s\".' % horizontal
            flag = False
        if vertical not in ['t', 'c', 'b', 'd', 'j']:
            print 'vertical should in: \"t\",\"c\",\"b\",\"d\",\"j\",but was \"%s\".' % vertical
            flag = False
        if border not in ['thick', 'thin', 'none']:
            print 'border should in: \"thick\",\"thin\",\"none\",but was \"%s\".' % border
            flag = False

        if flag:
            style.alignment = ExcelStyle.cell_alignment(vertical=vertical, horizontal=horizontal)
            style.borders = ExcelStyle.cell_border(border=border)
            style.font = ExcelStyle.cell_font(font_name=font_name, font_size=font_size, bold=bold, font_color=font_color)
            style.pattern = ExcelStyle.cell_background_color(background_color=background_color)
            return style
        else:
            raise KeyError

    @staticmethod
    def cell_font(font_name, font_size, bold, font_color):
        font = xlwt.Font()
        font.bold = bold
        font.name = font_name
        font.height = font_size * 20
        font.colour_index = font_color
        return font

    @staticmethod
    def cell_alignment(vertical, horizontal):
        alignment = xlwt.Alignment()
        if vertical == 't':
            alignment.vert = alignment.VERT_TOP
        elif vertical == 'c':
            alignment.vert = alignment.VERT_CENTER
        elif vertical == 'b':
            alignment.vert = alignment.VERT_BOTTOM
        elif vertical == 'd':
            alignment.vert = alignment.VERT_DISTRIBUTED
        elif vertical == 'j':
            alignment.vert = alignment.VERT_JUSTIFIED

        if horizontal == 'l':
            alignment.horz = alignment.HORZ_LEFT
        elif horizontal == 'c':
            alignment.horz = alignment.HORZ_CENTER
        elif horizontal == 'r':
            alignment.horz = alignment.HORZ_RIGHT
        elif horizontal == 'd':
            alignment.horz = alignment.HORZ_DISTRIBUTED
        elif horizontal == 'f':
            alignment.horz = alignment.HORZ_FILLED
        elif horizontal == 'j':
            alignment.horz = alignment.HORZ_JUSTIFIED
        elif horizontal == 'g':
            alignment.horz = alignment.HORZ_GENERAL
        elif horizontal == 'cas':
            alignment.horz = alignment.HORZ_CENTER_ACROSS_SEL

        return alignment

    @staticmethod
    def cell_border(border):
        if border == 'thin':
            return ExcelStyle.thin_border()
        elif border == 'thick':
            return ExcelStyle.thick_border()
        elif border == 'none':
            return ExcelStyle.none_border()

    @staticmethod
    def cell_background_color(background_color):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = background_color
        return pattern



    @staticmethod
    def thick_border():
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THICK
        borders.right = xlwt.Borders.THICK
        borders.top = xlwt.Borders.THICK
        borders.bottom = xlwt.Borders.THICK
        return borders

    @staticmethod
    def thin_border():
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    @staticmethod
    def none_border():
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.NO_LINE
        borders.right = xlwt.Borders.NO_LINE
        borders.top = xlwt.Borders.NO_LINE
        borders.bottom = xlwt.Borders.NO_LINE
        return borders

if __name__ == '__main__':
    ExcelStyle.cell_style()
    book = xlwt.Workbook()
    sheet = book.add_sheet('sss')
    sheet.write(0, 0, 'FontColorID', ExcelStyle.cell_style(font_size=15))
    sheet.write(0, 1, 'FontColor', ExcelStyle.cell_style(font_size=15))
    sheet.write(0, 3, 'BackgroudColorID', ExcelStyle.cell_style(font_size=15))
    sheet.write(0, 4, 'BackgroudColor', ExcelStyle.cell_style(font_size=15))
    for x in range(0, 101):
        sheet.write(x+1, 0, x, ExcelStyle.cell_style(font_size=15))
        sheet.write(x+1, 1, 'Color', ExcelStyle.cell_style(font_color=x, bold=True, font_size=15))
        sheet.write(x+1, 3, x, ExcelStyle.cell_style(font_size=15))
        sheet.write(x+1, 4, '', ExcelStyle.cell_style(font_size=15,background_color=x))
    book.save('ColorDemo.xls')
