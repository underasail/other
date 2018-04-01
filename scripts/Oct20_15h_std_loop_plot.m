p0V15h=[p0v4;p0v6;p0v9;p0v11;p0v14;p0v16;p0v19;p0v21;p0v24;p0v26;p0v29;p0v31;p0v34;p0v36;p0v39;p0v41;p0v44;p0v46;p0v49];
p0S15h=[p0s4;p0s6;p0s9;p0s11;p0s14;p0s16;p0s19;p0s21;p0s24;p0s26;p0s29;p0s31;p0s34;p0s36;p0s39;p0s41;p0s44;p0s46;p0s49];
p2V15h=[p2v4;p2v6;p2v9;p2v11;p2v14;p2v16;p2v19;p2v21;p2v24;p2v26;p2v29;p2v31;p2v34;p2v36;p2v39;p2v41;p2v44;p2v46;p2v49];
p2S15h=[p2s4;p2s6;p2s9;p2s11;p2s14;p2s16;p2s19;p2s21;p2s24;p2s26;p2s29;p2s31;p2s34;p2s36;p2s39;p2s41;p2s44;p2s46;p2s49];
p3V15h=[p3v4;p3v6;p3v9;p3v11;p3v14;p3v16;p3v19;p3v21;p3v24;p3v26;p3v29;p3v31;p3v34;p3v36;p3v39;p3v41;p3v44;p3v46;p3v49];
p3S15h=[p3s4;p3s6;p3s9;p3s11;p3s14;p3s16;p3s19;p3s21;p3s24;p3s26;p3s29;p3s31;p3s34;p3s36;p3s39;p3s41;p3s44;p3s46;p3s49];
Z15h=[4;6.5;9;11.5;14;16.5;19;21.5;24;26.5;29;31.5;34;36.5;39;41.5;44;46.5;49];

plot(p0V15h,Z15h,'blue',p2V15h,Z15h,'red',p3V15h,Z15h,'green');
    title('Velocity Profiles')
    xlabel('Velocity (m/s)')
    ylabel('Height (cm)')
    legend('Full Data Set','Two SD Removed','Three SD Removed','location','northwest','orientation','horizontal')
    legend('boxoff')
    
% plot(V15h,(S15h/V15h),'.');