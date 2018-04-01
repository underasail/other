load F15_M_AllUp.lvm
a=F15_M_AllUp;
% a=[1|2|3|4|5|6|7|8|9|10]
% a=[Year|Month|Day|Hour(24)|Minute|Seconds|Pto(V)|HotFilm1(V)|HotFilm2(V)|Pto(m/s)]
i1=[15,15,15,15,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16,16];
i2=[36,38,40,42,44,47,49,51,53,55,57,59,01,03,06,08,10,12,14,16];
i3=[1,4,6,9,11,14,16,19,21,24,26,29,31,34,36,39,41,44,46,49];
i4=[0,2,3];
for k=1:length(i1);
    for p=1:length(i4);
        d=0;
        i=find(a(:,4)==i1(k) & a(:,5)==i2(k));
        if i4(p)>0;
            v=mean(a(i,10)); % eval(['v',int2str(i3(k)),'=mean(a(i,10));']);
            s=std(a(i,10));  % eval(['s',int2str(i3(k)),'=std(a(i,10));']);
            while abs(s-d)>(0.01*s)
                length(i);
                d=std(a(i,10));
                jj=find((a(i,10)>(v-(i4(p)*s)))&(a(i,10)<(v+(i4(p))*s)));
                i=i(jj);
                v=mean(a(i,10)); s=std(a(i,10));
            end;
            eval(['p',int2str(i4(p)),'v',int2str(i3(k)),'=mean(a(i,10));']);
            eval(['p',int2str(i4(p)),'s',int2str(i3(k)),'=std(a(i,10));']);
        elseif i4(p)==0;
            eval(['p0','v',int2str(i3(k)),'=mean(a(i,10));']);
            eval(['p0','s',int2str(i3(k)),'=std(a(i,10));']);
        end
    end
end
prompt='Display velocity profile plot?(0=n/1=y)';
if input(prompt)==1
    run Oct20_15h_std_loop_plot
end