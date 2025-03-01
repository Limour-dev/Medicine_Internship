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

var nWind;
(async function(){
    var alldata = [];
    for(let one_option of document.querySelector("#listBoxLabOrMed").options){
        let one_sig = createSignal();
        (async (f_one, f_sig)=>{
            window.open = async function(){
                let tmpWind = oWindOpen.apply(this, arguments);
                console.log(f_one.value, tmpWind);
                f_sig.trigger(tmpWind);
            }
            PopupLabMedCheckEvent(f_one.value);
        })(one_option, one_sig);
        
        nWind = await one_sig.wait;

        let div = await isElLoaded(nWind, "#gridViewLabCheck");
        var data = {key: one_option.innerText, value: div?.textContent};
        console.log(data);
        alldata.push(data);
    }
    downloadFile(JSON.stringify(alldata), '急诊检验报告.json');
})();

// 麻了，如果第二次输出null的话，多半是右上的拦截没有开启始终允许
// window.open = async function(){
//     let tmpWind = oWindOpen.apply(this, arguments);
//     console.log(tmpWind);
//     tmpWind.close();
// }

// async function limour(){
//     for(let one_option of document.querySelector("#listBoxLabOrMed").options){
//         console.log(one_option.value);
//         PopupLabMedCheckEvent(one_option.value);
//         await sleep(2);
//     }
// };
// limour();
