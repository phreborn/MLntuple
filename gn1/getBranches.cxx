void getBranches(TString file){
  TFile *f = new TFile(file, "read");
  TTree *tree = (TTree*)f->Get("nominal");
  TObjArray *branches = tree->GetListOfBranches();
  for(int i = 0; i < branches->GetEntries(); i++){
    TBranch *branch = (TBranch *)branches->At(i);
    TString bname = branch->GetName();
    std::cout<< bname << std::endl;
  }
}
