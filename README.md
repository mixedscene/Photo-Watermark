# Photo-Watermark

## 项目简介
Photo-Watermark 是一个用于批量为照片添加拍摄日期水印的 Python 工具。水印日期格式为“年.月.日”，自动读取照片 EXIF 信息。

## 使用方法
1. 安装依赖：
	```bash
	pip install pillow piexif
	```
2. 运行主程序：
	```bash
	python photowatermark.py
	```
3. 按提示输入：
	- 图片文件夹路径
	- 字体大小（如 32）
	- 字体颜色（如 255,255,255）
	- 水印位置（left_top/center/right_bottom）

4. 程序会自动在原文件夹下生成“_watermark”后缀的新文件夹，保存加水印后的图片。

## 依赖说明
- Pillow
- piexif

## 注意事项
- 需保证图片包含 EXIF 拍摄时间信息，否则会跳过。
- 字体文件需为系统可用字体（如 Windows 下的 arial.ttf）。

## 版本
version-1.0