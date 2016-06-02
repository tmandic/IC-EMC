classdef radiPower < usb_instrument
    % radiPower - class defined to change settings of RadiPower 1006A power meter
    %   
    % F. Fajdetic, University of Zagreb, 2016

	properties
		filter_type = 'FILTER AUTO'
        frequency = '1000000 Hz'
    end

    methods
    	%% Constructor
        function this_radiPower = radiPower()
            this_radiPower@usb_instrument();
        end  
        %% Init instruments
        function initInstrument(this_radiPower)
            fprintf(this_radiPower.handle, this_radiPower.filter_type);
            fscanf(this_radiPower.handle);
            fprintf(this_radiPower.handle, this_radiPower.frequency);
            fscanf(this_radiPower.handle);
        end
        %% Setter for filter_type
        function this_radiPower = set.filter_type(this_radiPower, infilter_type)
            % old instrument setting
            fprintf(this_radiPower.handle, 'FILTER?'); 
            result_old = fscanf(this_radiPower.handle);
            result_old_formatted = result_old(1:numel(result_old)-1);
            % new setting
            fprintf(this_radiPower.handle, infilter_type);
            result=fscanf(this_radiPower.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result,'OK')
                this_radiPower.filter_type = infilter_type;
            else
                disp('Filter adjustment failed')
                to_send = ['FILTER ',result_old_formatted];
                fprintf(this_radiPower.handle, to_send);
            end
        end        
        %% Setter for frequency
        function this_radiPower = set.frequency(this_radiPower, infrequency)
            % old instrument setting
            fprintf(this_radiPower.handle, 'FREQUENCY?'); 
            result_old = fscanf(this_radiPower.handle);
            result_old_formatted = result_old(1:numel(result_old)-1);
            % new setting
            to_send=['FREQUENCY ', infrequency];
            fprintf(this_radiPower.handle, to_send);
            n=fscanf(this_radiPower.handle);
            n_correct=[n(1),n(2)];
            if strcmp(n_correct,'OK')
                this_radiPower.frequency = infrequency;
            else
                disp('Failed to load frequency')
                to_send = ['FREQUENCY ',result_old_formatted, ' Hz'];
                fprintf(this_radiPower.handle, to_send);
            end
        end
    end
end