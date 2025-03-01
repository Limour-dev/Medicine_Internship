var oWindOpen = window.open;

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


(async function(){
    var alldata = [];
    for(let one_option of document.querySelector("#listBoxTechReport1").options){
        SelectedOneTechReportMZ(one_option);
        let techForm = await isElLoaded(parent.frames["DetailZone"], "#form1");
        var data = {key: one_option.innerText, value: techForm.innerText};
        console.log(data);
        alldata.push(data);
    }
    downloadFile(JSON.stringify(alldata), '急诊检查报告.json');
})();