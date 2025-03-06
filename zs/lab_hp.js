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
function createSignal(){
    let resolve;
    let promise = new Promise((res) => {resolve = res});
    return {
        wait: promise,
        trigger: resolve,
    }
}
async function isElLoaded(nW, sl) {
    do{
        await sleep(0.1);
    } while (nW.document.querySelector(sl) === null);
    return nW.document.querySelector(sl);
}

let tF = frames['Contents'];
var oWindOpen = tF.window.open;

var nWind;
(async function(){
    var alldata = [];
    for(let one_option of Array.from(tF.document.querySelector("#tblLabContent").querySelectorAll('tr')).slice(1, -2)){
        nWind = oWindOpen(one_option.querySelector('td:nth-child(2) > a').href, "_blank", "scrollbars=1,height=700,width=900,top=200,left=200,status=yes,toolbar=no,menubar=no,location=no", "false");

        let div = await isElLoaded(nWind, "#tblLabReportDetail");
        
        var data = {key: one_option.innerText, value: div?.innerText};
        
        console.log(data);
        alldata.push(data);

        nWind.close();
    }
    downloadFile(JSON.stringify(alldata), '住院检验报告.json');
})();