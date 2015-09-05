// mtguru1.cpp : Defines the entry point for the DLL application.
//
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff from Windows headers
#include "stdafx.h"
#include <Python.h>

#define MT4_EXPFUNC __declspec(dllexport)

MT4_EXPFUNC double __stdcall __checkLibrary(){
	return 1.14;
}

MT4_EXPFUNC void __stdcall __predict(double* data, double* res, const int size){
	Py_Initialize();
	PyObject* main_module, *global_dict, *expression;
	main_module = PyImport_AddModule("__main__");
	global_dict = PyModule_GetDict(main_module);
	expression = PyDict_GetItemString(global_dict, "predict");

	PyObject *mylist = PyList_New(size);
	for (size_t i = 0; i != size; ++i){
		PyList_SET_ITEM(mylist, i, PyFloat_FromDouble(data[i]));
	}
	PyObject *arglist = Py_BuildValue("(o)", mylist);
	PyObject *result = PyObject_CallObject(expression, arglist);
	for (size_t i = 0; i < PyList_Size(result); i++){
		res[i] = PyFloat_AsDouble(PyList_GET_ITEM(result, i));
	}
	Py_Finalize();
}

MT4_EXPFUNC void __stdcall __loadNN(char* filename){
	FILE* exp_file = fopen(filename, "r");
	Py_Initialize();
	PyRun_SimpleFile(exp_file, NULL);
	Py_Finalize();
	fclose(exp_file);
}