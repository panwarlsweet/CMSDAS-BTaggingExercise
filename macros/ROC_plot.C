void graph() {
   //Draw a simple graph
   // To see the output of this macro, click begin_html <a href="gif/graph.gif">here</a>. end_html
   //Author: Rene Brun
   TFile *f = new TFile("phase2.root","recreate");
   TCanvas *c1 = new TCanvas("c1","SubJet_btagging_Phase2_vs_Run2",200,10,700,500);

   c1->SetFillColor(42);
   c1->SetGrid();

   const Int_t n = 20;
  // Double_t x[n], y[n];
    double  y[n]={1.0 ,
        0.208186547985 ,
        0.0868676737918 ,
        0.0519776844481 ,
        0.0357801040557 ,
        0.0269040305899 ,
        0.0209365009716 ,
        0.0165486115464 ,
        0.0134896257757 ,
        0.0111703127938 ,
        0.00959067260076 ,
        0.00812386385006 ,
        0.00670720240707 ,
        0.00550366702188 ,
        0.00453833134834 ,
        0.00378612173259 ,
        0.00292108067448 ,
        0.00221901836645 ,
        0.00136651413527 ,
        0.000626841346455 ,
    };
    double  x[n]={1.0 ,
        0.891670988487 ,
        0.789835079349 ,
        0.708992843066 ,
        0.639456487916 ,
        0.575562700965 ,
        0.51789233482 ,
        0.462835805414 ,
        0.412592054766 ,
        0.367824914428 ,
        0.330982263251 ,
        0.294015143657 ,
        0.258147495073 ,
        0.224872938492 ,
        0.191224976662 ,
        0.156726480656 ,
        0.124655118764 ,
        0.0929364173841 ,
        0.0605123949798 ,

        
    };
  f->cd();
   for (Int_t i=0;i<n;i++) {
     printf(" i %i %f %f \n",i,x[i],y[i]);
   }
   TGraph *gr = new TGraph(n,x,y);
   gr->SetLineColor(kGreen);
   gr->SetLineWidth(4);
   gr->SetLineStyle(1);
    gr->SetMarkerSize(0);
   gr->SetMarkerColor(kRed);
   gr->SetMarkerStyle(21);
   gr->SetTitle("DeepCSV_SubJet_btagging_Run2VsPhase2");
   gr->GetXaxis()->SetTitle("b-tagging efficiency");
   gr->GetYaxis()->SetTitle("mistag rate");
   gr->Draw();
   gr->Write();
   // TCanvas::Update() draws the frame, after which one can change it
   c1->Update();
   c1->SetLogy();
   c1->GetFrame()->SetFillColor(21);
   c1->GetFrame()->SetBorderSize(12);
   c1->Modified();
   c1->Write();
   c1->SaveAs("udsg_r.png");
   f->Close();
}

