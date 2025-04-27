#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <Windows.h>
#include <vector>
#include <stireg.h>
#include <thread>
#include <cstring>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <filesystem>
#include <iomanip>
#include <cstring>
#include <math.h>
using namespace std;
#undef main;

typedef struct pixColor
{
	unsigned char b;
	unsigned char g;
	unsigned char r;
} PIXCOLOR, *PPIXCOLOR;

// 有关查找rgb值,速度更快
BITMAPFILEHEADER bmf;
BITMAPINFOHEADER bif;
FILE *pf;
PPIXCOLOR *ColorData;
// 返回值为0表示打开成功，非0则为失败
errno_t err;

struct RGB
{
	int R;
	int G;
	int B;
};

#pragma pack(push, 1) // 禁用字节对齐，确保结构体按1字节对齐

struct BMPFileHeader
{
	uint16_t bfType;	  // 文件类型，必须是 "BM"
	uint32_t bfSize;	  // 文件大小（字节）
	uint16_t bfReserved1; // 保留，必须为0
	uint16_t bfReserved2; // 保留，必须为0
	uint32_t bfOffBits;	  // 从文件头到实际图像数据的偏移（字节）
};

struct BMPInfoHeader
{
	uint32_t biSize;		 // 本结构体的大小（字节）
	int32_t biWidth;		 // 图像宽度（像素）
	int32_t biHeight;		 // 图像高度（像素），正值表示图像数据从底部开始
	uint16_t biPlanes;		 // 平面数，必须为1
	uint16_t biBitCount;	 // 每个像素的位数，24位表示RGB各8位
	uint32_t biCompression;	 // 压缩类型，0表示不压缩
	uint32_t biSizeImage;	 // 图像大小（字节），对于不压缩的24位图像，等于宽度*高度*3
	int32_t biXPelsPerMeter; // 水平分辨率（像素/米）
	int32_t biYPelsPerMeter; // 垂直分辨率（像素/米）
	uint32_t biClrUsed;		 // 实际使用的颜色表中的颜色数，0表示使用所有颜色
	uint32_t biClrImportant; // 重要颜色数，0表示所有颜色都重要
};

#pragma pack(pop)

void writeBMP(const std::string &filename, const std::vector<uint8_t> &rgbData, int width, int height)
{
	// const int width = 5;
	// const int height = 2;
	const int rowSize = width * 3;				 // 每个像素3个字节（RGB）
	const int padding = (4 - (rowSize % 4)) % 4; // 行填充，使每行大小是4的倍数
	const int imageSize = rowSize * height + padding * height;

	BMPFileHeader fileHeader;
	BMPInfoHeader infoHeader;

	// 初始化文件头
	fileHeader.bfType = 0x4D42; // "BM"
	fileHeader.bfSize = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader) + imageSize;
	fileHeader.bfReserved1 = 0;
	fileHeader.bfReserved2 = 0;
	fileHeader.bfOffBits = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader);

	// 初始化信息头
	infoHeader.biSize = sizeof(BMPInfoHeader);
	infoHeader.biWidth = width;
	infoHeader.biHeight = height;
	infoHeader.biPlanes = 1;
	infoHeader.biBitCount = 24;
	infoHeader.biCompression = 0;
	infoHeader.biSizeImage = imageSize;
	infoHeader.biXPelsPerMeter = 0;
	infoHeader.biYPelsPerMeter = 0;
	infoHeader.biClrUsed = 0;
	infoHeader.biClrImportant = 0;

	// 打开文件进行写入
	std::ofstream file(filename, std::ios::binary);
	if (!file.is_open())
	{
		std::cerr << "无法打开文件 " << filename << std::endl;
		return;
	}

	// 写入文件头和信息头
	file.write(reinterpret_cast<const char *>(&fileHeader), sizeof(BMPFileHeader));
	file.write(reinterpret_cast<const char *>(&infoHeader), sizeof(BMPInfoHeader));

	// 写入图像数据，注意行填充
	int idx = 0;
	for (int y = height - 1; y >= 0; --y)
	{ // BMP图像数据是从底部开始的
		for (int x = 0; x < width; ++x)
		{
			if (idx < rgbData.size())
			{
				file.write(reinterpret_cast<const char *>(&rgbData[idx]), 3);
				idx += 3; // 每个像素3个字节
			}
			else
			{
				// 如果数据不足，填充黑色
				file.write("\0\0\0", 3);
			}
		}
		// 写入行填充
		for (int p = 0; p < padding; ++p)
		{
			file.write("\0", 1);
		}
	}

	file.close();
}
// 获取某一xy的RGB值
RGB GetNowRGB(PPIXCOLOR *ColorData, int ReadX, int ReadY)
{

	// 防止越界
	if (ReadX < 0)
		ReadX = 0;
	if (ReadY < 0)
		ReadY = 0;
	if (ReadX >= bif.biWidth)
		ReadX = bif.biWidth - 1;
	if (ReadY >= bif.biHeight)
		ReadY = bif.biHeight - 1;
	// cout << "ReadX:" << ReadX << " ReadY:" << ReadY << endl;
	RGB ReturnRGB = {ColorData[ReadY][ReadX].r, ColorData[ReadY][ReadX].g, ColorData[ReadY][ReadX].b};
	return ReturnRGB;
}
// rgb为小于等于的判断界限
bool J_judgeIsRGB(int x, int y, RGB rgb)
{
	RGB NowBlock = GetNowRGB(ColorData, x, y);
	// cout << "R:" << NowBlock.x << "G:" << NowBlock.y << "B:" << NowBlock.w << endl;
	if ((NowBlock.R <= rgb.R) && (NowBlock.G <= rgb.G) && (NowBlock.B <= rgb.B))
	{
		// cout << "j" << endl;
		return true;
	}
	return false;
}

