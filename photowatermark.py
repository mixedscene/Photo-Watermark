import os
import sys
from PIL import Image, ImageDraw, ImageFont
import piexif

def get_exif_date(img_path):
    try:
        exif_dict = piexif.load(img_path)
        date_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
        # 格式: "YYYY:MM:DD HH:MM:SS"
        date = date_str.split(' ')[0].replace(':', '.')
        return date
    except Exception:
        return None

def add_watermark(img_path, text, font_size, color, position):
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    font = ImageFont.truetype("arial.ttf", font_size)
    txt_layer = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    
    # text_w, text_h = draw.textsize(text, font=font)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 位置计算
    if position == "left_top":
        pos = (10, 10)
    elif position == "center":
        pos = ((width - text_w)//2, (height - text_h)//2)
    elif position == "right_bottom":
        pos = (width - text_w - 10, height - text_h - 10)
    else:
        pos = (10, 10)

    draw.text(pos, text, font=font, fill=color+(128,))
    watermarked = Image.alpha_composite(img, txt_layer)
    return watermarked.convert("RGB")

def main():
    img_dir = input("请输入图片文件夹路径: ").strip()
    font_size = int(input("请输入字体大小(如32): ").strip())
    color_input = input("请输入字体颜色(如255,255,255): ").strip()
    color = tuple(map(int, color_input.split(',')))
    position = input("请输入水印位置(left_top/center/right_bottom): ").strip()

    if not os.path.isdir(img_dir):
        print("路径不是有效的文件夹")
        sys.exit(1)

    out_dir = os.path.join(img_dir, os.path.basename(img_dir) + "_watermark")
    os.makedirs(out_dir, exist_ok=True)

    for fname in os.listdir(img_dir):
        fpath = os.path.join(img_dir, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            date = get_exif_date(fpath)
            if not date:
                print(f"{fname} 没有拍摄时间信息，跳过")
                continue
            watermarked = add_watermark(fpath, date, font_size, color, position)
            out_path = os.path.join(out_dir, fname)
            watermarked.save(out_path)
            print(f"已保存: {out_path}")
        except Exception as e:
            print(f"{fname} 处理失败: {e}")

if __name__ == "__main__":
    main()