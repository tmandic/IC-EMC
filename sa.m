classdef sa < gpib_instrument
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        rbw='3kHz'
        vbw='10kHz'
        detector = 'average' % 'average', 'quasipeak', 'autopeak'
        y_scale = 'DBUV' % 'DBM', 'DBMV', 'DBUV', 'DBUA', 'DBPW', 'V', 'A', 'W'    
        sweep_points = 4001
        f_start = '1GHz'
        f_stop = '3GHz'  
        %f_center = '1GHz'
        %f_span = '3GHz'          
        %ref_level = '-100DBUV'
    end
    
    methods
        %% Constructor
        function this_sa = sa()
            this_sa@gpib_instrument();
        end           
        %% Setter for rbw
        function this_sa = set.rbw(this_sa,inrbw)         
            to_send = ['BAND:RES ',inrbw];
            fprintf(this_sa.handle, to_send);            
            % check if it is written in instrument
            fprintf(this_sa.handle, 'BAND:RES?');    
            result = fscanf(this_sa.handle);
            if strcmp(inrbw,result)
                this_sa.rbw = inrbw;
            end
        end           
        %% Setter for vbw
        function this_sa = set.vbw(this_sa,invbw)         
            to_send = ['BAND:VID ',invbw];
            fprintf(this_sa.handle, to_send);            
            % check if it is written in instrument
            fprintf(this_sa.handle, 'BAND:VID?');    
            result = fscanf(this_sa.handle);
            if strcmp(invbw,result)
                this_sa.vbw = invbw;
            end
        end 
        %% Setter for detector
        function this_sa = set.detector(this_sa,indetector)         
            if strcmp(indetector,'quasipeak')
                to_send = 'DET QPE';
                fprintf(this_sa.handle, to_send);            
                % check if it is written in instrument
                fprintf(this_sa.handle, 'DET?');    
                result = fscanf(this_sa.handle);
                if strcmp('QPE',result)
                    this_sa.detector = indetector;
                end
            elseif strcmp(indetector,'average')
                to_send = 'DET AVER';
                fprintf(this_sa.handle, to_send);            
                % check if it is written in instrument
                fprintf(this_sa.handle, 'DET?');    
                result = fscanf(this_sa.handle);
                if strcmp('AVER',result)
                    this_sa.detector = indetector;
                end     
            elseif strcmp(indetector,'autopeak')
                to_send = 'DET APE';
                fprintf(this_sa.handle, to_send);            
                % check if it is written in instrument
                fprintf(this_sa.handle, 'DET?');    
                result = fscanf(this_sa.handle);
                if strcmp('APE',result)
                    this_sa.detector = indetector;
                end                 
            end
        end  
        %% Setter for y_scale
        function this_sa = set.y_scale(this_sa,iny_scale)         
            to_send = ['UNIT:POW ',iny_scale];
            fprintf(this_sa.handle, to_send);            
            % check if it is written in instrument
            fprintf(this_sa.handle, 'UNIT:POW?');    
            result = fscanf(this_sa.handle);
            if strcmp(invbw,result)
                this_sa.y_scale = iny_scale;
            end
        end 
        %% Setter for sweep_points
        function this_sa = set.sweep_points(this_sa,insweep_points)         
            to_send = ['SWE:POIN ',num2str(insweep_points)];
            fprintf(this_sa.handle, to_send);            
            % check if it is written in instrument
            fprintf(this_sa.handle, 'SWE:POIN?');    
            result = fscanf(this_sa.handle);
            if strcmp(invbw,result)
                this_sa.sweep_points = insweep_points;
            end
        end      
        %% Setter for start frequency
        function this_sa = set.f_start(this_sa,inf_start)         
            to_send = ['frequency:start ',inf_start];
            fprintf(this_sa.handle, to_send);            
            % check if it is written in instrument
            fprintf(this_sa.handle, 'frequency:start?');    
            result = fscanf(this_sa.handle);
            if strcmp(inf_start,result)
                this_sa.f_start = inf_start;
            end
        end          
        %% Setter for stop frequency
        function this_sa = set.f_stop(this_sa,inf_stop)         
            to_send = ['frequency:stop ',num2str(inf_stop)];
            fprintf(this_sa.handle, to_send);            
            % check if it is written in instrument
            fprintf(this_sa.handle, 'frequency:stop?');    
            result = fscanf(this_sa.handle);
            if strcmp(inf_stop,result)
                this_sa.f_stop = inf_stop;
            end
        end    
%         %% Setter for center frequency
%         function this_sa = set.f_center(this_sa,inf_center)         
%             to_send = ['frequency:cent ',inf_center];
%             fprintf(this_sa.handle, to_send);            
%             % check if it is written in instrument
%             fprintf(this_sa.handle, 'frequency:cent?');    
%             result = fscanf(this_sa.handle);
%             if strcmp(inf_center,result)
%                 this_sa.f_start = inf_center;
%             end
%         end          
%         %% Setter for span frequency
%         function this_sa = set.f_span(this_sa,inf_span)         
%             to_send = ['frequency:stop ',num2str(inf_span)];
%             fprintf(this_sa.handle, to_send);            
%             % check if it is written in instrument
%             fprintf(this_sa.handle, 'frequency:stop?');    
%             result = fscanf(this_sa.handle);
%             if strcmp(inf_span,result)
%                 this_sa.f_stop = inf_span;
%             end
%         end         
%         %% Setter for reference level
%         function this_sa = set.ref_level(this_sa,inref_level)         
%             to_send = ['DISP:WIND:TRAC:Y:RLEV ',num2str(inref_level)];
%             fprintf(this_sa.handle, to_send);            
%             % check if it is written in instrument
%             fprintf(this_sa.handle, 'DISP:WIND:TRAC:Y:RLEV?');    
%             result = fscanf(this_sa.handle);
%             if strcmp(inref_level,result)  
%                 this_sa.ref_level = inref_level;
%             end                
%         end     
    end
    
end

