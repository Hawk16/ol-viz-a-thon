var data = source.data;

var filetext = 'State,CourtName,CaseTypeDescription,AppealByRight,AppealByPermission,OriginalProceeding,InterlocutoryAppeal,Exclusive,Limited,MinValue,MaxValue,Notes\n';

for (var i = 0; i < data['State'].length; i++) {
    var currRow = [data['State'][i].toString(),
                   data['CourtName'][i].toString(),
                   data['CaseTypeDescription'][i].toString(),
                   data['AppealByRight'][i].toString(),
                   data['AppealByPermission'][i].toString(),
                   data['OriginalProceeding'][i].toString(),
                   data['InterlocutoryAppeal'][i].toString(),
                   data['Exclusive'][i].toString(),
                   data['Limited'][i].toString(),
                   data['MinValue'][i].toString(),
                   data['MaxValue'][i].toString(),
                   data['Notes'][i].toString().concat('\n')];

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