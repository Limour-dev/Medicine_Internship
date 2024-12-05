async function sleep(timeout) {
    await new Promise((s)=>setTimeout(s, timeout * 1000));
}
function downloadFile(data, filename){
    var blob = new Blob([data], {type: 'text/csv;charset=utf-8;'});
    var link = document.createElement('a');

    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}
var left = document.querySelector("#frameContents").contentDocument;
var pt_id;
var alldata = [];
async function limour() {
    for (var ltr of Array.from(left.querySelector("#tblLabContent").querySelectorAll('tr')).slice(1, -2)) {
        console.log(ltr.innerText);
        ltr.querySelector('td:nth-child(2) > a > span').click();
        await sleep(1);
        var right = document.querySelector("html > frameset > frameset > frame:nth-child(2)").contentDocument;
        pt_id = right.querySelector("body > div.ContainerCenter > div.ContainerCenter > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(2)").innerText;
        var data = {key: ltr.innerText, value: right.querySelector("#tblLabReportDetail").innerText};
        console.log(data);
        alldata.push(data);
    }
    downloadFile(JSON.stringify(alldata), pt_id + '.json');
}
limour();
