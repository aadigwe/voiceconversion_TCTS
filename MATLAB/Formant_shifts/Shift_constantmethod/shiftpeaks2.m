function [shifted_array]= shiftpeaks2(data, peak1_array,shift1_const, peak2_array,shift2_const)

%Input array
%data:the amplitude array
%peakarray:peakarray of eeach formant: 1st row is amplitude, 2nd row is positions
%shift1_const: shift const value for peak 1
%shift2_const: shift const value for peak 1

%OUTPUT array
%shifted array: array of zeroes and shifted value positions 


if nargin == 3
    peak2_array=[];
    shift2_const=0;
elseif nargin == 5
end;

%STEPS
%1.data array - clone size and make the new array with zeros
shifted_array=zeros(length(data), 1)';
shifted2_array=zeros(length(data), 1)';
%peak1_array=[peak1_array, peak2_array];
%disp(peak1_array)


for i = peak1_array(2,:)
    disp(i)
    shifted_array(i+shift1_const) = peak1_array(1,1+i-peak1_array(2,1));
end 

for i =peak2_array(2,:)
    disp('hey')
    %disp(shifted2_array(i+shift2_const))
    disp(shift2_const)
    disp(i)
    shifted2_array(i+shift2_const) = peak2_array(1,1+i-peak2_array(2,1));
end 


shifted_array=max([shifted_array;shifted2_array]);

