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

// �йز���rgbֵ,�ٶȸ���
BITMAPFILEHEADER bmf;
BITMAPINFOHEADER bif;
FILE *pf;
PPIXCOLOR *ColorData;
// ����ֵΪ0��ʾ�򿪳ɹ�����0��Ϊʧ��
errno_t err;

struct RGB
{
	int R;
	int G;
	int B;
};

#pragma pack(push, 1) // �����ֽڶ��룬ȷ���ṹ�尴1�ֽڶ���

struct BMPFileHeader
{
	uint16_t bfType;	  // �ļ����ͣ������� "BM"
	uint32_t bfSize;	  // �ļ���С���ֽڣ�
	uint16_t bfReserved1; // ����������Ϊ0
	uint16_t bfReserved2; // ����������Ϊ0
	uint32_t bfOffBits;	  // ���ļ�ͷ��ʵ��ͼ�����ݵ�ƫ�ƣ��ֽڣ�
};

struct BMPInfoHeader
{
	uint32_t biSize;		 // ���ṹ��Ĵ�С���ֽڣ�
	int32_t biWidth;		 // ͼ���ȣ����أ�
	int32_t biHeight;		 // ͼ��߶ȣ����أ�����ֵ��ʾͼ�����ݴӵײ���ʼ
	uint16_t biPlanes;		 // ƽ����������Ϊ1
	uint16_t biBitCount;	 // ÿ�����ص�λ����24λ��ʾRGB��8λ
	uint32_t biCompression;	 // ѹ�����ͣ�0��ʾ��ѹ��
	uint32_t biSizeImage;	 // ͼ���С���ֽڣ������ڲ�ѹ����24λͼ�񣬵��ڿ��*�߶�*3
	int32_t biXPelsPerMeter; // ˮƽ�ֱ��ʣ�����/�ף�
	int32_t biYPelsPerMeter; // ��ֱ�ֱ��ʣ�����/�ף�
	uint32_t biClrUsed;		 // ʵ��ʹ�õ���ɫ���е���ɫ����0��ʾʹ��������ɫ
	uint32_t biClrImportant; // ��Ҫ��ɫ����0��ʾ������ɫ����Ҫ
};

#pragma pack(pop)

