function [shiftconst_array1, shiftconst_array2] = formantshiftconst(diff_form1, diff_form2, fs)
    %the fftsize will be the one for formant 2
    f0_low_limit = 71;
    fft_size = 2 ^ ceil(log2(3 * fs / f0_low_limit + 1));
    stepvalue = fs/fft_size;
    shiftconst_array1=[];
    shiftconst_array2=[];
    for i = 1:length(diff_form1)
        shiftconst_array1=[shiftconst_array1;round(diff_form1(i)/stepvalue)];
        shiftconst_array2=[shiftconst_array2;round(diff_form2(i)/stepvalue)];
    end 
end 