int Translate16ToRGB(std::vector<unsigned char> data, int Place)
{
	// 减1是因为数组索引从0开始
	Place--;

	// 检查Place是否有效
	if (Place < 0 || Place >= data.size())
	{
		// std::cerr << "Error: Place index out of bounds!" << std::endl;
		return -1; // 返回一个错误码
	}

	// 取出指定位置的字节
	unsigned char byte = data[Place];

	// 提取高位（十六进制中的'e'）
	// char highNibble = (byte >> 4) & 0x0F;  // 右移4位并屏蔽低4位
	// char highNibbleChar = highNibble >= 10 ? ('a' + (highNibble - 10)) : ('0' + highNibble);

	// 提取低位（十六进制中的'8'）
	// 假设我们有一个字节，其值已知
	// char byte = 0x4F;  // 例如，这个值有01001111的二进制表示

	// 提取高4位（右移4位并与0x0F做与操作）
	char highNibble = (byte >> 4) & 0x0F;
	// 提取低4位（直接与0x0F做与操作）
	char lowNibble = byte & 0x0F;

	// 将nibble转换为字符
	char highNibbleChar = highNibble >= 10 ? ('A' + (highNibble - 10)) : ('0' + highNibble);
	char lowNibbleChar = lowNibble >= 10 ? ('A' + (lowNibble - 10)) : ('0' + lowNibble);

	// 输出转换后的字符
	// cout << "High Nibble Character: " << highNibbleChar << endl;
	// cout << "Low Nibble Character: " << lowNibbleChar << endl;

	// 将字符转换回数值
	int decimalValue = 0;
	if (highNibbleChar >= 'A')
	{
		decimalValue = highNibbleChar - 'A' + 10;
	}
	else
	{
		decimalValue = highNibbleChar - '0';
	}

	int decimalValue2 = 0;
	if (lowNibbleChar >= 'A')
	{
		decimalValue2 = lowNibbleChar - 'A' + 10;
	}
	else
	{
		decimalValue2 = lowNibbleChar - '0';
	}

	// 计算整个字节的十进制值
	int End = decimalValue * 16 + decimalValue2;
	// std::cout << "END: " <<   std::dec << End << std::endl; // 这将再次以十进制输出

	return End;
}

