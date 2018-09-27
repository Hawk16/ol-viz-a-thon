var data = source.data;

var filetext = 'State,PopDensity,Rural,TrialStructure,CrimProc,DeathPen,CaseloadSize\n';

for (var i = 0; i < data['State'].length; i++) {
    var currRow = [data['State'][i].toString(),
                   data['PopDensity'][i].toString(),
                   data['Rural'][i].toString(),
                   data['TrialStructure'][i].toString(),
                   data['CrimProc'][i].toString(),
                   data['DeathPen'][i].toString(),
                   data['CaseloadSize'][i].toString().concat('\n')];

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