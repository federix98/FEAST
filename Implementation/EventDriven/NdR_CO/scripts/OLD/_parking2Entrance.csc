set mod 0
loop
if($mod==0)
	areadsensor var
	rdata $var t x sensorVal1
	data p s42 $sensorVal1
	send $p 48
	while($sensorVal1<12.0)
		areadsensor var
		rdata $var t x sensorVal1
		data p s42 $sensorVal1
		send $p 48
		function y myedf parking2EntranceNormal,100,10
		delay $y
	end
	if($sensorVal1>=12.0)
		set mod 1
	end
end
if($mod==1)
	while($sensorVal1>=12.0)
		areadsensor var
		rdata $var t x sensorVal1	
		data p s42 $sensorVal1
		send $p 48
		function y myedf parking2EntranceCritical,100,10
		delay $y
	end
	if($sensorVal1<12.0)
		set mod 0
	end
end
