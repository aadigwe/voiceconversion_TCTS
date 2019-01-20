function [valleys_y,valleys_x]=findvalleys(x)



%[peaksfound, freq_peak]=findpeaks(B,A);
[minValues, minindexes] = findpeaks(x.*-1);
minValues=minValues.*-1;
valleys_y= minValues;
valleys_x= minindexes;


%TEST
%plot(zeropoint5)
%hold on
%plot(valleys_x,valleys_y,'ro')