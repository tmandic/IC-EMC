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
        %% Setter for filter_type
        function this_radiPower = set.filter_type(this_radiPower, infilter_type)
            fprintf(this_radiPower.handle, infilter_type);
            n=fscanf(this_radiPower.handle);
            n_correct=[n(1),n(2)];
            if strcmp(n_correct,'OK')
                this_radiPower.filter_type = infilter_type
            else
                disp('Filter adjustment failed')
            end
        end        
        %% Setter for frequency
        function this_radiPower = set.filter_type(this_radiPower, infrequency)
            to_send=['FREQUENCY ', infrequency];
            fprintf(this_radiPower.handle, to_send);
            n=fscanf(this_radiPower.handle);
            n_correct=[n(1),n(2)];
            if strcmp(n_correct,'OK')
                this_radiPower.frequency = infrequency
            else
                disp('Failed to load frequency')
            end
        end
	end