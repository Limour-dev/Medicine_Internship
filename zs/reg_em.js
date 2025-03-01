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

tF = frames['NavigateFuncZone'];
(async function(){
    var alldata = [];
    for(let one_option of tF.document.querySelector("#listBoxRegInfos").options){
        tF.document.querySelector("#listBoxRegInfos").onclick.apply(one_option);
        await sleep(5);
        let Form = await isElLoaded(frames["DetailZone"], "#frame4 > tbody > tr > td > table > tbody > tr > td > table:nth-child(3)");
        var data = {key: one_option.innerText, value: Form.innerText};
        console.log(data);
        alldata.push(data);
    }
    downloadFile(JSON.stringify(alldata), '急诊病历.json');
})();
