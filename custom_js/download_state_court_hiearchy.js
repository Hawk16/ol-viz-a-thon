var data = source.data;

var filetext = 'State,ChildCourtName,ParentCourtName\n';

for (var i = 0; i < data['State'].length; i++) {
    var currRow = [data['State'][i].toString(),
                   data['ChildCourtName'][i].toString(),
                   data['ParentCourtName'][i].toString().concat('\n')];

    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'state_court_research_results.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
} else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}