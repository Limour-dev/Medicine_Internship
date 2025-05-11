/* https://thebiogrid.org/ */
function downloadFile(data, filename){
    var blob = new Blob([data], {type: 'text/csv;charset=utf-8;'});
    var link = document.createElement('a');

    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

let tb = document.querySelector("#DataTables_Table_0 > tbody");
let tsv = Array.from(tb.querySelectorAll("tr")).map(tr =>
  Array.from(tr.querySelectorAll("td")).map(td =>
    td.textContent.replace(/[\r\n\t]+/g, '').trim()
  ).join('\t')
).join('\n');

 downloadFile(tsv, 'STAT3.tsv');