function downloadFile(data, filename){
    var blob = new Blob([data], {type: 'text/csv;charset=utf-8;'});
    var link = document.createElement('a');

    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

var d = document.querySelector("#DetailZone").contentDocument.querySelector("#frame4 > tbody > tr > td > table > tbody > tr > td > table.box2 > tbody > tr:nth-child(2) > td.middle").innerText;

var pt_id = document.querySelector("#PatientInfoZone").contentDocument.querySelector("#labelAdmitNO_RegDept").innerText;

downloadFile(d, pt_id + '_rec.txt');