void writeBMP(const std::string &filename, const std::vector<uint8_t> &rgbData, int width, int height)
{
	// const int width = 5;
	// const int height = 2;
	const int rowSize = width * 3;				 // ÿ������3���ֽڣ�RGB��
	const int padding = (4 - (rowSize % 4)) % 4; // ����䣬ʹÿ�д�С��4�ı���
	const int imageSize = rowSize * height + padding * height;

	BMPFileHeader fileHeader;
	BMPInfoHeader infoHeader;

	// ��ʼ���ļ�ͷ
	fileHeader.bfType = 0x4D42; // "BM"
	fileHeader.bfSize = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader) + imageSize;
	fileHeader.bfReserved1 = 0;
	fileHeader.bfReserved2 = 0;
	fileHeader.bfOffBits = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader);

	// ��ʼ����Ϣͷ
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

	// ���ļ�����д��
	std::ofstream file(filename, std::ios::binary);
	if (!file.is_open())
	{
		std::cerr << "�޷����ļ� " << filename << std::endl;
		return;
	}

	// д���ļ�ͷ����Ϣͷ
	file.write(reinterpret_cast<const char *>(&fileHeader), sizeof(BMPFileHeader));
	file.write(reinterpret_cast<const char *>(&infoHeader), sizeof(BMPInfoHeader));

	// д��ͼ�����ݣ�ע�������
	int idx = 0;
	for (int y = height - 1; y >= 0; --y)
	{ // BMPͼ�������Ǵӵײ���ʼ��
		for (int x = 0; x < width; ++x)
		{
			if (idx < rgbData.size())
			{
				file.write(reinterpret_cast<const char *>(&rgbData[idx]), 3);
				idx += 3; // ÿ������3���ֽ�
			}
			else
			{
				// ������ݲ��㣬����ɫ
				file.write("\0\0\0", 3);
			}
		}
		// д�������
		for (int p = 0; p < padding; ++p)
		{
			file.write("\0", 1);
		}
	}

	file.close();
}
// ��ȡĳһxy��RGBֵ
RGB GetNowRGB(PPIXCOLOR *ColorData, int ReadX, int ReadY)
{

	// ��ֹԽ��
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
// rgbΪС�ڵ��ڵ��жϽ���
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
	// ��1����Ϊ����������0��ʼ
	Place--;

	// ���Place�Ƿ���Ч
	if (Place < 0 || Place >= data.size())
	{
		// std::cerr << "Error: Place index out of bounds!" << std::endl;
		return -1; // ����һ��������
	}

	// ȡ��ָ��λ�õ��ֽ�
	unsigned char byte = data[Place];

	// ��ȡ��λ��ʮ�������е�'e'��
	// char highNibble = (byte >> 4) & 0x0F;  // ����4λ�����ε�4λ
	// char highNibbleChar = highNibble >= 10 ? ('a' + (highNibble - 10)) : ('0' + highNibble);

	// ��ȡ��λ��ʮ�������е�'8'��
	// ����������һ���ֽڣ���ֵ��֪
	// char byte = 0x4F;  // ���磬���ֵ��01001111�Ķ����Ʊ�ʾ

	// ��ȡ��4λ������4λ����0x0F���������
	char highNibble = (byte >> 4) & 0x0F;
	// ��ȡ��4λ��ֱ����0x0F���������
	char lowNibble = byte & 0x0F;

	// ��nibbleת��Ϊ�ַ�
	char highNibbleChar = highNibble >= 10 ? ('A' + (highNibble - 10)) : ('0' + highNibble);
	char lowNibbleChar = lowNibble >= 10 ? ('A' + (lowNibble - 10)) : ('0' + lowNibble);

	// ���ת������ַ�
	// cout << "High Nibble Character: " << highNibbleChar << endl;
	// cout << "Low Nibble Character: " << lowNibbleChar << endl;

	// ���ַ�ת������ֵ
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

	// ���������ֽڵ�ʮ����ֵ
	int End = decimalValue * 16 + decimalValue2;
	// std::cout << "END: " <<   std::dec << End << std::endl; // �⽫�ٴ���ʮ�������

	return End;
}

// ����ͼƬ�ļ�+��ȡ
void MixVecotrBlack(const char *filename)
{

	err = fopen_s(&pf, filename, "rb");
	if (0 == err)
	{
		fread(&bmf, sizeof(bmf), 1, pf);
		fread(&bif, sizeof(bif), 1, pf);

		if (0x4d42 != bmf.bfType)
		{
			cout << "�ļ�����λͼ��" << endl;
			fclose(pf);
		}
		else if (24 != bif.biBitCount)
		{
			cout << "λͼ����24λ��" << endl;
			fclose(pf);
		}
		else
		{
			// cout << "ͼƬ�Ŀ�ȣ�" << bif.biWidth << endl;
			// cout << "ͼƬ�ĸ߶ȣ�" << bif.biHeight << endl;

			ColorData = new PPIXCOLOR[bif.biHeight];

			// һ�е��ֽ���
			int lineCount = bif.biSizeImage / bif.biHeight;

			// ���ʱ��ӵ�����һ�п�ʼ�棬���Զ���ʱ������������һ�з�
			// ����ɫ����
			for (int i = bif.biHeight - 1; i >= 0; i--)
			{
				ColorData[i] = new PIXCOLOR[bif.biWidth];
				fread(ColorData[i], sizeof(PIXCOLOR), bif.biWidth, pf);
				// ƫ��  bif.biWidth * sizeof(PIXCOLOR)�ж��ٸ��ֽ�
				fseek(pf, lineCount - bif.biWidth * sizeof(PIXCOLOR), SEEK_CUR);
			}
			fclose(pf);
		}
	}

	// cout << "colorData�Ѿ���ֵ" << endl;
}