// 加载图片文件+读取
void MixVecotrBlack(const char *filename)
{

	err = fopen_s(&pf, filename, "rb");
	if (0 == err)
	{
		fread(&bmf, sizeof(bmf), 1, pf);
		fread(&bif, sizeof(bif), 1, pf);

		if (0x4d42 != bmf.bfType)
		{
			cout << "文件不是位图！" << endl;
			fclose(pf);
		}
		else if (24 != bif.biBitCount)
		{
			cout << "位图不是24位！" << endl;
			fclose(pf);
		}
		else
		{
			// cout << "图片的宽度：" << bif.biWidth << endl;
			// cout << "图片的高度：" << bif.biHeight << endl;

			ColorData = new PPIXCOLOR[bif.biHeight];

			// 一行的字节数
			int lineCount = bif.biSizeImage / bif.biHeight;

			// 存的时候从倒数第一行开始存，所以读的时候先往倒数第一行放
			// 读颜色数据
			for (int i = bif.biHeight - 1; i >= 0; i--)
			{
				ColorData[i] = new PIXCOLOR[bif.biWidth];
				fread(ColorData[i], sizeof(PIXCOLOR), bif.biWidth, pf);
				// 偏移  bif.biWidth * sizeof(PIXCOLOR)有多少个字节
				fseek(pf, lineCount - bif.biWidth * sizeof(PIXCOLOR), SEEK_CUR);
			}
			fclose(pf);
		}
	}

	// cout << "colorData已经赋值" << endl;
}

// 将int类型的RGB值数组转换为uint8_t类型的数组
std::vector<uint8_t> convertRGBToInt8(const std::vector<int> &rgbValues, int width, int height)
{
	std::vector<uint8_t> pixelData(width * height * 3); // 每个像素3个字节（RGB）
	for (int i = 0; i < rgbValues.size(); i += 3)
	{
		// 假设rgbValues中的值在0到255之间，可以直接转换为uint8_t
		pixelData[i] = static_cast<uint8_t>(rgbValues[i]);		   // R
		pixelData[i + 1] = static_cast<uint8_t>(rgbValues[i + 1]); // G
		pixelData[i + 2] = static_cast<uint8_t>(rgbValues[i + 2]); // B
	}
	return pixelData;
}

int Accuratew = 1;
bool saveBMP(const std::string &filename, int width, int height, const std::vector<int> &rgbValues)
{
	std::vector<uint8_t> pixelData = convertRGBToInt8(rgbValues, width, height);

	int rowPadding = (4 - (width * 3) % 4) % 4;
	int dataSize = (width * 3 + rowPadding) * height;
	int fileSize = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader) + dataSize;

	BMPFileHeader fileHeader;
	fileHeader.bfType = 0x4D42;
	fileHeader.bfSize = fileSize;
	fileHeader.bfReserved1 = 0;
	fileHeader.bfReserved2 = 0;
	fileHeader.bfOffBits = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader);

	BMPInfoHeader infoHeader;
	infoHeader.biSize = sizeof(BMPInfoHeader);
	infoHeader.biWidth = width;
	infoHeader.biHeight = height;
	infoHeader.biPlanes = 1;
	infoHeader.biBitCount = 24;
	infoHeader.biCompression = 0;
	infoHeader.biSizeImage = dataSize;
	infoHeader.biXPelsPerMeter = 0;
	infoHeader.biYPelsPerMeter = 0;
	infoHeader.biClrUsed = 0;
	infoHeader.biClrImportant = 0;

	std::ofstream bmpFile(filename, std::ios::binary);
	if (!bmpFile.is_open())
	{
		std::cerr << "无法打开文件 " << filename << "！" << std::endl;
		return false;
	}
	// cout << "l";
	bmpFile.write(reinterpret_cast<char *>(&fileHeader), sizeof(BMPFileHeader));
	bmpFile.write(reinterpret_cast<char *>(&infoHeader), sizeof(BMPInfoHeader));
	int Last = 0;
	// cout << "lwww";
	int cishua = 0;
	for (int y = height - 1; y >= 0; --y)
	{ // BMP是倒序存储图像的，所以从底部开始写
		for (int x = 0; x < width; ++x)
		{
			cishua++;
			int index = (y * width + x) * 3;
			bmpFile.write(reinterpret_cast<char *>(&pixelData[index]), 3);
		}
		if (rowPadding > 0)
		{
			std::vector<uint8_t> padding(rowPadding, 0);
			bmpFile.write(reinterpret_cast<char *>(padding.data()), padding.size());
		}
	}

	bmpFile.close();
	return true;
}

