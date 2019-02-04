--[[
timeFrame - Период свечи
periodOfSMA1 - Период быстрой скользящей средней 
periodOfSMA2 - Период медленной скользящей средней 
stopLoss - Укажите величину стоп_лосс 
takeProfit - Укажите величину тейк_профит
--]]

-- Период свечи, задаваемый в качестве параметра скрипта (см. строчку 2)
timeFrame = %1

-- Период для расчета индикатора SMA, задаваемый в качестве параметра скрипта (см. строчку 3) 
periodOfSMA1 = %2

-- Период для расчета индикатора SMA, задаваемый в качестве параметра скрипта (см. строчку 3) 
periodOfSMA2 = %3

-- Стоп-лосс, задаваемый в качестве параметра скрипта (см. строчку 4)
stopLoss = %4

-- Тейк-профит, задаваемый в качестве параметра скрипта (см. строчку 5)
takeProfit = %5

-- Идентификатор открытой LONG-позиции (или 'nil', если LONG-позиция сейчас не открыта). 
longPositionId = nil

-- Идентификатор открытой SHORT-позиции (или 'nil', если SHORT-позиция сейчас не открыта). 
shortPositionId = nil

function main() 
	
    on( "SMA", timeFrame, periodOfSMA1, nil ) 
    on( "SMA", timeFrame, periodOfSMA2, nil ) 

	-- Задаем обработчик события "NewCandle":
	on( "NewCandle", timeFrame, onNewCandle )
end

function onNewCandle( _openTime, _open, _max, _min, _close, _volume, _nextOpenPrice )
	
	on( "NewCandle", timeFrame, onNewCandle )

    sma1_0 = getIndicatorValue( "SMA".."_"..timeFrame.."_"..periodOfSMA1, 0 )
    if sma1_0 == nil then 
        return
    end
    if sma1_0.value == nil then 
        return
    end
    
    valueOfSMA1_0 = tonumber(sma1_0.value)

    sma2_0 = getIndicatorValue( "SMA".."_"..timeFrame.."_"..periodOfSMA2, 0 )
    if sma2_0 == nil then
        return
    end
    if sma2_0.value == nil then
        return
    end

    valueOfSMA2_0 = tonumber(sma2_0.value)
       
    sma1_1 = getIndicatorValue( "SMA".."_"..timeFrame.."_"..periodOfSMA1, 1)
    if sma1_1 == nil then
        return
    end
    if sma1_1.value == nil then
        return
    end
    valueOfSMA1_1 = tonumber(sma1_1.value) 
    sma2_1 = getIndicatorValue( "SMA".."_"..timeFrame.."_"..periodOfSMA2, 1 )
    if sma2_1 == nil then 
        return
    end    
    if sma2_1.value == nil then
        return
    end
    valueOfSMA2_1 = tonumber(sma2_1.value)

	if longPositionId == nil then

        if valueOfSMA1_0 > valueOfSMA2_0 and valueOfSMA1_1 < valueOfSMA2_1 then 
			if shortPositionId ~= nil then 
				closePosition( shortPositionId )
			end
			
			longPositionId = openLong( 1 )
			if longPositionId ~= nil then
			    -- Устанавливаем стоп-лосс и тейк-профит
				setSLTP( longPositionId, stopLoss, takeProfit ) 
				-- Устанавливаем функцию, которая будет вызвана при закрытии позиции
				onPositionClose( longPositionId, onLongPositionClose ) 
			end
		end			
	end

	if shortPositionId == nil then

        if valueOfSMA1_0 < valueOfSMA2_0 and valueOfSMA1_1 > valueOfSMA2_1 then 
			if longPositionId ~= nil then 
				closePosition( longPositionId )
			end
			
			shortPositionId = openShort( 1 ) 
			if shortPositionId ~= nil then
				setSLTP( shortPositionId, stopLoss, takeProfit )
				onPositionClose( shortPositionId, onShortPositionClose )
			end
		end			
	end
end


-- Callback-функция, которая вызывается, когда закрывается позиция LONG.

function onLongPositionClose( _positionId )
	longPositionId = nil
end 


-- Callback-функция, которая вызывается, когда закрывается позиция SHORT.

function onShortPositionClose( _positionId )
	shortPositionId = nil
end 
