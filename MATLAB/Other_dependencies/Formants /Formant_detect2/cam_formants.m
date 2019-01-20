function formant_matrix = cam_formants(x, fs, filename)
% ex103.m
% get a waveform
ms10=ceil(fs*0.005);
ms30=floor(fs*0.03);
ncoeff=2+fs/1000;           % rule of thumb for formant estimation
% plot waveform
t=(0:length(x)-1)/fs;
% process in chunks of 30ms
pos=1;
fm=[];      % formant peaks
ft=[];      % formant times
while (pos+ms10) <= length(x) %was ms30 before
    y=x(pos:pos+ms10-1); %was ms30 before
    y=y-mean(y);%Normalize
    % find LP filter
    a=lpc(y,ncoeff);
    % find roots
    r=roots(a);
    r=r(imag(r)>0.01);
    ffreq=sort(atan2(imag(r),real(r))*fs/(2*pi));
    fm = [fm ffreq(1:4)]; %%REDUCED FFREQ ARRAY TO 3 CAN INCREASE 6
    ft=[ft pos/fs];
    pos=pos+ms10;
end;

formant_matrix= [round(ft,3); fm]';
% plot formants trace