// ��int���͵�RGBֵ����ת��Ϊuint8_t���͵�����
std::vector<uint8_t> convertRGBToInt8(const std::vector<int> &rgbValues, int width, int height)
{
	std::vector<uint8_t> pixelData(width * height * 3); // ÿ������3���ֽڣ�RGB��
	for (int i = 0; i < rgbValues.size(); i += 3)
	{
		// ����rgbValues�е�ֵ��0��255֮�䣬����ֱ��ת��Ϊuint8_t
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
		std::cerr << "�޷����ļ� " << filename << "��" << std::endl;
		return false;
	}
	// cout << "l";
	bmpFile.write(reinterpret_cast<char *>(&fileHeader), sizeof(BMPFileHeader));
	bmpFile.write(reinterpret_cast<char *>(&infoHeader), sizeof(BMPInfoHeader));
	int Last = 0;
	// cout << "lwww";
	int cishua = 0;
	for (int y = height - 1; y >= 0; --y)
	{ // BMP�ǵ���洢ͼ��ģ����Դӵײ���ʼд
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

// 16����ת10����
int hexStringToDecimal(const std::string &hexStr)
{
	// ����һ���ַ����������ڴ��ַ����ж�ȡ����
	std::istringstream iss(hexStr);
	// �����������Ļ���Ϊ16����ʾ���ǽ�Ҫ��ȡʮ��������
	iss >> std::hex;
	// ����һ�������������洢ת�����ʮ������
	int decimalValue;
	// ���ַ������ж�ȡ���ݣ����洢��decimalValue��
	iss >> decimalValue;
	// ����ת�����ʮ������
	return decimalValue;
}

// ������ת��Ϊʮ�������ַ����ĺ���
std::string intToHexString(int value, int width = 2)
{
	// ʹ��std::stringstream������ʮ�������ַ���
	std::stringstream ss;

	// ���������ʽΪʮ�����ƣ��������ֶο�Ⱥ�����ַ�
	ss << std::hex << std::setw(width) << std::setfill('0');

	// ע�⣺�������ǽ�valueǿ��ת��Ϊunsigned char����ȷ��ֻȡ��8λ
	// ���value��ֵ����255���������ᶪʧ��λ��Ϣ��ֻ������8λ����Чʮ�����Ʊ�ʾ
	ss << (unsigned char)value;

	// ���ַ������л�ȡ���յ�ʮ�������ַ���
	return ss.str();
}

// �ļ�ת��ά��
void FileTranslateToTwoDiemionCode(const char Line[], string OutPut_Line, int wight, int hight)
{

	// ���ļ����Զ�����ģʽ
	std::ifstream file(Line, std::ios::binary | std::ios::ate); // ���ļ������������ļ�ָ���Ƶ�ĩβ
	if (!file.is_open())
	{
		std::cerr << "�޷����ļ���" << std::endl;
		system("pause");
		return;
	}
	// ��ȡ�ļ���С

	std::uintmax_t fileSize = file.tellg();
	file.seekg(0, std::ios::beg); // �����ļ�ָ�뵽�ļ���ʼ
	// ����һ���������洢��ȡ������
	std::vector<unsigned char> data;

	// ��ʱ������������һ�ζ�ȡһ������
	const std::size_t bufferSize = 1024;
	unsigned char buffer[bufferSize];
	std::uintmax_t bytesRead = 0; // �Ѷ�ȡ���ֽ���
	// ѭ����ȡ�ļ���ֱ���ļ�ĩβ
	int Last = 0;
	system("cls");
	cout << "�ļ���ȡ��zzz" << endl;
	while (file.read(reinterpret_cast<char *>(buffer), bufferSize))
	{
		// ����ȡ��������ӵ�������
		data.insert(data.end(), buffer, buffer + file.gcount());
		bytesRead += file.gcount();
		// ���㲢�������
		// float progress = static_cast<double>(bytesRead) / fileSize * 100.0;
		// cout << "bytesRead:" << bytesRead << "fileSize" << fileSize << endl;
		// Last  = CreatProcess(30, bytesRead, fileSize, true, "��", "��", Last, "", "\n");
	}
	Last = 0;
	// ����ļ�ĩβ�Ƿ���ʣ�����ݣ����һ�ζ�ȡ���ܲ���bufferSize��
	if (file.gcount() > 0)
	{
		data.insert(data.end(), buffer, buffer + file.gcount());
	}

	// �ر��ļ�
	file.close();
	// cout << "w";
	//  ��ӡ���ݣ���ʮ�����Ƹ�ʽ
	// �ߴ�ӡ�߼�¼��С
	int dataSize = 0;
	// cout << "l";
	// cout << "y";
	for (unsigned char byte : data)
	{
		// std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte) << " ";
		dataSize++;
	}
	// cout << "y";

	// �����ȡ�����ֽ�������ѭ�����д�����
	// std::cout << "\nTotal bytes read: " << dataSize << std::endl;
	// std::cout << "dataSize: " <<   std::dec << dataSize << std::endl; // �⽫�ٴ���ʮ�������
	std::cout << std::endl;

	// ��������ȸ�ֵ

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

	// �Ѿ���ȡ��������
	// ����Ϊ��ά������
	// ��ȡ��һ��RGB
	// int R = Translate16ToRGB(data, 111);
	//	cout << "R:" << R << endl;

	// �������RGBֵ��int����
	std::vector<int> rgbInts;
	// cout << "w";
	// ����rgbInts
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
		// ����

		rgbInts.push_back(B);

		rgbInts.push_back(G);
		rgbInts.push_back(R);
		//	cout << "���ڵ�RGB��" << R << " " << G << " " << B << " " << endl;
	}

	// ��ӱ�ʶ��:114514faceaa,16���Ƽ�Ϊ0B 2D 0E FA CE AA,RGBΪ11 45 14 250 206 170
	rgbInts.push_back(14);
	rgbInts.push_back(45);
	rgbInts.push_back(11);

	rgbInts.push_back(170);
	rgbInts.push_back(206);
	rgbInts.push_back(250);

	// ��Ӻ�׺
	// �������˺�׺��
	std::string HouZhui;
	std::string strLine(Line); // �� char ����ת��Ϊ std::string

	// ���� '.' ��λ��
	size_t dotPos = strLine.find('.');
	if (dotPos != std::string::npos)
	{
		// ��ȡ '.' ֮�������
		HouZhui = strLine.substr(dotPos + 1);
		// ������
		// std::cout << "Extension: " << extension << std::endl;
	}
	else
	{
		std::cout << "No '.' found in the string." << std::endl;
	}
	int HouzhuiNum = HouZhui.size();
	// ���6����׺
	/*
	0->a
	1->b
	25->z
	�����,��bmp����������pmb
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
	// cout << "��һ��RGB��" << "R:" << rgbInts[0] << "G:" << rgbInts[1] << "B:" << rgbInts[2] << endl;
	// std::cout << "BMP�ļ������ɡ�" << std::endl;
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

// ��ά��ת�ļ�
void TwoDiemionCodeTranslateToFile(const char Line[], string OutPut_Line)
{

	// ����ͼƬ
	MixVecotrBlack(Line);
	// ��ȡ�ļ���С
	std::ifstream file(Line, std::ios::binary | std::ios::ate); // ���ļ������������ļ�ָ���Ƶ�ĩβ
	if (!file.is_open())
	{
		std::cerr << "�޷����ļ���" << std::endl;
		system("pause");
		return;
	}
	// ��ȡ�ļ���С

	std::uintmax_t fileSize = file.tellg();
	file.seekg(0, std::ios::beg); // �����ļ�ָ�뵽�ļ���ʼ

	// std::cout << "File size: " << fileSize << " bytes" << std::endl;
	//  �ر��ļ�
	file.close();
	// system("pause");
	// ��������ȸ�ֵ
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
	// ��ȡRGB,תΪ16���ƶ�Ӧֵд��
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
			// ���ǲ��Ǳ�ʶ��
			if ((nowRgb.R == 11) && (nowRgb.G == 45) && (nowRgb.B == 14))
			{

				// ���ֵ�һ����ʶ��������һ��
				// cout << "�ҵ���" << endl;
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
					// ������,��ֹ
					// �����￴һ�������Ƿ���255��255��ʾ���ǿ�

					if (i == 1)
					{
						// ��ȥ2λ��
						i = wight;
						j--;
					}
					else if (i == 0)
					{
						// ��ȥ2
						i = wight - 1;
						j--;
					}
					else
					{
						i -= 2;
					}
					nowRgb = GetNowRGB(ColorData, i, j);
					// cout << "���ڵ�R:" << nowRgb.R << "G:" << nowRgb.G << "B:" << nowRgb.B << endl;

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

					// ʺɽ����һ����255Ҳ����ɾ��
					if (i == 0)
					{
						// ��ȥ2λ��
						i = wight - 1;
						j--;
					}
					else
					{
						i--;
					}
					nowRgb = GetNowRGB(ColorData, i, j);
					// cout << "���ڵ�R:" << nowRgb.R << "G:" << nowRgb.G << "B:" << nowRgb.B << endl;

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

					// ��ȡ��չ��
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

					// ��ɾ��ɾ����,
					goto jo;
				}
				else
				{
					// ����
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
	// ��������,ɾȥ3����β[ʺɽ��Ҫ��]-----------------------�����β�����⣬��������
	//  ɾ���������Ԫ��
	// VeRGB.erase(VeRGB.end() - 3, VeRGB.end());
	// д��
	//  ���ú���������д���ļ�
	//  ������ļ�
	vector<int> kkk = {232, 164, 240};

	// ������ɾȥ255��ֵ
	/*
	int jj = VeRGB.size() - 1;
	while (1) {
		if (VeRGB[jj] == 255) {
			//ɾȥ
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
	// std::cout << "������д���ļ� " << OutPut_Line <<  std::endl;

	// cout << "R:" << nowRgb.R << endl;
	// cout << "G:" << nowRgb.G << endl;
	// cout << "B:" << nowRgb.B << endl;
}

// Ҫ��ѡ��·������
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
// Wstirngתchar
std::string WStringToUTF8(const std::wstring &wstr)
{
	std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
	return converter.to_bytes(wstr);
}

int main(int argc, char const *argv[])
{
	freopen("../config.txt", "r", stdin);
	string mode, target_path, output_path;

	// д������
	cin >> mode;
	target_path = "../msg.txt";
	output_path = "../result.bmp";

	//  �ر�����������棬ʹЧ������
	ios::sync_with_stdio(false);
	// ���cin��cout��Ĭ�ϰ󶨣�������IO�ĸ���ʹЧ������
	cin.tie(NULL);
	// ҪҪ��ѡ��·��

	if (mode == "encode")
	{

		// ��ȡ�ļ���С,�����Ƽ����ش�С
		std::ifstream file(target_path, std::ios::binary | std::ios::ate); // ���ļ������������ļ�ָ���Ƶ�ĩβ
		if (!file.is_open())
			return 0;
		// ��ȡ�ļ���С

		std::uintmax_t fileSize = file.tellg();
		file.seekg(0, std::ios::beg); // �����ļ�ָ�뵽�ļ���ʼ

		//  �ر��ļ�
		file.close();

		float jjj = sqrt(fileSize / 3);
		int kk = jjj + 1;

		FileTranslateToTwoDiemionCode(target_path.c_str(), output_path, kk, kk);
	}
	if (mode == "decode")
		TwoDiemionCodeTranslateToFile(target_path.c_str(), output_path);
}