// 16进制转10进制
int hexStringToDecimal(const std::string &hexStr)
{
	// 创建一个字符串流，用于从字符串中读取数据
	std::istringstream iss(hexStr);
	// 设置输入流的基数为16，表示我们将要读取十六进制数
	iss >> std::hex;
	// 定义一个整数变量来存储转换后的十进制数
	int decimalValue;
	// 从字符串流中读取数据，并存储到decimalValue中
	iss >> decimalValue;
	// 返回转换后的十进制数
	return decimalValue;
}

// 将整数转换为十六进制字符串的函数
std::string intToHexString(int value, int width = 2)
{
	// 使用std::stringstream来构建十六进制字符串
	std::stringstream ss;

	// 设置输出格式为十六进制，并设置字段宽度和填充字符
	ss << std::hex << std::setw(width) << std::setfill('0');

	// 注意：这里我们将value强制转换为unsigned char，以确保只取低8位
	// 如果value的值大于255，这样做会丢失高位信息，只保留低8位的有效十六进制表示
	ss << (unsigned char)value;

	// 从字符串流中获取最终的十六进制字符串
	return ss.str();
}

// 文件转二维码
void FileTranslateToTwoDiemionCode(const char Line[], string OutPut_Line, int wight, int hight)
{

	// 打开文件，以二进制模式
	std::ifstream file(Line, std::ios::binary | std::ios::ate); // 打开文件，并立即将文件指针移到末尾
	if (!file.is_open())
	{
		std::cerr << "无法打开文件！" << std::endl;
		system("pause");
		return;
	}
	// 获取文件大小

	std::uintmax_t fileSize = file.tellg();
	file.seekg(0, std::ios::beg); // 重置文件指针到文件开始
	// 创建一个向量来存储读取的数据
	std::vector<unsigned char> data;

	// 临时缓冲区，用于一次读取一块数据
	const std::size_t bufferSize = 1024;
	unsigned char buffer[bufferSize];
	std::uintmax_t bytesRead = 0; // 已读取的字节数
	// 循环读取文件，直到文件末尾
	int Last = 0;
	system("cls");
	cout << "文件读取中zzz" << endl;
	while (file.read(reinterpret_cast<char *>(buffer), bufferSize))
	{
		// 将读取的数据添加到向量中
		data.insert(data.end(), buffer, buffer + file.gcount());
		bytesRead += file.gcount();
		// 计算并输出进度
		// float progress = static_cast<double>(bytesRead) / fileSize * 100.0;
		// cout << "bytesRead:" << bytesRead << "fileSize" << fileSize << endl;
		// Last  = CreatProcess(30, bytesRead, fileSize, true, "▉", "▏", Last, "", "\n");
	}
	Last = 0;
	// 检查文件末尾是否还有剩余数据（最后一次读取可能不足bufferSize）
	if (file.gcount() > 0)
	{
		data.insert(data.end(), buffer, buffer + file.gcount());
	}

	// 关闭文件
	file.close();
	// cout << "w";
	//  打印数据，以十六进制格式
	// 边打印边记录大小
	int dataSize = 0;
	// cout << "l";
	// cout << "y";
	for (unsigned char byte : data)
	{
		// std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte) << " ";
		dataSize++;
	}
	// cout << "y";

	// 输出读取的总字节数（即循环运行次数）
	// std::cout << "\nTotal bytes read: " << dataSize << std::endl;
	// std::cout << "dataSize: " <<   std::dec << dataSize << std::endl; // 这将再次以十进制输出
	std::cout << std::endl;

	// 给输出精度赋值

	if (dataSize <= 51200)
		Accuratew = 25;
	else if (dataSize <= 256000)
		Accuratew = 10;
	else if (dataSize <= 552960)
		Accuratew = 5;
	else if (dataSize <= 5529600)
		Accuratew = 1;
	else
	{
		Accuratew = 0.1;
	}

	// 已经获取了数据了
	// 处理为二维码生成
	// 获取第一个RGB
	// int R = Translate16ToRGB(data, 111);
	//	cout << "R:" << R << endl;

	// 假设你的RGB值是int类型
	std::vector<int> rgbInts;
	// cout << "w";
	// 填充给rgbInts
	// cout << "dataSize" << dataSize;

	int xunhuancishu = (dataSize + 1) / 3;
	if (dataSize % 3 != 0)
		xunhuancishu++;
	// cout << "xunhuancishu" << xunhuancishu;
	for (int i = 0; i < xunhuancishu; i++)
	{
		// cout << "i" << i << endl;
		// cout << "xunhuanci" << xunhuancishu << endl;
		// cout << "w";
		int R = Translate16ToRGB(data, i * 3 + 1);
		int G = Translate16ToRGB(data, i * 3 + 2);
		int B = Translate16ToRGB(data, i * 3 + 3);
		// 存入

		rgbInts.push_back(B);

		rgbInts.push_back(G);
		rgbInts.push_back(R);
		//	cout << "现在的RGB：" << R << " " << G << " " << B << " " << endl;
	}

	// 添加标识符:114514faceaa,16进制即为0B 2D 0E FA CE AA,RGB为11 45 14 250 206 170
	rgbInts.push_back(14);
	rgbInts.push_back(45);
	rgbInts.push_back(11);

	rgbInts.push_back(170);
	rgbInts.push_back(206);
	rgbInts.push_back(250);

	// 添加后缀
	// 这个里存了后缀名
	std::string HouZhui;
	std::string strLine(Line); // 将 char 数组转换为 std::string

	// 查找 '.' 的位置
	size_t dotPos = strLine.find('.');
	if (dotPos != std::string::npos)
	{
		// 提取 '.' 之后的内容
		HouZhui = strLine.substr(dotPos + 1);
		// 输出结果
		// std::cout << "Extension: " << extension << std::endl;
	}
	else
	{
		std::cout << "No '.' found in the string." << std::endl;
	}
	int HouzhuiNum = HouZhui.size();
	// 最大6个后缀
	/*
	0->a
	1->b
	25->z
	倒序的,如bmp存起来就是pmb
	*/
	for (int i = 0; i < HouzhuiNum; i++)
	{
		rgbInts.push_back(HouZhui[i] - 'a');
	}
	for (int i = 0; i < 3 - (HouzhuiNum % 3); i++)
	{
		rgbInts.push_back(222);
	}

	//	writeBMP(OutPut_Line, rgbData, 21, 21);
	// std::vector<int> rgbIntsw = {66,77,232,1,5,11};
	// cout << "a";
	saveBMP(OutPut_Line.c_str(), wight, hight, rgbInts);
	// cout << "第一个RGB：" << "R:" << rgbInts[0] << "G:" << rgbInts[1] << "B:" << rgbInts[2] << endl;
	// std::cout << "BMP文件已生成。" << std::endl;
}

