set mod 0
loop
if($mod==0)
	areadsensor var
	rdata $var t x sensorVal1
	data p s24 $sensorVal1
	send $p 51
	while($sensorVal1<10.0)
		areadsensor var
		rdata $var t x sensorVal1
		data p s24 $sensorVal1
		send $p 51
		function y myedf venue3EntranceNormal,100,10
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
		data p s24 $sensorVal1
		send $p 51
		function y myedf venue3EntranceCritical,100,10
		delay $y
	end
	if($sensorVal1<10.0)
		set mod 0
	end
end
