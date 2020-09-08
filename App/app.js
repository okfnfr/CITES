function onTextSearch()
{
    document.getElementById("res").innerHTML = "";

    valkey = document.getElementById("search").value;
    console.log(valkey)
    if (valkey == '')
        return;

    binclude = document.getElementById("inclusion").checked
    console.log(binclude)
    list = {}

    if (binclude == true)
        getListByText(valkey);
    else
        getListByTextBegin(valkey);
}


function getcountries()
{
    fetch('https://wild-species-okfn-api.herokuapp.com/countries/')
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log('Oups ' +
                        response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                    //console.log(data.response);
                    var list = JSON.parse(data.response);
                    console.log(list);
                    var countries = document.getElementById("countries");
                    list.forEach(function(item){
                        var option = document.createElement("option");
                        option.text = item.Name;
                        countries.add(option);
                    });
                });
            }
        )
        .catch(function (err) {
            console.log('Fetch Error :-S', err);
        });
}


function getListByText(str)
{
    url = 'https://wild-species-okfn-api.herokuapp.com/SearchIncludeText/' + str

    fetch(url)
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log('Oups ' +
                        response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                     //console.log(data.items);
                     var list = JSON.parse(data.items);
                     console.log(list);

                     document.getElementById("res").innerHTML += "<table>";

                     fragment = "<table>";

                     for (var key in list) {
                     if (list.hasOwnProperty(key)) {
                         var c = {}
                         c.class_c = list[key].class_c
                         c.family = list[key].family
                         c.wname = list[key].wname
                         c.scientific_name = list[key].scientific_name
                         c.image = list[key].image
                         c.genus = list[key].genus
                         c.order_c = list[key].order_c
                         c.phylum = list[key].phylum
                         c.species = list[key].species
                         c.subspecies = list[key].subspecies

                         c.citesid = list[key].citesid
                         c.listing_cites = list[key].listing_cites
                         c.wikidataid = list[key].wikidataid

                         fragment += "<tr style='border: dashed black; border-width: 1px;'>";
                         fragment += "<td width='40%' valign='top'>";
                         console.log(c.image)
                         if (c.image != '')
                            fragment += "<img width='250px' src='" + c.image + "'/>";
                         else
                             fragment += "<img src='Noimage.png'/>";

                         fragment += "</td>";

                         fragment += "<td align='left' width='50%' valign='top'>";

                         fragment += "<h1>" + c.wname + " <i>" + c.scientific_name + "</i></h1>"
                         fragment +="<br/>Family: " + c.family
                         fragment +="<br/>Class: " + c.class_c
                         fragment +="<br/>Genus: " + c.genus
                         fragment +="<br/>Order: " + c.order_c
                         fragment +="<br/>Phylum: " + c.phylum
                         fragment +="<br/>species: " + c.species
                         fragment +="<br/>CITES: " + c.listing_cites
                         fragment +="<br/>Wikidata: " + c.wikidataid
                         fragment += "</td>";
                         fragment += "</tr>";

                     }}
                     fragment += "</table>";
                     document.getElementById("res").innerHTML += fragment;                });
            }
        )
        .catch(function (err) {
            console.log('Fetch Error :-S', err);
        });
}


function getListByTextBegin(str)
{
    url = 'https://wild-species-okfn-api.herokuapp.com/SearchTextBegin/' + str

    fetch(url)
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log('Oups ' +
                        response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                     //console.log(data.items);
                     var list = JSON.parse(data.items);
                     console.log(list);

                     fragment = "<table>";

                     for (var key in list) {
                     if (list.hasOwnProperty(key)) {
                         var c = {}
                         c.class_c = list[key].class_c
                         c.family = list[key].family
                         c.wname = list[key].wname
                         c.scientific_name = list[key].scientific_name
                         c.image = list[key].image
                         c.genus = list[key].genus
                         c.order_c = list[key].order_c
                         c.phylum = list[key].phylum
                         c.species = list[key].species
                         c.subspecies = list[key].subspecies

                         c.citesid = list[key].citesid
                         c.listing_cites = list[key].listing_cites
                         c.wikidataid = list[key].wikidataid

                         fragment += "<tr style='border: dashed black; border-width: 1px;'>";
                         fragment += "<td width='40%' valign='top'>";
                         console.log(c.image)
                         if (c.image != '')
                            fragment += "<img width='250px' src='" + c.image + "'/>";
                         else
                             fragment += "<img src='Noimage.png'/>";

                         fragment += "</td>";

                         fragment += "<td align='left' width='50%' valign='top'>";

                         fragment += "<h1>" + c.wname + " <i>" + c.scientific_name + "</i></h1>"
                         fragment +="<br/>Family: " + c.family
                         fragment +="<br/>Class: " + c.class_c
                         fragment +="<br/>Genus: " + c.genus
                         fragment +="<br/>Order: " + c.order_c
                         fragment +="<br/>Phylum: " + c.phylum
                         fragment +="<br/>species: " + c.species
                         fragment +="<br/>CITES: " + c.listing_cites
                         fragment +="<br/>Wikidata: " + c.wikidataid
                         fragment += "</td>";
                         fragment += "</tr>";

                     }}
                     fragment += "</table>";
                     document.getElementById("res").innerHTML += fragment;                });
            }
        )
        .catch(function (err) {
            console.log('Fetch Error :-S', err);
        });
}


function onLoad()
{
    //getcountries();
    //getListByText('LION');
}