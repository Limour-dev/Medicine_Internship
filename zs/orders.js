function tableToCSV(table){
    var csv = [];
    var rows = table.querySelectorAll('tr');
    for (var row of rows){
        var cells = row.querySelectorAll('td, th');
        let csvRow = [];

        for (var cell of cells){
            var text = cell.innerText.replace(/"/g, '""');
            if (text.includes(',') || text.includes('\n')){
                text = `"${text}"`;
            }
            csvRow.push(text);
        }
        csv.push(csvRow.join(','));
    }
    return csv.join('\n');
}
function downloadFile(data, filename){
    var blob = new Blob([data], {type: 'text/csv;charset=utf-8;'});
    var link = document.createElement('a');

    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();

}

var d = tableToCSV(document.querySelector("#DetailZone").contentDocument.querySelector("#gridViewWardChanged"));

var pt_id = document.querySelector("#PatientInfoZone").contentDocument.querySelector("#labelAdmitNO_RegDept").innerText;

downloadFile(d, pt_id + '.txt');