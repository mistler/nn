//+------------------------------------------------------------------+
//|                                                         Demo.mq4 |
//|                                                       Codersguru |
//|                                         http://www.forex-tsd.com |
//+------------------------------------------------------------------+
#property copyright "Codersguru"
#property link      "http://www.forex-tsd.com"

#property indicator_chart_window
#include <gFiles.mqh>

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int init()
  {

   int file = gFileOpen("c:\mt4.log",WRITE); //open the file for read and write , create it if not exist
   string write = "Open Price: " + Open[1] + " - Close Price: " + Close[1];
   gFileWrite(file,write); //write some date
   gFileClose(file); //close the file
   
   

   return(0);
  }
//+------------------------------------------------------------------+
//| Custor indicator deinitialization function                       |
//+------------------------------------------------------------------+
int deinit()
  {
//---- 
   
//----
   return(0);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int start()
  {
   
   return(0);
  }
//+------------------------------------------------------------------+