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
            await sleep(1);
            // var newWindow = window;  //调试用
            // console.log("newWindow ", newWindow);
            // 100s 强制关闭
            setTimeout(()=>{
                if (!newWindow.closed) {
                    newWindow.close();
                    console.log("Manipulating Row", taskid, "Window closed at 100s");
                }
            }
            , 100000);

            var alerted = false;
            newWindow.confirm = (m)=>console.log('confirm', taskid, m);
            newWindow.alert = (m)=>{
                console.log('alert', taskid, m);
                alerted = true;
            }

            var isElLoaded = async sl=>{
                await sleep(0.05);
                if (newWindow.closed) {
                    throw taskid + "newWindow.closed"
                }
                while (newWindow.document.querySelector(sl) === null) {
                    await new Promise((resolve)=>{
                        requestAnimationFrame(resolve)
                    }
                    );
                }
                ;return newWindow.document.querySelector(sl);
            }
            ;
            function rrrand(min, max) {
                return Math.floor(Math.random() * (max - min + 1)) + min
            }
            ;function setValue(el, min, max) {
                if (!el || !el.value) {
                    el.value = rrrand(min, max).toFixed(1);
                }
            }
            ;await sleep(0.5);

            taskid = (await isElLoaded("#Name")).value + ' ' + taskid;

            while (!(await isElLoaded("#jjkzdqt")).value) {
                await sleep(1);
            }
            console.log(taskid, (await isElLoaded("#jjkzdqt")).value);

            (await isElLoaded("#A6")).click();
            console.log(taskid, alerted);
            alerted = false;
            while (!alerted) {
                await sleep(1);
            }
            (await isElLoaded("#sp3")).click();
            await sleep(2);
            (await isElLoaded("#span_btn_Scheme > a")).click();
            while ((await isElLoaded("#YXFAMAIN")).children.length < 2) {
                await sleep(1);
            }
            (await isElLoaded("#div_spn > span.buttons.btn_save6 > a")).click();

            console.log(taskid, '已选方案数量：', (await isElLoaded("#SchemeList > div")).children.length)
            newWindow.close();
            console.log("Manipulating Row", taskid, "Window closed");
            return newWindow;
        }

        console.log("Manipulating Row", i + 1);
        var currentRow = document.querySelector(`#dgvResult_${i}`);
        currentRow.click();
        showForm('ibtnUserDefine', 2);
        await sleep(30);

        window.focus();
        window.open = orignialWindowOpen;
    }
    ;
}
;async function limour_main() {
    while (true) {
        await processRows();
        document.querySelector("#QueryButton1_LinkButton1").click();
        await sleep(35);
    }
}
;limour_main()
