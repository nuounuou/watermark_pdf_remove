from PIL import Image


class RemoveColor:
    def remove_watermark(self, image_path, new_image_path):
        img = Image.open(image_path).convert("RGBA")  #打开带有水印的原始图片
        width, height = img.size    #获得原图片的宽和高（像素）

        for x in range(width):   #遍历图片中每一个点的像素
            for y in range(height):
                # 每个像素点与背景色对比，如果不超过阀值50，则用背景色填充，具体的背景色要根据实际图片修改，本例中背景是白色
                if self.is_color_similar(img.getpixel((x, y)), (255, 255, 255), 80):  
                    img.putpixel((x, y), (255, 255, 255, 255))  #最后一个255是透明度，255表示完全不透明

        img.save(new_image_path, "png")  #保存为新图片

    #判断颜色与背景色的差值是否超过阀值，不超过返回true，超过则返回false
    def is_color_similar(self, color, background_color, threshold):
        delta_red = abs(color[0] - background_color[0])
        delta_green = abs(color[1] - background_color[1])
        delta_blue = abs(color[2] - background_color[2])
        if delta_red < threshold and delta_green < threshold and delta_blue < threshold:
            return True
        return False


if __name__ == '__main__':
    file_name_path = r'中国电信渠道业[2024]16号全网分摊成本报表-识别水印索引_00.jpg'
    new_file_name_path = r'image/中国电信渠道业[2024]16号全网分摊成本报表-识别水印索引_00.jpg'
    remove_color = RemoveColor()
    remove_color.remove_watermark(file_name_path, new_file_name_path)