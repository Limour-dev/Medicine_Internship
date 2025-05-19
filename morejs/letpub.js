/* 
https://www.letpub.com.cn/ 
=TEXTBEFORE(C2," ")
*/

function downloadFile(data, filename){
    var blob = new Blob([data], {type: 'text/csv;charset=utf-8;'});
    var link = document.createElement('a');

    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

let tb = document.querySelector("#yxyz_content > table.table_yjfx > tbody");

let tsv = Array.from(tb.querySelectorAll("tr")).map(tr =>
  Array.from(tr.querySelectorAll("td")).map(td => {
    // 先把 <br> 替换成空格，再取纯文本
    let html = td.innerHTML.replace(/<br\s*\/?>/gi, ' ');
    // 创建临时元素提取纯文本
    let tmp = document.createElement('div');
    tmp.innerHTML = html;
    return tmp.textContent.replace(/[\r\n\t]+/g, ' ').replace(/\s+/g, ' ').trim();
  }).join('\t')
).join('\n');


 downloadFile(tsv, '1.tsv');