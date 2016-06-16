close all;
clear all;

DATA1 = dlmread('TEK0000.CSV',',',[19 1 2490 5]);
t1 = DATA1(:,3);
d1 = DATA1(:,4);
name{1} = 'struja, R=20k';

DATA2 = dlmread('TEK0001.CSV',',',[19 1 2490 5]);
t2 = DATA2(:,3);
d2 = DATA2(:,4);
name{2} = 'struja, R=40k';

figname = 'struja_vs_vrijeme.jpg';

current_vs_time = plot2D;
current_vs_time.x_data = [t1,t2];
current_vs_time.y_data = [d1,d2];
current_vs_time.x_label = 'Time [ns]';
current_vs_time.y_label = 'Current [A]';
current_vs_time.name = name;
current_vs_time.plot;

export_fig(figname);