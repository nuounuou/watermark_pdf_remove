from PIL import Image
from pdf2image import convert_from_path
import os
from reportlab.pdfgen import canvas

class RemoveColor:
    def remove_watermark(self, image_path, new_image_path):
        img = Image.open(image_path).convert("RGBA")  # 打开带有水印的原始图片
        width, height = img.size    # 获得原图片的宽和高（像素）

        for x in range(width):   # 遍历图片中每一个点的像素
            for y in range(height):
                # 每个像素点与背景色对比，如果不超过阀值50，则用背景色填充，具体的背景色要根据实际图片修改，本例中背景是白色
                if self.is_color_similar(img.getpixel((x, y)), (255, 255, 255, 255), 80):  
                    img.putpixel((x, y), (255, 255, 255, 255))  # 最后一个255是透明度，255表示完全不透明

        img.save(new_image_path, "PNG")  # 保存为新图片

    # 判断颜色与背景色的差值是否超过阀值，不超过返回true，超过则返回false
    def is_color_similar(self, color, background_color, threshold):
        delta_red = abs(color[0] - background_color[0])
        delta_green = abs(color[1] - background_color[1])
        delta_blue = abs(color[2] - background_color[2])
        delta_alpha = abs(color[3] - background_color[3])
        return (delta_red < threshold and
                delta_green < threshold and
                delta_blue < threshold and
                delta_alpha < threshold)

# 定义函数，将PDF的每一页转换为图片并去除水印
def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    image_paths = []
    
    for i, image in enumerate(images):
        image_path = f'page_{i}.png'  # 为每一页创建一个图像文件名
        image.save(image_path, 'PNG')  # 保存图片
        remover = RemoveColor()
        new_image_path = f'page_{i}_clean.png'
        image.save(new_image_path, 'PNG')
        remover.remove_watermark(image_path, new_image_path)  # 去除水印
        image_paths.append(new_image_path)  # 保存处理过的图像路径以便后续合并

    return image_paths

# 定义函数，将图片合并为PDF
def convert_image_to_rgb(image_path, output_path):
    # 打开图片，如果图片是RGBA（包含透明度），则转换为RGB
    image = Image.open(image_path)
    if image.mode == 'RGBA':
        # 创建一个白色背景的图片
        background = Image.new('RGB', image.size, (255, 255, 255))
        # 将原图片粘贴到背景图片上，alpha通道用作mask
        background.paste(image, mask=image.split()[3])
        image = background
    # 保存转换后的图片
    image.save(output_path)

def images_to_pdf(image_paths, output_path):
    # images = [Image.open(image).convert('RGB') for image in image_paths]
    # images[0].save(output_path, save_all=True, append_images=images[1:])
    images = []
    dpi = 300
    for image_path in image_paths:
        image = Image.open(image_path).convert('RGB')
        # 可以在这里设置DPI
        image = image.resize((image.width * dpi // 72, image.height * dpi // 72), Image.Resampling.LANCZOS)
        images.append(image)
    
    # 保存第一张图片，并附加后续图片
    images[0].save(output_path, save_all=True, append_images=images[1:], dpi=(dpi, dpi))

        

# 主程序
def main(pdf_path, output_pdf):
    image_paths = pdf_to_images(pdf_path)  # 转换PDF为图片并去水印
    images_to_pdf(image_paths, output_pdf)  # 合并图片为新的PDF


# 使用示例
if __name__ == "__main__":
    pdf_path = 'error_pdf/AZ09.pdf' # 输入PDF文件路径
    output_pdf = 'out_pdf_new/Output.pdf' # 输出PDF文件路径
    main(pdf_path, output_pdf)