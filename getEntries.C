//root
#include <TLine.h>
//#include <TStyle.h>
#include <TVirtualFFT.h>
#include <TString.h>
#include <TCanvas.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>
#include <TMath.h>
#include <TF1.h>

//C, C++
#include <stdio.h>
#include <assert.h>
//#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <vector>
//#include <string>
//#include <iomanip>

using namespace std;


void read(TString inFile);

int main(int argc, char *argv[]){
  TString inFile;

  if(argc == 2){
    inFile = argv[1];
    //cout<<"Input data file : "<< inFile <<endl;
    read(inFile);
  }
  else{
    cout<<" ERROR --->  in input arguments "<<endl
        <<"        [1] - in data file"<<endl;
  }
  return 0;
}

void read(TString inFile){

    TFile fileIn(inFile);
    TTree* theTree = nullptr;
    fileIn.GetObject("cbmsim",theTree);
    
    cout << inFile << " " << theTree->GetEntries() << endl;
    
}
