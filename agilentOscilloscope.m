classdef agilentOscilloscope < visa_instrument
    % agilentOscilloscope - class defined to change settings of Agilent MSO7034B oscilloscope
    %   
    % F. Fajdetic, University of Zagreb, 2016

	properties
		timebase_delay = '0';
        timebase_ref = 'CENT';
        chn1_probe = '10';
        chn1_range = '400 mV'; % 'uV','mV','V' Space is neccessary between value and unit.
        chn1_offset = '5 V'; % 'uV','mV','V'
        chn1_coupling = 'DC';
        chn1_bw_limit = 'OFF';
        trigger_level = '5 V'; % 'uV','mV','V'
        trigger_slope = 'POS';
        trigger_sweep = 'AUTO';
        acquire_type = 'AVER';
        acquire_count = '8';
        waveform_source = 'CHAN1';
        waveform_format = 'ASC';
        waveform_points_mode = 'MAX';
        waveform_points_num = '100000';
    end

    methods
    	%% Constructor
        function this_agilentOscilloscope = agilentOscilloscope()
            this_agilentOscilloscope@visa_instrument();
        end
        %% Method for vmax query
        function val = vmax(this_agilentOscilloscope)
            to_send = [':MEASure:VMAX? ',this_agilentOscilloscope.waveform_source];
            fprintf(this_agilentOscilloscope.handle, to_send);
            vmax_s = [];
            while isempty(vmax_s)
                vmax_s = fscanf(this_agilentOscilloscope.handle);
            end        
            val = str2double(vmax_s);                        
        end
        %% Method for vmin query
        function val = vmin(this_agilentOscilloscope)
            to_send = [':MEASure:VMIN? ',this_agilentOscilloscope.waveform_source];
            fprintf(this_agilentOscilloscope.handle, to_send);
            vmin_s = [];
            while isempty(vmin_s)
                vmin_s = fscanf(this_agilentOscilloscope.handle);
            end        
            val = str2double(vmin_s);                        
        end
        %% Method for vavg query
        function val = vavg(this_agilentOscilloscope)
            to_send = [':MEASure:VAVerage? ',this_agilentOscilloscope.waveform_source];
            fprintf(this_agilentOscilloscope.handle, to_send);
            vavg_s = [];
            while isempty(vavg_s)
                vavg_s = fscanf(this_agilentOscilloscope.handle);
            end        
            val = str2double(vavg_s);                        
        end 
        %% Init instrument
        function initInstrument(this_agilentOscilloscope)
            to_send = [':TIMebase:DELay ',this_agilentOscilloscope.timebase_delay];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':TIMebase:REFerence ',this_agilentOscilloscope.timebase_ref];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':CHANnel1:PROBe ',this_agilentOscilloscope.chn1_probe];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':CHANnel1:RANGe ',this_agilentOscilloscope.chn1_range];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':CHANnel1:OFFSet ',this_agilentOscilloscope.chn1_offset];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':CHANnel1:COUPling ',this_agilentOscilloscope.chn1_coupling];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':CHANnel1:BWLimit ',this_agilentOscilloscope.chn1_bw_limit];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':TRIGger:LEVel ',this_agilentOscilloscope.trigger_level];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':TRIGger:SLOPe ',this_agilentOscilloscope.trigger_slope];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':TRIGger:SWEep ',this_agilentOscilloscope.trigger_sweep];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':ACQuire:TYPE ',this_agilentOscilloscope.acquire_type];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':ACQuire:COUNt ',this_agilentOscilloscope.acquire_count];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':WAVeform:SOURce ',this_agilentOscilloscope.waveform_source];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':WAVeform:FORMat ',this_agilentOscilloscope.waveform_format];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':WAVeform:POINts:MODE ',this_agilentOscilloscope.waveform_points_mode];
            fprintf(this_agilentOscilloscope.handle, to_send);
            to_send = [':WAVeform:POINts ',this_agilentOscilloscope.waveform_points_num];
            fprintf(this_agilentOscilloscope.handle, to_send);
        end
        %% Setter for timebase_delay
        function this_agilentOscilloscope = set.timebase_delay(this_agilentOscilloscope, intimebase_delay)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':TIMebase:DELay?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = num2str(str2double(result_old));
            % new setting
            to_send = [':TIMebase:DELay ',intimebase_delay];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TIMebase:DELay?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = num2str(str2double(result));
            if strcmp(formatted_result, intimebase_delay)
                this_agilentOscilloscope.timebase_delay = intimebase_delay;
            else 
                to_disp = ['Unable to set timebase delay to ',intimebase_delay];
                disp(to_disp)
                to_send = [':TIMebase:DELay ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for timebase_ref
        function this_agilentOscilloscope = set.timebase_ref(this_agilentOscilloscope, intimebase_ref)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':TIMebase:REFerence?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':TIMebase:REFerence ',intimebase_ref];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TIMebase:REFerence?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, intimebase_ref)
                this_agilentOscilloscope.timebase_ref = intimebase_ref;
            else 
                to_disp = ['Unable to set timebase reference to ',intimebase_ref];
                disp(to_disp)
                to_send = [':TIMebase:REFerence ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for chn1_probe
        function this_agilentOscilloscope = set.chn1_probe(this_agilentOscilloscope, inchn1_probe)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:PROBe?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = num2str(str2double(result_old));
            % new setting
            to_send = [':CHANnel1:PROBe ',inchn1_probe];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:PROBe?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = num2str(str2double(result));
            if strcmp(formatted_result, inchn1_probe)
                this_agilentOscilloscope.chn1_probe = inchn1_probe;
            else 
                to_disp = ['Unable to set chn1 probe to ',inchn1_probe];
                disp(to_disp)
                to_send = [':TIMebase:REFerence ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for chn1_range
        function this_agilentOscilloscope = set.chn1_range(this_agilentOscilloscope, inchn1_range)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:RANGe?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = num2str(str2double(result_old));
            % new setting
            to_send = [':CHANnel1:RANGe ',inchn1_range];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:RANGe?');
            result = fscanf(this_agilentOscilloscope.handle);
            result_num = str2double(result);
            inchn1_range_split = strsplit(inchn1_range);
            if strcmp(inchn1_range_split(2),'mV')
                result_num = result_num*1000;
            end
            if strcmp(inchn1_range_split(2),'uV')
                result_num = result_num*1000000;
            end
            formatted_result = num2str(result_num);
            if strcmp(formatted_result, inchn1_range_split(1))
                this_agilentOscilloscope.chn1_range = inchn1_range;
            else 
                to_disp = ['Unable to set chn1 range to ',inchn1_range,', ',formatted_result, ' is recommended'];
                disp(to_disp)
                to_send = [':CHANnel1:RANGe ',formatted_result_old,' V'];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for chn1_offset
        function this_agilentOscilloscope = set.chn1_offset(this_agilentOscilloscope, inchn1_offset)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:OFFSet?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = num2str(str2double(result_old));
            % new setting
            to_send = [':CHANnel1:OFFSet ',inchn1_offset];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:OFFSet?');
            result = fscanf(this_agilentOscilloscope.handle);
            offset_split = strsplit(inchn1_offset,' ');
            result_num = str2double(result);
            if strcmp(offset_split(2),'mV')
                result_num = result_num*1000;
            end
            if strcmp(offset_split(2),'uV')
                result_num = result_num*1000000;
            end
            formatted_result = num2str(result_num);
            if strcmp(formatted_result, offset_split(1))
                this_agilentOscilloscope.chn1_offset = inchn1_offset;
            else 
                to_disp = ['Unable to set chn1 offset to ',inchn1_offset,', ', formatted_result, ' is recommended'];
                disp(to_disp)
                to_send = [':CHANnel1:OFFSet ',formatted_result_old,' V'];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end 
        %% Setter for chn1_coupling
        function this_agilentOscilloscope = set.chn1_coupling(this_agilentOscilloscope, inchn1_coupling)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:COUPling?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':CHANnel1:COUPling ',inchn1_coupling];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:COUPling?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, inchn1_coupling)
                this_agilentOscilloscope.chn1_coupling = inchn1_coupling;
            else 
                to_disp = ['Unable to set chn1 coupling to ',inchn1_coupling];
                disp(to_disp)
                to_send = [':CHANnel1:COUPling ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for chn1_bw_limit
        function this_agilentOscilloscope = set.chn1_bw_limit(this_agilentOscilloscope, inchn1_bw_limit)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:BWLimit?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':CHANnel1:BWLimit ',inchn1_bw_limit];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:BWLimit?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(inchn1_bw_limit, 'OFF') || strcmp(inchn1_bw_limit, '0')
                if strcmp(formatted_result, '0')
                    this_agilentOscilloscope.chn1_bw_limit = inchn1_bw_limit;
                else 
                    to_disp = ['Unable to set chn1 bw limit to ',inchn1_bw_limit];
                    disp(to_disp)
                    to_send = [':CHANnel1:BWLimit ',formatted_result_old];
                    fprintf(this_agilentOscilloscope.handle, to_send);
                end
            else
                if strcmp(formatted_result, '1')
                    this_agilentOscilloscope.chn1_bw_limit = inchn1_bw_limit;
                else
                    to_disp = ['Unable to set chn1 bw limit to ',inchn1_bw_limit];
                    disp(to_disp)
                    to_send = [':CHANnel1:BWLimit ',formatted_result_old];
                    fprintf(this_agilentOscilloscope.handle, to_send);
                end
            end
        end 
        %% Setter for trigger_level
        function this_agilentOscilloscope = set.trigger_level(this_agilentOscilloscope, intrigger_level)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:LEVel?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = num2str(str2double(result_old));
            % new setting
            to_send = [':TRIGger:LEVel ',intrigger_level];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:LEVel?');
            result = fscanf(this_agilentOscilloscope.handle);
            trigger_level_split = strsplit(intrigger_level,' ');
            result_num = str2double(result);
            if strcmp(trigger_level_split(2),'mV')
                result_num = result_num*1000;
            end
            if strcmp(trigger_level_split(2),'uV')
                result_num = result_num*1000000;
            end
            formatted_result = num2str(result_num);
            if strcmp(formatted_result, trigger_level_split(1))
                this_agilentOscilloscope.trigger_level = intrigger_level;
            else 
                to_disp = ['Unable to set trigger level to ',intrigger_level,', ', formatted_result, ' is recommended'];
                disp(to_disp)
                to_send = [':TRIGger:LEVel ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for trigger_slope
        function this_agilentOscilloscope = set.trigger_slope(this_agilentOscilloscope, intrigger_slope)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:SLOPe?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':TRIGger:SLOPe ',intrigger_slope];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:SLOPe?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, intrigger_slope)
                this_agilentOscilloscope.trigger_slope = intrigger_slope;
            else 
                to_disp = ['Unable to set trigger slope to ',intrigger_slope];
                disp(to_disp)
                to_send = [':TRIGger:SLOPe ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for trigger_sweep
        function this_agilentOscilloscope = set.trigger_sweep(this_agilentOscilloscope, intrigger_sweep)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:SWEep?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':TRIGger:SWEep ', intrigger_sweep];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:SWEep?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, intrigger_sweep)
                this_agilentOscilloscope.trigger_sweep = intrigger_sweep;
            else 
                to_disp = ['Unable to set trigger sweep to ',intrigger_sweep];
                disp(to_disp)
                to_send = [':TRIGger:SWEep ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for acquire_type
        function this_agilentOscilloscope = set.acquire_type(this_agilentOscilloscope, inacquire_type)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':ACQuire:TYPE?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':ACQuire:TYPE ', inacquire_type];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':ACQuire:TYPE?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, inacquire_type)
                this_agilentOscilloscope.acquire_type = inacquire_type;
            else 
                to_disp = ['Unable to set acquire type to ',inacquire_type];
                disp(to_disp)
                to_send = [':ACQuire:TYPE ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for acquire_count
        function this_agilentOscilloscope = set.acquire_count(this_agilentOscilloscope, inacquire_count)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':ACQuire:COUNt?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = num2str(str2double(result_old));
            % new setting
            to_send = [':ACQuire:COUNt ', inacquire_count];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':ACQuire:COUNt?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = num2str(str2double(result));
            if strcmp(formatted_result, inacquire_count)
                this_agilentOscilloscope.acquire_count = inacquire_count;
            else 
                to_disp = ['Unable to set acquire count to ',inacquire_count];
                disp(to_disp)
                to_send = [':ACQuire:COUNt ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for waveform_source
        function this_agilentOscilloscope = set.waveform_source(this_agilentOscilloscope, inwaveform_source)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:SOURce?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':WAVeform:SOURce ', inwaveform_source];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:SOURce?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, inwaveform_source)
                this_agilentOscilloscope.waveform_source = inwaveform_source;
            else 
                to_disp = ['Unable to set waveform source to ',inwaveform_source];
                disp(to_disp)
                to_send = [':WAVeform:SOURce ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for waveform_format
        function this_agilentOscilloscope = set.waveform_format(this_agilentOscilloscope, inwaveform_format)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:FORMat?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':WAVeform:FORMat ', inwaveform_format];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:FORMat?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, inwaveform_format)
                this_agilentOscilloscope.waveform_format = inwaveform_format;
            else 
                to_disp = ['Unable to set waveform format to ',inwaveform_format];
                disp(to_disp)
                to_send = [':WAVeform:FORMat ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for waveform_points_mode
        function this_agilentOscilloscope = set.waveform_points_mode(this_agilentOscilloscope, inwaveform_points_mode)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:POINts:MODE?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = result_old(1:numel(result_old)-1);
            % new setting
            to_send = [':WAVeform:POINts:MODE ', inwaveform_points_mode];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:POINts:MODE?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = result(1:numel(result)-1);
            if strcmp(formatted_result, inwaveform_points_mode)
                this_agilentOscilloscope.waveform_points_mode = inwaveform_points_mode;
            else 
                to_disp = ['Unable to set waveform points mode to ',inwaveform_points_mode];
                disp(to_disp)
                to_send = [':WAVeform:POINts:MODE ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end
        %% Setter for waveform_points_num
        function this_agilentOscilloscope = set.waveform_points_num(this_agilentOscilloscope, inwaveform_points_num)
            % old instrument setting
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:POINts?'); 
            result_old = fscanf(this_agilentOscilloscope.handle);
            formatted_result_old = num2str(str2double(result_old));
            % new setting
            to_send = [':WAVeform:POINts ', inwaveform_points_num];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:POINts?');
            result = fscanf(this_agilentOscilloscope.handle);
            formatted_result = num2str(str2double(result));
            if strcmp(formatted_result, inwaveform_points_num)
                this_agilentOscilloscope.waveform_points_num = inwaveform_points_num;
            else 
                to_disp = ['Unable to set waveform points num to ',inwaveform_points_num];
                disp(to_disp)
                to_send = [':WAVeform:POINts ',formatted_result_old];
                fprintf(this_agilentOscilloscope.handle, to_send);
            end
        end          
    end
end