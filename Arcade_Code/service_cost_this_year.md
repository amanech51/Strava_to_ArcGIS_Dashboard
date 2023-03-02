# Calculate service costs for this year

The Arcade expression uses the hosted Feature Service from the Survey 123 form to calculate the maintenance cost for the current year. The result is a FeatureSet that can be used as in input for an *Indicator* element in the ArcGIS Dashboard. 

```js
var agol = Portal('https://www.arcgis.com/');

//fs is the hosted feature service from the Survey123.
//Replace XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX with your item id. Fields will depend on the survey design.

var fs = FeatureSetByPortalItem(
    agol,
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    0,
    [
        'bike',
        'maintenance_date',
        'service',
        'component',
        'comments',
        'dollars'
    ],
    false
);


//Find current year
var This_Year = Year(Today())

var start_this_year = Date(This_Year,0,1)

var end_this_year = Date(This_Year,11,31)

//Replace YYYYYYYY with the gear_id you want to know the running costs.
var sql = "bike = 'YYYYYYYY' AND (maintenance_date > @start_this_year AND maintenance_date < @end_this_year)"
var Result =  Round(Sum(Filter(fs,sql),'dollars'),2)

// create data schema
var Dict = {
    'fields': [
        {'name': 'TotalDollars', 'type': 'esriFieldTypeDouble'}
    ],
    'geometryType': '',   
    'features': []};

// fill the data schema with the data
Dict.features[0] = {
            'attributes': {
                'TotalDollars': Result
            }}

// return the featureset
return FeatureSet(Text(Dict));
```
