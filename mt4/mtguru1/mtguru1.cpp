// mtguru1.cpp : Defines the entry point for the DLL application.
//
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff from Windows headers
#include "stdafx.h"
#include <Python.h>

#define MT4_EXPFUNC __declspec(dllexport)

MT4_EXPFUNC double __stdcall __checkLibrary(){
	return 1.14;
}

MT4_EXPFUNC void __stdcall __predict(double* data, double* result, const int dataSize, const int inputSize){
	Py_Initialize();

	Py_Finalize();
}

MT4_EXPFUNC void __stdcall __loadNN(const char* filename){
	FILE* exp_file = fopen(filename, "r");
	Py_Initialize();
	PyRun_SimpleFile(exp_file, NULL);
	Py_Finalize();
}