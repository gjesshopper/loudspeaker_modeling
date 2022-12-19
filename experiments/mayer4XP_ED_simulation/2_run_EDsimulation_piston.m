

addpath("/Users/jesperholsten/Desktop/ELSYS/5. År/Høst 2022/RFE4580 Prosjektoppgave/EDtoolbox/Edge-diffraction-Matlab-toolbox-master");

mfile = mfilename('fullpath');
[infilepath,filestem] = fileparts(mfile);

[corners,planecorners] = GEOmakeshoebox(0.1025,0.1025,0.1454);

geofiledata = struct('corners',corners,'planecorners',planecorners);
soucoordinates = GEOcirclepoints(0.05*0.8,1);  %here
soucoordinates(:,3) = 0.0001; 
Sindata = struct('coordinates',soucoordinates);
Sindata.doaddsources = 1;

%load source amplitudes from python
pythondata = load('source_amplitudes_fp_9.mat'); 
Sindata.sourceamplitudes = pythondata.source_amplitudes;

%define receiver angles
phivec = [[0:3:87] [93:3:267] [273:3:360]].';
recradius = 2.35;
Rindata = struct('coordinates',recradius*[sind(phivec) 0*phivec cosd(phivec)]);

%set samling frequency
controlparameters = struct('fs',48000);

filehandlingparameters = struct('outputdirectory',[infilepath,filesep,'results_after_sa_final_1layers']); %here
filehandlingparameters.filestem = filestem;
filehandlingparameters.savelogfile = 1;
filehandlingparameters.showtext = 1;


nfft = 8192;
fvec = controlparameters.fs/nfft*[0:nfft/2-1];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

controlparameters.difforder = 8; 
controlparameters.ngauss = 48;


%Pick out desired frequencies for the simulation
fvec_tf = fvec(10:5 :1000);

controlparameters.frequencies = fvec_tf;

%run the simulation
EDmain_convexESIE(geofiledata,Sindata,Rindata,struct,controlparameters,filehandlingparameters);



