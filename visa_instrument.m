classdef visa_instrument
    % visa_instrument - connect and disconect to VISA instrument
    %   
    % F. Fajdetic, University of Zagreb, 2016
    
    properties
        vendor = 'ni'
        handle
        adress = 'USB0::0x0957::0x173D::MY50340261::0::INSTR'
        buffer_size = 1044480
        timeout = 60
    end
    
    methods
        %% Constructor
        function this_visa_instrument = visa_instrument(invendor, inadress, inbuffer_size, intimeout)
            if nargin == 4
                this_visa_instrument.vendor = invendor;
                this_visa_instrument.adress = inadress;
                this_visa_instrument.buffer_size = inbuffer_size;
                this_visa_instrument.timeout = intimeout;
            end             
        end
        %% open visa port
        function this_visa_instrument = open(this_visa_instrument)
            this_visa_instrument.handle = visa(this_visa_instrument.vendor, this_visa_instrument.adress);
            this_visa_instrument.handle.InputBufferSize = this_visa_instrument.buffer_size;
            this_visa_instrument.handle.Timeout = this_visa_instrument.timeout;    
            fopen(this_visa_instrument.handle);
            if strcmp('open', this_visa_instrument.handle.status)  
                disp('visa_instrument: VISA port open');     
            elseif strcmp('closed', this_usb_instrument.handle.status)             
                disp('visa_instrument: Unable to open VISA port');     
            end
        end
        %% close visa port
        function this_visa_instrument = close(this_visa_instrument)
            fclose(this_visa_instrument.handle);
            if strcmp('open', this_visa_instrument.handle.status)  
                disp('visa_instrument: Unable to close VISA port');     
            elseif strcmp('closed', this_visa_instrument.handle.status)             
                disp('visa_instrument: VISA port closed');     
            end            
        end  
    end   
end