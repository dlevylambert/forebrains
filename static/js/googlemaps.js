var lat,lng;
var watcher;
var map, player, yourMarker, pursuer, target, pursuerMarker, targetMarker, game, targetLat, targetLng, pursuerLat, pursuerLng;

$(document).ready(function(){
    initializeMap();
    $.getJSON("/getCurrentUser", function (data) {
	player = data;
    });
    $.getJSON("/getCurrentGame", function (data) {
	game = data;
    });
    $.getJSON("/getTarget", function (data) {
	target = data;
    });
    $.getJSON("/getPursuer", function (data) {
	pursuer = data;
    });
});
	    

function initializeMap() {
    getLocation(makeMap);
}

function getLocation(e)
{
    if (navigator.geolocation)
    {
	var opts= {'enableHighAccuracy':true,
		   'timeout':10000,
		   'maximumAge':0};
	navigator.geolocation.getCurrentPosition(e,function(){},opts);
    }
    else{field.innerHTML="Geolocation is not supported by this browser.";}
}
 var gamestarted = false;
function makeMap(position)
{
    lat = position.coords.latitude;
    lng = position.coords.longitude;
    console.log(lat);
    console.log(lng);
    $.ajaxSetup({
	async: false
    });
    $.getJSON("/started",function(data){
	gamestarted = data;
    });   
    $.getJSON("/updatelocation",{xcor:lat,ycor:lng},function(){});
    var mapOptions = {
	center: new google.maps.LatLng(lat,lng),
	zoom: 14,
	mapTypeId: google.maps.MapTypeId.ROADMAP
	};
    map = new google.maps.Map(document.getElementById("field"), mapOptions);
    console.log(document.getElementById("field"));
    watcher = navigator.geolocation.watchPosition(updateYourMarker,
						  updateYourMarker,
						  {'enableHighAccuracy':true,
						   'timeout':10000,
						   'maximumAge':0});
    var myLatlng = new google.maps.LatLng(lat,lng);
    console.log(myLatlng);
    var yourMarker = new google.maps.Marker({
	position: myLatlng,
	map: map,
	title:"YOU"
	    });
    setInterval(updateYourMarker,500);
    if (gamestarted) {
    $.getJSON("/getTargetLocation", function (data) {
	targetLat = data[0];
	targetLng = data[1];
	var targetLatlng = new google.maps.LatLng(targetLat,targetLng);
	var targetMarker = new google.maps.Marker({
	    position: targetLatlng,
	    map: map,
	    title: "TARGET"
	});
    });};
    if (gamestarted){
    $.getJSON("/getPursuerLocation", function (data) {
	pursuerLat = data[0];
	pursuerLng = data[1];
	var pursuerLatlng = new google.maps.LatLng(pursuerLat,pursuerLng);
	var pursuerMarker = new google.maps.Marker({
	    position: pursuerLatlng,
	    map: map,
	    title: "PURSUER"
	});
    });};
    
}

function updateYourMarker(e){
    getLocation(function(p) {
	lat = p.coords.latitude;
	lng = p.coords.longitude;
	var yourMarker;
	try {
	yourMarker.setPosition(new google.maps.LatLng(lat, lng));
	}
	catch (err) {}
    });
}
