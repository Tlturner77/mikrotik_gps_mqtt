
############### MQTT ####################
:local broker "AWS"
:local topic "sensor/gps"

# TEST DATA
:local gpsTime ([ / system clock get date ] . " " . [ / system clock get time ]);
#:local gpsLat "77.00010m"
#:local gpsLon "129.0010 k/mh"
############### GPS DATA ###############
:local gpsData [/system gps monitor once as-value]


#:local gpsTime ($gpsData->"date-and-time")
:local gpsLat ($gpsData->"latitude")
:local gpsLon ($gpsData->"longitude")
:local gpsAlt ($gpsData->"altitude")
:local gpsSpeed ($gpsData->"speed")
:local gpsDstBrg ($gpsData->"destination-bearing")
:local gpsTrueBrg ($gpsData->"true-bearing")
:local gpsMagBrg ($gpsData->"magnetic-bearing")
:local gpsSats ($gpsData->"satellites")
:local gpsFixQlt ($gpsData->"fix-quality")
# :local gpsHorzDil ($gpsData->"horizontal-dilution")
:local gpsDateAge ($gpsData->"data-age")

############### GPS Clean up Data ###############
# [\6D] is the hex for "m"
# [\20] is the hex for space

:local FuncClean do={
:local endIdx ([:find $clean "\20"]+1)
:local startIdx ($endIdx -1)
:local char [:pick $clean $startIdx $endIdx]
:if ($clean = "none") do={
	:set $clean 0; 
	:return $clean;
} else={
	:if ($char = "\20") do={
	:set startIdx 0;
	:set endIdx [:find $clean "\20"];
	:set $clean [:pick $clean $startIdx $endIdx];
	:return $clean;
	} else={
		:set startIdx 0;
		:set endIdx [:find $clean "\6D"];
		:set $clean [:pick $clean $startIdx $endIdx];
		:return $clean;
	}
 }   
 
}

############### Call Cleanup Functions ###############
:set gpsLat [$FuncClean clean=$gpsLat]
:set gpsLon [$FuncClean clean=$gpsLon]
:set gpsAlt [$FuncClean clean=$gpsAlt]
:set gpsSpeed [$FuncClean clean=$gpsSpeed]
:set gpsDstBrg [$FuncClean clean=$gpsDstBrg]
:set gpsTrueBrg [$FuncClean clean=$gpsTrueBrg]
:set gpsMagBrg [$FuncClean clean=$gpsMagBrg]

# Used for testing
:put ("Lat: " . $gpsLat)
:put ("Lon: " . $gpsLon)
:put ("ALT: " . $gpsAlt)
:put ("Distance Brg: " . $gpsDstBrg)
:put ("Speed: ". $gpsSpeed)
############### GPS Topic Message ###############
:local message \
"{\
	\"timestamp\":\"$gpsTime\",\
	\"latitude\":\"$gpsLat\",\
	\"longitude\":\"$gpsLon\",\
	\"altitude\":\"$gpsAlt\",\
	\"speed\":\"$gpsSpeed\",\
	\"destination-bearing\":\"$gpsDstBrg\",\
	\"true-bearing\":\"$gpsTrueBrg\",\
	\"magnetic-bearing\":\"$gpsMagBrg\",\
	\"satellites\":\"$gpsSats\",\
    \"fix-quality\":\"$gpsFixQlt\"\
}"
############### Log Message ###############
:log info "$message";

############### Publish Topic Message ###############
:put $message;

/iot mqtt publish broker=$broker topic=$topic message=$message
