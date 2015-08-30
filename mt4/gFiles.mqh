//+------------------------------------------------------------------+
//|                                                       gFiles.mqh |
//|                                                       Codersguru |
//|                                         http://www.forex-tsd.com |
//+------------------------------------------------------------------+
#property copyright "Codersguru."
#property link      "http://www.forex-tsd.com"

//open mode constants
#define READ 1
#define WRITE 2
#define READWRITE 3
//seek mode constants
#define FILE_BEGIN 0
#define FILE_CURRENT 1
#define FILE_END 2

#import "mtguru1.dll"

int  gFileOpen(string file_name,int mode);
bool gFileWrite(int handle,string data);
bool  gFileClose(int handle);
string gFileRead(int handle,int length=0);
void gFileSeek(int handle,int offset, int mode);
bool gFileDelete(string file_name);
int gFileSize(int handle);

#import