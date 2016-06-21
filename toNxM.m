classdef toNxM
    %UNTITLED12 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    end
    
    methods
        % Constructor
        function this_toNxM = toNxM()            
        end         
        % convert to matrix
        function outData = convert(this_toNxM,inData)
            if iscell(inData)
                for j = 1:numel(inData)
                    outData(j,:) = inData{j}; %#ok<AGROW>
                end
            else
                sizeof_inData = size(inData);
                if sizeof_inData(1) > sizeof_inData(2)
                    outData = inData';
                else
                    outData = inData;
                end
            end
        end
    end
    
end

