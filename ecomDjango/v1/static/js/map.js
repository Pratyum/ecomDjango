//var postalCodes = [
//    '637639',
//    '636960',
////    '189677',
////    '180231',
//    '188382',
//    '189673',
//    '189702'
//];

function initialize() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(1.3396232, 103.778713),
        zoom: 11
    });

    var latlngs = [];
    var postalCodes = [];
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://localhost:8000/get_orders/", false ); // false for synchronous request
    xmlHttp.send( null );
    data = JSON.parse(JSON.parse(xmlHttp.responseText).orders);
//    console.log("Main data", data)
    var returned_data = geocodeAddress(map, data);
    var latlngs = returned_data[0]
    var titles = returned_data[1]
    console.log("latlngs", latlngs)
    setTimeout(function(){
        var markers = latlngs.map(function(location, i) {
            return new google.maps.Marker({
                position: location,
                label: titles[i].toString()
            });
        });

        // Add a marker clusterer to manage the markers.
        var markerCluster = new MarkerClusterer(map, markers, {
            imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
            minimumClusterSize: 3,
        });
        setTimeout(function(){
            var clusters = markerCluster.clusters_; // use the get clusters method which returns an array of objects
            console.log("ALL CLUSTERS", clusters)
            var max = 0;
            var main_cluster = null;
            var orderIds = []
            for( var i=0, l=clusters.length; i<l; i++ ){
                if (max < clusters[i.toString()].markers_.length){
                    main_cluster = clusters[i];
                    max = clusters[i].markers_.length;
                }
            }
            console.log("MAIN CLUSTER", main_cluster)
            for (var i =0, l= main_cluster.markers_.length; i<l; i++){
                orderIds.push(main_cluster.markers_[i].label)
            }
            console.log("ORDERS", orderIds)
            marker_center = new google.maps.Marker({
                    position: main_cluster.getCenter(),
                    label: "CENTER"
                });
            var data = {
                "orderids" : orderIds,
                "center": {
                    "lat": marker_center.getPosition().lat(),
                    "lng": marker_center.getPosition().lng()
                }
            }
            console.log("DATA", data)

    //        #################
            fetch('https://maps.googleapis.com/maps/api/geocode/json?latlng='+data.center.lat+','+data.center.lng+'&key=AIzaSyAxDUNnLRbtEHflMVMPtylD5I5sSFK6QVQ').then(function(response){
                if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' +
                      response.status);
                    return;
                  }
                  // Examine the text in the response
                  response.json().then(function(res) {
                      console.log(
                          "RESULT", res)
                    for( var i=0, l=res.results.length; i<l; i++ ){
                        if( res.results[i].types[0] == "postal_code" ){
                            data["destination_postal_code"] = res.results[i].address_components[0].short_name;
                            console.log("POSTAL", res.results[i].address_components[0].short_name)
                            break;
                        }
                    }
                  });
                })

    //        #################
//                console.log("DATA", data)
            setTimeout(function(){

                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/post_collated_orders?data='+JSON.stringify(data), false);
                xhr.onload = function () {
                    console.log(this.responseText);
                };
                xhr.send(data);
                console.log("DATA END", data)
        }, 300);
        }, 300);
    }, 800);

}

function geocodeAddress(map, data){
    var markers = [];
    var markerLocs =[];
    var titles = [];
    data.map(function(postalCode,index){
         titles.push(postalCode.pk)
         return fetch('https://maps.googleapis.com/maps/api/geocode/json?address='+postalCode.fields.address+',+SG&key=AIzaSyAxDUNnLRbtEHflMVMPtylD5I5sSFK6QVQ').then(function(response){
            if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status);
                return;
              }
              // Examine the text in the response
              response.json().then(function(data) {
                markerLocs.push(data.results[0].geometry.location);
                return data.results[0].geometry.location
              });
        })
    });
    console.log("markerLocs",typeof(markerLocs),markerLocs);

    // Add a marker clusterer to manage the markers.
    return [markerLocs, titles];

}
