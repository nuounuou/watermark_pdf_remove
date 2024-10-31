import os
from PyPDF4 import PdfFileReader, PdfFileWriter
from PIL import Image


#判断颜色与背景色的差值是否超过阀值，不超过返回true，超过则返回false
def is_color_similar(self, color, background_color, threshold):
    delta_red = abs(color[0] - background_color[0])
    delta_green = abs(color[1] - background_color[1])
    delta_blue = abs(color[2] - background_color[2])
    if delta_red < threshold and delta_green < threshold and delta_blue < threshold:
        return True
    return False

def remove_content_watermark(image_path, new_image_path):
    img = Image.open(image_path).convert("RGBA")  #打开带有水印的原始图片
    width, height = img.size    #获得原图片的宽和高（像素）

    for x in range(width):   #遍历图片中每一个点的像素
        for y in range(height):
            # 每个像素点与背景色对比，如果不超过阀值50，则用背景色填充，具体的背景色要根据实际图片修改，本例中背景是白色
            if is_color_similar(img.getpixel((x, y)), (255, 255, 255), 80):  
                img.putpixel((x, y), (255, 255, 255, 255))  #最后一个255是透明度，255表示完全不透明

    img.save(new_image_path, "png")  #保存为新图片


def remove_watermark(pdf_path, new_path):
    """
    去除pdf水印:param pdf_path: 带水印pdf路径; param new_path: 去水印保存的路径
    """
    output = PdfFileWriter()
    pdf = PdfFileReader(pdf_path, 'rb')
   
    for page_num in range(pdf.getNumPages()): # 遍历PDF
        page = pdf.getPage(page_num)
        resources = page['/Resources']
        print(page_num)
        print(resources)
        print('***************************')
        if '/XObject' in resources:
            xobjects = resources['/XObject']
            # print(xobjects)
            for obj in list(xobjects.keys()):  # 创建对象键的列表，以便在循环中修改字典
                # 保留以"IM"开头的对象（即图片）
                if not obj.startswith("/IM") and not obj.startswith("/Im"):
                    del xobjects[obj]
            output.addPage(page)
        else:
            remove_content_watermark(pdf_path, new_path)

    # 写入新的PDF文件
    with open(new_path, 'wb') as ouf:
        output.write(ouf)


if __name__ == '__main__':
    directory_old = "error_pdf"  # 存放带水印pdf的文件夹
    directory_new = "out_pdf_new"  # 去除水印后的文件夹

    for root, dirs, files in os.walk(directory_old):
        for file in files:
            file_path = os.path.join(root, file)
            remove_watermark(file_path, r"{}\{}".format(directory_new, os.path.basename(file_path)))
