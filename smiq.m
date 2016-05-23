classdef smiq < gpib_instrument
    % smiq - class defined to change settings of Rohde & Schwarz SMIQ03B signal generator
    %   
    % F. Fajdetic, University of Zagreb, 2016

	properties
		frequency = '1MHz'
		power = '-42dBm'
		rf_output = 'ON'
    end

    methods
    	%% Constructor
        function this_smiq = smiq()
            this_smiq@gpib_instrument();
        end           
        %% Setter for frequency
        function this_smiq = set.frequency(this_smiq, infrequency)         
            to_send = ['FREQ ',infrequency];
            fprintf(this_smiq.handle, to_send);
            this_smiq.frequency = infrequency;            
            % check if it is written in instrument - won't work because it returns floating point numbers without a unit, like 1E6
            % fprintf(this_smiq.handle, 'FREQ?');    
            % result = fscanf(this_smiq.handle);
            % if strcmp(infrequency,result)
            %     this_smiq.frequency = infrequency;
            % end
        end
        %% Setter for power
        function this_smiq = set.power(this_smiq, inpower)         
            to_send = ['POW ',inpower];
            fprintf(this_smiq.handle, to_send); 
            this_smiq.power = inpower;           
            % check if it is written in instrument - - won't work because it returns floating point numbers without a unit, like 1E6
            % fprintf(this_smiq.handle, 'POW?');    
            % result = fscanf(this_smiq.handle);
            % if strcmp(inpower,result)
            %     this_smiq.power = inpower;
            % end
        end
        %% Setter for rf_output
        function this_smiq = set.rf_output(this_smiq, inrf_output)         
            to_send = ['OUTP:STAT ', inrf_output];
            fprintf(this_smiq.handle, to_send);            
            % check if it is written in instrument
            fprintf(this_smiq.handle, 'OUTP:STAT?');    
            result = fscanf(this_smiq.handle);
            if strcmp(inrf_output,result)
                this_smiq.rf_output = inrf_output;
            end
        end
	end