set mod 0
loop
if($mod==0)
	areadsensor var
	rdata $var t x sensorVal1
	data p s34 $sensorVal1
	send $p 47
	while($sensorVal1<10.0)
		areadsensor var
		rdata $var t x sensorVal1
		data p s34 $sensorVal1
		send $p 47
		function y myf parking1EntranceNormal,100,10
		delay $y
	end
	if($sensorVal1>=10.0)
		set mod 1
	end
end
if($mod==1)
	while($sensorVal1>=10.0)
		areadsensor var
		rdata $var t x sensorVal1
		data p s34 $sensorVal1
		send $p 47
		function y myf parking1EntranceCritical,100,10
		delay $y
	end
	if($sensorVal1<10.0)
		set mod 0
	end
end