void writeHexToFile(const std::vector<int> &data, const std::string &filename)
{
	std::ofstream file(filename, std::ios::binary);
	if (!file.is_open())
	{
		std::cerr << "Failed to open file: " << filename << std::endl;
		return;
	}

	for (int value : data)
	{
		// Ensure value is within the range of 0 to 255
		if (value < 0 || value > 255)
		{
			std::cerr << "Value out of range: " << value << std::endl;
			continue;
		}

		// Write the value as a single byte to the file
		char byte = static_cast<char>(value);
		file.write(&byte, 1);
	}

	file.close();
}

// 二维码转文件
void TwoDiemionCodeTranslateToFile(const char Line[], string OutPut_Line)
{

	// 加载图片
	MixVecotrBlack(Line);
	// 获取文件大小
	std::ifstream file(Line, std::ios::binary | std::ios::ate); // 打开文件，并立即将文件指针移到末尾
	if (!file.is_open())
	{
		std::cerr << "无法打开文件！" << std::endl;
		system("pause");
		return;
	}
	// 获取文件大小

	std::uintmax_t fileSize = file.tellg();
	file.seekg(0, std::ios::beg); // 重置文件指针到文件开始

	// std::cout << "File size: " << fileSize << " bytes" << std::endl;
	//  关闭文件
	file.close();
	// system("pause");
	// 给输出精度赋值
	int Last = 0;
	if (fileSize <= 51200)
		Accuratew = 25;
	else if (fileSize <= 256000)
		Accuratew = 10;
	else if (fileSize <= 552960)
		Accuratew = 5;
	else if (fileSize <= 5529600)
		Accuratew = 1;
	else
	{
		Accuratew = 0.1;
	}
	// 获取RGB,转为16进制对应值写入
	int wight = bif.biWidth;
	int hight = bif.biHeight;
	vector<int> VeRGB;
	int cih = 0;

	// cout << "size:" << fileSize;
	// system("pause");
	string HouName = "";
	for (int j = 0; j < hight; j++)
	{
		for (int i = 0; i < wight; i++)
		{
			cih++;
			RGB nowRgb = GetNowRGB(ColorData, i, j);
			// 看是不是标识符
			if ((nowRgb.R == 11) && (nowRgb.G == 45) && (nowRgb.B == 14))
			{

				// 发现第一个标识符，找下一个
				// cout << "找到了" << endl;
				if (i != wight)
					i++;
				else
				{
					j++;
				}
				nowRgb = GetNowRGB(ColorData, i, j);
				int hx = i;
				int hy = j;
				if ((nowRgb.R == 250) && (nowRgb.G == 206) && (nowRgb.B == 170))
				{
					// 发现是,终止
					// 在这里看一下上面是否有255，255表示的是空

					if (i == 1)
					{
						// 减去2位置
						i = wight;
						j--;
					}
					else if (i == 0)
					{
						// 减去2
						i = wight - 1;
						j--;
					}
					else
					{
						i -= 2;
					}
					nowRgb = GetNowRGB(ColorData, i, j);
					// cout << "现在的R:" << nowRgb.R << "G:" << nowRgb.G << "B:" << nowRgb.B << endl;

					if (nowRgb.R == 255)
					{
						// cout << "1";
						VeRGB.erase(VeRGB.end() - 1);
					}
					if (nowRgb.G == 255)
					{
						// cout << "2";
						VeRGB.erase(VeRGB.end() - 1);
					}
					if (nowRgb.B == 255)
					{
						// cout << "3";
						VeRGB.erase(VeRGB.end() - 1);
					}

					// 屎山把上一个的255也尝试删了
					if (i == 0)
					{
						// 减去2位置
						i = wight - 1;
						j--;
					}
					else
					{
						i--;
					}
					nowRgb = GetNowRGB(ColorData, i, j);
					// cout << "现在的R:" << nowRgb.R << "G:" << nowRgb.G << "B:" << nowRgb.B << endl;

					if (nowRgb.R == 255)
					{
						// cout << "1";
						VeRGB.erase(VeRGB.end() - 1);
					}
					if (nowRgb.G == 255)
					{
						// cout << "2";
						VeRGB.erase(VeRGB.end() - 1);
					}
					if (nowRgb.B == 255)
					{
						// cout << "3";
						VeRGB.erase(VeRGB.end() - 1);
					}
					// SDL_Delay(888888);

					// 获取拓展名
					if (hx == wight - 1)
					{

						hx = 0;
						hy++;
					}
					else
					{
						hx++;
					}
					vector<int> TempVe;
					RGB nowRgb1 = GetNowRGB(ColorData, hx, hy);
					if (hx == wight - 1)
					{

						hx = 0;
						hy++;
					}
					else
					{
						hx++;
					}
					RGB nowRgb2 = GetNowRGB(ColorData, hx, hy);
					if (nowRgb1.B != 222)
						TempVe.push_back(nowRgb1.B);
					if (nowRgb1.G != 222)
						TempVe.push_back(nowRgb1.G);
					if (nowRgb1.R != 222)
						TempVe.push_back(nowRgb1.R);
					if (nowRgb2.B != 222)
						TempVe.push_back(nowRgb2.B);
					if (nowRgb2.G != 222)
						TempVe.push_back(nowRgb2.G);
					if (nowRgb2.R != 222)
						TempVe.push_back(nowRgb2.R);

					for (int i = 0; i < TempVe.size(); i++)
					{
						char cm = TempVe[i] + 'a';
						HouName += cm;
					}

					// 该删的删完了,
					goto jo;
				}
				else
				{
					// 不是
					i--;
					j--;
				}
			}
			VeRGB.push_back(nowRgb.R);
			VeRGB.push_back(nowRgb.G);
			VeRGB.push_back(nowRgb.B);
			// cout << "w";
		}
	}
jo:
	// 改正错误,删去3个结尾[屎山不要动]-----------------------这里结尾有问题，回来改正
	//  删除最后三个元素
	// VeRGB.erase(VeRGB.end() - 3, VeRGB.end());
	// 写入
	//  调用函数将数据写入文件
	//  打开输出文件
	vector<int> kkk = {232, 164, 240};

	// 接下来删去255的值
	/*
	int jj = VeRGB.size() - 1;
	while (1) {
		if (VeRGB[jj] == 255) {
			//删去
			cout << "kkk" << endl;
			VeRGB.erase(VeRGB.end() - 1);
			cout << "kkkw" << endl;
		}
		else
		{
			//cout << "kkk" << endl;
			break;
		}
		jj--;
	}
	*/
	writeHexToFile(VeRGB, OutPut_Line + "." + HouName);
	// std::cout << "数据已写入文件 " << OutPut_Line <<  std::endl;

	// cout << "R:" << nowRgb.R << endl;
	// cout << "G:" << nowRgb.G << endl;
	// cout << "B:" << nowRgb.B << endl;
}

