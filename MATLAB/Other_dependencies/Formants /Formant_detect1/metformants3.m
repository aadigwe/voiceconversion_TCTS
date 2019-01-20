function outfile = metformants3(x, fs, fname)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%KEVIN SAYS FROM HERE!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
% find all roots whose magnitude is greater than threshold
    n=1;
    F=[];
    frame=1;
    Lm=40;
    L=400;
    Rm=10;
    R=100;
    xin=[];
    nmax=length(x);
    p=16; %lpc system order
    minrad=0.9;
    dthr=0.05;

    
% process speech on a frame-by-frame basis until no more viable frames
    while (n+L-1 <= nmax)
        
% perform LPC analysis on each frame of speech using autocorrelation method
        fmax=max(abs(x(n:n+L-1)));
        if (fmax == 0) 
            x(n:n+L-1)=randn(1,L);
        end
        xlpc=x(n:n+L-1).*hamming(L);
        [A,G,a,r]=autolpc(xlpc,p);
        
% find roots of LPC polynomial, eliminate all roots where imag(root)<=0, or
% where abs(root) < minrad 
        Ar=roots(A);
        Ar(find(imag(Ar)<=0))=0;
        Ar(find(abs(Ar)<=minrad))=NaN;
        angr=atan2(imag(Ar),real(Ar))*fs/(2*pi);
        angr(find(angr > 4500))=NaN;
        F=[F angr];
        n=n+R;
        frame=frame+1;
    end
    
% sort putative formants in ascending order
% keep track of the number of putative formants at each frame
    FS=sort(F);
    f1=p-sum(isnan(FS));
%%%%%END    
% open output file for printing results
    outfile=['out_',fname,'_formants.csv'];
    fidw=fopen(outfile,'w');
    
% write header for output file
    
% write out formant estimates from lpc root analysis
    nfrm=frame-1;
    for frame=1:nfrm
        if (f1(frame) == 0)
            fprintf(fidw,'%6.3f, %d, %d \n',(frame*0.01-0.01),frame,0);
        elseif (f1(frame) == 1)
            fprintf(fidw,'%6.3f, %d, %6.2f \n',...
                (frame*0.01), frame,FS(1:f1(frame),frame));
        elseif (f1(frame) == 2)
            fprintf(fidw,'%6.3f, %d, %6.2f, %6.2f \n',...
                (frame*0.01),frame,FS(1:f1(frame),frame));
        elseif (f1(frame) == 3)
            fprintf(fidw,'%6.3f, %d, %6.2f, %6.2f, %6.2f \n',...
                (frame*0.01),frame,FS(1:f1(frame),frame));
        elseif (f1(frame) == 4)
            fprintf(fidw,'%6.3f, %d, %6.2f, %6.2f, %6.2f, %6.2f \n',...
               (frame*0.01),frame,FS(1:f1(frame),frame));
        elseif (f1(frame) == 5)
            fprintf(fidw,'%6.3f, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f \n',...
                (frame*0.01),frame,FS(1:f1(frame),frame));
        else
            fprintf(fidw,'%6.3f, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f \n',...
                (frame*0.01),frame,FS(1:5,frame));
        end
    end


