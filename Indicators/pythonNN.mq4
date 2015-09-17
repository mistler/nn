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

int __predict(long& dv[], double& data[], double& res[]);
int __connect();
int __disconnect();

#import


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
   __connect();
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
   if(i > 1000){
      i = 1000;
   }
   double result[1];
   double data[4];
   long dv[2];
   while(i >= 0){
      dv[0] = Time[i];
      dv[1] = Volume[i];
      data[0] = Low[i];
      data[1] = Open[i];
      data[2] = Close[i];
      data[3] = High[i];
      __predict(dv, data, result);
      highBuffer[i] = result[0];
      i--;
   }
   return(rates_total);
}
