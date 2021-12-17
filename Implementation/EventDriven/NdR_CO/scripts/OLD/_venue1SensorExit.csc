set mod 0
loop
if($mod==0)
	areadsensor var
	rdata $var t x sensorVal1
	data p s2 $sensorVal1
	send $p 49
	while($sensorVal1<10.0)
		areadsensor var
		rdata $var t x sensorVal1
		data p s2 $sensorVal1
		send $p 49
		function y myedf venue1SensorExitNormal,100,10
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
		data p s2 $sensorVal1
		send $p 49
		function y myedf venue1SensorExitCritical,100,10
		delay $y
	end
	if($sensorVal1<10.0)
		set mod 0
	end
end