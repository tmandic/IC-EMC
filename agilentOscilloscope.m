classdef agilentOscilloscope < visa_instrument
    % agilentOscilloscope - class defined to change settings of Agilent MSO7034B oscilloscope
    %   
    % F. Fajdetic, University of Zagreb, 2016

	properties
		timebase_delay = '0';
        timebase_ref = 'CENT';
        chn1_probe = '10';
        chn1_range = '400 mV';
        chn1_offset = '5 V';
        chn1_coupling = 'DC';
        chn1_bw_limit = 'OFF';
        trigger_level = '5 V';
        trigger_slope = 'POS';
        trigger_sweep = 'AUTO';
        acquire_type = 'AVER';
        acquire_count = '8';
        waveform_source = 'CHAN1';
        waveform_format = 'ASC';
        waveform_points_mode = 'MAXimum';
        waveform_points_num = '100000';
    end

    methods
    	%% Constructor
        function this_agilentOscilloscope = agilentOscilloscope()
            this_agilentOscilloscope@visa_instrument();
        end   
        %% Setter for timebase_delay
        function this_agilentOscilloscope = set.timebase_delay(this_agilentOscilloscope, intimebase_delay)
            to_send = [':TIMebase:DELay ',intimebase_delay];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TIMebase:DELay?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, intimebase_delay)
                this_agilentOscilloscope.timebase_delay = intimebase_delay;
            end
        end
        %% Setter for timebase_ref
        function this_agilentOscilloscope = set.timebase_ref(this_agilentOscilloscope, intimebase_ref)
            to_send = [':TIMebase:REFerence ',intimebase_ref];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TIMebase:REFerence?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, intimebase_ref)
                this_agilentOscilloscope.timebase_ref = intimebase_ref;
            end
        end
        %% Setter for chn1_probe
        function this_agilentOscilloscope = set.chn1_probe(this_agilentOscilloscope, inchn1_probe)
            to_send = [':CHANnel1:PROBe  ',inchn1_probe];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:PROBe?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inchn1_probe)
                this_agilentOscilloscope.chn1_probe = inchn1_probe;
            end
        end
        %% Setter for chn1_range
        function this_agilentOscilloscope = set.chn1_range(this_agilentOscilloscope, inchn1_range)
            to_send = [':CHANnel1:RANGe ',inchn1_range];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:RANGe?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inchn1_range)
                this_agilentOscilloscope.chn1_range = inchn1_range;
            end
        end
        %% Setter for chn1_offset
        function this_agilentOscilloscope = set.chn1_offset(this_agilentOscilloscope, inchn1_offset)
            to_send = [':CHANnel1:OFFSet ',inchn1_offset];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:OFFSet?');
            result = fscanf(this_agilentOscilloscope.handle);
            offset_number = strsplit(inchn1_offset,' ');
            if strcmp(result, offset_number(1))
                this_agilentOscilloscope.chn1_offset = inchn1_offset;
            end
        end 
        %% Setter for chn1_coupling
        function this_agilentOscilloscope = set.chn1_coupling(this_agilentOscilloscope, inchn1_coupling)
            to_send = [':CHANnel1:COUPling ',inchn1_coupling];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:COUPling?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inchn1_coupling)
                this_agilentOscilloscope.chn1_coupling = inchn1_coupling;
            end
        end
        %% Setter for chn1_bw_limit
        function this_agilentOscilloscope = set.chn1_bw_limit(this_agilentOscilloscope, inchn1_bw_limit)
            to_send = [':CHANnel1:BWLimit ',inchn1_bw_limit];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':CHANnel1:BWLimit?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(inchn1_bw_limit, 'OFF') || strcmp(inchn1_bw_limit, '0')
                if strcmp(result, '0')
                    this_agilentOscilloscope.chn1_bw_limit = inchn1_bw_limit;
                end
            else
                if strcmp(result, '1')
                    this_agilentOscilloscope.chn1_bw_limit = inchn1_bw_limit;
                end
            end
        end 
        %% Setter for trigger_level
        function this_agilentOscilloscope = set.trigger_level(this_agilentOscilloscope, intrigger_level)
            to_send = [':TRIGger:LEVel ',intrigger_level];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:LEVel?');
            result = fscanf(this_agilentOscilloscope.handle);
            trigger_level_number = strsplit(intrigger_level,' ');
            if strcmp(result, trigger_level_number(1))
                this_agilentOscilloscope.trigger_level = intrigger_level;
            end
        end
        %% Setter for trigger_slope
        function this_agilentOscilloscope = set.trigger_slope(this_agilentOscilloscope, intrigger_slope)
            to_send = [':TRIGger:SLOPe ',intrigger_slope];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:SLOPe?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, intrigger_slope)
                this_agilentOscilloscope.trigger_slope = intrigger_slope;
            end
        end
        %% Setter for trigger_sweep
        function this_agilentOscilloscope = set.trigger_sweep(this_agilentOscilloscope, intrigger_sweep)
            to_send = [':TRIGger:SWEep ', intrigger_sweep];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':TRIGger:SWEep?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, intrigger_sweep)
                this_agilentOscilloscope.trigger_sweep = intrigger_sweep;
            end
        end
        %% Setter for acquire_type
        function this_agilentOscilloscope = set.acquire_type(this_agilentOscilloscope, inacquire_type)
            to_send = [':ACQuire:TYPE ', intrigger_sweep];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':ACQuire:TYPE?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inacquire_type)
                this_agilentOscilloscope.acquire_type = inacquire_type;
            end
        end
        %% Setter for acquire_count
        function this_agilentOscilloscope = set.acquire_count(this_agilentOscilloscope, inacquire_count)
            to_send = [':ACQuire:COUNt ', inacquire_count];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':ACQuire:COUNt?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inacquire_count)
                this_agilentOscilloscope.acquire_count = inacquire_count;
            end
        end
        %% Setter for waveform_source
        function this_agilentOscilloscope = set.waveform_source(this_agilentOscilloscope, inwaveform_source)
            to_send = [':WAVeform:SOURce ', inwaveform_source];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:SOURce?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inwaveform_source)
                this_agilentOscilloscope.waveform_source = inwaveform_source;
            end
        end
        %% Setter for waveform_format
        function this_agilentOscilloscope = set.waveform_format(this_agilentOscilloscope, inwaveform_format)
            to_send = [':WAVeform:FORMat ', inwaveform_format];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:FORMat?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inwaveform_format)
                this_agilentOscilloscope.waveform_format = inwaveform_format;
            end
        end
        %% Setter for waveform_points_mode
        function this_agilentOscilloscope = set.waveform_points_mode(this_agilentOscilloscope, inwaveform_points_mode)
            to_send = [':WAVeform:POINts:MODE ', inwaveform_points_mode];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:POINts:MODE?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inwaveform_points_mode)
                this_agilentOscilloscope.waveform_points_mode = inwaveform_points_mode;
            end
        end
        %% Setter for waveform_points_num
        function this_agilentOscilloscope = set.waveform_points_num(this_agilentOscilloscope, inwaveform_points_num)
            to_send = [':WAVeform:POINts ', inwaveform_points_num];
            fprintf(this_agilentOscilloscope.handle, to_send);
            fprintf(this_agilentOscilloscope.handle, ':WAVeform:POINts?');
            result = fscanf(this_agilentOscilloscope.handle);
            if strcmp(result, inwaveform_points_num)
                this_agilentOscilloscope.waveform_points_num = inwaveform_points_num;
            end
        end          
	end