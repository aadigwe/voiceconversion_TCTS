

function [diff_form1, diff_form2]= formant_difference(formant_array1, formant_array2)
    %Thus function takes in the formant matrixes of twodifferent files and
    %finds the diffrence in each corresponding first and second peaks and outputs a matrix
    %The goal is to make audio 1 become audio 2 so we need to to find the
    %shift necessary for this differences
    diff_form1=[];
    diff_form2=[];
        if length(formant_array2) > length(formant_array1)
            for i=1:length(formant_array1)
                diff_form1=[diff_form1; formant_array2(i,1)-formant_array1(i,1)];
                diff_form2=[diff_form2; formant_array2(i,2)-formant_array1(i,2)];
            end 
        else 
            for i=1:length(formant_array2)
                diff_form1=[diff_form1; formant_array2(i,1)-formant_array1(i,1)];
                diff_form2=[diff_form2; formant_array2(i,2)-formant_array1(i,2)];
            end
        end 
end 