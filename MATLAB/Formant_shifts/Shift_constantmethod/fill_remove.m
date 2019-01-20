function [newarray]= fill_remove(data,shifted_array,indices_array, indices_array2,shift_const1,shift_const2)
%INPUT
%x1 - original data array
%shifted_array=zeros and the shifted array 
%indices_array for original data=peak1_array(2,:)
%OUTPUT 
%newarray= shifting and 



for i= 1:length(data)
    if shifted_array(i)==0 && i<indices_array(1)
       shifted_array(i)=data(i);
    elseif shifted_array(i)==0 && i<(indices_array(end)+shift_const1)
       shifted_array(i)= data(indices_array(1));
    elseif shifted_array(i)==0 && i<indices_array2(1)
       shifted_array(i)=data(i);
    elseif shifted_array(i)==0 && i<(indices_array2(end)+shift_const2)
       shifted_array(i)= data(indices_array2(1));
    elseif shifted_array(i)==0 
       shifted_array(i)=data(i);
    end 
end


newarray=shifted_array;