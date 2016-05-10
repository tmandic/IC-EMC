classdef gpib_instrument
    %gpib_instrument - connect and disconect to GPIB instrument
    %   
    % T. Mandic, University of Zagreb, 2016
    
    properties
        address = 18
        vendor = 'ni'
        handle
        buffer_size = 1044480
        boardindex = 0;
    end
    
    methods
        %% Constructor
        function this_gpib_instrument = gpib_instrument(inaddress, invendor, inbuffer_size, inboardindex)
            if nargin == 4
                this_gpib_instrument.address = inaddress;
                this_gpib_instrument.vendor = invendor;
                this_gpib_instrument.buffer_size = inbuffer_size;
                this_gpib_instrument.boardindex = inboardindex;
            end             
        end
        %% open gpib port
        function this_gpib_instrument = open(this_gpib_instrument)
            this_gpib_instrument.handle = gpib(this_gpib_instrument.vendor,this_gpib_instrument.boardindex,this_gpib_instrument.address);    
            this_gpib_instrument.handle.InputBufferSize = this_gpib_instrument.buffer_size;
            fopen(this_gpib_instrument.handle);
            if strcmp('open', this_gpib_instrument.handle.status)  
                disp('gpib_instrument: GPIB port open');     
            elseif strcmp('closed', this_gpib_instrument.handle.status)             
                disp('gpib_instrument: Unable to open GPIB port');     
            end
        end
        %% close gpib port
        function this_gpib_instrument = close(this_gpib_instrument)
            fclose(this_gpib_instrument.handle);
            if strcmp('open', this_gpib_instrument.handle.status)  
                disp('gpib_instrument: Unable to close GPIB port');     
            elseif strcmp('closed', this_gpib_instrument.handle.status)             
                disp('gpib_instrument: GPIB port closed');     
            end            
        end        
    end
    
end

