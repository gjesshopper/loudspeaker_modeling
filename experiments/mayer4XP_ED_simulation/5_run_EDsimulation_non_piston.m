%add path to Peter Svenssons EDtoolbox
addpath("/Users/jesperholsten/Desktop/ELSYS/5. År/Høst 2022/RFE4580 Prosjektoppgave/EDtoolbox/Edge-diffraction-Matlab-toolbox-master");

mfile = mfilename('fullpath');
[infilepath,filestem] = fileparts(mfile);

[corners,planecorners] = GEOmakeshoebox(0.1025,0.1025,0.1454);

geofiledata = struct('corners',corners,'planecorners',planecorners);
soucoordinates = GEOcirclepoints(0.05*0.8,2);
soucoordinates(:,3) = 0.0001; 
Sindata = struct('coordinates',soucoordinates);
Sindata.doaddsources = 0;

%define receiver angles
phivec = [[0:3:87] [93:3:267] [273:3:360]].';
recradius = 2.35;
Rindata = struct('coordinates',recradius*[sind(phivec) 0*phivec cosd(phivec)]);

%set sampling frequency
controlparameters = struct('fs',48000);

filehandlingparameters = struct('outputdirectory',[infilepath,filesep,'results_before_sa_final_2layers']);
filehandlingparameters.filestem = filestem;
filehandlingparameters.savelogfile = 1;
filehandlingparameters.showtext = 1;


nfft = 8192;
fvec = controlparameters.fs/nfft*[0:nfft/2-1];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

controlparameters.difforder = 8; 
controlparameters.ngauss = 48;


%Pick out desired frequencies for the simulation
fvec_tf = fvec(10:5:1000)

controlparameters.frequencies = fvec_tf;

%run the simulation
EDmain_convexESIE(geofiledata,Sindata,Rindata,struct,controlparameters,filehandlingparameters);






