//+------------------------------------------------------------------+
//|                                                     pythonNN.mq4 |
//|                        Copyright 2015, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2015, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
#property indicator_chart_window
#property indicator_buffers 2
#property indicator_plots   2
//--- plot low
#property indicator_label1  "low"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrBlue
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- plot high
#property indicator_label2  "high"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrSeaGreen
#property indicator_style2  STYLE_SOLID
#property indicator_width2  1




#import "mtguru1.dll"

double __checkLibrary();
void __loadNN(char& array[]);

#import



extern string NN_LOADER_FILENAME = "loadNN.py";

//--- indicator buffers
double         lowBuffer[];
double         highBuffer[];
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,lowBuffer);
   SetIndexBuffer(1,highBuffer);
   
   SetIndexStyle (0,DRAW_LINE,STYLE_SOLID,1);
   SetIndexStyle (1,DRAW_LINE,STYLE_SOLID,1);
   
   
   char CHAR_FILENAME[];
   ArrayResize(CHAR_FILENAME, StringLen(NN_LOADER_FILENAME) + 1);
   StringToCharArray(NN_LOADER_FILENAME, CHAR_FILENAME);
   CHAR_FILENAME[StringLen(NN_LOADER_FILENAME)] = '\0';
   __loadNN(CHAR_FILENAME);
   
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[]){
   int i;
   int Counted_bars;
   Counted_bars=IndicatorCounted();
   i=Bars-Counted_bars-1;
   while(i>=0){
      lowBuffer[i]=__checkLibrary();
      highBuffer[i]=Low[i];
      i--;
   }
   return(rates_total);
}
