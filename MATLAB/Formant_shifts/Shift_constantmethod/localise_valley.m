function [peakarray]= localise_valley(data, peak_freq, peak_amp)
%localise_valley(zeropoint5,27,0.02133)
%for more than one formant use a loop with the localise_valley 
%function to extract peak array
%INPUT ARGS
%data: data set consists of the amplitude for now ?*#
%peak_freq:the frequency/x vaue of the peak
%peak_amp: the amplitude/y vaue of the peak
%OUTPUT ARGS
%peakarray: array values between valley left and valley right
[valleys_y,valleys_x]=findvalleys(data);
disp('bbbbbbhhhhhhhhaaaaabhabahbahabha')
disp(valleys_x)
disp('bbbbbbhhhhhhhhaaaaabhabahbahabhahhhhhhhhaaaaabhabahbahabha')
disp(peak_freq)
disp('bbbbbbhhhhhhhhaaaaabhabahbahabha')
leftpeakvalleys=[0]; %%%%0WARNING
rightpeakvalleys=[];
leftvalleypos=[1]; %%%%1WARNING
rightvalleypos=[];
for i = valleys_x'  %%WARNING APOSTROPHE AFTER VALLEYS_X
    if i<peak_freq %x value or index
        leftpeakvalleys=[leftpeakvalleys,data(i)];
        leftvalleypos= [leftvalleypos,i];
    else
        rightpeakvalleys=[rightpeakvalleys,data(i)];
        rightvalleypos= [rightvalleypos,i];
    end 
end


peakarray=[];
peakarraypos=[];
for i = [leftvalleypos(end):1:rightvalleypos(1)]
   peakarray= [peakarray,data(i)];
   peakarraypos= [peakarraypos,i];
end
peakarray=[peakarray;peakarraypos];

