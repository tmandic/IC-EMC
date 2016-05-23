classdef usb_instrument
    % usb_instrument - connect and disconect to USB instrument
    %   
    % F. Fajdetic, University of Zagreb, 2016
    
    properties
        port = 'COM5'
        handle
        baudRate = 115200
    end
    
    methods
        %% Constructor
        function this_usb_instrument = usb_instrument(inport, inbaudRate)
            if nargin == 2
                this_usb_instrument.port = inport;
                this_usb_instrument.baudRate = inbaudRate;
            end             
        end
        %% open usb port
        function this_usb_instrument = open(this_usb_instrument)
            this_usb_instrument.handle = serial(this_usb_instrument.port, 'BaudRate', this_usb_instrument.baudRate);    
            fopen(this_usb_instrument.handle);
            if strcmp('open', this_usb_instrument.handle.status)  
                disp('usb_instrument: USB port open');     
            elseif strcmp('closed', this_usb_instrument.handle.status)             
                disp('usb_instrument: Unable to open USB port');     
            end
        end
        %% close usb port
        function this_usb_instrument = close(this_usb_instrument)
            fclose(this_usb_instrument.handle);
            if strcmp('open', this_usb_instrument.handle.status)  
                disp('usb_instrument: Unable to close USB port');     
            elseif strcmp('closed', this_usb_instrument.handle.status)             
                disp('usb_instrument: USB port closed');     
            end            
        end        
    end
    
end