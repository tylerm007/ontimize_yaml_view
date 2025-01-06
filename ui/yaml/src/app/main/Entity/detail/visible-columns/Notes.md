Local Storage Key: com.ontimize.web.ngx.jee.seed15x
{users: {admin: {components: {CustomerTable_/main/Customer:{base64.decode(...)} }}}}

storedComponentsByUser = (users[session.user] || {})[LocalStorageService.COMPONENTS_STORAGE_KEY] || {};
const decoded = atob((storedComponents[key]));
try {
    componentData = JSON.parse(decoded);
} catch (e) {
    componentData = undefined;
}

CustomerTable_/main/Customer:{
  "sort-columns": "CompanyName:asc",
  "oColumns-display": [
    {"attr": "ContactName", "visible": true},
    {"attr": "CompanyName", "visible": true},
    {"attr": "ContactTitle", "visible": true},
    {"attr": "Address", "visible": true},
    {"attr": "City", "visible": true},
    {"attr": "Region", "visible": true},
    {"attr": "PostalCode", "visible": true},
    {"attr": "Country", "visible": false},
    {"attr": "Phone", "visible": false},
    {"attr": "Fax", "visible": false},
    {"attr": "Balance", "visible": false},
    {"attr": "CreditLimit", "visible": false},
    {"attr": "OrderCount", "visible": false},
    {"attr": "UnpaidOrderCount", "visible": false},
    {"attr": "Id", "visible": false},
    {"attr": "Client_id", "visible": false}
  ],
  "select-column-visible": false,
  "oColumns": [
    {"attr": "ContactName", "searchable": true, "searching": true},
    {"attr": "CompanyName", "searchable": true, "searching": true},
    {"attr": "ContactTitle", "searchable": true, "searching": true},
    {"attr": "Address", "searchable": true, "searching": true},
    {"attr": "City", "searchable": true, "searching": true},
    {"attr": "Region", "searchable": true, "searching": true},
    {"attr": "PostalCode", "searchable": true, "searching": true},
    {"attr": "Country", "searchable": true, "searching": true},
    {"attr": "Phone", "searchable": true, "searching": true},
    {"attr": "Fax", "searchable": true, "searching": true},
    {"attr": "Balance", "searchable": true, "searching": true},
    {"attr": "CreditLimit", "searchable": true, "searching": true},
    {"attr": "OrderCount", "searchable": true, "searching": true},
    {"attr": "UnpaidOrderCount", "searchable": true, "searching": true},
    {"attr": "Id", "searchable": true, "searching": true},
    {"attr": "Client_id", "searchable": true, "searching": true}
  ],
  "filter-case-sensitive": false,
  "query-rows": 20,
  "selection": [],
  "initial-configuration": {
    "oColumns-display": [
      {"attr": "CompanyName", "visible": true},
      {"attr": "ContactName", "visible": true},
      {"attr": "ContactTitle", "visible": true},
      {"attr": "Address", "visible": true},
      {"attr": "City", "visible": true},
      {"attr": "Region", "visible": true},
      {"attr": "PostalCode", "visible": true},
      {"attr": "Country", "visible": true},
      {"attr": "Phone", "visible": true},
      {"attr": "Fax", "visible": true},
      {"attr": "Balance", "visible": true},
      {"attr": "CreditLimit", "visible": true},
      {"attr": "OrderCount", "visible": true},
      {"attr": "UnpaidOrderCount", "visible": true},
      {"attr": "Id", "visible": false},
      {"attr": "Client_id", "visible": true}
    ],
    "sort-columns": "CompanyName",
    "select-column-visible": false,
    "filter-case-sensitive": false,
    "query-rows": 20,
    "filter-colum-active-by-default": true,
    "filter-columns": [],
    "grouped-columns": []
  },
  "filter-columns": [],
  "filter-column-active": true,
  "grouped-columns": ["City"],
  "grouped-column-types": [],
  "user-stored-filters": [],
  "user-stored-configurations": []
}

### Reading Browser Local Storage

To read data from the browser's local storage, you can use the following JavaScript code:

```javascript
// Retrieve data from local storage
const data = localStorage.getItem('com.ontimize.web.ngx.jee.seed15x');

// Check if data exists
if (data) {
    // Parse the JSON data
    const parsedData = JSON.parse(data);
    console.log(parsedData);
} else {
    console.log('No data found in local storage');
}
```

This code snippet retrieves the data stored under the key `com.ontimize.web.ngx.jee.seed15x`, checks if the data exists, and then parses and logs it to the console.