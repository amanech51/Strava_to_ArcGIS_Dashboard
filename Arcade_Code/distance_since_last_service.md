# Calculate distance ridden since last service

This Arcade expresion uses the hosted Table with activities and hosted Feature Service from the Survey123 form used to log the bike services.

The result of this expression is a FeatureSet that can be used to bring the **distance** as an *Indicator* element within the ArcGIS Dashboard. 


```js
var agol = Portal('https://www.arcgis.com/');

//fs1 = Survey123 hosted Feature Layer: replace XXXXX... with item id for this hosted feature layer and fields as needed. 
//Fields will depend on your Survey123 form.

var fs1 = FeatureSetByPortalItem(
    agol,
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    0,
    [
        'bike',
        'maintenance_date',
        'service',
        'component',
        'comments',
    ],
    false
);

// sql variable contains the query wiht the gear_id of the specifc bike you want to calculate distance since last service. 
//Replace YYYYYYYYYYY with gear_id in slq and sql2

var sql = "bike = 'YYYYYYYYYYY'"
var LastServiceDateFeatureSet = Top(OrderBy(Filter(fs1,sql), 'maintenance_date DESC'),1)
var LastServiceDateFeature = First(LastServiceDateFeatureSet)

//fs2 is the hosted Table with activities: replace XXXXXXXXXXX... with item id for this table
var fs2 = FeatureSetByPortalItem(
    agol,
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    9,
    [
        'name',
        'distance',
        'start_date_local',
        'gear_id',
    ],
    false
);

var LastMaintenance = LastServiceDateFeature.maintenance_date

var sql2 = "gear_id = 'YYYYYYYYYYY' AND start_date_local > @LastMaintenance"
var Result =  Round(Sum(Filter(fs2,sql2),'distance'),2)

// create data schema
var Dict = {
    'fields': [
        {'name': 'TotalDist', 'type': 'esriFieldTypeDouble'}
    ],
    'geometryType': '',   
    'features': []};

// fill the data schema with the data from dictionary
Dict.features[0] = {
            'attributes': {
                'TotalDist': Result
            }}

// return the featureset
return FeatureSet(Text(Dict));
```
