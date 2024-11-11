async function sleep(timeout) {
    await new Promise((resolve)=>{
        setTimeout(resolve, timeout * 1000);
    }
    );
}
;async function processRows() {

    for (let i = 0; i <= 29; i++) {

        var orignialWindowOpen = window.open;
        window.open = async function() {
            var taskid = i + 1
            var newWindow = orignialWindowOpen.apply(this, arguments);
            newWindow.close();
            console.log("Manipulating Row", taskid, "Window closed");
            return newWindow;
        }

        console.log("Manipulating Row", i + 1);
        var currentRow = document.querySelector(`#dgvResult_${i}`);
        currentRow.click();
        showForm('ibtnUserDefine', 4);
        RequestAjax("http://1.1.1.230:7000/UserDefine/Ajax.ashx?type=SaveResidentUserDefine4&fwwcqkstar=0&shfsstar=0&tzzbstar=0&ztpjstar=0&OneStep=", escape($("#hidbid").val()), function(data) {
            console.log(escape($("#hidbid").val()));
            console.log(data)
        })
        await sleep(0.5);

        window.focus();
        window.open = orignialWindowOpen;
    }
    ;
}
;async function limour_main() {
    while (true) {
        await processRows();
        document.querySelector("#QueryButton1_LinkButton1").click();
        await sleep(15);
    }
}
;limour_main()