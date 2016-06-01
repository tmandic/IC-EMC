classdef smiq < gpib_instrument
    % smiq - class defined to change settings of Rohde & Schwarz SMIQ03B signal generator
    %   
    % F. Fajdetic, University of Zagreb, 2016

	properties
		frequency = '1 MHz' % 'kHz', 'MHz', 'GHz'. Space is neccessary between value and unit.
		level = '-42 dBm' % 'dBm','dB','dBuV','dBmV','V','mV','uV'
		rf_output = 'OFF' % 'OFF','ON','1','0'
    end

    methods
    	%% Constructor
        function this_smiq = smiq()
            this_smiq@gpib_instrument();
        end  
        %% Init instrument
        function initInstrument(this_smiq)
            to_send = ['FREQ ',this_smiq.frequency];
            fprintf(this_smiq.handle, to_send);
            to_send = ['POW ',this_smiq.level];
            fprintf(this_smiq.handle, to_send);
            to_send = ['OUTP:STAT ', this_smiq.rf_output];
            fprintf(this_smiq.handle, to_send);
        end
        %% Setter for frequency
        function this_smiq = set.frequency(this_smiq, infrequency)         
            % old instrument setting
            fprintf(this_smiq.handle, 'FREQ?'); 
            result_old = fscanf(this_smiq.handle);
            % new setting           
            to_send = ['FREQ ',infrequency];
            fprintf(this_smiq.handle, to_send);           
            fprintf(this_smiq.handle, 'FREQ?'); 
            % result je u Hz
            result = fscanf(this_smiq.handle);
            frequency_split = strsplit(infrequency,' ');
            result_num = str2double(result);
            % Napravi pretvorbu ovisno o mjernoj jedinici
            if strcmp(frequency_split(2),'kHz')
                result_num = result_num/1000;
            else if strcmp(frequency_split(2),'MHz')
                    result_num = result_num/1000000;
                else if strcmp(frequency_split(2),'GHz')
                        result_num = result_num/1000000000;
                    end
                end
            end
            formatted_result = num2str(result_num);
            if strcmp(frequency_split(1), formatted_result)
                this_smiq.frequency = infrequency;
            else 
                to_disp = ['Unable to set frequency to ', infrequency];
                disp(to_disp)
                to_send = ['FREQ ',result_old,' Hz'];
                fprintf(this_smiq.handle, to_send);   
            end
        end
        %% Setter for level
        function this_smiq = set.level(this_smiq, inlevel)
            % old instrument setting
            fprintf(this_smiq.handle, 'POW?'); 
            result_old = fscanf(this_smiq.handle);
            % new setting
            to_send = ['POW ',inlevel];
            fprintf(this_smiq.handle, to_send);        
            fprintf(this_smiq.handle, 'POW?'); 
            % result je u dB
            result = fscanf(this_smiq.handle);
            level_split = strsplit(inlevel,' ');
            inlevel_level = level_split(1);
            % Napravi pretvorbu ako nije zadano u dBm/dB
            if strcmp(level_split(2),'V')
                lvl = 10 + 20*log10(str2double(level_split(1))*sqrt(2));
                inlevel_level = num2str(round(lvl*100)/100);
            end
            if strcmp(level_split(2),'mV')
                lvl = 10 + 20*log10((str2double(level_split(1))/1000)*sqrt(2));
                inlevel_level = num2str(round(lvl*100)/100);
            end
            if strcmp(level_split(2),'uV')
                lvl = 10 + 20*log10((str2double(level_split(1))/1000000)*sqrt(2));
                inlevel_level = num2str(round(lvl*100)/100);
            end
            if strcmp(level_split(2),'dBmV')
                lvl = str2double(level_split(1)) - 46.99;
                inlevel_level = num2str(round(lvl*100)/100);
            end
            if strcmp(level_split(2),'dBuV')
                lvl = str2double(level_split(1)) - 106.99;
                inlevel_level = num2str(round(lvl*100)/100);
            end
            formatted_result = num2str(str2double(result));
            if strcmp(inlevel_level,formatted_result)
                this_smiq.level = inlevel;
            else 
                to_disp = ['Unable to set level to ', inlevel];
                disp(to_disp)
                to_send = ['POW ',result_old,' dBm'];
                fprintf(this_smiq.handle, to_send); 
            end
        end
        %% Setter for rf_output
        function this_smiq = set.rf_output(this_smiq, inrf_output)
            % old instrument setting
            fprintf(this_smiq.handle, 'OUTP:STAT?'); 
            result_old = fscanf(this_smiq.handle);
            % new setting
            to_send = ['OUTP:STAT ', inrf_output];
            fprintf(this_smiq.handle, to_send);
            fprintf(this_smiq.handle, 'OUTP:STAT?');    
            result = fscanf(this_smiq.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(inrf_output, 'OFF') || strcmp(inrf_output, '0')
                if strcmp(formatted_result, '0')
                    this_smiq.rf_output = inrf_output;
                else 
                    to_disp = ['Unable to set RF output to ',inrf_output];
                    disp(to_disp)
                    to_send = ['OUTP:STAT ',result_old];
                    fprintf(this_smiq.handle, to_send);
                end
            else
                if strcmp(formatted_result, '1')
                    this_smiq.rf_output = inrf_output;
                else
                    to_disp = ['Unable to set RF output to ',inrf_output];
                    disp(to_disp)
                    to_send = ['OUTP:STAT ',result_old];
                    fprintf(this_smiq.handle, to_send);
                end
            end
        end
    end
end