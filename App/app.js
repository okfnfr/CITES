$(document).ready(function() {


     $.ajax({
        type: 'GET',
        url: 'https://wild-species-okfn-api.herokuapp.com/countries/',
        dataType: 'json',
        success: function (data) {

            var countries = [];

            var items = $.parseJSON(data.response);
            //console.log(items);

            items.forEach(function(item){
                //console.log(item);
                countries.push(item.Name);
            });

            $('#countries').autocomplete({
                source : countries
            });
        }
     });
});

