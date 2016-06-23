classdef plot2D < toNxM
    %UNTITLED11 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        x_data
        y_data
        name
        x_label
        y_label
        x_min
        x_max
        y_min
        y_max
    end
    
    properties (Constant,Hidden)
       colors = {'k','b','r','g','m','y'} 
       fontax = 38
       fonttitle = 38
       fontlabel= 38        
       position = []
       location = 'NorthWest';
       axes_width = 4
       line_width = 4
       marker_size = 16
    end        
    
    methods
        %% Constructor
        function this_plot2D = plot2D(inx_data,iny_data)            
            if nargin == 2
                this_plot2D.x_data = inx_data; 
                this_plot2D.y_data = iny_data;                                                               
            end
        end         
        % Method to plot
        function plot(this_plot2D)     
            figure1 = figure;
            hold on;
            box on;   
            converted_x = this_plot2D.convert(this_plot2D.x_data);
            converted_y = this_plot2D.convert(this_plot2D.y_data);
            size_x  = size(converted_x);
            size_y  = size(converted_y);
            if size_x == size_y
                for j = 1:size_x(1)
                    plot(converted_x(j,:), converted_y(j,:), 'Color', this_plot2D.colors{j}, 'LineWidth', this_plot2D.line_width, 'LineStyle', '-','DisplayName',this_plot2D.name{j});                            
                end
                set(gca,'FontSize',this_plot2D.fontax,'FontName','Times', 'YColor',[0 0 0],'LineWidth', this_plot2D.axes_width);
                set(gca,'YGrid', 'on', 'XGrid', 'on');
                ylabel(this_plot2D.y_label,'FontSize',this_plot2D.fontax,'FontName','Times', 'Color', [0 0 0]);                    
                xlabel(this_plot2D.x_label,'FontSize',this_plot2D.fontax,'FontName','Times', 'Color', [0 0 0]);
                if isempty(this_plot2D.x_min)
                    this_plot2D.x_min = min(converted_x(1,:));
                end
                if isempty(this_plot2D.x_max)
                    this_plot2D.x_max = max(converted_x(1,:));
                end   
                if isempty(this_plot2D.y_min)
                    this_plot2D.y_min = min(converted_y(1,:)) - 0.2*abs(min(converted_y(1,:)));
                end
                if isempty(this_plot2D.y_max)
                    this_plot2D.y_max = max(converted_y(1,:)) + 0.2*abs(max(converted_y(1,:)));
                end  
                xlim([this_plot2D.x_min this_plot2D.x_max]);
                ylim([this_plot2D.y_min this_plot2D.y_max]);                
                legend1 = legend(gca,'show');
                if isempty(this_plot2D.position)
                    set(legend1,'Location',this_plot2D.location);            
                else
                    set(legend1,'Position',this_plot2D.position);            
                end 
                set(figure1, 'Color', 'w');            
                scrsz = get(0,'ScreenSize');
                set(gcf,'OuterPosition',[1 1 scrsz(3) scrsz(4)]);
                dpi = 100;
                set(gcf, 'paperposition', [0 0 scrsz(3)/dpi scrsz(4)/dpi]);
                set(gcf, 'papersize', [scrsz(3)/dpi scrsz(4)/dpi]);  
            end
        end
    end
    
end

