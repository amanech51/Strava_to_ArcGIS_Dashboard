# Get the last service done
This Arcade expression uses the Survey123 form and retrieves the last service done to display within a table element in the ArcGIS Dashboard.


```js
var portal = Portal('https://www.arcgis.com/');

// fs is the hosted Feature Service from the Survey123 form.
// Replace ############################# with yout item id.
// Make sure you are using the right layer ID within the hosted feature service. In this case is 0.
// Fields will depend on the Survey123 form you have created.

var fs = FeatureSetByPortalItem(
    portal,
    '#############################',
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
var sql = "bike = 'b11595068'"
return Top(OrderBy(Filter(fs,sql), 'maintenance_date DESC'),1)
```