// 要求选择路径函数
//  Function to display an Open File Dialog and return the selected path as a std::wstring
std::wstring GetSelectedPath()
{
	OPENFILENAMEW ofn;		  // common dialog box structure
	wchar_t szFile[MAX_PATH]; // buffer for file name, MAX_PATH is defined in windows.h
	std::wstring selectedPath;

	// Initialize OPENFILENAMEW
	ZeroMemory(&ofn, sizeof(ofn));
	ofn.lStructSize = sizeof(ofn);
	ofn.hwndOwner = NULL;
	ofn.lpstrFile = szFile;
	ofn.lpstrFile[0] = L'\0';
	ofn.nMaxFile = sizeof(szFile) / sizeof(wchar_t); // Ensure we use wchar_t size
	ofn.lpstrFilter = NULL;
	ofn.nFilterIndex = 0;
	ofn.lpstrFileTitle = NULL;
	ofn.nMaxFileTitle = 0;
	ofn.lpstrInitialDir = NULL;
	ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST | OFN_NOCHANGEDIR | OFN_EXPLORER;

	// Note: OFN_FILEMUSTEXIST may not be what you want if you only want a directory path.
	// If you want a directory selector, use SHBrowseForFolder.

	// Display the Open dialog box.
	if (GetOpenFileNameW(&ofn) == TRUE)
	{
		// Construct the full path from the directory and file name
		selectedPath = ofn.lpstrFile;

		// If you only want the directory path, you can remove the file name part like this:
		// wchar_t* lastBackslash = wcsrchr(selectedPath.data(), L'\\');
		// if (lastBackslash)
		// {
		//     selectedPath.resize(lastBackslash - selectedPath.data() + 1); // Include the backslash
		// }
		// else
		// {
		//     selectedPath.clear(); // No valid path found
		// }

		// The above code snippet is optional and depends on your needs.
	}

	return selectedPath;
}
// Wstirng转char
std::string WStringToUTF8(const std::wstring &wstr)
{
	std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
	return converter.to_bytes(wstr);
}

int main(int argc, char const *argv[])
{
	freopen("../config.txt", "r", stdin);
	string mode, target_path, output_path;

	// 写入配置
	cin >> mode;
	target_path = "../msg.txt";
	output_path = "../result.bmp";

	//  关闭输入输出缓存，使效率提升
	ios::sync_with_stdio(false);
	// 解除cin和cout的默认绑定，来降低IO的负担使效率提升
	cin.tie(NULL);
	// 要要求选择路径

	if (mode == "encode")
	{

		// 获取文件大小,用于推荐像素大小
		std::ifstream file(target_path, std::ios::binary | std::ios::ate); // 打开文件，并立即将文件指针移到末尾
		if (!file.is_open())
			return 0;
		// 获取文件大小

		std::uintmax_t fileSize = file.tellg();
		file.seekg(0, std::ios::beg); // 重置文件指针到文件开始

		//  关闭文件
		file.close();

		float jjj = sqrt(fileSize / 3);
		int kk = jjj + 1;

		FileTranslateToTwoDiemionCode(target_path.c_str(), output_path, kk, kk);
	}
	if (mode == "decode")
		TwoDiemionCodeTranslateToFile(target_path.c_str(), output_path);
}